"""
CIE-10 (Clasificación Internacional de Enfermedades, 10ª Revisión) Model

Official diagnosis codes catalog for Colombian health system.
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Cie10(Base):
    """
    CIE-10 Catalog Model

    Stores the International Classification of Diseases (ICD-10) codes
    used for standardizing diagnosis coding in the Colombian health system.

    Examples:
        - I10: Hipertensión esencial (primaria)
        - E11.9: Diabetes mellitus tipo 2 sin complicaciones
        - J44: Enfermedad pulmonar obstructiva crónica (EPOC)
    """
    __tablename__ = 'cie10_catalog'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # CIE-10 Code (unique identifier)
    code = Column(String(10), unique=True, nullable=False, index=True)
    # Examples: "I10", "E11", "E11.9", "J44.0"

    # Descriptions
    short_description = Column(String(200), nullable=False, index=True)
    # Short, concise description for display

    full_description = Column(Text, nullable=True)
    # Complete, detailed description

    # Hierarchical Organization
    chapter = Column(String(100), nullable=False, index=True)
    # Example: "IX - Enfermedades del sistema circulatorio"

    chapter_code = Column(String(10), nullable=False, index=True)
    # Example: "IX", "IV", "X"

    category = Column(String(150), nullable=True)
    # Sub-category within chapter
    # Example: "Enfermedades hipertensivas", "Diabetes mellitus"

    # Hierarchy
    is_subcategory = Column(Boolean, default=False, index=True)
    # True if code has decimal (e.g., E11.9 is subcategory of E11)

    parent_code = Column(String(10), nullable=True, index=True)
    # Reference to parent code if is_subcategory=True
    # Example: For E11.9, parent_code="E11"

    # Classification Flags
    is_common = Column(Boolean, default=False, index=True)
    # True if frequently used in primary care
    # Helps prioritize search results

    # Additional Info
    notes = Column(Text, nullable=True)
    # Clinical notes, special considerations, relationships

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Cie10(code='{self.code}', description='{self.short_description}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'code': self.code,
            'short_description': self.short_description,
            'full_description': self.full_description,
            'chapter': self.chapter,
            'chapter_code': self.chapter_code,
            'category': self.category,
            'is_subcategory': self.is_subcategory,
            'parent_code': self.parent_code,
            'is_common': self.is_common,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
