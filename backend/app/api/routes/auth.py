"""
Authentication Routes - Endpoints de autenticación

Endpoints:
- POST /auth/login - Iniciar sesión
- POST /auth/refresh - Renovar access token
- POST /auth/logout - Cerrar sesión
- GET /auth/me - Obtener usuario actual
- POST /auth/change-password - Cambiar contraseña
- POST /auth/validate - Validar token
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies.auth import get_current_active_user, get_current_user
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.auth import (
    UserLogin,
    LoginResponse,
    Token,
    TokenRefresh,
    TokenRefreshResponse,
    LogoutResponse,
    TokenValidationRequest,
    TokenValidationResponse,
)
from app.schemas.user import UserResponse, PasswordChange
from app.services import auth_service
from app.core.security import get_password_hash, verify_password


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido"},
    }
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_client_ip(request: Request) -> Optional[str]:
    """Obtiene la IP del cliente desde el request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


def get_user_agent(request: Request) -> Optional[str]:
    """Obtiene el user agent del cliente."""
    return request.headers.get("User-Agent")


# ============================================================================
# LOGIN ENDPOINT
# ============================================================================

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="""
    Autentica un usuario y genera tokens JWT.

    **Credenciales:**
    - Username o email
    - Contraseña

    **Respuesta:**
    - Access token (30 minutos)
    - Refresh token (7 días)
    - Información del usuario

    **Seguridad:**
    - Bloqueo después de 5 intentos fallidos (15 minutos)
    - Registro en audit log
    - Actualiza last_login del usuario

    **Usuarios de prueba:**
    - admin / Admin123!
    - dr.martinez / Medico123!
    - aux.garcia / Auxiliar123!
    - op.lopez / Operador123!
    """
)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login.

    Retorna access token, refresh token y datos del usuario.
    """
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)

    try:
        result = auth_service.login(
            db=db,
            username=credentials.username,
            password=credentials.password,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        # Log error inesperado
        AuditLog.log_action(
            db=db,
            user_id=None,
            username=credentials.username,
            action="auth.login.error",
            category="authentication",
            status="error",
            details={"error": str(e)},
            ip_address=ip_address
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# ============================================================================
# REFRESH TOKEN ENDPOINT
# ============================================================================

@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    summary="Renovar access token",
    description="""
    Genera un nuevo access token usando un refresh token válido.

    **Input:**
    - Refresh token válido

    **Output:**
    - Nuevo access token (30 minutos)
    - Token type: bearer
    - Expires in: segundos hasta expiración

    **Notas:**
    - NO genera un nuevo refresh token
    - El refresh token original sigue siendo válido
    - Verifica que el refresh token no esté en blacklist
    """
)
async def refresh_token(
    token_data: TokenRefresh,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para renovar access token.
    """
    ip_address = get_client_ip(request)

    try:
        result = auth_service.refresh_access_token(
            db=db,
            refresh_token=token_data.refresh_token,
            ip_address=ip_address
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al renovar token"
        )


# ============================================================================
# LOGOUT ENDPOINT
# ============================================================================

