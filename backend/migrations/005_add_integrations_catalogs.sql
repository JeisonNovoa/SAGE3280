-- Migration: Add Integration Catalogs (EPS, CIE-10, CUPS)
-- Date: 2025-12-15
-- Description: Creates catalog tables for Colombian health system integrations
--   - EPS catalog (health insurance providers)
--   - CIE-10 catalog (disease codes)
--   - CUPS catalog (procedure codes)

-- =========================================================
-- 1. Create EPS catalog table
-- =========================================================

CREATE TABLE IF NOT EXISTS eps_catalog (
    id SERIAL PRIMARY KEY,

    -- Identification
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    short_name VARCHAR(100),
    nit VARCHAR(20),

    -- Type and status
    regime_type VARCHAR(20) NOT NULL DEFAULT 'contributivo',
    is_active BOOLEAN DEFAULT TRUE,

    -- Contact
    phone VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(200),
    address VARCHAR(300),

    -- Geographic coverage
    coverage_nationwide BOOLEAN DEFAULT FALSE,
    departments VARCHAR(500),

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    notes VARCHAR(500)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_eps_code ON eps_catalog(code);
CREATE INDEX IF NOT EXISTS idx_eps_name ON eps_catalog(name);
CREATE INDEX IF NOT EXISTS idx_eps_active ON eps_catalog(is_active);

-- Comments
COMMENT ON TABLE eps_catalog IS 'Catálogo oficial de EPS activas en Colombia';
COMMENT ON COLUMN eps_catalog.code IS 'Código oficial de la EPS (Supersalud)';
COMMENT ON COLUMN eps_catalog.regime_type IS 'Tipo de régimen: contributivo, subsidiado, especial';

-- =========================================================
-- 2. Create CIE-10 catalog table
-- =========================================================

CREATE TABLE IF NOT EXISTS cie10_catalog (
    id SERIAL PRIMARY KEY,

    -- CIE-10 code
    code VARCHAR(10) NOT NULL UNIQUE,

    -- Descriptions
    description TEXT NOT NULL,
    description_en TEXT,

    -- Categorization
    chapter VARCHAR(200),
    chapter_code VARCHAR(10),
    category VARCHAR(200),

    -- Sex specific
    sex_specific VARCHAR(1),  -- 'M', 'F', null

    -- Type
    is_chronic BOOLEAN DEFAULT FALSE,
    is_infectious BOOLEAN DEFAULT FALSE,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    notes TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cie10_code ON cie10_catalog(code);
CREATE INDEX IF NOT EXISTS idx_cie10_chapter ON cie10_catalog(chapter_code);
CREATE INDEX IF NOT EXISTS idx_cie10_chronic ON cie10_catalog(is_chronic);
CREATE INDEX IF NOT EXISTS idx_cie10_active ON cie10_catalog(is_active);

-- Comments
COMMENT ON TABLE cie10_catalog IS 'Catálogo CIE-10: Clasificación Internacional de Enfermedades';
COMMENT ON COLUMN cie10_catalog.code IS 'Código CIE-10 (ej: I10, E11.9, C50.1)';
COMMENT ON COLUMN cie10_catalog.is_chronic IS 'Marca si es una enfermedad crónica para SAGE3280';

-- =========================================================
-- 3. Create CUPS catalog table
-- =========================================================

CREATE TABLE IF NOT EXISTS cups_catalog (
    id SERIAL PRIMARY KEY,

    -- CUPS code
    code VARCHAR(20) NOT NULL UNIQUE,

    -- Description
    description TEXT NOT NULL,

    -- Classification
    chapter VARCHAR(200),
    category VARCHAR(200),
    subcategory VARCHAR(200),

    -- Type
    procedure_type VARCHAR(100),  -- Diagnóstico, Terapéutico, Preventivo

    -- Complexity
    complexity_level VARCHAR(20),  -- Baja, Media, Alta

    -- Location
    ambulatory BOOLEAN DEFAULT TRUE,
    requires_hospitalization BOOLEAN DEFAULT FALSE,

    -- Specialty
    specialty VARCHAR(200),

    -- Time
    estimated_duration_minutes INTEGER,

    -- Cost
    reference_cost FLOAT,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    contraindications TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cups_code ON cups_catalog(code);
CREATE INDEX IF NOT EXISTS idx_cups_type ON cups_catalog(procedure_type);
CREATE INDEX IF NOT EXISTS idx_cups_complexity ON cups_catalog(complexity_level);
CREATE INDEX IF NOT EXISTS idx_cups_active ON cups_catalog(is_active);

-- Comments
COMMENT ON TABLE cups_catalog IS 'Catálogo CUPS: Clasificación Única de Procedimientos en Salud (Colombia)';
COMMENT ON COLUMN cups_catalog.code IS 'Código CUPS oficial (Resolución 8430/2020)';
COMMENT ON COLUMN cups_catalog.complexity_level IS 'Nivel de complejidad del procedimiento';

-- =========================================================
-- 4. Create update triggers
-- =========================================================

-- Trigger for eps_catalog
DROP TRIGGER IF EXISTS update_eps_catalog_updated_at ON eps_catalog;
CREATE TRIGGER update_eps_catalog_updated_at
    BEFORE UPDATE ON eps_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for cie10_catalog
DROP TRIGGER IF EXISTS update_cie10_catalog_updated_at ON cie10_catalog;
CREATE TRIGGER update_cie10_catalog_updated_at
    BEFORE UPDATE ON cie10_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for cups_catalog
DROP TRIGGER IF EXISTS update_cups_catalog_updated_at ON cups_catalog;
CREATE TRIGGER update_cups_catalog_updated_at
    BEFORE UPDATE ON cups_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =========================================================
-- 5. Insert sample EPS data (principales EPS de Colombia)
-- =========================================================

INSERT INTO eps_catalog (code, name, short_name, regime_type, is_active, coverage_nationwide) VALUES
('EPS001', 'Nueva EPS', 'Nueva EPS', 'contributivo', true, true),
('EPS002', 'Sura EPS', 'SURA', 'contributivo', true, true),
('EPS003', 'Salud Total EPS', 'Salud Total', 'contributivo', true, true),
('EPS004', 'Sanitas EPS', 'Sanitas', 'contributivo', true, true),
('EPS005', 'Compensar EPS', 'Compensar', 'contributivo', true, false),
('EPS006', 'Famisanar EPS', 'Famisanar', 'contributivo', true, false),
('EPS007', 'Colsanitas EPS', 'Colsanitas', 'contributivo', true, true),
('EPS008', 'Coosalud EPS', 'Coosalud', 'subsidiado', true, false),
('EPS009', 'Capital Salud EPS', 'Capital Salud', 'subsidiado', true, false),
('EPS010', 'Aliansalud EPS', 'Aliansalud', 'subsidiado', true, false)
ON CONFLICT (code) DO NOTHING;

-- =========================================================
-- 6. Insert sample CIE-10 codes (most common for Colombia)
-- =========================================================

INSERT INTO cie10_catalog (code, description, chapter, chapter_code, is_chronic, is_active) VALUES
-- Cardiovascular (Chapter I)
('I10', 'Hipertensión esencial (primaria)', 'Enfermedades del sistema circulatorio', 'I', true, true),
('I11', 'Enfermedad cardíaca hipertensiva', 'Enfermedades del sistema circulatorio', 'I', true, true),
('I25', 'Cardiopatía isquémica crónica', 'Enfermedades del sistema circulatorio', 'I', true, true),
('I50', 'Insuficiencia cardíaca', 'Enfermedades del sistema circulatorio', 'I', true, true),

-- Endocrine (Chapter E)
('E11', 'Diabetes mellitus no insulinodependiente', 'Enfermedades endocrinas, nutricionales y metabólicas', 'E', true, true),
('E11.9', 'Diabetes mellitus no insulinodependiente, sin mención de complicación', 'Enfermedades endocrinas', 'E', true, true),
('E10', 'Diabetes mellitus insulinodependiente', 'Enfermedades endocrinas', 'E', true, true),
('E03', 'Otro hipotiroidismo', 'Enfermedades endocrinas', 'E', true, true),
('E66', 'Obesidad', 'Enfermedades endocrinas', 'E', true, true),

-- Respiratory (Chapter J)
('J44', 'Otra enfermedad pulmonar obstructiva crónica', 'Enfermedades del sistema respiratorio', 'J', true, true),
('J45', 'Asma', 'Enfermedades del sistema respiratorio', 'J', true, true),

-- Genitourinary (Chapter N)
('N18', 'Enfermedad renal crónica', 'Enfermedades del sistema genitourinario', 'N', true, true),

-- Pregnancy (Chapter O - Female specific)
('O00-O99', 'Embarazo, parto y puerperio', 'Embarazo, parto y puerperio', 'O', false, true)
ON CONFLICT (code) DO NOTHING;

-- =========================================================
-- 7. Insert sample CUPS codes (common procedures)
-- =========================================================

INSERT INTO cups_catalog (code, description, procedure_type, complexity_level, ambulatory, is_active) VALUES
-- Consultation codes
('890201', 'Consulta de primera vez por medicina general', 'Diagnóstico', 'Baja', true, true),
('890202', 'Consulta de primera vez por medicina especializada', 'Diagnóstico', 'Media', true, true),
('890203', 'Consulta de control por medicina general', 'Diagnóstico', 'Baja', true, true),
('890204', 'Consulta de control por medicina especializada', 'Diagnóstico', 'Media', true, true),

-- Laboratory codes
('902210', 'Hemoglobina glicosilada (HbA1c)', 'Diagnóstico', 'Baja', true, true),
('902216', 'Colesterol total', 'Diagnóstico', 'Baja', true, true),
('902217', 'Colesterol HDL', 'Diagnóstico', 'Baja', true, true),
('902218', 'Colesterol LDL', 'Diagnóstico', 'Baja', true, true),
('902252', 'Creatinina', 'Diagnóstico', 'Baja', true, true),
('902215', 'Glicemia en ayunas', 'Diagnóstico', 'Baja', true, true),

-- Imaging
('870101', 'Toma de presión arterial', 'Diagnóstico', 'Baja', true, true),
('890301', 'Control prenatal', 'Preventivo', 'Media', true, true),
('890401', 'Citología cervicovaginal', 'Preventivo', 'Baja', true, true),
('890601', 'Mamografía bilateral', 'Preventivo', 'Media', true, true)
ON CONFLICT (code) DO NOTHING;

COMMIT;
