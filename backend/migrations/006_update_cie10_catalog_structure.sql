-- Migration: Update CIE-10 Catalog Structure
-- Date: 2025-12-31
-- Description: Updates cie10_catalog table structure to match new model requirements
--   - Adds short_description and full_description fields
--   - Adds hierarchical fields (is_subcategory, parent_code)
--   - Adds is_common flag for prioritization
--   - Migrates existing data

-- =========================================================
-- 1. Add new columns
-- =========================================================

-- Add short_description (required)
ALTER TABLE cie10_catalog 
ADD COLUMN IF NOT EXISTS short_description VARCHAR(200);

-- Add full_description (optional detailed description)
ALTER TABLE cie10_catalog 
ADD COLUMN IF NOT EXISTS full_description TEXT;

-- Add hierarchical fields
ALTER TABLE cie10_catalog 
ADD COLUMN IF NOT EXISTS is_subcategory BOOLEAN DEFAULT FALSE;

ALTER TABLE cie10_catalog 
ADD COLUMN IF NOT EXISTS parent_code VARCHAR(10);

-- Add common flag for prioritization
ALTER TABLE cie10_catalog 
ADD COLUMN IF NOT EXISTS is_common BOOLEAN DEFAULT FALSE;

-- =========================================================
-- 2. Migrate existing data
-- =========================================================

-- Copy description to short_description for existing records
UPDATE cie10_catalog 
SET short_description = description 
WHERE short_description IS NULL;

-- Copy description to full_description as well
UPDATE cie10_catalog 
SET full_description = description 
WHERE full_description IS NULL;

-- Mark existing codes as common (they were added as sample common codes)
UPDATE cie10_catalog 
SET is_common = TRUE 
WHERE is_chronic = TRUE;

-- Identify subcategories (codes with decimal point)
UPDATE cie10_catalog 
SET is_subcategory = TRUE 
WHERE code LIKE '%.%';

-- Set parent codes for subcategories
UPDATE cie10_catalog 
SET parent_code = SUBSTRING(code FROM 1 FOR POSITION('.' IN code) - 1)
WHERE is_subcategory = TRUE;

-- =========================================================
-- 3. Add indexes for new fields
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_cie10_short_description ON cie10_catalog(short_description);
CREATE INDEX IF NOT EXISTS idx_cie10_is_subcategory ON cie10_catalog(is_subcategory);
CREATE INDEX IF NOT EXISTS idx_cie10_parent_code ON cie10_catalog(parent_code);
CREATE INDEX IF NOT EXISTS idx_cie10_is_common ON cie10_catalog(is_common);

-- =========================================================
-- 4. Update constraints
-- =========================================================

-- Make short_description NOT NULL (after migration)
ALTER TABLE cie10_catalog 
ALTER COLUMN short_description SET NOT NULL;

-- =========================================================
-- 5. Add comments
-- =========================================================

COMMENT ON COLUMN cie10_catalog.short_description IS 'Descripción corta para visualización';
COMMENT ON COLUMN cie10_catalog.full_description IS 'Descripción completa y detallada';
COMMENT ON COLUMN cie10_catalog.is_subcategory IS 'TRUE si el código tiene punto decimal (ej: E11.9)';
COMMENT ON COLUMN cie10_catalog.parent_code IS 'Código padre si is_subcategory=TRUE (ej: E11 para E11.9)';
COMMENT ON COLUMN cie10_catalog.is_common IS 'TRUE si es código frecuente en atención primaria';

COMMIT;
