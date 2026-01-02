"""
Endpoints para consultar catálogos oficiales (EPS, CIE-10, CUPS)
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List
from app.database import get_db
from app.models.eps import Eps
from app.schemas.catalogs import (
    EpsResponse,
    EpsListResponse,
    EpsSearchResponse,
    EpsSearchMatch,
    Cie10Response,
    Cie10ListResponse,
    Cie10SearchResponse,
    Cie10SearchMatch,
    CupsResponse,
    CupsListResponse,
    CupsSearchResponse,
    CupsSearchMatch
)

router = APIRouter(prefix="/catalogs", tags=["Catálogos"])


# ============================================================================
# ENDPOINTS DE EPS
# ============================================================================

@router.get(
    "/eps",
    response_model=EpsListResponse,
    summary="Listar EPS",
    description="""
    Obtiene el listado de EPS (Entidades Promotoras de Salud) con filtros opcionales.

    **Filtros disponibles:**
    - `regime_type`: Filtrar por tipo de régimen (contributivo, subsidiado, especial)
    - `is_active`: Filtrar por estado (true = activas, false = liquidadas/inactivas)
    - `coverage_nationwide`: Solo EPS con cobertura nacional
    - `limit` y `offset`: Para paginación

    **Ejemplos:**
    - `/api/catalogs/eps` - Todas las EPS
    - `/api/catalogs/eps?regime_type=contributivo` - Solo contributivas
    - `/api/catalogs/eps?is_active=true` - Solo activas
    - `/api/catalogs/eps?coverage_nationwide=true` - Solo nacionales
    """
)
def list_eps(
    regime_type: Optional[str] = Query(
        None,
        description="Filtrar por tipo de régimen",
        enum=["contributivo", "subsidiado", "especial"]
    ),
    is_active: Optional[bool] = Query(
        None,
        description="Filtrar por estado (true = activas, false = inactivas)"
    ),
    coverage_nationwide: Optional[bool] = Query(
        None,
        description="Solo EPS con cobertura nacional"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Cantidad de registros a retornar"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Número de registros a saltar (paginación)"
    ),
    db: Session = Depends(get_db)
):
    """
    Lista todas las EPS del catálogo con filtros opcionales
    """
    # Construir query base
    query = db.query(Eps)

    # Aplicar filtros
    if regime_type is not None:
        query = query.filter(Eps.regime_type == regime_type)

    if is_active is not None:
        query = query.filter(Eps.is_active == is_active)

    if coverage_nationwide is not None:
        query = query.filter(Eps.coverage_nationwide == coverage_nationwide)

    # Contar total
    total = query.count()

    # Aplicar paginación y ordenar
    items = query.order_by(Eps.regime_type, Eps.code).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


@router.get(
    "/eps/search",
    response_model=EpsSearchResponse,
    summary="Buscar EPS (búsqueda fuzzy)",
    description="""
    Búsqueda inteligente de EPS por cualquier campo.

    **La búsqueda es flexible y encuentra coincidencias en:**
    - Código (exacto o parcial)
    - Nombre oficial (parcial, case-insensitive)
    - Nombre corto (parcial, case-insensitive)
    - NIT (exacto o parcial)

    **Scoring de resultados:**
    - 100 puntos: Coincidencia exacta en código
    - 90 puntos: Coincidencia exacta en NIT
    - 80 puntos: Coincidencia en nombre corto (case-insensitive)
    - 70 puntos: Coincidencia en código parcial
    - 60 puntos: Coincidencia en nombre oficial
    - 50 puntos: Coincidencia en NIT parcial

    **Ejemplos:**
    - `/api/catalogs/eps/search?q=sura` → Encuentra "EPS SURA"
    - `/api/catalogs/eps/search?q=800088702` → Encuentra por NIT de SURA
    - `/api/catalogs/eps/search?q=EPS010` → Encuentra por código exacto
    - `/api/catalogs/eps/search?q=salud` → Encuentra "Salud Total", "Salud Mía", etc.
    """
)
def search_eps(
    q: str = Query(
        ...,
        min_length=2,
        description="Término de búsqueda (mínimo 2 caracteres)"
    ),
    only_active: bool = Query(
        True,
        description="Solo buscar en EPS activas"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=50,
        description="Máximo de resultados a retornar"
    ),
    db: Session = Depends(get_db)
):
    """
    Búsqueda fuzzy de EPS por múltiples campos
    """
    search_term = q.strip()
    search_term_lower = search_term.lower()

    # Query base
    query = db.query(Eps)

    if only_active:
        query = query.filter(Eps.is_active == True)

    # Lista para almacenar resultados con score
    results = []

    # 1. Búsqueda por código EXACTO (100 puntos)
    exact_code = query.filter(func.lower(Eps.code) == search_term_lower).all()
    for eps in exact_code:
        results.append({
            "eps": eps,
            "score": 100,
            "match_field": "code_exact"
        })

    # 2. Búsqueda por NIT EXACTO (90 puntos)
    exact_nit = query.filter(Eps.nit == search_term).all()
    for eps in exact_nit:
        if not any(r["eps"].id == eps.id for r in results):
            results.append({
                "eps": eps,
                "score": 90,
                "match_field": "nit_exact"
            })

    # 3. Búsqueda por short_name (case-insensitive) (80 puntos)
    short_name_match = query.filter(
        func.lower(Eps.short_name).like(f"%{search_term_lower}%")
    ).all()
    for eps in short_name_match:
        if not any(r["eps"].id == eps.id for r in results):
            results.append({
                "eps": eps,
                "score": 80,
                "match_field": "short_name"
            })

    # 4. Búsqueda por código PARCIAL (70 puntos)
    partial_code = query.filter(
        func.lower(Eps.code).like(f"%{search_term_lower}%")
    ).all()
    for eps in partial_code:
        if not any(r["eps"].id == eps.id for r in results):
            results.append({
                "eps": eps,
                "score": 70,
                "match_field": "code_partial"
            })

    # 5. Búsqueda por nombre oficial (60 puntos)
    name_match = query.filter(
        func.lower(Eps.name).like(f"%{search_term_lower}%")
    ).all()
    for eps in name_match:
        if not any(r["eps"].id == eps.id for r in results):
            results.append({
                "eps": eps,
                "score": 60,
                "match_field": "name"
            })

    # 6. Búsqueda por NIT PARCIAL (50 puntos)
    partial_nit = query.filter(
        Eps.nit.like(f"%{search_term}%")
    ).all()
    for eps in partial_nit:
        if not any(r["eps"].id == eps.id for r in results):
            results.append({
                "eps": eps,
                "score": 50,
                "match_field": "nit_partial"
            })

    # Ordenar por score (descendente)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Limitar resultados
    results = results[:limit]

    # Formatear respuesta
    matches = []
    for result in results:
        eps = result["eps"]
        matches.append(EpsSearchMatch(
            id=eps.id,
            code=eps.code,
            name=eps.name,
            short_name=eps.short_name,
            regime_type=eps.regime_type,
            is_active=eps.is_active,
            score=result["score"],
            match_field=result["match_field"]
        ))

    return {
        "query": search_term,
        "total_matches": len(matches),
        "matches": matches
    }


@router.get(
    "/eps/code/{code}",
    response_model=EpsResponse,
    summary="Obtener EPS por código",
    description="""
    Obtiene una EPS específica por su código oficial.

    **Ejemplos:**
    - `/api/catalogs/eps/code/EPS010` - SURA
    - `/api/catalogs/eps/code/ESS024` - Coosalud
    """
)
def get_eps_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene una EPS específica por su código oficial
    """
    eps = db.query(Eps).filter(Eps.code == code).first()

    if not eps:
        raise HTTPException(
            status_code=404,
            detail=f"EPS con código '{code}' no encontrada"
        )

    return eps


