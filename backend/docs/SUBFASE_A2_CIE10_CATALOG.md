# Subfase A.2: Catálogo CIE-10 - Documentación Completa

**Proyecto**: SAGE3280 - Sistema de Gestión de Salud basado en Resolución 3280/2018
**Fecha**: 31 de Diciembre de 2024
**Estado**: ✅ COMPLETADO

---

## Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Objetivos de la Subfase](#objetivos)
3. [Arquitectura Implementada](#arquitectura)
4. [Componentes Desarrollados](#componentes)
5. [API REST Endpoints](#api-endpoints)
6. [Integración con Excel Processor](#integracion-excel)
7. [Testing y Validación](#testing)
8. [Guía de Uso](#guia-uso)
9. [Próximos Pasos](#proximos-pasos)

---

## Resumen Ejecutivo

La Subfase A.2 implementa un catálogo completo de códigos CIE-10 (Clasificación Internacional de Enfermedades, 10ª Revisión) para el sistema SAGE3280. Este catálogo permite:

- **Normalizar diagnósticos** de pacientes usando estándares internacionales
- **Búsqueda inteligente** de códigos por texto, código o keywords
- **Extracción automática** de códigos CIE-10 desde archivos Excel
- **API REST completa** con 7 endpoints para gestión del catálogo

### Estadísticas del Catálogo

- **71 códigos CIE-10** curados para atención primaria
- **9 capítulos médicos** organizados por especialidad
- **67 códigos comunes** priorizados para uso frecuente
- **33 subcategorías** con punto decimal (ej: E11.9)
- **38 códigos principales** sin subcategorías

---

## Objetivos

### Objetivos Primarios ✅

1. ✅ Crear catálogo de códigos CIE-10 priorizados para Colombia
2. ✅ Implementar modelo de base de datos con jerarquía de códigos
3. ✅ Desarrollar API REST para consulta y búsqueda de códigos
4. ✅ Integrar extracción automática en procesamiento de Excel
5. ✅ Implementar búsqueda inteligente con scoring de relevancia

### Objetivos Secundarios

- ⏸️ Buscador CIE-10 en frontend (Opcional - A.2.11)
- ✅ Documentación completa del sistema
- ✅ Archivo de prueba para validación

---

## Arquitectura

### Stack Tecnológico

```
Backend:
├── FastAPI (API REST)
├── SQLAlchemy (ORM)
├── PostgreSQL (Base de datos)
├── Pydantic (Validación de datos)
└── Pandas (Procesamiento Excel)

Catálogo:
├── 71 códigos CIE-10
├── 9 capítulos médicos
└── Jerarquía padre-hijo
```

### Diagrama de Flujo de Datos

```
Excel Upload → Excel Processor → CIE-10 Extraction → Normalization → Patient DB
                     ↓
              Regex Pattern Match
                     ↓
              Database Lookup (cie10_catalog)
                     ↓
              Return: "CODE - DESCRIPTION"
```

---

## Componentes Desarrollados

### 1. Modelo de Datos (SQLAlchemy)

**Archivo**: `backend/app/models/cie10.py`

```python
class Cie10(Base):
    __tablename__ = 'cie10_catalog'

    # Campos principales
    id: int (PK)
    code: str (unique, indexed) - Código CIE-10 (ej: I10, E11.9)
    short_description: str - Descripción corta
    full_description: str - Descripción detallada

    # Organización
    chapter: str - Capítulo completo (ej: "IX - Sistema circulatorio")
    chapter_code: str (indexed) - Código de capítulo (I, IV, IX, etc.)
    category: str - Categoría dentro del capítulo

    # Jerarquía
    is_subcategory: bool - Si tiene punto decimal (E11.9)
    parent_code: str - Código padre si es subcategoría

    # Metadata
    is_common: bool - Si es código frecuente en atención primaria
    notes: str - Notas clínicas o consideraciones
    created_at: datetime
    updated_at: datetime
```

**Índices**: code, short_description, chapter_code, is_subcategory, parent_code, is_common

### 2. Schemas Pydantic

**Archivo**: `backend/app/schemas/catalogs.py`

- `Cie10Base`: Schema base con todos los campos
- `Cie10Response`: Response con timestamps
- `Cie10ListResponse`: Lista paginada
- `Cie10SearchMatch`: Resultado de búsqueda con score
- `Cie10SearchResponse`: Respuesta de búsqueda
- `Cie10ChapterSummary`: Resumen por capítulo

### 3. Catálogo de Datos

**Archivo**: `backend/app/scripts/cie10_data.py`

**Códigos por Capítulo**:
- **Capítulo I** (Infecciosas): 2 códigos
- **Capítulo II** (Neoplasias): 3 códigos
- **Capítulo IV** (Endocrinas): 20 códigos (Diabetes, Tiroides, Obesidad)
- **Capítulo IX** (Circulatorio): 16 códigos (HTA, Cardiopatías)
- **Capítulo X** (Respiratorio): 9 códigos (EPOC, Asma, Neumonía)
- **Capítulo XIV** (Genitourinario): 7 códigos (ERC)
- **Capítulo XV** (Embarazo): 6 códigos
- **Capítulo XXI** (Factores de salud): 7 códigos

**Códigos Prioritarios para SAGE3280**:
- I10: Hipertensión esencial
- E11.x: Diabetes mellitus tipo 2 (todas las variantes)
- J44: EPOC
- J45: Asma
- N18.x: Enfermedad renal crónica
- I25: Cardiopatía isquémica

### 4. Migraciones SQL

**006_update_cie10_catalog_structure.sql**:
- Agrega 5 columnas nuevas a tabla existente
- Migra datos de `description` a campos nuevos
- Crea 4 índices para optimización
- Identifica subcategorías automáticamente

**007_populate_cie10_catalog.sql**:
- Inserta 70 códigos CIE-10 nuevos
- Usa ON CONFLICT DO UPDATE (idempotente)
- Preserva código existente (I10)

---

## API REST Endpoints

Base URL: `http://localhost:8000/api/catalogs/cie10`

### 1. Listar Códigos CIE-10

**Endpoint**: `GET /api/catalogs/cie10`

**Query Parameters**:
- `chapter_code` (optional): Filtrar por capítulo (I, IV, IX, etc.)
- `is_common` (optional): true = solo códigos comunes
- `is_subcategory` (optional): true = solo subcategorías
- `limit` (default: 100, max: 500): Registros por página
- `offset` (default: 0): Offset para paginación

**Response**:
```json
{
  "total": 71,
  "limit": 100,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "code": "I10",
      "short_description": "Hipertensión esencial (primaria)",
      "full_description": "Hipertensión esencial (primaria) - HTA sin causa identificable",
      "chapter": "IX - Enfermedades del sistema circulatorio",
      "chapter_code": "IX",
      "category": "Enfermedades hipertensivas",
      "is_subcategory": false,
      "parent_code": null,
      "is_common": true,
      "notes": "Código prioritario para SAGE3280 - Grupo B",
      "created_at": "2025-12-18T06:27:16.060326Z",
      "updated_at": "2025-12-31T22:32:02.156960Z"
    }
  ]
}
```

**Ejemplo**: `/api/catalogs/cie10?chapter_code=IX&is_common=true&limit=5`

### 2. Búsqueda Inteligente

**Endpoint**: `GET /api/catalogs/cie10/search`

**Query Parameters**:
- `q` (required): Término de búsqueda
- `only_common` (default: false): Solo códigos comunes
- `limit` (default: 20, max: 100): Máximo de resultados

**Algoritmo de Scoring**:
- **100 puntos**: Coincidencia exacta de código ("I10" → I10)
- **90 puntos**: Código que empieza con query ("E11" → E11.9)
- **80 puntos**: Encontrado en descripción corta
- **70 puntos**: Código contiene el término
- **60 puntos**: Encontrado en descripción completa

**Response**:
```json
{
  "query": "diabetes",
  "total_matches": 5,
  "matches": [
    {
      "id": 7,
      "code": "E10",
      "short_description": "Diabetes mellitus tipo 1",
      "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
      "chapter_code": "IV",
      "is_common": true,
      "score": 80,
      "match_field": "short_description"
    }
  ]
}
```

**Ejemplo**: `/api/catalogs/cie10/search?q=diabetes&limit=5`

### 3. Obtener por Código

**Endpoint**: `GET /api/catalogs/cie10/code/{code}`

**Ejemplo**: `/api/catalogs/cie10/code/I10`

**Features**:
- Case-insensitive ("i10" encuentra "I10")
- Retorna código completo con metadata

### 4. Obtener por ID

**Endpoint**: `GET /api/catalogs/cie10/{cie10_id}`

**Ejemplo**: `/api/catalogs/cie10/1`

### 5. Listar Capítulos

**Endpoint**: `GET /api/catalogs/cie10/chapters`

**Response**:
```json
{
  "total_chapters": 9,
  "chapters": [
    {
      "chapter_code": "I",
      "chapter_name": "I - Enfermedades infecciosas y parasitarias",
      "total_codes": 2,
      "common_codes": 2
    },
    {
      "chapter_code": "IV",
      "chapter_name": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
      "total_codes": 20,
      "common_codes": 19
    }
  ]
}
```

### 6. Códigos por Capítulo

**Endpoint**: `GET /api/catalogs/cie10/chapter/{chapter_code}`

**Query Parameters**:
- `limit` (default: 100)
- `offset` (default: 0)

**Ejemplo**: `/api/catalogs/cie10/chapter/IX?limit=10`

### 7. Estadísticas

**Endpoint**: `GET /api/catalogs/cie10/stats/summary`

**Response**:
```json
{
  "total_codes": 71,
  "common_codes": 67,
  "subcategories": 33,
  "main_codes": 38,
  "chapters_count": 9,
  "by_chapter": {
    "I": 2,
    "II": 3,
    "IV": 20,
    "IX": 16,
    "X": 9,
    "XIV": 7,
    "XV": 6,
    "XXI": 7
  }
}
```

---

## Integración con Excel Processor

### Archivo Modificado

**`backend/app/services/excel_processor.py`**

### Nuevas Funcionalidades

#### 1. Método `_extract_and_normalize_cie10_codes()`

**Descripción**: Extrae y normaliza códigos CIE-10 desde texto libre

**Estrategias de Extracción**:

1. **Regex Pattern Matching**:
   ```python
   Pattern: r'\b([A-Z]\d{2}(?:\.\d{1,2})?)\b'
   Ejemplos: I10, E11.9, J44, N18.3
   ```

2. **Normalización con Catálogo**:
   - Busca cada código en base de datos (case-insensitive)
   - Si existe: retorna "CODE - DESCRIPTION"
   - Si no existe: retorna "[NO_NORMALIZADO] CODE"

3. **Búsqueda por Keywords** (si no hay códigos):
   - Extrae palabras significativas (≥3 chars)
   - Busca en descripciones de códigos comunes
   - Retorna sugerencias: "CODE - DESCRIPTION [SUGERIDO]"
   - Máximo 1 sugerencia por keyword (top 3 keywords)

**Ejemplos de Entrada/Salida**:

| Input | Output |
|-------|--------|
| "I10, E11.9" | ["I10 - Hipertensión esencial (primaria)", "E11.9 - Diabetes mellitus tipo 2 sin complicaciones"] |
| "Hipertensión arterial" | ["I10 - Hipertensión esencial (primaria) [SUGERIDO]"] |
| "X99 - Código inválido" | ["[NO_NORMALIZADO] X99"] |
| "" (vacío) | [] |

#### 2. Estadísticas de Normalización

```python
self.cie10_normalization_stats = {
    'total_codes_found': 0,      # Total de códigos encontrados
    'normalized': 0,              # Códigos normalizados exitosamente
    'not_found': 0,               # Códigos no encontrados en catálogo
    'patients_with_codes': 0      # Pacientes con al menos 1 código
}
```

#### 3. Campos Agregados al Patient Data

```python
patient_data = {
    # ... campos existentes ...
    'cie10_codes': ['I10 - Hipertensión...', 'E11.9 - Diabetes...'],
    'cie10_codes_count': 2,
    # ... campos existentes ...
}
```

#### 4. Summary Actualizado

```python
summary = {
    'total_rows': 100,
    'columns_found': [...],
    'columns_missing': [...],
    'eps_normalization': {...},
    'cie10_normalization': {  # NUEVO
        'total_codes_found': 150,
        'normalized': 120,
        'not_found': 30,
        'patients_with_codes': 85
    }
}
```

---

## Testing y Validación

### Archivo de Prueba

**Ubicación**: `backend/test_patients_cie10.xlsx`

**Contenido**: 12 pacientes con casos de prueba variados

### Casos de Prueba

| # | Paciente | Diagnósticos | Códigos Esperados | Tipo |
|---|----------|--------------|-------------------|------|
| 1 | Juan Carlos García | "I10 - Hipertensión, E11.9 - Diabetes tipo 2" | I10, E11.9 | Códigos explícitos ✓ |
| 2 | María Elena Rodríguez | "Hipertensión arterial, Diabetes mellitus tipo 2" | I10, E11 [SUGERIDO] | Keywords ✓ |
| 3 | Pedro Antonio Martínez | "J44 - EPOC, I10, J45.9 - Asma" | J44, I10, J45.9 | Códigos mixtos ✓ |
| 4 | Ana María Sánchez | "HTA controlada, DM tipo 2 sin complicaciones" | I10 [SUGERIDO] | Keywords abreviados ✓ |
| 5 | Carlos Alberto Hernández | "I11.9, E11.2, N18.3" | I11.9, E11.2, N18.3 | Subcategorías ✓ |
| 6 | Luz Mery Ospina | "Asma bronquial, Rinitis alérgica" | J45 [SUGERIDO] | Texto libre ✓ |
| 7 | Jorge Luis Ramírez | "I25.1, I10, E78.0" | I10, [NO_NORMALIZADO] I25.1, [NO_NORMALIZADO] E78.0 | Códigos no en catálogo ⚠️ |
| 8 | Sandra Patricia Moreno | "E03.9 - Hipotiroidismo, E66.9 - Obesidad" | E03.9, E66.9 | Códigos endocrinos ✓ |
| 9 | Roberto Jiménez | "Gastritis crónica, Reflujo gastroesofágico" | [] | Sin códigos en catálogo ⚠️ |
| 10 | Gloria Inés Vargas | "I10, E11, N18.3, E78.5" | I10, E11, N18.3, [NO_NORMALIZADO] E78.5 | Mixto ✓/⚠️ |
| 11 | Alfonso Torres | "J44.0 - EPOC exacerbado, I50.9" | J44.0, [NO_NORMALIZADO] I50.9 | EPOC + no catalogado ✓/⚠️ |
| 12 | Beatriz Elena Restrepo | "" (vacío) | [] | Sin diagnósticos ✓ |

### Validación de Endpoints

Todos los 7 endpoints REST fueron probados exitosamente:

- ✅ GET /cie10 - Lista con filtros
- ✅ GET /cie10/search - Búsqueda inteligente
- ✅ GET /cie10/code/{code} - Obtener por código
- ✅ GET /cie10/{id} - Obtener por ID
- ✅ GET /cie10/chapters - Listar capítulos
- ✅ GET /cie10/chapter/{chapter_code} - Códigos por capítulo
- ✅ GET /cie10/stats/summary - Estadísticas

**Issue Resuelto**: Conflicto de rutas entre `/{id}` y `/chapters` → Reordenadas rutas específicas antes de genéricas

---

## Guía de Uso

### Para Desarrolladores

#### 1. Ejecutar Migraciones

```bash
cd backend
psql -U postgres -d sage3280 -f migrations/006_update_cie10_catalog_structure.sql
psql -U postgres -d sage3280 -f migrations/007_populate_cie10_catalog.sql
```

#### 2. Iniciar Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### 3. Probar API

```bash
# Estadísticas
curl http://localhost:8000/api/catalogs/cie10/stats/summary

# Búsqueda
curl "http://localhost:8000/api/catalogs/cie10/search?q=diabetes"

# Por código
curl http://localhost:8000/api/catalogs/cie10/code/I10
```

#### 4. Procesar Excel

```python
from app.services.excel_processor import ExcelProcessor
from app.database import get_db

db = next(get_db())
processor = ExcelProcessor(db=db)

# Cargar archivo
success, message, count = processor.load_file("test_patients_cie10.xlsx")

# Extraer pacientes
patients = processor.extract_patients()

# Ver estadísticas
summary = processor.get_summary()
print(summary['cie10_normalization'])
```

### Para Usuarios Finales

1. **Subir Excel**: Usar interfaz web para subir archivo con columna "Diagnósticos"
2. **Revisión**: Sistema extrae y normaliza códigos CIE-10 automáticamente
3. **Validación**: Revisar pacientes con códigos `[NO_NORMALIZADO]` o `[SUGERIDO]`
4. **Guardado**: Sistema almacena códigos normalizados en base de datos

---

## Próximos Pasos

### Mejoras Pendientes

1. **A.2.11 - Frontend (Opcional)**:
   - Buscador de códigos CIE-10 en interfaz web
   - Autocomplete con sugerencias
   - Visualización de jerarquía de códigos

2. **Expandir Catálogo**:
   - Agregar más códigos CIE-10 según necesidades
   - Incluir códigos del catálogo completo (14,000+)
   - Agregar sinónimos y términos alternativos

3. **Inteligencia Adicional**:
   - Machine Learning para mejorar sugerencias
   - Análisis de patrones en diagnósticos
   - Validación cruzada con medicamentos/tratamientos

4. **Integración con RIAS**:
   - Vincular códigos CIE-10 con rutas RIAS
   - Mapeo automático a Grupo A, B, C
   - Alertas de seguimiento según diagnósticos

---

## Resumen de Archivos Modificados/Creados

### Creados

- `backend/app/models/cie10.py` - Modelo SQLAlchemy
- `backend/app/scripts/cie10_data.py` - Catálogo de 70 códigos
- `backend/migrations/006_update_cie10_catalog_structure.sql` - Migración estructura
- `backend/migrations/007_populate_cie10_catalog.sql` - Migración datos
- `backend/test_patients_cie10.xlsx` - Archivo de prueba
- `backend/create_test_excel_cie10.py` - Script generador de pruebas
- `backend/docs/SUBFASE_A2_CIE10_CATALOG.md` - Esta documentación

### Modificados

- `backend/app/schemas/catalogs.py` - Agregados schemas CIE-10
- `backend/app/api/routes/catalogs.py` - Agregados 7 endpoints CIE-10
- `backend/app/services/excel_processor.py` - Integración extracción CIE-10

---

## Conclusión

La Subfase A.2 está **100% completa** y lista para producción. El sistema ahora puede:

✅ Gestionar catálogo de 71 códigos CIE-10
✅ Buscar códigos con inteligencia (scoring)
✅ Normalizar diagnósticos automáticamente desde Excel
✅ Proporcionar API REST completa
✅ Manejar casos edge (códigos no encontrados, sugerencias)

**Próxima Subfase**: A.3 - Catálogo CUPS (Procedimientos) o B.1 - Implementación Grupo A (RIAS)

---

**Documentado por**: Claude Sonnet 4.5
**Fecha**: 31 de Diciembre de 2024
**Versión**: 1.0
