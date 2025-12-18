from sqlalchemy import Column, Integer, String, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class ControlRule(Base):
    """
    Reglas configurables para generación de controles.

    Permite parametrizar las reglas de negocio sin modificar código,
    facilitando ajustes según cambios normativos o necesidades específicas.
    """
    __tablename__ = "control_rules"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Identificación de la regla
    rule_code = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "CONTROL_HTA_MENSUAL"
    rule_name = Column(String(200), nullable=False)  # e.g., "Control de Hipertensión Arterial"
    description = Column(Text, nullable=True)  # Descripción detallada

    # Control Type
    control_type = Column(String(100), nullable=False)  # ControlTypeEnum value

    # Criterios de aplicación (JSON para flexibilidad)
    criteria = Column(JSON, nullable=False)
    # Ejemplo:
    # {
    #     "age_min": 18,
    #     "age_max": null,
    #     "age_group": "adultez",
    #     "sex": null,  # null = ambos
    #     "requires_condition": ["is_hypertensive"],  # Condiciones requeridas
    #     "excludes_condition": [],  # Condiciones excluyentes
    #     "attention_type": ["grupo_b"]  # A qué grupos aplica
    # }

    # Frecuencia y urgencia
    frequency_days = Column(Integer, nullable=True)  # Cada cuántos días
    is_urgent_if_overdue = Column(Boolean, default=True)  # ¿Es urgente si está vencido?
    overdue_threshold_days = Column(Integer, nullable=True)  # Días de tolerancia antes de marcar urgente

    # Prioridad (para ordenar controles)
    priority = Column(Integer, default=50)  # 0-100, mayor = más prioritario

    # RIAS Information
    rias_stage = Column(String(50), nullable=True)  # e.g., "primera_infancia", "adultez"
    rias_description = Column(Text, nullable=True)  # Descripción oficial RIAS
    normative_reference = Column(String(200), nullable=True)  # e.g., "Resolución 3280 de 2018"

    # Estado
    is_active = Column(Boolean, default=True)  # Permite desactivar reglas sin eliminarlas

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(200), nullable=True)
    updated_by = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)  # Notas administrativas

    def __repr__(self):
        return f"<ControlRule {self.rule_code} - {self.rule_name}>"