@router.get(
    "/eps/{eps_id}",
    response_model=EpsResponse,
    summary="Obtener EPS por ID",
    description="Obtiene el detalle completo de una EPS específica por su ID"
)
def get_eps_by_id(
    eps_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una EPS específica por ID
    """
    eps = db.query(Eps).filter(Eps.id == eps_id).first()

    if not eps:
        raise HTTPException(
            status_code=404,
            detail=f"EPS con ID {eps_id} no encontrada"
        )

    return eps


# ============================================================================
# ENDPOINTS PARA ESTADÍSTICAS
# ============================================================================

@router.get(
    "/eps/stats/summary",
    summary="Estadísticas del catálogo de EPS",
    description="Obtiene estadísticas generales del catálogo de EPS"
)
def get_eps_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas del catálogo de EPS
    """
    total = db.query(Eps).count()
    active = db.query(Eps).filter(Eps.is_active == True).count()
    inactive = db.query(Eps).filter(Eps.is_active == False).count()

    # Por régimen
    by_regime = db.query(
        Eps.regime_type,
        func.count(Eps.id).label("count")
    ).group_by(Eps.regime_type).all()

    regime_stats = {regime: count for regime, count in by_regime}

    # Con cobertura nacional
    nationwide = db.query(Eps).filter(
        Eps.coverage_nationwide == True,
        Eps.is_active == True
    ).count()

    return {
        "total_eps": total,
        "active_eps": active,
        "inactive_eps": inactive,
        "by_regime": regime_stats,
        "nationwide_coverage": nationwide
    }


# ============================================================================
# ENDPOINTS DE CIE-10
# ============================================================================

@router.get(
    "/cie10",
    response_model=Cie10ListResponse,
    summary="Listar códigos CIE-10",
    description="""
    Obtiene el listado de códigos CIE-10 (Clasificación Internacional de Enfermedades) con filtros opcionales.

    **Filtros disponibles:**
    - `chapter_code`: Filtrar por código de capítulo (I, IV, IX, X, XIV, XV, XXI)
    - `is_common`: Filtrar por códigos comunes en atención primaria
    - `is_subcategory`: Filtrar por subcategorías (códigos con punto decimal)
    - `limit` y `offset`: Para paginación

    **Ejemplos:**
    - `/api/catalogs/cie10` - Todos los códigos
    - `/api/catalogs/cie10?chapter_code=IX` - Solo capítulo IX (circulatorio)
    - `/api/catalogs/cie10?is_common=true` - Solo códigos comunes
    """
)
def list_cie10(
    chapter_code: Optional[str] = Query(
        None,
        description="Filtrar por código de capítulo (I, IV, IX, etc.)"
    ),
    is_common: Optional[bool] = Query(
        None,
        description="Filtrar por códigos comunes (true = solo comunes)"
    ),
    is_subcategory: Optional[bool] = Query(
        None,
        description="Filtrar por subcategorías (true = solo subcategorías con punto)"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Cantidad de registros a retornar"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Número de registros a saltar (paginación)"
    ),
    db: Session = Depends(get_db)
):
    """
    Lista todos los códigos CIE-10 del catálogo con filtros opcionales
    """
    from app.models.cie10 import Cie10

    # Construir query base
    query = db.query(Cie10)

    # Aplicar filtros
    if chapter_code is not None:
        query = query.filter(Cie10.chapter_code == chapter_code)

    if is_common is not None:
        query = query.filter(Cie10.is_common == is_common)

    if is_subcategory is not None:
        query = query.filter(Cie10.is_subcategory == is_subcategory)

    # Contar total
    total = query.count()

    # Aplicar paginación y ordenar
    items = query.order_by(Cie10.chapter_code, Cie10.code).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


@router.get(
    "/cie10/search",
    response_model=Cie10SearchResponse,
    summary="Buscar códigos CIE-10 (búsqueda fuzzy)",
    description="""
    Búsqueda inteligente de códigos CIE-10 por código o descripción.

    **La búsqueda es flexible y encuentra coincidencias en:**
    - Código (exacto o parcial)
    - Descripción corta (parcial, case-insensitive)
    - Descripción completa (parcial, case-insensitive)

    **Scoring de resultados:**
    - 100 puntos: Coincidencia exacta en código
    - 90 puntos: Código inicia con el término de búsqueda
    - 80 puntos: Palabra exacta en descripción corta
    - 70 puntos: Código contiene el término
    - 60 puntos: Palabra en descripción completa

    **Ejemplos:**
    - `/api/catalogs/cie10/search?q=I10` → Encuentra "I10 - Hipertensión esencial"
    - `/api/catalogs/cie10/search?q=diabetes` → Encuentra todos los códigos de diabetes
    - `/api/catalogs/cie10/search?q=E11` → Encuentra E11 y subcódigos E11.x
    - `/api/catalogs/cie10/search?q=hipertension` → Encuentra códigos de HTA
    """
)
def search_cie10(
    q: str = Query(
        ...,
        min_length=1,
        description="Término de búsqueda (mínimo 1 carácter)"
    ),
    only_common: bool = Query(
        False,
        description="Solo buscar en códigos comunes"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Máximo de resultados a retornar"
    ),
    db: Session = Depends(get_db)
):
    """
    Búsqueda fuzzy de códigos CIE-10 por múltiples campos
    """
    from app.models.cie10 import Cie10

    search_term = q.strip()
    search_term_upper = search_term.upper()
    search_term_lower = search_term.lower()

    # Query base
    query = db.query(Cie10)

    if only_common:
        query = query.filter(Cie10.is_common == True)

    # Lista para almacenar resultados con score
    results = []

    # 1. Búsqueda por código EXACTO (100 puntos)
    exact_code = query.filter(func.upper(Cie10.code) == search_term_upper).all()
    for cie10 in exact_code:
        results.append({
            "cie10": cie10,
            "score": 100,
            "match_field": "code_exact"
        })

    # 2. Código INICIA CON el término (90 puntos)
    starts_with_code = query.filter(
        func.upper(Cie10.code).like(f"{search_term_upper}%")
    ).all()
    for cie10 in starts_with_code:
        if not any(r["cie10"].id == cie10.id for r in results):
            results.append({
                "cie10": cie10,
                "score": 90,
                "match_field": "code_starts"
            })

    # 3. Palabra exacta en short_description (80 puntos)
    short_desc_match = query.filter(
        func.lower(Cie10.short_description).like(f"%{search_term_lower}%")
    ).all()
    for cie10 in short_desc_match:
        if not any(r["cie10"].id == cie10.id for r in results):
            results.append({
                "cie10": cie10,
                "score": 80,
                "match_field": "short_description"
            })

    # 4. Código CONTIENE el término (70 puntos)
    contains_code = query.filter(
        func.upper(Cie10.code).like(f"%{search_term_upper}%")
    ).all()
    for cie10 in contains_code:
        if not any(r["cie10"].id == cie10.id for r in results):
            results.append({
                "cie10": cie10,
                "score": 70,
                "match_field": "code_contains"
            })

    # 5. Búsqueda en full_description (60 puntos)
    full_desc_match = query.filter(
        func.lower(Cie10.full_description).like(f"%{search_term_lower}%")
    ).all()
    for cie10 in full_desc_match:
        if not any(r["cie10"].id == cie10.id for r in results):
            results.append({
                "cie10": cie10,
                "score": 60,
                "match_field": "full_description"
            })

    # Ordenar por score (descendente)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Limitar resultados
    results = results[:limit]

    # Formatear respuesta
    from app.schemas.catalogs import Cie10SearchMatch
    matches = []
    for result in results:
        cie10 = result["cie10"]
        matches.append(Cie10SearchMatch(
            id=cie10.id,
            code=cie10.code,
            short_description=cie10.short_description,
            chapter=cie10.chapter,
            chapter_code=cie10.chapter_code,
            is_common=cie10.is_common,
            score=result["score"],
            match_field=result["match_field"]
        ))

    return {
        "query": search_term,
        "total_matches": len(matches),
        "matches": matches
    }


@router.get(
    "/cie10/code/{code}",
    response_model=Cie10Response,
    summary="Obtener código CIE-10 por código",
    description="""
    Obtiene un código CIE-10 específico por su código oficial.

    **Ejemplos:**
    - `/api/catalogs/cie10/code/I10` - Hipertensión esencial
    - `/api/catalogs/cie10/code/E11.9` - Diabetes tipo 2 sin complicaciones
    - `/api/catalogs/cie10/code/J44` - EPOC
    """
)
def get_cie10_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene un código CIE-10 específico por su código oficial
    """
    from app.models.cie10 import Cie10

    # Normalizar código a mayúsculas
    code_upper = code.upper()

    cie10 = db.query(Cie10).filter(func.upper(Cie10.code) == code_upper).first()

    if not cie10:
        raise HTTPException(
            status_code=404,
            detail=f"Código CIE-10 '{code}' no encontrado"
        )

    return cie10


@router.get(
    "/cie10/chapters",
    summary="Listar capítulos CIE-10",
    description="Obtiene la lista de capítulos CIE-10 con estadísticas"
)
def list_cie10_chapters(db: Session = Depends(get_db)):
    """
    Obtiene lista de capítulos CIE-10 con estadísticas
    """
    from app.models.cie10 import Cie10
    from app.schemas.catalogs import Cie10ChapterSummary

    # Obtener estadísticas por capítulo
    chapters_data = db.query(
        Cie10.chapter_code,
        Cie10.chapter,
        func.count(Cie10.id).label("total"),
        func.count(func.nullif(Cie10.is_common, False)).label("common")
    ).group_by(
        Cie10.chapter_code,
        Cie10.chapter
    ).order_by(Cie10.chapter_code).all()

    chapters = []
    for chapter_code, chapter_name, total, common in chapters_data:
        chapters.append({
            "chapter_code": chapter_code,
            "chapter_name": chapter_name,
            "total_codes": total,
            "common_codes": common
        })

    return {
        "total_chapters": len(chapters),
        "chapters": chapters
    }


@router.get(
    "/cie10/chapter/{chapter_code}",
    response_model=Cie10ListResponse,
    summary="Obtener códigos por capítulo",
    description="""
    Obtiene todos los códigos CIE-10 de un capítulo específico.

    **Capítulos disponibles:**
    - I: Enfermedades infecciosas y parasitarias
    - II: Neoplasias
    - IV: Enfermedades endocrinas, nutricionales y metabólicas
    - IX: Enfermedades del sistema circulatorio
    - X: Enfermedades del sistema respiratorio
    - XIV: Enfermedades del sistema genitourinario
    - XV: Embarazo, parto y puerperio
    - XXI: Factores que influyen en el estado de salud
    """
)
def get_cie10_by_chapter(
    chapter_code: str,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Obtiene códigos CIE-10 de un capítulo específico
    """
    from app.models.cie10 import Cie10

    # Normalizar a mayúsculas
    chapter_code_upper = chapter_code.upper()

    query = db.query(Cie10).filter(Cie10.chapter_code == chapter_code_upper)

    total = query.count()

    if total == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Capítulo '{chapter_code}' no encontrado"
        )

    items = query.order_by(Cie10.code).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


