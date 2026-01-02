"""
Schemas Pydantic para catálogos (EPS, CIE-10, CUPS)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# SCHEMAS PARA EPS
# ============================================================================

class EpsBase(BaseModel):
    """Schema base para EPS"""
    code: str = Field(..., description="Código oficial de la EPS")
    name: str = Field(..., description="Nombre oficial completo")
    short_name: Optional[str] = Field(None, description="Nombre corto o comercial")
    nit: Optional[str] = Field(None, description="NIT con dígito de verificación")
    regime_type: str = Field(..., description="Tipo de régimen: contributivo, subsidiado, especial")
    is_active: bool = Field(True, description="Si la EPS está activa o liquidada")
    phone: Optional[str] = Field(None, description="Teléfono de contacto")
    email: Optional[str] = Field(None, description="Email de contacto")
    website: Optional[str] = Field(None, description="Sitio web")
    coverage_nationwide: bool = Field(False, description="Si tiene cobertura nacional")
    departments: Optional[str] = Field(None, description="Departamentos donde opera")
    notes: Optional[str] = Field(None, description="Notas adicionales")


class EpsResponse(EpsBase):
    """Schema de respuesta para EPS (incluye id y timestamps)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EpsListResponse(BaseModel):
    """Schema de respuesta para lista paginada de EPS"""
    total: int = Field(..., description="Total de registros que coinciden con los filtros")
    limit: int = Field(..., description="Cantidad de registros por página")
    offset: int = Field(..., description="Desplazamiento para paginación")
    items: List[EpsResponse] = Field(..., description="Lista de EPS")


class EpsSearchMatch(BaseModel):
    """Schema para resultado de búsqueda de EPS"""
    id: int
    code: str
    name: str
    short_name: Optional[str]
    regime_type: str
    is_active: bool
    score: int = Field(..., description="Puntuación de similitud (0-100)")
    match_field: str = Field(..., description="Campo donde se encontró la coincidencia")

    class Config:
        from_attributes = True


class EpsSearchResponse(BaseModel):
    """Schema de respuesta para búsqueda de EPS"""
    query: str = Field(..., description="Término de búsqueda original")
    total_matches: int = Field(..., description="Total de coincidencias encontradas")
    matches: List[EpsSearchMatch] = Field(..., description="Lista de coincidencias ordenadas por relevancia")


# ============================================================================
# SCHEMAS PARA CIE-10
# ============================================================================

class Cie10Base(BaseModel):
    """Schema base para CIE-10"""
    code: str = Field(..., description="Código CIE-10 (ej: I10, E11.9)")
    short_description: str = Field(..., description="Descripción corta para visualización")
    full_description: Optional[str] = Field(None, description="Descripción completa y detallada")
    chapter: str = Field(..., description="Capítulo CIE-10 completo")
    chapter_code: str = Field(..., description="Código del capítulo (I, IV, IX, etc.)")
    category: Optional[str] = Field(None, description="Categoría dentro del capítulo")
    is_subcategory: bool = Field(False, description="Si es subcódigo con punto decimal")
    parent_code: Optional[str] = Field(None, description="Código padre si es subcategoría")
    is_common: bool = Field(False, description="Si es código frecuente en atención primaria")
    notes: Optional[str] = Field(None, description="Notas clínicas o consideraciones")


