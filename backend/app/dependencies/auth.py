"""
Authentication Dependencies - FastAPI Dependency Injection

Dependencias para autenticación y autorización:
- get_current_user: Obtiene usuario desde JWT token
- get_current_active_user: Obtiene usuario activo
- require_role: Verifica rol específico
- require_permission: Verifica permiso específico
"""
from typing import Optional, List
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.jwt import decode_token, is_token_blacklisted, verify_token_type
from app.models.user import User
from app.models.role import Role


# ============================================================================
# SECURITY SCHEME
# ============================================================================

# HTTP Bearer token scheme (Authorization: Bearer <token>)
security = HTTPBearer(
    scheme_name="JWT Bearer Token",
    description="JWT token en header Authorization"
)


# ============================================================================
# CORE DEPENDENCIES
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual desde el JWT token.

    Args:
        credentials: Credenciales HTTP Bearer (token JWT)
        db: Sesión de base de datos

    Returns:
        Usuario autenticado

    Raises:
        HTTPException 401: Si el token es inválido, expiró o está blacklisted
        HTTPException 404: Si el usuario no existe

    Examples:
        @app.get("/me")
        async def get_me(current_user: User = Depends(get_current_user)):
            return current_user.to_dict()

    Notes:
        - Verifica firma del token
        - Verifica expiración
        - Verifica que sea access token (no refresh)
        - Verifica blacklist
        - Actualiza last_login del usuario
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extraer token
    token = credentials.credentials

    # Decodificar token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Verificar tipo de token (debe ser "access")
    if not verify_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar blacklist
    jti = payload.get("jti")
    if jti and is_token_blacklisted(db, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalidado (sesión cerrada)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener user_id del token (viene como string en JWT spec)
    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception

    # Buscar usuario en DB
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Actualizar last_login (opcional, solo en login exitoso)
    # user.last_login = datetime.now()
    # db.commit()

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Obtiene el usuario actual y verifica que esté activo.

    Args:
        current_user: Usuario obtenido del token

    Returns:
        Usuario autenticado y activo

    Raises:
        HTTPException 403: Si el usuario está inactivo o bloqueado

    Examples:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_active_user)):
            return {"message": f"Hola {user.username}!"}

    Notes:
        - Verifica que user.is_active == True
        - Verifica que la cuenta no esté bloqueada (locked_until)
    """
    # Verificar si está activo
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Verificar si está bloqueado
    if current_user.is_locked():
        locked_until_str = current_user.locked_until.strftime("%Y-%m-%d %H:%M:%S")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cuenta bloqueada hasta {locked_until_str} por intentos fallidos"
        )

    return current_user


# ============================================================================
# ROLE-BASED DEPENDENCIES
# ============================================================================

class RoleChecker:
    """
    Dependency class para verificar roles.

    Examples:
        require_admin = RoleChecker(["admin"])

        @app.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            current_user: User = Depends(require_admin)
        ):
            # Solo admin puede acceder
            ...
    """

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        Verifica que el usuario tenga uno de los roles permitidos.

        Args:
            current_user: Usuario autenticado

        Returns:
            Usuario si tiene el rol requerido

        Raises:
            HTTPException 403: Si no tiene el rol
        """
        # Superuser siempre pasa
        if current_user.is_superuser:
            return current_user

        # Verificar roles
        user_roles = [role.name for role in current_user.roles]
        if not any(role in self.allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requiere uno de estos roles: {', '.join(self.allowed_roles)}"
            )

        return current_user


def require_role(allowed_roles: List[str]):
    """
    Factory function para crear dependencias de verificación de roles.

    Args:
        allowed_roles: Lista de roles permitidos

    Returns:
        Dependencia FastAPI que verifica roles

    Examples:
        @app.get("/admin/dashboard")
        async def admin_dashboard(
            user: User = Depends(require_role(["admin"]))
        ):
            return {"message": "Admin dashboard"}

        @app.get("/medical/patients")
        async def medical_patients(
            user: User = Depends(require_role(["admin", "medico"]))
        ):
            return {"patients": [...]}
    """
    return RoleChecker(allowed_roles)


# ============================================================================
# PERMISSION-BASED DEPENDENCIES
# ============================================================================

class PermissionChecker:
    """
    Dependency class para verificar permisos específicos.

    Examples:
        require_patient_edit = PermissionChecker("patients.update")

        @app.put("/patients/{patient_id}")
        async def update_patient(
            patient_id: int,
            current_user: User = Depends(require_patient_edit)
        ):
            # Solo usuarios con permiso patients.update
            ...
    """

    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        Verifica que el usuario tenga el permiso requerido.

        Args:
            current_user: Usuario autenticado

        Returns:
            Usuario si tiene el permiso

        Raises:
            HTTPException 403: Si no tiene el permiso
        """
        # Superuser siempre pasa
        if current_user.is_superuser:
            return current_user

        # Verificar permiso
        if not current_user.has_permission(self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {self.required_permission}"
            )

        return current_user


def require_permission(permission: str):
    """
    Factory function para crear dependencias de verificación de permisos.

    Args:
        permission: Permiso requerido (ej: "patients.update", "reports.export")

    Returns:
        Dependencia FastAPI que verifica el permiso

    Examples:
        @app.delete("/patients/{patient_id}")
        async def delete_patient(
            patient_id: int,
            user: User = Depends(require_permission("patients.delete"))
        ):
            # Solo usuarios con permiso patients.delete
            ...

        @app.post("/reports/export")
        async def export_report(
            user: User = Depends(require_permission("reports.export"))
        ):
            # Solo usuarios con permiso reports.export
            ...

    Notes:
        - Soporta permisos wildcard: "patients.*" da acceso a patients.create, patients.read, etc.
        - Admin con permiso "*" tiene acceso a todo
    """
    return PermissionChecker(permission)


# ============================================================================
# CONVENIENCE DEPENDENCIES (PRE-CONFIGURED)
# ============================================================================

# Solo Admin
require_admin = RoleChecker(["admin"])

# Admin o Médico
require_medical_staff = RoleChecker(["admin", "medico"])

# Admin, Médico o Auxiliar
require_healthcare_staff = RoleChecker(["admin", "medico", "auxiliar"])

# Cualquier usuario autenticado y activo (ya existe: get_current_active_user)