@router.get(
    "/cie10/stats/summary",
    summary="Estadísticas del catálogo CIE-10",
    description="Obtiene estadísticas generales del catálogo CIE-10"
)
def get_cie10_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas del catálogo CIE-10
    """
    from app.models.cie10 import Cie10

    total = db.query(Cie10).count()
    common = db.query(Cie10).filter(Cie10.is_common == True).count()
    subcategories = db.query(Cie10).filter(Cie10.is_subcategory == True).count()

    # Por capítulo
    by_chapter = db.query(
        Cie10.chapter_code,
        func.count(Cie10.id).label("count")
    ).group_by(Cie10.chapter_code).all()

    chapter_stats = {chapter: count for chapter, count in by_chapter}

    return {
        "total_codes": total,
        "common_codes": common,
        "subcategories": subcategories,
        "main_codes": total - subcategories,
        "chapters_count": len(chapter_stats),
        "by_chapter": chapter_stats
    }


@router.get(
    "/cie10/{cie10_id}",
    response_model=Cie10Response,
    summary="Obtener código CIE-10 por ID",
    description="Obtiene el detalle completo de un código CIE-10 específico por su ID"
)
def get_cie10_by_id(
    cie10_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un código CIE-10 específico por ID
    """
    from app.models.cie10 import Cie10

    cie10 = db.query(Cie10).filter(Cie10.id == cie10_id).first()

    if not cie10:
        raise HTTPException(
            status_code=404,
            detail=f"Código CIE-10 con ID {cie10_id} no encontrado"
        )

    return cie10


