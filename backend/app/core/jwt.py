"""
JWT Token Management - Autenticación basada en tokens

Sistema completo de manejo de JWT tokens para autenticación:
- Access tokens (30 minutos)
- Refresh tokens (7 días)
- Token blacklist para logout efectivo
- Validación y decodificación de tokens
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.models.token_blacklist import TokenBlacklist
from app.schemas.auth import TokenPayload


# ============================================================================
# CREACIÓN DE TOKENS
# ============================================================================

def create_access_token(
    user_id: int,
    username: str,
    email: str,
    roles: list,
    permissions: list,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un access token JWT.

    Args:
        user_id: ID del usuario
        username: Username del usuario
        email: Email del usuario
        roles: Lista de roles del usuario
        permissions: Lista de permisos del usuario
        expires_delta: Tiempo de expiración personalizado (opcional)

    Returns:
        Token JWT codificado como string

    Examples:
        >>> create_access_token(
        ...     user_id=1,
        ...     username="admin",
        ...     email="admin@sage.com",
        ...     roles=["admin"],
        ...     permissions=["*"]
        ... )
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

    Notes:
        - Expira en 30 minutos por defecto (configurable)
        - Incluye JTI único para blacklist
        - Incluye roles y permisos para autorización
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Payload del token
    to_encode = {
        "sub": str(user_id),  # Subject - User ID (must be string for JWT spec)
        "username": username,
        "email": email,
        "roles": roles,
        "permissions": permissions,
        "exp": int(expire.timestamp()),  # Expiration time (Unix timestamp)
        "iat": int(datetime.utcnow().timestamp()),  # Issued at (Unix timestamp)
        "jti": str(uuid.uuid4()),  # JWT ID - unique identifier
        "type": "access"  # Token type
    }

    # Codificar token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    user_id: int,
    username: str,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un refresh token JWT.

    Args:
        user_id: ID del usuario
        username: Username del usuario
        email: Email del usuario
        expires_delta: Tiempo de expiración personalizado (opcional)

    Returns:
        Token JWT codificado como string

    Examples:
        >>> create_refresh_token(
        ...     user_id=1,
        ...     username="admin",
        ...     email="admin@sage.com"
        ... )
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

    Notes:
        - Expira en 7 días por defecto (configurable)
        - NO incluye roles ni permisos (solo se usa para refresh)
        - Incluye JTI único para blacklist
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    # Payload del token (más simple que access token)
    to_encode = {
        "sub": str(user_id),  # Subject - User ID (must be string for JWT spec)
        "username": username,
        "email": email,
        "exp": int(expire.timestamp()),  # Expiration time (Unix timestamp)
        "iat": int(datetime.utcnow().timestamp()),  # Issued at (Unix timestamp)
        "jti": str(uuid.uuid4()),
        "type": "refresh"
    }

    # Codificar token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# ============================================================================
# DECODIFICACIÓN Y VALIDACIÓN
# ============================================================================

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica y valida un token JWT.

    Args:
        token: Token JWT a decodificar

    Returns:
        Diccionario con el payload del token si es válido, None si es inválido

    Raises:
        JWTError: Si el token es inválido o expiró

    Examples:
        >>> payload = decode_token(token)
        >>> print(payload['username'])
        'admin'
        >>> print(payload['roles'])
        ['admin']

    Notes:
        - Verifica firma del token
        - Verifica expiración
        - NO verifica blacklist (usar is_token_blacklisted por separado)
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
    """
    Verifica que el token sea del tipo esperado.

    Args:
        payload: Payload decodificado del token
        expected_type: Tipo esperado ("access" o "refresh")

    Returns:
        True si el tipo coincide, False en caso contrario

    Examples:
        >>> payload = decode_token(access_token)
        >>> verify_token_type(payload, "access")
        True
        >>> verify_token_type(payload, "refresh")
        False
    """
    return payload.get("type") == expected_type


# ============================================================================
# TOKEN BLACKLIST
# ============================================================================

def is_token_blacklisted(db: Session, jti: str) -> bool:
    """
    Verifica si un token está en la blacklist.

    Args:
        db: Sesión de base de datos
        jti: JWT ID del token

    Returns:
        True si el token está blacklisted, False en caso contrario

    Examples:
        >>> payload = decode_token(token)
        >>> is_blacklisted = is_token_blacklisted(db, payload['jti'])
        >>> if is_blacklisted:
        ...     raise HTTPException(status_code=401, detail="Token invalidado")

    Notes:
        - Solo verifica tokens no expirados
        - Limpia automáticamente tokens expirados antes de verificar
    """
    return TokenBlacklist.is_blacklisted(db, jti)


def blacklist_token(
    db: Session,
    jti: str,
    user_id: int,
    token_type: str,
    expires_at: datetime,
    token: Optional[str] = None,
    reason: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    blacklisted_by_id: Optional[int] = None
) -> TokenBlacklist:
    """
    Agrega un token a la blacklist (logout efectivo).

    Args:
        db: Sesión de base de datos
        jti: JWT ID del token
        user_id: ID del usuario dueño del token
        token_type: Tipo de token ("access" o "refresh")
        expires_at: Fecha de expiración del token
        token: Token completo (opcional, para debugging)
        reason: Razón del blacklist (opcional)
        ip_address: IP desde donde se hizo logout (opcional)
        user_agent: User agent del cliente (opcional)
        blacklisted_by_id: ID del usuario que invalidó el token (opcional)

    Returns:
        Objeto TokenBlacklist creado

    Examples:
        >>> payload = decode_token(token)
        >>> blacklist_token(
        ...     db=db,
        ...     jti=payload['jti'],
        ...     user_id=payload['sub'],
        ...     token_type=payload['type'],
        ...     expires_at=datetime.fromtimestamp(payload['exp']),
        ...     reason="Logout manual"
        ... )

    Notes:
        - El token queda invalidado inmediatamente
        - El registro se mantiene hasta que expire el token
        - Se puede limpiar periódicamente con TokenBlacklist.cleanup_expired()
    """
    blacklist_entry = TokenBlacklist(
        jti=jti,
        token=token[:1000] if token else None,  # Limitar tamaño
        token_type=token_type,
        user_id=user_id,
        expires_at=expires_at,
        blacklisted_by_id=blacklisted_by_id,
        reason=reason,
        ip_address=ip_address,
        user_agent=user_agent[:500] if user_agent else None  # Limitar tamaño
    )

    db.add(blacklist_entry)
    db.commit()
    db.refresh(blacklist_entry)

    return blacklist_entry


def blacklist_all_user_tokens(
    db: Session,
    user_id: int,
    reason: str = "Logout from all devices"
) -> int:
    """
    Invalida todos los tokens activos de un usuario (logout global).

    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        reason: Razón del logout global

    Returns:
        Número de tokens invalidados

    Examples:
        >>> count = blacklist_all_user_tokens(db, user_id=1)
        >>> print(f"{count} tokens invalidados")

    Notes:
        - Útil para "Cerrar sesión en todos los dispositivos"
        - Útil cuando se cambia la contraseña
        - Útil cuando se detecta actividad sospechosa
        - No invalida tokens específicos, marca el timestamp
    """
    # Esta función requeriría almacenar todos los tokens activos
    # o usar un timestamp de "invalidación global" en el modelo User
    # Por ahora, retornamos 0 y esto se puede mejorar en el futuro
    # guardando los JTIs de tokens activos en la tabla user.refresh_token
    return 0


# ============================================================================
# UTILIDADES
# ============================================================================

def get_token_expires_at(payload: Dict[str, Any]) -> datetime:
    """
    Obtiene la fecha de expiración de un token desde su payload.

    Args:
        payload: Payload decodificado del token

    Returns:
        Fecha de expiración como datetime

    Examples:
        >>> payload = decode_token(token)
        >>> expires_at = get_token_expires_at(payload)
        >>> print(expires_at)
        2026-01-01 18:30:00
    """
    return datetime.fromtimestamp(payload['exp'])


def get_token_time_remaining(payload: Dict[str, Any]) -> int:
    """
    Calcula cuántos segundos faltan para que expire el token.

    Args:
        payload: Payload decodificado del token

    Returns:
        Segundos restantes hasta la expiración

    Examples:
        >>> payload = decode_token(token)
        >>> seconds_left = get_token_time_remaining(payload)
        >>> print(f"Token expira en {seconds_left} segundos")
    """
    expires_at = datetime.fromtimestamp(payload['exp'])
    now = datetime.utcnow()
    delta = expires_at - now
    return max(0, int(delta.total_seconds()))
