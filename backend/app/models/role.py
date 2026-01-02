"""
Role Model - Sistema de Roles y Permisos SAGE3280

Define los roles del sistema y sus permisos asociados.
Usa RBAC (Role-Based Access Control) simplificado.

Roles predefinidos:
- Admin: Acceso completo al sistema
- Médico: Gestión de pacientes, consultas y reportes
- Auxiliar: Visualización de pacientes y marcado de contactos
- Operador: Solo carga de archivos Excel
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import user_roles


class Role(Base):
    """
    Modelo de Rol para control de acceso basado en roles (RBAC).

    Cada rol tiene un conjunto predefinido de permisos que determinan
    qué acciones puede realizar un usuario en el sistema.
    """
    __tablename__ = 'roles'

    # ========================================================================
    # IDENTIFICACIÓN
    # ========================================================================
    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Nombre del rol (admin, medico, auxiliar, operador)"
    )
    display_name = Column(
        String(100),
        nullable=False,
        comment="Nombre para mostrar en UI"
    )
    description = Column(
        Text,
        nullable=True,
        comment="Descripción detallada del rol y sus capacidades"
    )

    # ========================================================================
    # PERMISOS
    # ========================================================================
    permissions = Column(
        JSON,
        nullable=False,
        default=list,
        comment="Lista de permisos en formato ['resource.action', ...]"
    )

    # ========================================================================
    # ESTADO Y AUDITORÍA
    # ========================================================================
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Si el rol está activo y puede ser asignado"
    )
    is_system_role = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Si es un rol del sistema (no se puede eliminar)"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )

    # ========================================================================
    # RELACIONES
    # ========================================================================
    users = relationship(
        'User',
        secondary=user_roles,
        back_populates='roles',
        primaryjoin='Role.id == user_roles.c.role_id',
        secondaryjoin='User.id == user_roles.c.user_id'
    )

    # ========================================================================
    # MÉTODOS
    # ========================================================================

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        """Convierte el rol a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'permissions': self.permissions,
            'is_active': self.is_active,
            'is_system_role': self.is_system_role,
            'user_count': len(self.users),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el rol tiene un permiso específico.

        Soporta wildcards:
        - "patients.*" permite "patients.create", "patients.read", etc.
        - "*" permite todo

        Args:
            permission: Permiso a verificar (ej: "patients.edit")

        Returns:
            True si el rol tiene el permiso, False en caso contrario
        """
        if not self.is_active:
            return False

        if not self.permissions:
            return False

        # Wildcard completo
        if "*" in self.permissions:
            return True

        # Permiso exacto
        if permission in self.permissions:
            return True

        # Wildcard de recurso (ej: "patients.*" permite "patients.create")
        resource = permission.split('.')[0] if '.' in permission else permission
        resource_wildcard = f"{resource}.*"
        if resource_wildcard in self.permissions:
            return True

        return False

    def get_permissions(self) -> list:
        """
        Obtiene la lista de permisos del rol.

        Returns:
            Lista de permisos
        """
        return self.permissions if self.permissions else []

    @staticmethod
    def get_role_permissions_map():
        """
        Define los permisos predefinidos para cada rol del sistema.

        Returns:
            Diccionario con permisos por rol
        """
        return {
            'admin': {
                'display_name': 'Administrador',
                'description': 'Acceso completo al sistema. Puede gestionar usuarios, configuración y todos los módulos.',
                'permissions': ['*'],  # Acceso total
                'is_system_role': True
            },
            'medico': {
                'display_name': 'Médico',
                'description': 'Profesional de salud. Puede gestionar pacientes, consultas, controles y generar reportes médicos.',
                'permissions': [
                    # Pacientes
                    'patients.create',
                    'patients.read',
                    'patients.update',
                    'patients.delete',
                    'patients.export',
                    # Consultas y controles
                    'consultations.create',
                    'consultations.read',
                    'consultations.update',
                    'controls.create',
                    'controls.read',
                    'controls.update',
                    # Alertas
                    'alerts.read',
                    'alerts.update',
                    # Reportes
                    'reports.read',
                    'reports.create',
                    'reports.export',
                    # Catálogos (solo lectura)
                    'catalogs.read',
                    # Estadísticas
                    'stats.read',
                ],
                'is_system_role': True
            },
            'auxiliar': {
                'display_name': 'Auxiliar de Enfermería',
                'description': 'Personal de apoyo. Puede ver pacientes, marcar contactos y realizar seguimiento básico.',
                'permissions': [
                    # Pacientes (solo lectura y contacto)
                    'patients.read',
                    'patients.contact',  # Marcar como contactado
                    'patients.export',
                    # Controles (solo lectura)
                    'controls.read',
                    # Alertas (solo lectura)
                    'alerts.read',
                    # Catálogos (solo lectura)
                    'catalogs.read',
                    # Estadísticas (solo lectura)
                    'stats.read',
                ],
                'is_system_role': True
            },
            'operador': {
                'display_name': 'Operador de Datos',
                'description': 'Personal administrativo. Puede cargar archivos Excel y ver estadísticas básicas.',
                'permissions': [
                    # Upload de archivos
                    'upload.create',
                    'upload.read',
                    # Pacientes (solo lectura)
                    'patients.read',
                    # Estadísticas (solo lectura)
                    'stats.read',
                    # Catálogos (solo lectura)
                    'catalogs.read',
                ],
                'is_system_role': True
            }
        }


# ============================================================================
# CONSTANTES DE PERMISOS
# ============================================================================

class Permissions:
    """
    Constantes de permisos del sistema.

    Organizado por recurso y acción.
    Útil para validaciones y autocomplete en IDE.
    """

    # Pacientes
    PATIENTS_CREATE = 'patients.create'
    PATIENTS_READ = 'patients.read'
    PATIENTS_UPDATE = 'patients.update'
    PATIENTS_DELETE = 'patients.delete'
    PATIENTS_EXPORT = 'patients.export'
    PATIENTS_CONTACT = 'patients.contact'

    # Consultas
    CONSULTATIONS_CREATE = 'consultations.create'
    CONSULTATIONS_READ = 'consultations.read'
    CONSULTATIONS_UPDATE = 'consultations.update'
    CONSULTATIONS_DELETE = 'consultations.delete'

    # Controles
    CONTROLS_CREATE = 'controls.create'
    CONTROLS_READ = 'controls.read'
    CONTROLS_UPDATE = 'controls.update'
    CONTROLS_DELETE = 'controls.delete'

    # Alertas
    ALERTS_CREATE = 'alerts.create'
    ALERTS_READ = 'alerts.read'
    ALERTS_UPDATE = 'alerts.update'
    ALERTS_DELETE = 'alerts.delete'

    # Reportes
    REPORTS_CREATE = 'reports.create'
    REPORTS_READ = 'reports.read'
    REPORTS_EXPORT = 'reports.export'
    REPORTS_DELETE = 'reports.delete'

    # Upload de archivos
    UPLOAD_CREATE = 'upload.create'
    UPLOAD_READ = 'upload.read'
    UPLOAD_DELETE = 'upload.delete'

    # Estadísticas
    STATS_READ = 'stats.read'

    # Catálogos (EPS, CIE-10, CUPS)
    CATALOGS_READ = 'catalogs.read'
    CATALOGS_UPDATE = 'catalogs.update'

    # Usuarios (solo admin)
    USERS_CREATE = 'users.create'
    USERS_READ = 'users.read'
    USERS_UPDATE = 'users.update'
    USERS_DELETE = 'users.delete'

    # Roles (solo admin)
    ROLES_CREATE = 'roles.create'
    ROLES_READ = 'roles.read'
    ROLES_UPDATE = 'roles.update'
    ROLES_DELETE = 'roles.delete'

    # Configuración (solo admin)
    CONFIG_READ = 'config.read'
    CONFIG_UPDATE = 'config.update'

    # Auditoría (solo admin)
    AUDIT_READ = 'audit.read'