# ============================================================================
# ENDPOINTS DE CUPS
# ============================================================================

@router.get(
    "/cups",
    response_model=CupsListResponse,
    summary="Listar códigos CUPS",
    description="""
    Obtiene el listado de códigos CUPS (Clasificación Única de Procedimientos en Salud) con filtros opcionales.

    **Filtros disponibles:**
    - `category`: Filtrar por categoría
    - `procedure_type`: Filtrar por tipo de procedimiento (Preventivo, Diagnóstico, Terapéutico)
    - `specialty`: Filtrar por especialidad
    - `ambulatory`: Solo procedimientos ambulatorios
    - `complexity_level`: Filtrar por nivel de complejidad (Baja, Media, Alta)
    - `limit` y `offset`: Para paginación

    **Ejemplos:**
    - `/api/catalogs/cups` - Todos los códigos
    - `/api/catalogs/cups?category=Consultas médicas` - Solo consultas
    - `/api/catalogs/cups?procedure_type=Preventivo` - Solo preventivos
    - `/api/catalogs/cups?specialty=Laboratorio clínico` - Solo laboratorio
    """
)
def list_cups(
    category: Optional[str] = Query(
        None,
        description="Filtrar por categoría"
    ),
    procedure_type: Optional[str] = Query(
        None,
        description="Filtrar por tipo de procedimiento",
        enum=["Preventivo", "Diagnóstico", "Terapéutico"]
    ),
    specialty: Optional[str] = Query(
        None,
        description="Filtrar por especialidad"
    ),
    ambulatory: Optional[bool] = Query(
        None,
        description="Solo procedimientos ambulatorios"
    ),
    complexity_level: Optional[str] = Query(
        None,
        description="Filtrar por nivel de complejidad",
        enum=["Baja", "Media", "Alta"]
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Cantidad de registros a retornar"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Número de registros a saltar (paginación)"
    ),
    db: Session = Depends(get_db)
):
    """
    Lista todos los códigos CUPS del catálogo con filtros opcionales
    """
    from app.models.cups import Cups

    # Construir query base
    query = db.query(Cups)

    # Aplicar filtros
    if category is not None:
        query = query.filter(Cups.category == category)

    if procedure_type is not None:
        query = query.filter(Cups.procedure_type == procedure_type)

    if specialty is not None:
        query = query.filter(Cups.specialty == specialty)

    if ambulatory is not None:
        query = query.filter(Cups.ambulatory == ambulatory)

    if complexity_level is not None:
        query = query.filter(Cups.complexity_level == complexity_level)

    # Contar total
    total = query.count()

    # Aplicar paginación y ordenar
    items = query.order_by(Cups.category, Cups.code).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


