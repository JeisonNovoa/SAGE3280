from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class Cie10(Base):
    """
    Catálogo de códigos CIE-10 (Clasificación Internacional de Enfermedades).

    Versión 10, OMS. Permite diagnósticos estructurados en lugar de texto libre.
    """
    __tablename__ = "cie10_catalog"

    id = Column(Integer, primary_key=True, index=True)

    # Código CIE-10
    code = Column(String(10), nullable=False, unique=True, index=True)  # e.g., "I10", "E11.9"

    # Descripción
    description = Column(Text, nullable=False)  # Descripción oficial en español
    description_en = Column(Text, nullable=True)  # Descripción en inglés

    # Categorización
    chapter = Column(String(200), nullable=True)  # Capítulo del CIE-10
    chapter_code = Column(String(10), nullable=True)  # Código del capítulo (e.g., "I", "E")
    category = Column(String(200), nullable=True)  # Categoría específica

    # Sexo aplicable
    sex_specific = Column(String(1), nullable=True)  # 'M', 'F', null=ambos

    # Tipo de diagnóstico
    is_chronic = Column(Boolean, default=False)  # Es enfermedad crónica
    is_infectious = Column(Boolean, default=False)  # Es enfermedad infecciosa

    # Estado
    is_active = Column(Boolean, default=True)  # Código activo en CIE-10

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True)  # Notas clínicas adicionales

    def __repr__(self):
        return f"<CIE10 {self.code} - {self.description[:50]}>"