@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Cerrar sesión",
    description="""
    Invalida los tokens del usuario (logout efectivo).

    **Requiere autenticación:** Sí (Bearer token)

    **Proceso:**
    1. Invalida el access token actual
    2. Opcionalmente invalida el refresh token
    3. Agrega tokens a la blacklist
    4. Registra logout en audit log

    **Notas:**
    - Los tokens quedan invalidados inmediatamente
    - No se pueden usar para nuevas requests
    - El usuario debe hacer login nuevamente
    """
)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint de logout.

    Invalida tokens del usuario actual.
    """
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)

    # Extraer tokens del request
    auth_header = request.headers.get("Authorization")
    access_token = None
    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header.replace("Bearer ", "")

    # Obtener refresh token del usuario si existe
    refresh_token = current_user.refresh_token

    try:
        result = auth_service.logout(
            db=db,
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=current_user.id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cerrar sesión"
        )


# ============================================================================
# ME ENDPOINT (Current User)
# ============================================================================

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario actual",
    description="""
    Retorna información del usuario autenticado.

    **Requiere autenticación:** Sí (Bearer token)

    **Respuesta:**
    - ID, username, email, nombre completo
    - Roles asignados
    - Permisos del usuario
    - Estado de la cuenta
    - Fecha de último login

    **Uso:**
    - Obtener información del usuario actual
    - Verificar permisos en el frontend
    - Mostrar perfil del usuario
    """
)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint para obtener información del usuario actual.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "roles": [role.name for role in current_user.roles],
        "permissions": current_user.get_permissions(),
        "created_at": current_user.created_at,
        "last_login": current_user.last_login,
        "failed_login_attempts": current_user.failed_login_attempts,
        "is_locked": current_user.is_locked()
    }


# ============================================================================
# CHANGE PASSWORD ENDPOINT
# ============================================================================

@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Cambiar contraseña",
    description="""
    Cambia la contraseña del usuario actual.

    **Requiere autenticación:** Sí (Bearer token)

    **Validaciones:**
    - Contraseña actual debe ser correcta
    - Nueva contraseña debe cumplir requisitos:
      * Mínimo 8 caracteres
      * Al menos una mayúscula
      * Al menos una minúscula
      * Al menos un número
    - Confirmación debe coincidir

    **Seguridad:**
    - Invalida todos los tokens del usuario (logout global)
    - Actualiza password_changed_at
    - Registra cambio en audit log
    - Usuario debe hacer login nuevamente
    """
)
async def change_password(
    password_data: PasswordChange,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para cambiar contraseña.
    """
    ip_address = get_client_ip(request)

    # Verificar contraseña actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        # Registrar intento fallido
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            action="auth.password.change.failed",
            category="authentication",
            status="failed",
            details={"reason": "invalid_current_password"},
            ip_address=ip_address
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )

    # Actualizar contraseña
    from datetime import datetime
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.password_changed_at = datetime.now()

    # Limpiar refresh token (forzar re-login)
    current_user.refresh_token = None

    db.commit()

    # Registrar cambio exitoso
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="auth.password.changed",
        category="authentication",
        status="success",
        ip_address=ip_address
    )

    # TODO: Invalidar todos los tokens del usuario
    # Esto requeriría agregar los JTIs a la blacklist

    return {
        "message": "Contraseña actualizada exitosamente",
        "password_changed_at": current_user.password_changed_at.isoformat()
    }


# ============================================================================
# VALIDATE TOKEN ENDPOINT
# ============================================================================

@router.post(
    "/validate",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar token",
    description="""
    Valida un token JWT y retorna su estado.

    **Input:**
    - Token JWT (access o refresh)

    **Output:**
    - valid: Si el token es válido
    - expired: Si el token expiró
    - blacklisted: Si el token está invalidado
    - user_id: ID del usuario (si es válido)
    - expires_at: Fecha de expiración

    **Uso:**
    - Verificar validez de tokens en el frontend
    - Debugging de problemas de autenticación
    """
)
async def validate_token(
    token_data: TokenValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para validar un token.
    """
    result = auth_service.validate_token(db, token_data.token)
    return result


# ============================================================================
# HEALTH CHECK (No Auth)
# ============================================================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check del sistema de autenticación",
    description="Verifica que el sistema de autenticación esté funcionando"
)
async def auth_health_check(db: Session = Depends(get_db)):
    """
    Health check del sistema de autenticación.
    """
    # Verificar conexión a DB
    try:
        from app.models.role import Role
        role_count = db.query(Role).count()
        user_count = db.query(User).count()

        return {
            "status": "healthy",
            "service": "authentication",
            "database": "connected",
            "roles_count": role_count,
            "users_count": user_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "authentication",
            "error": str(e)
        }
