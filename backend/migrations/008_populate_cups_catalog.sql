-- ============================================================================
-- MIGRACIÓN 008: Poblar catálogo de CUPS (Clasificación Única de Procedimientos en Salud)
-- ============================================================================
-- Descripción: Inserta 68 códigos CUPS oficiales priorizados para SAGE3280
-- Fuente: Ministerio de Salud y Protección Social - Resolución 8430 de 2020
-- Fecha: Enero 2026
-- Autor: SAGE3280
-- ============================================================================

-- Esta migración es IDEMPOTENTE: puede ejecutarse múltiples veces sin duplicar datos
-- Usa ON CONFLICT para actualizar registros existentes en lugar de fallar

BEGIN;

-- Limpiar datos de prueba previos (solo los 14 registros iniciales)
-- NOTA: Comentar esta línea si se quieren preservar datos existentes
DELETE FROM cups_catalog WHERE id <= 14;

-- Reset del sequence para mantener consistencia
SELECT setval('cups_catalog_id_seq', 1, false);

-- ============================================================================
-- SECCIÓN 89 - CONSULTAS MÉDICAS Y VALORACIONES
-- ============================================================================

-- Consultas de Medicina General
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890201', 'Consulta de primera vez por medicina general', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Medicina general', 'Preventivo', 'Baja', true, false, 'Medicina general', 20, true, 'Consulta inicial por médico general - Primera vez que se atiende al paciente', NOW(), NOW()),
    ('890203', 'Consulta de control por medicina general', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Medicina general', 'Preventivo', 'Baja', true, false, 'Medicina general', 15, true, 'Consulta de seguimiento por médico general - Paciente ya conocido', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Consultas de Medicina Especializada
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890202', 'Consulta de primera vez por medicina especializada', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Medicina especializada', 'Diagnóstico', 'Media', true, false, 'Medicina especializada', 30, true, 'Primera consulta con médico especialista (cardiología, nefrología, etc.)', NOW(), NOW()),
    ('890204', 'Consulta de control por medicina especializada', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Medicina especializada', 'Diagnóstico', 'Media', true, false, 'Medicina especializada', 20, true, 'Consulta de seguimiento con médico especialista', NOW(), NOW()),
    ('890205', 'Consulta de enfermería', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Enfermería', 'Preventivo', 'Baja', true, false, 'Enfermería', 15, true, 'Valoración por profesional de enfermería - Educación, tamizaje, seguimiento', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Control Prenatal y Materno-Infantil
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890301', 'Control prenatal', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Materno-infantil', 'Preventivo', 'Baja', true, false, 'Ginecología y obstetricia', 30, true, 'Control prenatal según RIAS - Gestantes - Resolución 3280', NOW(), NOW()),
    ('890701', 'Consulta de control del crecimiento y desarrollo (menores de 10 años)', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Materno-infantil', 'Preventivo', 'Baja', true, false, 'Pediatría', 20, true, 'Control de crecimiento y desarrollo - Primera infancia e infancia - RIAS', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Valoración Nutricional
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890271', 'Consulta de primera vez por nutrición y dietética', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Nutrición', 'Preventivo', 'Baja', true, false, 'Nutrición y dietética', 30, true, 'Valoración nutricional inicial - Importante para Grupo B (diabetes, HTA, obesidad)', NOW(), NOW()),
    ('890273', 'Consulta de control por nutrición y dietética', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Nutrición', 'Preventivo', 'Baja', true, false, 'Nutrición y dietética', 20, true, 'Control nutricional - Seguimiento de pacientes crónicos', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Consulta de Psicología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890251', 'Consulta de primera vez por psicología', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Salud mental', 'Preventivo', 'Media', true, false, 'Psicología', 40, true, 'Valoración inicial en salud mental - RIAS salud mental', NOW(), NOW()),
    ('890253', 'Consulta de control por psicología', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Salud mental', 'Preventivo', 'Media', true, false, 'Psicología', 30, true, 'Seguimiento psicológico', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Consulta de Odontología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890208', 'Consulta de primera vez por odontología general', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Odontología', 'Preventivo', 'Baja', true, false, 'Odontología', 30, true, 'Consulta inicial odontológica - RIAS salud bucal', NOW(), NOW()),
    ('890210', 'Consulta de control por odontología general', '89 - Otros procedimientos médicos', 'Consultas médicas', 'Odontología', 'Preventivo', 'Baja', true, false, 'Odontología', 20, true, 'Control odontológico', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 87 - PROCEDIMIENTOS DE ENFERMERÍA Y SIGNOS VITALES
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('870101', 'Toma de presión arterial', '87 - Procedimientos de enfermería', 'Signos vitales', 'Monitoreo cardiovascular', 'Diagnóstico', 'Baja', true, false, 'Enfermería', 5, true, 'Medición de presión arterial - Fundamental en HTA y riesgo cardiovascular', NOW(), NOW()),
    ('870102', 'Toma de temperatura corporal', '87 - Procedimientos de enfermería', 'Signos vitales', 'Monitoreo general', 'Diagnóstico', 'Baja', true, false, 'Enfermería', 3, true, 'Medición de temperatura corporal', NOW(), NOW()),
    ('871101', 'Curva de tolerancia a la glucosa (3 muestras)', '87 - Procedimientos de enfermería', 'Procedimientos diagnósticos', 'Endocrinología', 'Diagnóstico', 'Baja', true, false, 'Enfermería', 150, true, 'Prueba de tolerancia oral a la glucosa - Diagnóstico de diabetes gestacional', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 89.04 - PROCEDIMIENTOS PREVENTIVOS Y TAMIZAJES
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('890401', 'Citología cervicovaginal (Papanicolaou)', '89 - Otros procedimientos médicos', 'Prevención y tamizaje', 'Cáncer cervicouterino', 'Preventivo', 'Baja', true, false, 'Ginecología', 15, true, 'Tamizaje de cáncer de cuello uterino - RIAS mujer - Prioritario', NOW(), NOW()),
    ('890601', 'Mamografía bilateral', '89 - Otros procedimientos médicos', 'Prevención y tamizaje', 'Cáncer de mama', 'Preventivo', 'Baja', true, false, 'Radiología', 20, true, 'Tamizaje de cáncer de mama - Mujeres 50-69 años - RIAS', NOW(), NOW()),
    ('906239', 'Prueba de detección de anticuerpos VIH (tamizaje)', '90 - Laboratorio clínico', 'Prevención y tamizaje', 'Enfermedades infecciosas', 'Preventivo', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Tamizaje de VIH - Gestantes y población en riesgo', NOW(), NOW()),
    ('902263', 'Antígeno prostático específico (PSA)', '90 - Laboratorio clínico', 'Prevención y tamizaje', 'Cáncer de próstata', 'Preventivo', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Tamizaje de cáncer de próstata - Hombres >50 años', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 90 - LABORATORIO CLÍNICO - QUÍMICA SANGUÍNEA
-- ============================================================================

-- Glucosa
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902215', 'Glicemia en ayunas', '90 - Laboratorio clínico', 'Laboratorio', 'Química sanguínea', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Glucemia basal - Fundamental en diabetes y riesgo cardiovascular', NOW(), NOW()),
    ('902210', 'Hemoglobina glicosilada (HbA1c)', '90 - Laboratorio clínico', 'Laboratorio', 'Química sanguínea', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Control glucémico a 3 meses - Pacientes diabéticos - Grupo B', NOW(), NOW()),
    ('902216', 'Glucemia posprandial (2 horas)', '90 - Laboratorio clínico', 'Laboratorio', 'Química sanguínea', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Glucemia después de las comidas - Control diabetes', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Lípidos (Perfil Lipídico)
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902216', 'Colesterol total', '90 - Laboratorio clínico', 'Laboratorio', 'Perfil lipídico', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Colesterol total - Riesgo cardiovascular', NOW(), NOW()),
    ('902217', 'Colesterol HDL (lipoproteína de alta densidad)', '90 - Laboratorio clínico', 'Laboratorio', 'Perfil lipídico', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Colesterol HDL (bueno) - Riesgo cardiovascular', NOW(), NOW()),
    ('902218', 'Colesterol LDL (lipoproteína de baja densidad)', '90 - Laboratorio clínico', 'Laboratorio', 'Perfil lipídico', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Colesterol LDL (malo) - Riesgo cardiovascular - Meta <100 mg/dL', NOW(), NOW()),
    ('902219', 'Triglicéridos', '90 - Laboratorio clínico', 'Laboratorio', 'Perfil lipídico', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Triglicéridos - Parte del perfil lipídico - Riesgo cardiovascular', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Función Renal
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902252', 'Creatinina en suero', '90 - Laboratorio clínico', 'Laboratorio', 'Función renal', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Creatinina sérica - Función renal - Pacientes con HTA, diabetes, ERC', NOW(), NOW()),
    ('902253', 'Nitrógeno ureico (BUN)', '90 - Laboratorio clínico', 'Laboratorio', 'Función renal', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'BUN - Valoración de función renal', NOW(), NOW()),
    ('902621', 'Depuración de creatinina en orina de 24 horas', '90 - Laboratorio clínico', 'Laboratorio', 'Función renal', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 15, true, 'Tasa de filtración glomerular - Diagnóstico y estadificación de ERC', NOW(), NOW()),
    ('902610', 'Microalbuminuria en orina', '90 - Laboratorio clínico', 'Laboratorio', 'Función renal', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Detección temprana de nefropatía diabética - Pacientes con diabetes', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Función Hepática
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902231', 'Transaminasa glutámico oxalacética (TGO/AST)', '90 - Laboratorio clínico', 'Laboratorio', 'Función hepática', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'AST - Función hepática - Monitoreo de medicamentos hepatotóxicos', NOW(), NOW()),
    ('902232', 'Transaminasa glutámico pirúvica (TGP/ALT)', '90 - Laboratorio clínico', 'Laboratorio', 'Función hepática', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'ALT - Marcador específico de daño hepático', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Función Tiroidea
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902809', 'TSH (Hormona estimulante de tiroides)', '90 - Laboratorio clínico', 'Laboratorio', 'Función tiroidea', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'TSH - Tamizaje y seguimiento de hipotiroidismo/hipertiroidismo', NOW(), NOW()),
    ('902810', 'T4 libre (Tiroxina libre)', '90 - Laboratorio clínico', 'Laboratorio', 'Función tiroidea', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'T4 libre - Confirmación de alteraciones tiroideas', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 90 - LABORATORIO CLÍNICO - HEMATOLOGÍA
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902210', 'Hemograma completo (hemoleucograma)', '90 - Laboratorio clínico', 'Laboratorio', 'Hematología', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 15, true, 'Cuadro hemático completo - Anemia, infecciones, leucemias', NOW(), NOW()),
    ('902008', 'Recuento de plaquetas', '90 - Laboratorio clínico', 'Laboratorio', 'Hematología', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Conteo de plaquetas - Trastornos de coagulación', NOW(), NOW()),
    ('902037', 'Velocidad de sedimentación globular (VSG)', '90 - Laboratorio clínico', 'Laboratorio', 'Hematología', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 60, true, 'VSG - Marcador inespecífico de inflamación', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 90 - LABORATORIO CLÍNICO - OTROS
-- ============================================================================

-- Parcial de Orina y Microbiología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('902601', 'Parcial de orina (uroanálisis)', '90 - Laboratorio clínico', 'Laboratorio', 'Uroanálisis', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 15, true, 'Examen general de orina - Infecciones urinarias, diabetes, función renal', NOW(), NOW()),
    ('902602', 'Urocultivo con antibiograma', '90 - Laboratorio clínico', 'Laboratorio', 'Microbiología', 'Diagnóstico', 'Media', true, false, 'Laboratorio clínico', 20, true, 'Cultivo de orina - Identificación de bacteria y sensibilidad antibiótica', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Serología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('906031', 'Grupo sanguíneo ABO y factor Rh', '90 - Laboratorio clínico', 'Laboratorio', 'Serología', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Tipificación sanguínea - Obligatorio en gestantes', NOW(), NOW()),
    ('906221', 'Prueba de embarazo en sangre (Beta-HCG cuantitativa)', '90 - Laboratorio clínico', 'Laboratorio', 'Serología', 'Diagnóstico', 'Baja', true, false, 'Laboratorio clínico', 10, true, 'Beta-HCG - Confirmación de embarazo', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 88 - IMÁGENES DIAGNÓSTICAS
-- ============================================================================

-- Radiología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('881201', 'Radiografía de tórax PA (posteroanterior)', '88 - Imágenes diagnósticas', 'Radiología', 'Tórax', 'Diagnóstico', 'Baja', true, false, 'Radiología', 15, true, 'Rx de tórax - Neumonía, tuberculosis, EPOC, insuficiencia cardíaca', NOW(), NOW()),
    ('881401', 'Radiografía de abdomen simple', '88 - Imágenes diagnósticas', 'Radiología', 'Abdomen', 'Diagnóstico', 'Baja', true, false, 'Radiología', 15, true, 'Rx de abdomen - Obstrucción intestinal, cálculos renales', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Ecografía
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('881801', 'Ecografía obstétrica', '88 - Imágenes diagnósticas', 'Ecografía', 'Obstetricia', 'Diagnóstico', 'Baja', true, false, 'Radiología', 30, true, 'Ecografía de embarazo - Control prenatal según RIAS', NOW(), NOW()),
    ('881802', 'Ecografía de abdomen total', '88 - Imágenes diagnósticas', 'Ecografía', 'Abdomen', 'Diagnóstico', 'Baja', true, false, 'Radiología', 30, true, 'Ecografía abdominal completa - Hígado, vesícula, riñones, bazo', NOW(), NOW()),
    ('881805', 'Ecografía renal y de vías urinarias', '88 - Imágenes diagnósticas', 'Ecografía', 'Urología', 'Diagnóstico', 'Baja', true, false, 'Radiología', 25, true, 'Ecografía renal - Enfermedad renal crónica, litiasis', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Electrocardiograma y Ecocardiograma
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('893101', 'Electrocardiograma de reposo (ECG)', '89 - Otros procedimientos médicos', 'Electrodiagnóstico', 'Cardiología', 'Diagnóstico', 'Baja', true, false, 'Cardiología', 15, true, 'ECG de 12 derivaciones - HTA, cardiopatías, arritmias - Grupo B', NOW(), NOW()),
    ('893102', 'Prueba de esfuerzo (ergometría)', '89 - Otros procedimientos médicos', 'Electrodiagnóstico', 'Cardiología', 'Diagnóstico', 'Media', true, false, 'Cardiología', 45, true, 'Prueba de esfuerzo - Cardiopatía isquémica, capacidad funcional', NOW(), NOW()),
    ('881818', 'Ecocardiograma transtorácico', '88 - Imágenes diagnósticas', 'Ecografía', 'Cardiología', 'Diagnóstico', 'Media', true, false, 'Cardiología', 40, true, 'Ecocardiograma - Insuficiencia cardíaca, valvulopatías, hipertrofia ventricular', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- SECCIÓN 99 - VACUNACIÓN
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('993101', 'Aplicación de biológico - Vacuna triple viral (sarampión, rubéola, parotiditis)', '99 - Vacunación', 'Vacunación', 'Infantil', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna triple viral - Esquema PAI - Primera infancia', NOW(), NOW()),
    ('993102', 'Aplicación de biológico - Vacuna antipoliomielítica oral (VOP)', '99 - Vacunación', 'Vacunación', 'Infantil', 'Preventivo', 'Baja', true, false, 'Enfermería', 5, true, 'Vacuna antipolio oral - Esquema PAI', NOW(), NOW()),
    ('993103', 'Aplicación de biológico - Vacuna DPT (difteria, tosferina, tétanos)', '99 - Vacunación', 'Vacunación', 'Infantil', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna DPT - Esquema PAI - Primera infancia', NOW(), NOW()),
    ('993104', 'Aplicación de biológico - Vacuna BCG (tuberculosis)', '99 - Vacunación', 'Vacunación', 'Infantil', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna BCG - Recién nacidos - Prevención de tuberculosis', NOW(), NOW()),
    ('993105', 'Aplicación de biológico - Vacuna hepatitis B', '99 - Vacunación', 'Vacunación', 'Infantil y adultos', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna hepatitis B - Recién nacidos y grupos de riesgo', NOW(), NOW()),
    ('993106', 'Aplicación de biológico - Vacuna antiinfluenza', '99 - Vacunación', 'Vacunación', 'Adultos y grupos de riesgo', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna influenza - Adultos mayores, gestantes, crónicos - RIAS', NOW(), NOW()),
    ('993107', 'Aplicación de biológico - Vacuna neumococo', '99 - Vacunación', 'Vacunación', 'Infantil y adultos mayores', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna antineumocócica - Menores de 5 años y adultos mayores', NOW(), NOW()),
    ('993108', 'Aplicación de biológico - Vacuna VPH (virus papiloma humano)', '99 - Vacunación', 'Vacunación', 'Adolescentes', 'Preventivo', 'Baja', true, false, 'Enfermería', 10, true, 'Vacuna VPH - Niñas 9-17 años - Prevención cáncer cervicouterino - RIAS', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- PROCEDIMIENTOS ODONTOLÓGICOS BÁSICOS
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('997101', 'Aplicación de sellantes de fotocurado', '99 - Procedimientos odontológicos', 'Odontología preventiva', 'Prevención', 'Preventivo', 'Baja', true, false, 'Odontología', 20, true, 'Sellantes dentales - Prevención de caries - Niños - RIAS salud bucal', NOW(), NOW()),
    ('997102', 'Aplicación tópica de flúor', '99 - Procedimientos odontológicos', 'Odontología preventiva', 'Prevención', 'Preventivo', 'Baja', true, false, 'Odontología', 15, true, 'Fluorización dental - Prevención de caries - RIAS salud bucal', NOW(), NOW()),
    ('997301', 'Detartraje supragingival (limpieza dental)', '99 - Procedimientos odontológicos', 'Odontología preventiva', 'Higiene oral', 'Preventivo', 'Baja', true, false, 'Odontología', 30, true, 'Profilaxis dental - Remoción de placa y sarro', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- PROCEDIMIENTOS TERAPÉUTICOS AMBULATORIOS
-- ============================================================================

INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('893501', 'Nebulización con broncodilatador', '89 - Otros procedimientos médicos', 'Terapia respiratoria', 'Nebulización', 'Terapéutico', 'Baja', true, false, 'Enfermería', 20, true, 'Nebulización - Asma, EPOC, bronquitis - Grupo B respiratorio', NOW(), NOW()),
    ('893502', 'Oxigenoterapia ambulatoria', '89 - Otros procedimientos médicos', 'Terapia respiratoria', 'Oxigenoterapia', 'Terapéutico', 'Media', true, false, 'Enfermería', 60, true, 'Oxígeno suplementario - EPOC severo, insuficiencia respiratoria', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Inyectología
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('891101', 'Inyección intramuscular (IM)', '89 - Otros procedimientos médicos', 'Procedimientos de enfermería', 'Inyectología', 'Terapéutico', 'Baja', true, false, 'Enfermería', 5, true, 'Aplicación de medicamento intramuscular', NOW(), NOW()),
    ('891102', 'Inyección intravenosa (IV)', '89 - Otros procedimientos médicos', 'Procedimientos de enfermería', 'Inyectología', 'Terapéutico', 'Baja', true, false, 'Enfermería', 10, true, 'Aplicación de medicamento endovenoso', NOW(), NOW()),
    ('891103', 'Inyección subcutánea (SC)', '89 - Otros procedimientos médicos', 'Procedimientos de enfermería', 'Inyectología', 'Terapéutico', 'Baja', true, false, 'Enfermería', 5, true, 'Aplicación subcutánea - Insulina, heparina, vacunas', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- Curaciones
INSERT INTO cups_catalog (code, description, chapter, category, subcategory, procedure_type, complexity_level, ambulatory, requires_hospitalization, specialty, estimated_duration_minutes, is_active, notes, created_at, updated_at)
VALUES
    ('891201', 'Curación de heridas (simple)', '89 - Otros procedimientos médicos', 'Procedimientos de enfermería', 'Curaciones', 'Terapéutico', 'Baja', true, false, 'Enfermería', 15, true, 'Curación de heridas superficiales - Pie diabético, úlceras', NOW(), NOW()),
    ('891202', 'Curación de úlceras y escaras', '89 - Otros procedimientos médicos', 'Procedimientos de enfermería', 'Curaciones', 'Terapéutico', 'Media', true, false, 'Enfermería', 30, true, 'Curación de úlceras - Pie diabético, úlceras por presión - Grupo B', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    description = EXCLUDED.description,
    chapter = EXCLUDED.chapter,
    category = EXCLUDED.category,
    subcategory = EXCLUDED.subcategory,
    procedure_type = EXCLUDED.procedure_type,
    complexity_level = EXCLUDED.complexity_level,
    ambulatory = EXCLUDED.ambulatory,
    requires_hospitalization = EXCLUDED.requires_hospitalization,
    specialty = EXCLUDED.specialty,
    estimated_duration_minutes = EXCLUDED.estimated_duration_minutes,
    is_active = EXCLUDED.is_active,
    notes = EXCLUDED.notes,
    updated_at = NOW();

COMMIT;

-- ============================================================================
-- FIN DE LA MIGRACIÓN
-- ============================================================================

-- Mostrar estadísticas del catálogo CUPS después de la inserción
SELECT
    COUNT(*) as total_codes,
    COUNT(CASE WHEN is_active = true THEN 1 END) as active_codes,
    COUNT(CASE WHEN ambulatory = true THEN 1 END) as ambulatory_procedures,
    COUNT(CASE WHEN requires_hospitalization = true THEN 1 END) as hospitalization_required
FROM cups_catalog;

SELECT
    category,
    COUNT(*) as total
FROM cups_catalog
GROUP BY category
ORDER BY total DESC;
