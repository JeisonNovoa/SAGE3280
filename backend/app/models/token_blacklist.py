"""
TokenBlacklist Model - Sistema de Invalidación de Tokens JWT

Permite implementar logout efectivo al invalidar tokens.
Los tokens blacklisteados no pueden ser usados aunque sean válidos.

Casos de uso:
- Logout manual del usuario
- Cambio de contraseña (invalidar todos los tokens)
- Desactivación de cuenta
- Revocación administrativa
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TokenBlacklist(Base):
    """
    Lista negra de tokens JWT invalidados.

    Un token en esta tabla no puede ser usado aunque sea válido
    según su firma y fecha de expiración.

    Limpieza automática:
    - Se deben eliminar tokens expirados periódicamente
    - Usar tarea programada (cron) o al momento de validar
    """
    __tablename__ = 'token_blacklist'

    # ========================================================================
    # IDENTIFICACIÓN
    # ========================================================================
    id = Column(Integer, primary_key=True, index=True)

    # JTI (JWT ID) - Identificador único del token
    # Se obtiene del claim "jti" en el payload del JWT
    jti = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
        comment="JWT ID (jti claim) - Identificador único del token"
    )

    # Token completo (opcional, para debugging)
    # ADVERTENCIA: Almacenar tokens completos puede ser un riesgo de seguridad
    # Solo almacenar si es necesario para auditoría
    token = Column(
        String(1000),
        nullable=True,
        comment="Token completo (opcional, solo para auditoría)"
    )

    # ========================================================================
    # INFORMACIÓN DEL TOKEN
    # ========================================================================
    token_type = Column(
        String(20),
        nullable=False,
        default='access',
        comment="Tipo de token: 'access' o 'refresh'"
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment="Usuario dueño del token"
    )

    # ========================================================================
    # EXPIRACIÓN
    # ========================================================================
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Fecha de expiración del token (para limpieza automática)"
    )

    # ========================================================================
    # AUDITORÍA
    # ========================================================================
    blacklisted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Cuándo fue blacklisteado"
    )

    blacklisted_by_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        comment="Quién blacklisteó el token (para revocación administrativa)"
    )

    reason = Column(
        String(200),
        nullable=True,
        comment="Razón de la invalidación: logout, password_change, admin_revoke, etc."
    )

    ip_address = Column(
        String(50),
        nullable=True,
        comment="IP desde donde se realizó el logout/invalidación"
    )

    user_agent = Column(
        String(500),
        nullable=True,
        comment="User agent del navegador/cliente"
    )

    # ========================================================================
    # RELACIONES
    # ========================================================================
    user = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='blacklisted_tokens'
    )

    blacklisted_by = relationship(
        'User',
        foreign_keys=[blacklisted_by_id]
    )

    # ========================================================================
    # MÉTODOS
    # ========================================================================

    def __repr__(self):
        return f"<TokenBlacklist jti={self.jti[:8]}... user_id={self.user_id}>"

    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'blacklisted_at': self.blacklisted_at.isoformat() if self.blacklisted_at else None,
            'reason': self.reason,
            'ip_address': self.ip_address
        }

    @staticmethod
    def is_blacklisted(db, jti: str) -> bool:
        """
        Verifica si un token está en la lista negra.

        Args:
            db: Sesión de base de datos
            jti: JWT ID del token

        Returns:
            True si está blacklisteado, False en caso contrario
        """
        from datetime import datetime

        # Buscar token en blacklist
        token = db.query(TokenBlacklist).filter(
            TokenBlacklist.jti == jti,
            TokenBlacklist.expires_at > datetime.now()  # Solo tokens no expirados
        ).first()

        return token is not None

    @staticmethod
    def cleanup_expired_tokens(db):
        """
        Elimina tokens expirados de la blacklist.

        Se debe ejecutar periódicamente (ej: cron diario)
        para mantener la tabla limpia.

        Args:
            db: Sesión de base de datos

        Returns:
            Número de tokens eliminados
        """
        from datetime import datetime

        deleted = db.query(TokenBlacklist).filter(
            TokenBlacklist.expires_at <= datetime.now()
        ).delete()

        db.commit()
        return deleted

    @staticmethod
    def blacklist_all_user_tokens(db, user_id: int, reason: str = "logout_all"):
        """
        Invalida todos los tokens de un usuario.

        Útil para:
        - Cambio de contraseña (invalidar sesiones en todos los dispositivos)
        - Desactivación de cuenta
        - Revocación administrativa

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            reason: Razón de la invalidación

        Returns:
            Número de tokens blacklisteados
        """
        # NOTA: Esto requiere guardar todos los tokens activos en DB
        # o usar una estrategia diferente (ej: timestamp de "invalidar antes de")

        # Por simplicidad, marcaremos un flag en el usuario
        # En producción, considerar guardar todos los JTI activos

        return 0  # Placeholder - Implementar según estrategia elegida


# Agregar relación inversa a User
# (Debe agregarse en user.py después de importar TokenBlacklist)
# User.blacklisted_tokens = relationship('TokenBlacklist', foreign_keys='TokenBlacklist.user_id')


# ========================================================================
# ÍNDICES COMPUESTOS
# ========================================================================

# Índice compuesto para búsquedas eficientes
Index('idx_blacklist_jti_expires', TokenBlacklist.jti, TokenBlacklist.expires_at)
Index('idx_blacklist_user_expires', TokenBlacklist.user_id, TokenBlacklist.expires_at)
