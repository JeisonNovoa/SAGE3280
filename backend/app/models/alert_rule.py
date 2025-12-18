from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class AlertRule(Base):
    """
    Reglas configurables para generación de alertas.

    Permite parametrizar umbrales, criterios y prioridades de alertas
    sin modificar código, facilitando ajustes normativos.
    """
    __tablename__ = "alert_rules"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Identificación de la regla
    rule_code = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "ALERT_HBA1C_DIABETES"
    rule_name = Column(String(200), nullable=False)  # e.g., "Hemoglobina Glicosilada (HbA1c)"
    description = Column(Text, nullable=True)  # Descripción detallada del examen/alerta

    # Alert Type
    alert_type = Column(String(100), nullable=False)  # AlertTypeEnum value

    # Criterios de aplicación (JSON para flexibilidad)
    criteria = Column(JSON, nullable=False)
    # Ejemplo:
    # {
    #     "age_min": 40,
    #     "age_max": null,
    #     "age_group": null,
    #     "sex": "F",  # M, F, null = ambos
    #     "requires_condition": ["is_diabetic"],  # Condiciones requeridas
    #     "excludes_condition": ["is_pregnant"],  # Condiciones excluyentes
    #     "attention_type": ["grupo_b"],  # A qué grupos aplica
    #     "additional_criteria": {
    #         "last_hba1c_date": {"older_than_days": 90}
    #     }
    # }

    # Frecuencia y periodicidad
    frequency_days = Column(Integer, nullable=True)  # Cada cuántos días debe realizarse
    due_date_calculation = Column(String(50), default="frequency")  # "frequency", "custom", "condition_based"

    # Prioridad
    priority = Column(String(20), nullable=False)  # AlertPriorityEnum: urgente, alta, media, baja
    priority_score = Column(Integer, default=50)  # 0-100 para ordenar

    # Umbrales (si aplica - para alertas basadas en valores)
    threshold_config = Column(JSON, nullable=True)
    # Ejemplo para alertas de laboratorio:
    # {
    #     "hba1c": {"critical": 9.0, "warning": 7.5, "optimal": 7.0},
    #     "glucose": {"critical": 180, "warning": 140, "optimal": 100}
    # }

    # Motivo/Razón (mensaje al usuario)
    reason_template = Column(Text, nullable=True)  # e.g., "Control de diabetes - cada {frequency_days} días"

    # Información normativa
    normative_reference = Column(String(200), nullable=True)  # e.g., "Resolución 412 de 2000"
    clinical_guidelines = Column(Text, nullable=True)  # Guías clínicas aplicables

    # Estado
    is_active = Column(Boolean, default=True)  # Permite desactivar reglas sin eliminarlas

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(200), nullable=True)
    updated_by = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)  # Notas administrativas

    def __repr__(self):
        return f"<AlertRule {self.rule_code} - {self.rule_name}>"
