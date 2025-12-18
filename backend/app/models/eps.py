from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum


class EpsTypeEnum(str, enum.Enum):
    """Tipo de régimen de la EPS"""
    CONTRIBUTIVO = "contributivo"
    SUBSIDIADO = "subsidiado"
    ESPECIAL = "especial"  # Fuerzas militares, Ecopetrol, etc.


class Eps(Base):
    """
    Catálogo de Entidades Promotoras de Salud (EPS) activas en Colombia.

    Fuente oficial: Superintendencia Nacional de Salud
    https://www.supersalud.gov.co/
    """
    __tablename__ = "eps_catalog"

    id = Column(Integer, primary_key=True, index=True)

    # Identificación
    code = Column(String(20), nullable=False, unique=True, index=True)  # Código oficial
    name = Column(String(200), nullable=False, index=True)  # Nombre oficial
    short_name = Column(String(100), nullable=True)  # Nombre corto/comercial
    nit = Column(String(20), nullable=True)  # NIT de la EPS

    # Tipo y estado
    regime_type = Column(String(20), nullable=False, default="contributivo")
    is_active = Column(Boolean, default=True, index=True)  # Si está activa o liquidada

    # Contacto
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    address = Column(String(300), nullable=True)

    # Cobertura geográfica
    coverage_nationwide = Column(Boolean, default=False)  # Cobertura nacional
    departments = Column(String(500), nullable=True)  # Departamentos donde opera (comma-separated)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(String(500), nullable=True)  # Notas administrativas

    def __repr__(self):
        return f"<Eps {self.code} - {self.name}>"