@router.get(
    "/cups/search",
    response_model=CupsSearchResponse,
    summary="Buscar códigos CUPS (búsqueda fuzzy)",
    description="""
    Búsqueda inteligente de códigos CUPS por código o descripción.

    **La búsqueda es flexible y encuentra coincidencias en:**
    - Código (exacto o parcial)
    - Descripción (parcial, case-insensitive)
    - Categoría (parcial, case-insensitive)
    - Especialidad (parcial, case-insensitive)

    **Scoring de resultados:**
    - 100 puntos: Coincidencia exacta en código
    - 90 puntos: Código inicia con el término de búsqueda
    - 80 puntos: Palabra exacta en descripción
    - 70 puntos: Código contiene el término
    - 60 puntos: Palabra en categoría
    - 50 puntos: Palabra en especialidad

    **Ejemplos:**
    - `/api/catalogs/cups/search?q=890201` → Encuentra consulta medicina general
    - `/api/catalogs/cups/search?q=glicemia` → Encuentra exámenes de glucosa
    - `/api/catalogs/cups/search?q=902` → Encuentra códigos de laboratorio (90XXXX)
    - `/api/catalogs/cups/search?q=ecografia` → Encuentra todos los tipos de ecografías
    """
)
def search_cups(
    q: str = Query(
        ...,
        min_length=2,
        description="Término de búsqueda (mínimo 2 caracteres)"
    ),
    only_active: bool = Query(
        True,
        description="Solo buscar en códigos activos"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Máximo de resultados a retornar"
    ),
    db: Session = Depends(get_db)
):
    """
    Búsqueda fuzzy de códigos CUPS por múltiples campos
    """
    from app.models.cups import Cups

    search_term = q.strip()
    search_term_lower = search_term.lower()

    # Query base
    query = db.query(Cups)

    if only_active:
        query = query.filter(Cups.is_active == True)

    # Lista para almacenar resultados con score
    results = []

    # 1. Búsqueda por código EXACTO (100 puntos)
    exact_code = query.filter(Cups.code == search_term).all()
    for cups in exact_code:
        results.append({
            "cups": cups,
            "score": 100,
            "match_field": "code_exact"
        })

    # 2. Código INICIA CON el término (90 puntos)
    starts_with_code = query.filter(
        Cups.code.like(f"{search_term}%")
    ).all()
    for cups in starts_with_code:
        if not any(r["cups"].id == cups.id for r in results):
            results.append({
                "cups": cups,
                "score": 90,
                "match_field": "code_starts"
            })

    # 3. Palabra en descripción (80 puntos)
    desc_match = query.filter(
        func.lower(Cups.description).like(f"%{search_term_lower}%")
    ).all()
    for cups in desc_match:
        if not any(r["cups"].id == cups.id for r in results):
            results.append({
                "cups": cups,
                "score": 80,
                "match_field": "description"
            })

    # 4. Código CONTIENE el término (70 puntos)
    contains_code = query.filter(
        Cups.code.like(f"%{search_term}%")
    ).all()
    for cups in contains_code:
        if not any(r["cups"].id == cups.id for r in results):
            results.append({
                "cups": cups,
                "score": 70,
                "match_field": "code_contains"
            })

    # 5. Búsqueda en categoría (60 puntos)
    category_match = query.filter(
        func.lower(Cups.category).like(f"%{search_term_lower}%")
    ).all()
    for cups in category_match:
        if not any(r["cups"].id == cups.id for r in results):
            results.append({
                "cups": cups,
                "score": 60,
                "match_field": "category"
            })

    # 6. Búsqueda en especialidad (50 puntos)
    specialty_match = query.filter(
        func.lower(Cups.specialty).like(f"%{search_term_lower}%")
    ).all()
    for cups in specialty_match:
        if not any(r["cups"].id == cups.id for r in results):
            results.append({
                "cups": cups,
                "score": 50,
                "match_field": "specialty"
            })

    # Ordenar por score (descendente)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Limitar resultados
    results = results[:limit]

    # Formatear respuesta
    from app.schemas.catalogs import CupsSearchMatch
    matches = []
    for result in results:
        cups = result["cups"]
        matches.append(CupsSearchMatch(
            id=cups.id,
            code=cups.code,
            description=cups.description,
            category=cups.category,
            procedure_type=cups.procedure_type,
            specialty=cups.specialty,
            score=result["score"],
            match_field=result["match_field"]
        ))

    return {
        "query": search_term,
        "total_matches": len(matches),
        "matches": matches
    }


