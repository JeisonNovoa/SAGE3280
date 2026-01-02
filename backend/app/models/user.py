"""
User Model - Sistema de Autenticación SAGE3280

Modelo de usuario con campos de auditoría y seguridad.
Soporta autenticación JWT y control de acceso basado en roles.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# Tabla de asociación many-to-many entre User y Role
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('assigned_at', DateTime(timezone=True), server_default=func.now()),
    Column('assigned_by_id', Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
)


class User(Base):
    """
    Modelo de Usuario para SAGE3280.

    Incluye:
    - Información básica (username, email, nombre completo)
    - Seguridad (password hash, intentos fallidos, bloqueo)
    - Auditoría (creación, actualización, último login)
    - Roles y permisos (relación many-to-many con Role)

    Roles soportados:
    - Admin: Acceso total al sistema
    - Médico: Gestión de pacientes y reportes
    - Auxiliar: Visualización de pacientes y marcado de contactos
    - Operador: Solo carga de archivos Excel
    """
    __tablename__ = 'users'

    # ========================================================================
    # IDENTIFICACIÓN
    # ========================================================================
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=False)

    # ========================================================================
    # SEGURIDAD
    # ========================================================================
    hashed_password = Column(String(255), nullable=False)
    password_changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha del último cambio de contraseña"
    )

    # Protección contra fuerza bruta
    failed_login_attempts = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Número de intentos de login fallidos consecutivos"
    )
    locked_until = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Fecha hasta la cual la cuenta está bloqueada"
    )

    # Refresh token (opcional: guardar en DB para invalidación)
    refresh_token = Column(
        String(500),
        nullable=True,
        comment="Refresh token activo (para invalidación si es necesario)"
    )

    # ========================================================================
    # ESTADO Y PERMISOS
    # ========================================================================
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Si el usuario puede acceder al sistema"
    )
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Si tiene todos los permisos (bypass de roles)"
    )

    # ========================================================================
    # AUDITORÍA
    # ========================================================================
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha de creación del usuario"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="Fecha de última actualización"
    )
    updated_by_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        comment="ID del usuario que realizó la última modificación"
    )
    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Fecha y hora del último login exitoso"
    )

    # ========================================================================
    # RELACIONES
    # ========================================================================
    # Relación con Roles (many-to-many)
    roles = relationship(
        'Role',
        secondary=user_roles,
        back_populates='users',
        lazy='joined',
        primaryjoin='User.id == user_roles.c.user_id',
        secondaryjoin='Role.id == user_roles.c.role_id'
    )

    # Relación con usuario que lo modificó
    updated_by = relationship(
        'User',
        remote_side=[id],
        foreign_keys=[updated_by_id],
        uselist=False
    )

    # Relación con audit logs (historial de acciones)
    audit_logs = relationship(
        'AuditLog',
        back_populates='user',
        foreign_keys='AuditLog.user_id',
        cascade='all, delete-orphan'
    )

    # Relación con tokens blacklisteados
    blacklisted_tokens = relationship(
        'TokenBlacklist',
        back_populates='user',
        foreign_keys='TokenBlacklist.user_id',
        cascade='all, delete-orphan'
    )

    # ========================================================================
    # MÉTODOS
    # ========================================================================

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def to_dict(self):
        """Convierte el usuario a diccionario (sin password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'roles': [role.name for role in self.roles],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'failed_login_attempts': self.failed_login_attempts,
            'is_locked': self.is_locked()
        }

    def has_role(self, role_name: str) -> bool:
        """
        Verifica si el usuario tiene un rol específico.

        Args:
            role_name: Nombre del rol a verificar (ej: "admin", "medico")

        Returns:
            True si el usuario tiene el rol, False en caso contrario
        """
        if self.is_superuser:
            return True
        return any(role.name.lower() == role_name.lower() for role in self.roles)

    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el usuario tiene un permiso específico.

        Args:
            permission: Permiso a verificar (ej: "patients.edit", "upload.create")

        Returns:
            True si el usuario tiene el permiso, False en caso contrario
        """
        if self.is_superuser:
            return True

        for role in self.roles:
            if role.has_permission(permission):
                return True
        return False

    def is_locked(self) -> bool:
        """
        Verifica si la cuenta está bloqueada por intentos fallidos.

        Returns:
            True si la cuenta está bloqueada, False en caso contrario
        """
        if not self.locked_until:
            return False

        from datetime import datetime
        return datetime.now(self.locked_until.tzinfo) < self.locked_until

    def increment_failed_login(self):
        """
        Incrementa el contador de intentos fallidos.
        Bloquea la cuenta si supera el límite.
        """
        from datetime import datetime, timedelta

        self.failed_login_attempts += 1

        # Bloquear cuenta después de 5 intentos fallidos
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.now() + timedelta(minutes=15)

    def reset_failed_login(self):
        """Resetea el contador de intentos fallidos después de login exitoso."""
        self.failed_login_attempts = 0
        self.locked_until = None

    def get_permissions(self) -> list:
        """
        Obtiene lista de todos los permisos del usuario.

        Returns:
            Lista de strings con los permisos
        """
        if self.is_superuser:
            return ["*"]  # Superusuario tiene todos los permisos

        permissions = set()
        for role in self.roles:
            permissions.update(role.get_permissions())

        return sorted(list(permissions))
