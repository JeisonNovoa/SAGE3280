from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MedicationStatusEnum(str, enum.Enum):
    ACTIVO = "activo"
    SUSPENDIDO = "suspendido"
    COMPLETADO = "completado"


class AdherenceEnum(str, enum.Enum):
    BUENA = "buena"  # >80% cumplimiento
    REGULAR = "regular"  # 50-80% cumplimiento
    MALA = "mala"  # <50% cumplimiento
    NO_EVALUADO = "no_evaluado"


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)

    # Patient reference
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Medication info
    medication_name = Column(String(200), nullable=False)
    generic_name = Column(String(200), nullable=True)
    presentation = Column(String(100), nullable=True)  # Tableta, jarabe, inyección, etc.
    concentration = Column(String(50), nullable=True)  # 500mg, 10mg/ml, etc.

    # Dosage
    dose = Column(String(100), nullable=False)  # 1 tableta, 5ml, etc.
    frequency = Column(String(100), nullable=False)  # Cada 8 horas, 2 veces al día, etc.
    route = Column(String(50), nullable=True)  # Oral, IV, IM, etc.

    # Indication
    indication = Column(String(200), nullable=True)  # Para qué se prescribió
    prescriber = Column(String(200), nullable=True)  # Médico que prescribió

    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Null si es tratamiento indefinido
    last_refill_date = Column(Date, nullable=True)  # Última vez que renovó
    next_refill_date = Column(Date, nullable=True)  # Próxima renovación programada

    # Status
    status = Column(Enum(MedicationStatusEnum), default=MedicationStatusEnum.ACTIVO, index=True)
    adherence = Column(Enum(AdherenceEnum), default=AdherenceEnum.NO_EVALUADO)

    # Refill info
    refill_frequency_days = Column(Integer, nullable=True)  # Cada cuántos días debe renovar
    requires_refill_alert = Column(Boolean, default=True)  # Si se debe alertar cuando necesite renovar

    # Notes
    notes = Column(Text, nullable=True)
    side_effects = Column(Text, nullable=True)  # Efectos secundarios reportados

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String(200), nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="medications")

    def __repr__(self):
        return f"<Medication {self.medication_name} for Patient {self.patient_id} - {self.status}>"

    def is_active(self) -> bool:
        """Check if medication is currently active"""
        return self.status == MedicationStatusEnum.ACTIVO

    def needs_refill(self, days_ahead: int = 7) -> bool:
        """
        Check if medication needs refill within specified days
        Args:
            days_ahead: Number of days to check ahead (default 7)
        Returns:
            True if refill is needed within days_ahead
        """
        if not self.next_refill_date or not self.is_active():
            return False

        from datetime import datetime, timedelta
        alert_date = datetime.now().date() + timedelta(days=days_ahead)
        return self.next_refill_date <= alert_date