@router.get(
    "/cups/code/{code}",
    response_model=CupsResponse,
    summary="Obtener código CUPS por código",
    description="""
    Obtiene un código CUPS específico por su código oficial.

    **Ejemplos:**
    - `/api/catalogs/cups/code/890201` - Consulta medicina general
    - `/api/catalogs/cups/code/902215` - Glicemia en ayunas
    - `/api/catalogs/cups/code/893101` - Electrocardiograma
    """
)
def get_cups_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene un código CUPS específico por su código oficial
    """
    from app.models.cups import Cups

    cups = db.query(Cups).filter(Cups.code == code).first()

    if not cups:
        raise HTTPException(
            status_code=404,
            detail=f"Código CUPS '{code}' no encontrado"
        )

    return cups


@router.get(
    "/cups/categories",
    summary="Listar categorías CUPS",
    description="Obtiene la lista de categorías CUPS con estadísticas"
)
def list_cups_categories(db: Session = Depends(get_db)):
    """
    Obtiene lista de categorías CUPS con estadísticas
    """
    from app.models.cups import Cups

    # Obtener estadísticas por categoría
    categories_data = db.query(
        Cups.category,
        func.count(Cups.id).label("total"),
        func.count(func.nullif(Cups.ambulatory, False)).label("ambulatory"),
        func.count(func.nullif(Cups.requires_hospitalization, False)).label("hospitalization")
    ).group_by(
        Cups.category
    ).order_by(Cups.category).all()

    categories = []
    for category_name, total, ambulatory, hospitalization in categories_data:
        categories.append({
            "category": category_name,
            "total_codes": total,
            "ambulatory": ambulatory,
            "hospitalization_required": hospitalization
        })

    return {
        "total_categories": len(categories),
        "categories": categories
    }


@router.get(
    "/cups/category/{category}",
    response_model=CupsListResponse,
    summary="Obtener códigos por categoría",
    description="""
    Obtiene todos los códigos CUPS de una categoría específica.

    **Categorías disponibles:**
    - Consultas médicas
    - Laboratorio
    - Radiología
    - Ecografía
    - Prevención y tamizaje
    - Vacunación
    - Procedimientos de enfermería
    - etc.
    """
)
def get_cups_by_category(
    category: str,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Obtiene códigos CUPS de una categoría específica
    """
    from app.models.cups import Cups

    query = db.query(Cups).filter(Cups.category == category)

    total = query.count()

    if total == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría '{category}' no encontrada"
        )

    items = query.order_by(Cups.code).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


