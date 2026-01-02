"""
Authentication Service - Lógica de negocio de autenticación

Servicios de autenticación:
- Login (usuario/password)
- Refresh token
- Logout (simple y global)
- Validación de credenciales
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import verify_password
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
    blacklist_token,
    is_token_blacklisted,
    get_token_expires_at
)
from app.config import settings


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

def authenticate_user(
    db: Session,
    username: str,
    password: str,
    ip_address: Optional[str] = None
) -> Optional[User]:
    """
    Autentica un usuario por username/email y contraseña.

    Args:
        db: Sesión de base de datos
        username: Username o email del usuario
        password: Contraseña en texto plano
        ip_address: IP del cliente (para audit log)

    Returns:
        Usuario si las credenciales son correctas, None en caso contrario

    Notes:
        - Soporta login con username o email
        - Incrementa failed_login_attempts en caso de fallo
        - Bloquea cuenta después de 5 intentos fallidos (15 minutos)
        - Resetea failed_login_attempts en caso de éxito
        - Registra en audit log
    """
    # Buscar usuario por username o email
    user = db.query(User).filter(
        (User.username == username.lower()) | (User.email == username.lower())
    ).first()

    # Usuario no existe
    if not user:
        # Registrar intento fallido (sin revelar si el usuario existe)
        AuditLog.log_action(
            db=db,
            user_id=None,
            username=username,
            action="auth.login.failed",
            category="authentication",
            status="failed",
            details={"reason": "user_not_found"},
            ip_address=ip_address
        )
        return None

    # Verificar si la cuenta está bloqueada
    if user.is_locked():
        locked_until_str = user.locked_until.strftime("%Y-%m-%d %H:%M:%S")
        AuditLog.log_action(
            db=db,
            user_id=user.id,
            username=user.username,
            action="auth.login.blocked",
            category="authentication",
            status="blocked",
            details={
                "reason": "account_locked",
                "locked_until": locked_until_str,
                "failed_attempts": user.failed_login_attempts
            },
            ip_address=ip_address
        )
        return None

    # Verificar contraseña
    if not verify_password(password, user.hashed_password):
        # Incrementar intentos fallidos
        user.increment_failed_login()
        db.commit()

        # Registrar intento fallido
        AuditLog.log_action(
            db=db,
            user_id=user.id,
            username=user.username,
            action="auth.login.failed",
            category="authentication",
            status="failed",
            details={
                "reason": "invalid_password",
                "failed_attempts": user.failed_login_attempts,
                "locked": user.is_locked()
            },
            ip_address=ip_address
        )
        return None

    # Verificar si está activo
    if not user.is_active:
        AuditLog.log_action(
            db=db,
            user_id=user.id,
            username=user.username,
            action="auth.login.failed",
            category="authentication",
            status="failed",
            details={"reason": "user_inactive"},
            ip_address=ip_address
        )
        return None

    # Login exitoso - resetear intentos fallidos
    user.reset_failed_login()
    user.last_login = datetime.now()
    db.commit()

    # Registrar login exitoso
    AuditLog.log_action(
        db=db,
        user_id=user.id,
        username=user.username,
        action="auth.login.success",
        category="authentication",
        status="success",
        details={"roles": [role.name for role in user.roles]},
        ip_address=ip_address
    )

    return user


def login(
    db: Session,
    username: str,
    password: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Dict[str, Any]:
    """
    Realiza login completo y genera tokens JWT.

    Args:
        db: Sesión de base de datos
        username: Username o email
        password: Contraseña en texto plano
        ip_address: IP del cliente
        user_agent: User agent del navegador

    Returns:
        Diccionario con access_token, refresh_token y datos del usuario

    Raises:
        HTTPException 401: Si las credenciales son inválidas
        HTTPException 403: Si la cuenta está bloqueada o inactiva

    Examples:
        >>> result = login(db, "admin", "Admin123!", "192.168.1.1")
        >>> print(result['access_token'])
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    # Autenticar usuario
    user = authenticate_user(db, username, password, ip_address)

    if not user:
        # Obtener detalles del error para mensaje personalizado
        temp_user = db.query(User).filter(
            (User.username == username.lower()) | (User.email == username.lower())
        ).first()

        if temp_user and temp_user.is_locked():
            locked_until = temp_user.locked_until.strftime("%Y-%m-%d %H:%M:%S")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cuenta bloqueada hasta {locked_until} por múltiples intentos fallidos"
            )
        elif temp_user and not temp_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cuenta inactiva. Contacte al administrador."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Obtener roles y permisos
    roles = [role.name for role in user.roles]
    permissions = user.get_permissions()

    # Crear tokens
    access_token = create_access_token(
        user_id=user.id,
        username=user.username,
        email=user.email,
        roles=roles,
        permissions=permissions
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
        username=user.username,
        email=user.email
    )

    # Guardar refresh token en usuario (opcional, para invalidación)
    user.refresh_token = refresh_token
    db.commit()

    # Retornar respuesta completa
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # segundos
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "roles": roles,
            "permissions": permissions,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
    }