class Cie10Response(Cie10Base):
    """Schema de respuesta para CIE-10 (incluye id y timestamps)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Cie10ListResponse(BaseModel):
    """Schema de respuesta para lista paginada de CIE-10"""
    total: int = Field(..., description="Total de códigos que coinciden con los filtros")
    limit: int = Field(..., description="Cantidad de registros por página")
    offset: int = Field(..., description="Desplazamiento para paginación")
    items: List[Cie10Response] = Field(..., description="Lista de códigos CIE-10")


class Cie10SearchMatch(BaseModel):
    """Schema para resultado de búsqueda de CIE-10"""
    id: int
    code: str
    short_description: str
    chapter: str
    chapter_code: str
    is_common: bool
    score: int = Field(..., description="Puntuación de similitud (0-100)")
    match_field: str = Field(..., description="Campo donde se encontró la coincidencia")

    class Config:
        from_attributes = True


class Cie10SearchResponse(BaseModel):
    """Schema de respuesta para búsqueda de CIE-10"""
    query: str = Field(..., description="Término de búsqueda original")
    total_matches: int = Field(..., description="Total de coincidencias encontradas")
    matches: List[Cie10SearchMatch] = Field(..., description="Lista de coincidencias ordenadas por relevancia")


class Cie10ChapterSummary(BaseModel):
    """Schema para resumen de capítulo CIE-10"""
    chapter_code: str = Field(..., description="Código del capítulo")
    chapter_name: str = Field(..., description="Nombre del capítulo")
    total_codes: int = Field(..., description="Total de códigos en el capítulo")
    common_codes: int = Field(..., description="Códigos comunes en el capítulo")


# ============================================================================
# SCHEMAS PARA CUPS
# ============================================================================

class CupsBase(BaseModel):
    """Schema base para CUPS"""
    code: str = Field(..., description="Código CUPS (ej: 890201, 902215)")
    description: str = Field(..., description="Descripción del procedimiento")
    chapter: Optional[str] = Field(None, description="Capítulo/Sección CUPS")
    category: Optional[str] = Field(None, description="Categoría del procedimiento")
    subcategory: Optional[str] = Field(None, description="Subcategoría")
    procedure_type: Optional[str] = Field(None, description="Tipo: Preventivo, Diagnóstico, Terapéutico")
    complexity_level: Optional[str] = Field(None, description="Nivel de complejidad: Baja, Media, Alta")
    ambulatory: bool = Field(True, description="Si se puede realizar ambulatoriamente")
    requires_hospitalization: bool = Field(False, description="Si requiere hospitalización")
    specialty: Optional[str] = Field(None, description="Especialidad que realiza el procedimiento")
    estimated_duration_minutes: Optional[int] = Field(None, description="Duración estimada en minutos")
    is_active: bool = Field(True, description="Si el procedimiento está vigente")
    notes: Optional[str] = Field(None, description="Notas técnicas")


class CupsResponse(CupsBase):
    """Schema de respuesta para CUPS (incluye id y timestamps)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CupsListResponse(BaseModel):
    """Schema de respuesta para lista paginada de CUPS"""
    total: int = Field(..., description="Total de códigos que coinciden con los filtros")
    limit: int = Field(..., description="Cantidad de registros por página")
    offset: int = Field(..., description="Desplazamiento para paginación")
    items: List[CupsResponse] = Field(..., description="Lista de códigos CUPS")


class CupsSearchMatch(BaseModel):
    """Schema para resultado de búsqueda de CUPS"""
    id: int
    code: str
    description: str
    category: Optional[str]
    procedure_type: Optional[str]
    specialty: Optional[str]
    score: int = Field(..., description="Puntuación de similitud (0-100)")
    match_field: str = Field(..., description="Campo donde se encontró la coincidencia")

    class Config:
        from_attributes = True


class CupsSearchResponse(BaseModel):
    """Schema de respuesta para búsqueda de CUPS"""
    query: str = Field(..., description="Término de búsqueda original")
    total_matches: int = Field(..., description="Total de coincidencias encontradas")
    matches: List[CupsSearchMatch] = Field(..., description="Lista de coincidencias ordenadas por relevancia")


class CupsCategorySummary(BaseModel):
    """Schema para resumen de categoría CUPS"""
    category: str = Field(..., description="Nombre de la categoría")
    total_codes: int = Field(..., description="Total de códigos en la categoría")
    ambulatory: int = Field(..., description="Códigos ambulatorios")
    hospitalization_required: int = Field(..., description="Códigos que requieren hospitalización")
