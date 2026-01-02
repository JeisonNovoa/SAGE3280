"""
AuditLog Model - Sistema de Auditoría SAGE3280

Registra todas las acciones importantes del sistema para:
- Trazabilidad y cumplimiento normativo
- Seguridad e investigación de incidentes
- Auditorías administrativas
- Análisis de uso del sistema

Acciones registradas:
- Login/Logout
- Creación/Edición/Eliminación de registros
- Cambios de configuración
- Acceso a información sensible
- Acciones administrativas
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    """
    Registro de auditoría de acciones del sistema.

    Cada registro contiene:
    - Quién: user_id
    - Qué: action
    - Cuándo: timestamp
    - Dónde: ip_address, user_agent
    - Detalles: resource_type, resource_id, details
    """
    __tablename__ = 'audit_logs'

    # ========================================================================
    # IDENTIFICACIÓN
    # ========================================================================
    id = Column(Integer, primary_key=True, index=True)

    # ========================================================================
    # QUIÉN (Usuario)
    # ========================================================================
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        comment="Usuario que realizó la acción (NULL = sistema/anónimo)"
    )

    username = Column(
        String(50),
        nullable=True,
        comment="Username al momento de la acción (por si el usuario se elimina)"
    )

    # ========================================================================
    # QUÉ (Acción)
    # ========================================================================
    action = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Acción realizada (ej: login, patient.create, user.update)"
    )

    # Categoría de la acción (para filtrado)
    category = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Categoría: auth, patient, upload, admin, config, etc."
    )

    # ========================================================================
    # DÓNDE (Recurso afectado)
    # ========================================================================
    resource_type = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Tipo de recurso: patient, user, upload, etc."
    )

    resource_id = Column(
        Integer,
        nullable=True,
        comment="ID del recurso afectado"
    )

    resource_name = Column(
        String(200),
        nullable=True,
        comment="Nombre/identificador del recurso (ej: nombre del paciente)"
    )

    # ========================================================================
    # CUÁNDO
    # ========================================================================
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Fecha y hora de la acción"
    )

    # ========================================================================
    # CONTEXTO (Información técnica)
    # ========================================================================
    ip_address = Column(
        String(50),
        nullable=True,
        comment="Dirección IP del cliente"
    )

    user_agent = Column(
        String(500),
        nullable=True,
        comment="User agent del navegador/cliente"
    )

    # ========================================================================
    # DETALLES
    # ========================================================================
    details = Column(
        JSON,
        nullable=True,
        comment="Detalles adicionales de la acción (cambios, parámetros, etc.)"
    )

    status = Column(
        String(20),
        nullable=True,
        default='success',
        comment="Estado de la acción: success, failed, error"
    )

    error_message = Column(
        Text,
        nullable=True,
        comment="Mensaje de error si la acción falló"
    )

    # ========================================================================
    # RELACIONES
    # ========================================================================
    user = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='audit_logs'
    )

    # ========================================================================
    # MÉTODOS
    # ========================================================================

    def __repr__(self):
        return f"<AuditLog {self.action} by user_id={self.user_id} at {self.timestamp}>"

    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'category': self.category,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'details': self.details,
            'status': self.status,
            'error_message': self.error_message
        }

    @staticmethod
    def log_action(
        db,
        user_id: int = None,
        username: str = None,
        action: str = None,
        category: str = None,
        resource_type: str = None,
        resource_id: int = None,
        resource_name: str = None,
        ip_address: str = None,
        user_agent: str = None,
        details: dict = None,
        status: str = 'success',
        error_message: str = None
    ):
        """
        Método estático para registrar una acción en el log de auditoría.

        Args:
            db: Sesión de base de datos
            user_id: ID del usuario que realizó la acción
            username: Username del usuario
            action: Acción realizada (ej: "login", "patient.create")
            category: Categoría de la acción
            resource_type: Tipo de recurso afectado
            resource_id: ID del recurso afectado
            resource_name: Nombre del recurso
            ip_address: IP del cliente
            user_agent: User agent
            details: Detalles adicionales (dict)
            status: Estado de la acción
            error_message: Mensaje de error si falló

        Returns:
            Objeto AuditLog creado
        """
        audit_log = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            category=category,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            status=status,
            error_message=error_message
        )

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)

        return audit_log


# ========================================================================
# CONSTANTES DE ACCIONES DE AUDITORÍA
# ========================================================================

class AuditActions:
    """
    Constantes para acciones de auditoría.
    Útil para consistencia y autocomplete.
    """

    # Autenticación
    LOGIN_SUCCESS = 'auth.login.success'
    LOGIN_FAILED = 'auth.login.failed'
    LOGOUT = 'auth.logout'
    PASSWORD_CHANGED = 'auth.password.changed'
    TOKEN_REFRESHED = 'auth.token.refreshed'
    ACCOUNT_LOCKED = 'auth.account.locked'

    # Pacientes
    PATIENT_CREATED = 'patient.created'
    PATIENT_UPDATED = 'patient.updated'
    PATIENT_DELETED = 'patient.deleted'
    PATIENT_VIEWED = 'patient.viewed'
    PATIENT_EXPORTED = 'patient.exported'
    PATIENT_CONTACTED = 'patient.contacted'

    # Upload de archivos
    UPLOAD_CREATED = 'upload.created'
    UPLOAD_PROCESSED = 'upload.processed'
    UPLOAD_FAILED = 'upload.failed'
    UPLOAD_DELETED = 'upload.deleted'

    # Usuarios (administración)
    USER_CREATED = 'user.created'
    USER_UPDATED = 'user.updated'
    USER_DELETED = 'user.deleted'
    USER_ACTIVATED = 'user.activated'
    USER_DEACTIVATED = 'user.deactivated'
    USER_ROLE_CHANGED = 'user.role.changed'

    # Roles
    ROLE_CREATED = 'role.created'
    ROLE_UPDATED = 'role.updated'
    ROLE_DELETED = 'role.deleted'

    # Controles
    CONTROL_CREATED = 'control.created'
    CONTROL_UPDATED = 'control.updated'
    CONTROL_DELETED = 'control.deleted'

    # Alertas
    ALERT_CREATED = 'alert.created'
    ALERT_UPDATED = 'alert.updated'
    ALERT_RESOLVED = 'alert.resolved'

    # Configuración
    CONFIG_UPDATED = 'config.updated'
    RULE_CREATED = 'rule.created'
    RULE_UPDATED = 'rule.updated'
    RULE_DELETED = 'rule.deleted'

    # Reportes
    REPORT_GENERATED = 'report.generated'
    REPORT_EXPORTED = 'report.exported'

    # Sistema
    SYSTEM_STARTUP = 'system.startup'
    SYSTEM_SHUTDOWN = 'system.shutdown'
    MIGRATION_EXECUTED = 'system.migration.executed'


class AuditCategories:
    """
    Categorías de acciones de auditoría.
    """
    AUTH = 'auth'
    PATIENT = 'patient'
    UPLOAD = 'upload'
    USER = 'user'
    ROLE = 'role'
    CONTROL = 'control'
    ALERT = 'alert'
    CONFIG = 'config'
    REPORT = 'report'
    SYSTEM = 'system'


# ========================================================================
# ÍNDICES COMPUESTOS
# ========================================================================

# Índices para búsquedas eficientes
Index('idx_audit_user_timestamp', AuditLog.user_id, AuditLog.timestamp)
Index('idx_audit_action_timestamp', AuditLog.action, AuditLog.timestamp)
Index('idx_audit_category_timestamp', AuditLog.category, AuditLog.timestamp)
Index('idx_audit_resource', AuditLog.resource_type, AuditLog.resource_id)
