"""
Security Utilities - Password Hashing y Verificación

Utiliza bcrypt directamente para hashing seguro de contraseñas.
Compatible con los hashes generados en la migración.
"""
import bcrypt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña almacenado en DB

    Returns:
        True si la contraseña coincide, False en caso contrario

    Examples:
        >>> verify_password("Admin123!", "$2b$12$LQv3c1yqBWVHxkd...")
        True
        >>> verify_password("wrongpass", "$2b$12$LQv3c1yqBWVHxkd...")
        False
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except (ValueError, AttributeError):
        return False


def get_password_hash(password: str) -> str:
    """
    Genera un hash bcrypt de la contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash bcrypt de la contraseña

    Examples:
        >>> get_password_hash("Admin123!")
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeZMqVlXCh/4.VAAe'

    Notes:
        - Usa 12 rounds por defecto (configurable en settings.BCRYPT_ROUNDS)
        - Cada vez que se llama genera un salt aleatorio diferente
        - El mismo password generará diferentes hashes (esto es correcto)
    """
    # Generar salt con el número de rounds configurado
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)

    # Generar hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Retornar como string
    return hashed.decode('utf-8')


def needs_update(hashed_password: str) -> bool:
    """
    Verifica si un hash necesita ser actualizado.

    Args:
        hashed_password: Hash almacenado en DB

    Returns:
        True si el hash usa rounds diferentes a la configuración actual

    Notes:
        Útil para re-hashear passwords con configuración actualizada
    """
    try:
        # Extraer el número de rounds del hash
        # Un hash bcrypt tiene formato: $2b$12$...
        # Donde 12 es el número de rounds
        parts = hashed_password.split('$')
        if len(parts) >= 3:
            current_rounds = int(parts[2])
            return current_rounds != settings.BCRYPT_ROUNDS
        return False
    except (ValueError, IndexError):
        return True  # Si no podemos parsear, mejor actualizar
