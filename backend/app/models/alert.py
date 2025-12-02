from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AlertTypeEnum(str, enum.Enum):
    # Exámenes de laboratorio
    PERFIL_LIPIDICO = "perfil_lipidico"
    GLICEMIA = "glicemia"
    HBA1C = "hba1c"
    CREATININA = "creatinina"
    POTASIO = "potasio"
    MICROALBUMINURIA = "microalbuminuria"

    # Exámenes de imágenes
    MAMOGRAFIA = "mamografia"
    ECOGRAFIA = "ecografia"
    RAYOS_X = "rayos_x"
    EKG = "ekg"

    # Tamizajes
    PSA = "psa"
    CITOLOGIA = "citologia"
    VPH = "vph"
    COLONOSCOPIA = "colonoscopia"

    # Evaluaciones
    FONDO_OJO = "fondo_ojo"
    VALORACION_PIE_DIABETICO = "valoracion_pie_diabetico"
    EVALUACION_RIESGO_CV = "evaluacion_riesgo_cardiovascular"

    # Otros
    VACUNA = "vacuna"
    TOMA_PRESION = "toma_presion"
    MEDICION_IMC = "medicion_imc"


class AlertPriorityEnum(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class AlertStatusEnum(str, enum.Enum):
    ACTIVA = "activa"
    NOTIFICADA = "notificada"
    PROGRAMADA = "programada"
    COMPLETADA = "completada"
    IGNORADA = "ignorada"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Patient reference
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Alert info
    alert_type = Column(Enum(AlertTypeEnum), nullable=False, index=True)
    alert_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(AlertPriorityEnum), default=AlertPriorityEnum.MEDIA, index=True)
    status = Column(Enum(AlertStatusEnum), default=AlertStatusEnum.ACTIVA, index=True)

    # Reasoning
    reason = Column(Text, nullable=True)  # Por qué se generó esta alerta
    criteria = Column(Text, nullable=True)  # Criterios que cumplió (edad, sexo, riesgo, etc.)

    # Dates
    created_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)  # Fecha límite recomendada
    notified_date = Column(DateTime, nullable=True)
    completed_date = Column(Date, nullable=True)

    # Action taken
    action_taken = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.alert_type} for Patient {self.patient_id} - {self.priority}>"
