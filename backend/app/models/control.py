from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ControlTypeEnum(str, enum.Enum):
    # Controles RIAS por grupo etario (Grupo A - Prevención)
    CONTROL_PRIMERA_INFANCIA = "control_primera_infancia"  # 0-5 años
    CONTROL_CRECIMIENTO_DESARROLLO = "control_crecimiento_desarrollo"  # 0-5 años
    CONTROL_INFANCIA = "control_infancia"  # 6-11 años
    CONTROL_ADOLESCENCIA = "control_adolescencia"  # 12-17 años
    CONTROL_JUVENTUD = "control_juventud"  # 18-28 años
    CONTROL_ADULTEZ = "control_adultez"  # 29-59 años
    CONTROL_VEJEZ = "control_vejez"  # 60+ años

    # Controles preventivos específicos (Grupo A)
    SALUD_SEXUAL_REPRODUCTIVA = "salud_sexual_reproductiva"
    PLANIFICACION_FAMILIAR = "planificacion_familiar"
    DETECCION_ITS = "deteccion_its"  # Infecciones de transmisión sexual
    SALUD_MENTAL = "salud_mental"
    SALUD_ORAL = "salud_oral"
    VALORACION_NUTRICIONAL = "valoracion_nutricional"
    VALORACION_GERIATRICA = "valoracion_geriatrica"
    EVALUACION_FUNCIONALIDAD = "evaluacion_funcionalidad"  # Adulto mayor
    VACUNACION = "vacunacion"

    # Controles para condiciones crónicas (Grupo B)
    CONTROL_PRENATAL = "control_prenatal"
    CONTROL_HIPERTENSO = "control_hipertenso"
    CONTROL_DIABETICO = "control_diabetico"
    CONTROL_HIPOTIROIDISMO = "control_hipotiroidismo"
    CONTROL_EPOC = "control_epoc"  # Enfermedad Pulmonar Obstructiva Crónica
    CONTROL_ASMA = "control_asma"
    CONTROL_IRC = "control_irc"  # Insuficiencia Renal Crónica
    CONTROL_CARDIOVASCULAR = "control_cardiovascular"  # Enfermedad cardiovascular establecida
    CONTROL_RIESGO_CV = "control_riesgo_cardiovascular"  # Evaluación de riesgo

    # Controles de seguimiento
    CONTROL_MEDICAMENTOS = "control_medicamentos"  # Revisión de adherencia
    CONTROL_RESULTADOS = "control_resultados"  # Revisión de resultados de exámenes


class ControlStatusEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    PROGRAMADO = "programado"
    COMPLETADO = "completado"
    VENCIDO = "vencido"
    CANCELADO = "cancelado"


class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)

    # Patient reference
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Control info
    control_type = Column(Enum(ControlTypeEnum), nullable=False, index=True)
    control_name = Column(String(200), nullable=False)
    status = Column(Enum(ControlStatusEnum), default=ControlStatusEnum.PENDIENTE, index=True)

    # Dates
    last_date = Column(Date, nullable=True)  # Fecha del último control de este tipo
    due_date = Column(Date, nullable=True)  # Fecha esperada del próximo control
    scheduled_date = Column(Date, nullable=True)  # Fecha programada (si ya tiene cita)
    completed_date = Column(Date, nullable=True)  # Fecha en que se completó

    # Priority
    is_urgent = Column(Boolean, default=False)
    priority_score = Column(Integer, default=0)  # 0-100, calculado según riesgo

    # Frequency and description (from Resolución 3280/412)
    recommended_frequency_days = Column(Integer, nullable=True)  # Frecuencia recomendada en días
    description = Column(String(500), nullable=True)  # Descripción del control según RIAS

    # Notes
    notes = Column(String(500), nullable=True)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="controls")

    def __repr__(self):
        return f"<Control {self.control_type} for Patient {self.patient_id} - {self.status}>"
