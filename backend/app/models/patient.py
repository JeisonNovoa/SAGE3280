from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class SexEnum(str, enum.Enum):
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "O"


class AgeGroupEnum(str, enum.Enum):
    PRIMERA_INFANCIA = "primera_infancia"  # 0-5 años
    INFANCIA = "infancia"  # 6-11 años
    ADOLESCENCIA = "adolescencia"  # 12-17 años
    JUVENTUD = "juventud"  # 18-28 años
    ADULTEZ = "adultez"  # 29-59 años
    VEJEZ = "vejez"  # 60+ años


class RiskLevelEnum(str, enum.Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"
    MUY_ALTO = "muy_alto"


class AttentionTypeEnum(str, enum.Enum):
    """
    Tipo de atención según clasificación SAGE3280:
    - GRUPO_A: Atención preventiva (RIAS) - Pacientes sanos o con factores de riesgo
    - GRUPO_B: Paciente crónico - Seguimiento activo de condiciones crónicas
    - GRUPO_C: Consulta externa general - No clasificable en A o B
    """
    GRUPO_A = "grupo_a"  # Atención Preventiva (RIAS)
    GRUPO_B = "grupo_b"  # Paciente Crónico
    GRUPO_C = "grupo_c"  # Consulta Externa General


class Patient(Base):
    __tablename__ = "patients"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Identificación
    document_type = Column(String(10), nullable=True)  # CC, TI, RC, etc.
    document_number = Column(String(20), nullable=False, unique=True, index=True)

    # Datos personales
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False, index=True)
    birth_date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(Enum(SexEnum), nullable=True)

    # Clasificación
    age_group = Column(Enum(AgeGroupEnum), nullable=True, index=True)
    attention_type = Column(String(20), nullable=True, index=True)  # Grupo A/B/C (grupo_a, grupo_b, grupo_c)

    # Contacto
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(200), nullable=True)
    neighborhood = Column(String(100), nullable=True)  # Barrio / Vereda
    city = Column(String(100), nullable=True)

    # Estado de salud - Condiciones generales
    is_pregnant = Column(Boolean, default=False)

    # Condiciones crónicas - Grupo B
    is_hypertensive = Column(Boolean, default=False)
    is_diabetic = Column(Boolean, default=False)
    has_hypothyroidism = Column(Boolean, default=False)  # Hipotiroidismo
    has_copd = Column(Boolean, default=False)  # EPOC
    has_asthma = Column(Boolean, default=False)  # Asma
    has_ckd = Column(Boolean, default=False)  # IRC - Insuficiencia Renal Crónica
    has_cardiovascular_disease = Column(Boolean, default=False)  # Enfermedad cardiovascular establecida

    # Riesgo cardiovascular
    has_cardiovascular_risk = Column(Boolean, default=False)
    cardiovascular_risk_level = Column(Enum(RiskLevelEnum), nullable=True)

    # Estratificación de condiciones crónicas
    hypertension_stage = Column(String(20), nullable=True)  # I, II, III
    diabetes_complications = Column(Boolean, default=False)  # DM con/sin complicaciones
    metabolic_control = Column(String(20), nullable=True)  # controlado, no_controlado

    # Indicadores clínicos (últimos valores registrados)
    last_systolic_bp = Column(Integer, nullable=True)  # Última PAS
    last_diastolic_bp = Column(Integer, nullable=True)  # Última PAD
    last_bp_date = Column(Date, nullable=True)  # Fecha de última presión
    last_glucose = Column(Float, nullable=True)  # Última glicemia en mg/dL
    last_glucose_date = Column(Date, nullable=True)
    last_hba1c = Column(Float, nullable=True)  # Última HbA1c en %
    last_hba1c_date = Column(Date, nullable=True)
    last_cholesterol = Column(Float, nullable=True)  # Último colesterol total
    last_hdl = Column(Float, nullable=True)  # Último HDL
    last_ldl = Column(Float, nullable=True)  # Último LDL
    last_lipid_profile_date = Column(Date, nullable=True)
    last_creatinine = Column(Float, nullable=True)  # Última creatinina
    last_creatinine_date = Column(Date, nullable=True)
    is_smoker = Column(Boolean, default=False)  # Tabaquismo

    # Diagnósticos (JSON o texto)
    diagnoses = Column(Text, nullable=True)  # Pueden ser múltiples diagnósticos separados por coma

    # Controles
    last_control_date = Column(Date, nullable=True)  # Mantener por compatibilidad
    last_general_control_date = Column(Date, nullable=True)  # Fecha ultimo control general
    last_3280_control_date = Column(Date, nullable=True)  # Fecha ultimo control 3280
    last_hta_control_date = Column(Date, nullable=True)  # Fecha ultimo control HTA
    last_dm_control_date = Column(Date, nullable=True)  # Fecha ultimo control DM
    next_control_date = Column(Date, nullable=True)
    control_frequency_days = Column(Integer, nullable=True)  # Cada cuántos días debe tener control

    # Aseguramiento
    eps = Column(String(100), nullable=True)
    tipo_convenio = Column(String(100), nullable=True)  # Tipo de convenio
    regimen = Column(String(50), nullable=True)  # Mantener por compatibilidad - Contributivo, Subsidiado, etc.

    # Estado de contacto
    is_contacted = Column(Boolean, default=False)
    contact_attempts = Column(Integer, default=0)
    last_contact_date = Column(DateTime, nullable=True)
    contact_status = Column(String(50), nullable=True)  # contactado, no_contesta, rechaza, etc.

    # Metadatos
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    upload = relationship("Upload", back_populates="patients")
    controls = relationship("Control", back_populates="patient", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="patient", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.document_number} - {self.full_name}>"
