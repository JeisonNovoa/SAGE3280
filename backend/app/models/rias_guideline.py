from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Boolean
from app.database import Base


class RiasGuideline(Base):
    """
    Guías oficiales RIAS (Rutas Integrales de Atención en Salud).

    Almacena las descripciones oficiales y parámetros de cada etapa del
    curso de vida según Resolución 3280 de 2018.
    """
    __tablename__ = "rias_guidelines"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Identificación
    guideline_code = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "RIAS_PRIMERA_INFANCIA"
    guideline_name = Column(String(200), nullable=False)  # e.g., "RIAS Primera Infancia (0-5 años)"

    # Etapa del curso de vida
    life_stage = Column(String(50), nullable=False, index=True)  # AgeGroupEnum value

    # Descripción oficial
    official_description = Column(Text, nullable=False)  # Descripción completa según normativa
    objectives = Column(Text, nullable=True)  # Objetivos de la atención en esta etapa

    # Parámetros de edad
    age_min = Column(Integer, nullable=True)  # Edad mínima en años
    age_max = Column(Integer, nullable=True)  # Edad máxima en años

    # Controles y actividades recomendadas (JSON estructurado)
    recommended_controls = Column(JSON, nullable=True)
    # Ejemplo:
    # {
    #     "controls": [
    #         {
    #             "name": "Control de crecimiento y desarrollo",
    #             "frequency": "Mensual < 1 año, trimestral 1-2 años, semestral 2-5 años",
    #             "includes": ["Peso", "Talla", "Perímetro cefálico", "Desarrollo psicomotor"]
    #         },
    #         {
    #             "name": "Vacunación",
    #             "frequency": "Según esquema PAI",
    #             "includes": ["BCG", "Hepatitis B", "Pentavalente", "Triple viral", "etc."]
    #         }
    #     ]
    # }

    # Tamizajes y exámenes específicos
    screening_activities = Column(JSON, nullable=True)
    # Ejemplo:
    # {
    #     "screening": [
    #         {"name": "Tamizaje visual", "age": "4 años"},
    #         {"name": "Tamizaje auditivo", "age": "4 años"}
    #     ]
    # }

    # Referencias normativas
    normative_reference = Column(String(300), nullable=False)  # e.g., "Resolución 3280 de 2018, Artículo X"
    additional_references = Column(Text, nullable=True)  # Otras normas o guías aplicables

    # Observaciones y notas clínicas
    clinical_notes = Column(Text, nullable=True)  # Notas importantes para profesionales de salud
    special_considerations = Column(Text, nullable=True)  # Consideraciones especiales (embarazo, discapacidad, etc.)

    # Estado
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")  # Control de versiones de la guía

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(200), nullable=True)
    updated_by = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<RiasGuideline {self.guideline_code} - {self.guideline_name}>"
