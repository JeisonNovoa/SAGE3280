from sqlalchemy import Column, Integer, String, Text, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class Cups(Base):
    """
    Catálogo de códigos CUPS (Clasificación Única de Procedimientos en Salud).

    Sistema oficial de Colombia para procedimientos, intervenciones y servicios de salud.
    Resolución 8430 de 2020 - Ministerio de Salud.
    """
    __tablename__ = "cups_catalog"

    id = Column(Integer, primary_key=True, index=True)

    # Código CUPS
    code = Column(String(20), nullable=False, unique=True, index=True)  # e.g., "890201", "890301"

    # Descripción
    description = Column(Text, nullable=False)  # Descripción oficial del procedimiento

    # Clasificación
    chapter = Column(String(200), nullable=True)  # Capítulo/Sección
    category = Column(String(200), nullable=True)  # Categoría del procedimiento
    subcategory = Column(String(200), nullable=True)  # Subcategoría

    # Tipo de procedimiento
    procedure_type = Column(String(100), nullable=True)  # "Diagnóstico", "Terapéutico", "Preventivo", etc.

    # Nivel de complejidad
    complexity_level = Column(String(20), nullable=True)  # "Baja", "Media", "Alta"

    # Lugar de realización
    ambulatory = Column(Boolean, default=True)  # Se puede realizar ambulatoriamente
    requires_hospitalization = Column(Boolean, default=False)  # Requiere hospitalización

    # Especialidad
    specialty = Column(String(200), nullable=True)  # Especialidad que realiza el procedimiento

    # Tiempo estimado
    estimated_duration_minutes = Column(Integer, nullable=True)  # Duración estimada en minutos

    # Costo referencial (opcional)
    reference_cost = Column(Float, nullable=True)  # Costo de referencia

    # Estado
    is_active = Column(Boolean, default=True, index=True)  # Procedimiento vigente

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True)  # Notas técnicas
    contraindications = Column(Text, nullable=True)  # Contraindicaciones

    def __repr__(self):
        return f"<CUPS {self.code} - {self.description[:50]}>"
