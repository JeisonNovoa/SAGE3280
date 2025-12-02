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

    # Contacto
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)

    # Estado de salud
    is_pregnant = Column(Boolean, default=False)
    is_hypertensive = Column(Boolean, default=False)
    is_diabetic = Column(Boolean, default=False)
    has_cardiovascular_risk = Column(Boolean, default=False)
    cardiovascular_risk_level = Column(Enum(RiskLevelEnum), nullable=True)

    # Diagnósticos (JSON o texto)
    diagnoses = Column(Text, nullable=True)  # Pueden ser múltiples diagnósticos separados por coma

    # Controles
    last_control_date = Column(Date, nullable=True)
    next_control_date = Column(Date, nullable=True)
    control_frequency_days = Column(Integer, nullable=True)  # Cada cuántos días debe tener control

    # Aseguramiento
    eps = Column(String(100), nullable=True)
    regimen = Column(String(50), nullable=True)  # Contributivo, Subsidiado, etc.

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

    def __repr__(self):
        return f"<Patient {self.document_number} - {self.full_name}>"