# ============================================================================
# REFRESH TOKEN
# ============================================================================

def refresh_access_token(
    db: Session,
    refresh_token: str,
    ip_address: Optional[str] = None
) -> Dict[str, Any]:
    """
    Genera un nuevo access token usando un refresh token válido.

    Args:
        db: Sesión de base de datos
        refresh_token: Refresh token válido
        ip_address: IP del cliente

    Returns:
        Diccionario con nuevo access_token

    Raises:
        HTTPException 401: Si el refresh token es inválido o expiró

    Examples:
        >>> result = refresh_access_token(db, refresh_token, "192.168.1.1")
        >>> print(result['access_token'])
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

    Notes:
        - NO genera un nuevo refresh token (mantiene el actual)
        - Verifica que el token sea tipo "refresh"
        - Verifica blacklist
        - Registra en audit log
    """
    # Decodificar token
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar tipo de token
    if not verify_token_type(payload, "refresh"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido (esperaba refresh token)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar blacklist
    jti = payload.get("jti")
    if jti and is_token_blacklisted(db, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalidado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener usuario (sub viene como string en JWT spec)
    user_id_str = payload.get("sub")
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Obtener roles y permisos actualizados
    roles = [role.name for role in user.roles]
    permissions = user.get_permissions()

    # Crear nuevo access token
    access_token = create_access_token(
        user_id=user.id,
        username=user.username,
        email=user.email,
        roles=roles,
        permissions=permissions
    )

    # Registrar en audit log
    AuditLog.log_action(
        db=db,
        user_id=user.id,
        username=user.username,
        action="auth.token.refreshed",
        category="authentication",
        status="success",
        ip_address=ip_address
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


# ============================================================================
# LOGOUT
# ============================================================================

def logout(
    db: Session,
    access_token: str,
    refresh_token: Optional[str] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Dict[str, Any]:
    """
    Invalida tokens (logout efectivo).

    Args:
        db: Sesión de base de datos
        access_token: Access token a invalidar
        refresh_token: Refresh token a invalidar (opcional)
        user_id: ID del usuario (opcional, para audit log)
        ip_address: IP del cliente
        user_agent: User agent del navegador

    Returns:
        Diccionario con mensaje y cantidad de tokens invalidados

    Examples:
        >>> result = logout(db, access_token, refresh_token, user_id=1)
        >>> print(result['tokens_invalidated'])
        2

    Notes:
        - Invalida access token y refresh token si se provee
        - Agrega tokens a blacklist
        - Registra en audit log
    """
    tokens_invalidated = 0

    # Invalidar access token
    access_payload = decode_token(access_token)
    if access_payload:
        blacklist_token(
            db=db,
            jti=access_payload['jti'],
            user_id=access_payload['sub'],
            token_type="access",
            expires_at=get_token_expires_at(access_payload),
            token=access_token,
            reason="Logout manual",
            ip_address=ip_address,
            user_agent=user_agent,
            blacklisted_by_id=user_id
        )
        tokens_invalidated += 1

    # Invalidar refresh token si se provee
    if refresh_token:
        refresh_payload = decode_token(refresh_token)
        if refresh_payload:
            blacklist_token(
                db=db,
                jti=refresh_payload['jti'],
                user_id=refresh_payload['sub'],
                token_type="refresh",
                expires_at=get_token_expires_at(refresh_payload),
                token=refresh_token,
                reason="Logout manual",
                ip_address=ip_address,
                user_agent=user_agent,
                blacklisted_by_id=user_id
            )
            tokens_invalidated += 1

    # Limpiar refresh token del usuario
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.refresh_token = None
            db.commit()

        # Registrar logout en audit log
        AuditLog.log_action(
            db=db,
            user_id=user_id,
            username=user.username if user else None,
            action="auth.logout",
            category="authentication",
            status="success",
            details={"tokens_invalidated": tokens_invalidated},
            ip_address=ip_address
        )

    return {
        "message": "Logout exitoso",
        "tokens_invalidated": tokens_invalidated
    }


# ============================================================================
# UTILIDADES
# ============================================================================

def validate_token(db: Session, token: str) -> Dict[str, Any]:
    """
    Valida un token y retorna información sobre su estado.

    Args:
        db: Sesión de base de datos
        token: Token JWT a validar

    Returns:
        Diccionario con información del token

    Examples:
        >>> result = validate_token(db, token)
        >>> print(result['valid'])
        True
        >>> print(result['user_id'])
        1
    """
    payload = decode_token(token)

    if payload is None:
        return {
            "valid": False,
            "expired": True,
            "message": "Token inválido o expirado"
        }

    # Verificar blacklist
    jti = payload.get("jti")
    if jti and is_token_blacklisted(db, jti):
        return {
            "valid": False,
            "blacklisted": True,
            "message": "Token invalidado"
        }

    return {
        "valid": True,
        "expired": False,
        "blacklisted": False,
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "token_type": payload.get("type"),
        "expires_at": datetime.fromtimestamp(payload['exp']).isoformat()
    }