@router.get(
    "/cups/stats/summary",
    summary="Estadísticas del catálogo CUPS",
    description="Obtiene estadísticas generales del catálogo CUPS"
)
def get_cups_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas del catálogo CUPS
    """
    from app.models.cups import Cups

    total = db.query(Cups).count()
    active = db.query(Cups).filter(Cups.is_active == True).count()
    ambulatory = db.query(Cups).filter(Cups.ambulatory == True).count()
    hospitalization = db.query(Cups).filter(Cups.requires_hospitalization == True).count()

    # Por categoría
    by_category = db.query(
        Cups.category,
        func.count(Cups.id).label("count")
    ).group_by(Cups.category).all()

    category_stats = {category: count for category, count in by_category}

    # Por tipo de procedimiento
    by_type = db.query(
        Cups.procedure_type,
        func.count(Cups.id).label("count")
    ).group_by(Cups.procedure_type).all()

    type_stats = {proc_type: count for proc_type, count in by_type}

    # Por complejidad
    by_complexity = db.query(
        Cups.complexity_level,
        func.count(Cups.id).label("count")
    ).group_by(Cups.complexity_level).all()

    complexity_stats = {level: count for level, count in by_complexity}

    return {
        "total_codes": total,
        "active_codes": active,
        "ambulatory_procedures": ambulatory,
        "hospitalization_required": hospitalization,
        "categories_count": len(category_stats),
        "by_category": category_stats,
        "by_procedure_type": type_stats,
        "by_complexity": complexity_stats
    }


@router.get(
    "/cups/{cups_id}",
    response_model=CupsResponse,
    summary="Obtener código CUPS por ID",
    description="Obtiene el detalle completo de un código CUPS específico por su ID"
)
def get_cups_by_id(
    cups_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un código CUPS específico por ID
    """
    from app.models.cups import Cups

    cups = db.query(Cups).filter(Cups.id == cups_id).first()

    if not cups:
        raise HTTPException(
            status_code=404,
            detail=f"Código CUPS con ID {cups_id} no encontrado"
        )

    return cups
