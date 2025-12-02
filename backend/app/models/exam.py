from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ExamTypeEnum(str, enum.Enum):
    """
    Types of exams tracked in the system.
    Maps to AlertTypeEnum for consistency.
    """
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


class ExamResultEnum(str, enum.Enum):
    """Result status of exam"""
    NORMAL = "normal"
    ANORMAL = "anormal"
    PENDIENTE_RESULTADO = "pendiente_resultado"
    NO_CONCLUYENTE = "no_concluyente"


class Exam(Base):
    """
    Model to track patient exam history.

    This model stores all completed (and scheduled) exams for patients,
    allowing the system to:
    1. Avoid generating duplicate alerts for recent exams
    2. Track exam history for better patient care
    3. Calculate due dates based on last exam date
    4. Generate reports on exam compliance
    """
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    # Patient reference
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Exam info
    exam_type = Column(Enum(ExamTypeEnum), nullable=False, index=True)
    exam_name = Column(String(200), nullable=False)

    # Dates
    exam_date = Column(Date, nullable=False, index=True)  # When exam was performed
    ordered_date = Column(Date, nullable=True)  # When exam was ordered
    result_date = Column(Date, nullable=True)  # When results were received

    # Result
    result_status = Column(Enum(ExamResultEnum), default=ExamResultEnum.PENDIENTE_RESULTADO)
    result_value = Column(String(200), nullable=True)  # Numeric or text result (e.g., "120 mg/dL", "Negativo")
    result_numeric = Column(Float, nullable=True)  # Numeric value if applicable (for trending)
    result_notes = Column(Text, nullable=True)  # Additional notes about result

    # Provider info
    provider = Column(String(200), nullable=True)  # Where exam was done
    ordered_by = Column(String(200), nullable=True)  # Doctor who ordered it

    # Follow-up
    requires_followup = Column(String(10), nullable=True)  # "si" or "no"
    followup_notes = Column(Text, nullable=True)

    # Integration
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)  # Link to alert that generated this

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(200), nullable=True)  # User who registered the exam

    # Relationships
    patient = relationship("Patient", back_populates="exams")

    def __repr__(self):
        return f"<Exam {self.exam_type} for Patient {self.patient_id} on {self.exam_date}>"

    def is_recent(self, interval_days: int) -> bool:
        """Check if exam is recent enough (within interval_days from today)"""
        from datetime import date, timedelta
        cutoff_date = date.today() - timedelta(days=interval_days)
        return self.exam_date >= cutoff_date
