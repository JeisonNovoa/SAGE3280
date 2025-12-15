-- Migration: Add new patient fields for enhanced Excel import
-- Date: 2025-12-14
-- Description: Adds new fields to patients table to support updated Excel format
--   - Adds tipo_convenio field for agreement type
--   - Adds specific control date fields (general, 3280, HTA, DM)

-- =========================================================
-- 1. Add new fields to patients table
-- =========================================================

ALTER TABLE patients
ADD COLUMN IF NOT EXISTS neighborhood VARCHAR(100),
ADD COLUMN IF NOT EXISTS tipo_convenio VARCHAR(100),
ADD COLUMN IF NOT EXISTS last_general_control_date DATE,
ADD COLUMN IF NOT EXISTS last_3280_control_date DATE,
ADD COLUMN IF NOT EXISTS last_hta_control_date DATE,
ADD COLUMN IF NOT EXISTS last_dm_control_date DATE;

-- =========================================================
-- 2. Comments for documentation
-- =========================================================

COMMENT ON COLUMN patients.neighborhood IS 'Barrio / Vereda del paciente';
COMMENT ON COLUMN patients.tipo_convenio IS 'Tipo de convenio (agreement type) for the patient';
COMMENT ON COLUMN patients.last_general_control_date IS 'Fecha del último control general';
COMMENT ON COLUMN patients.last_3280_control_date IS 'Fecha del último control según Resolución 3280';
COMMENT ON COLUMN patients.last_hta_control_date IS 'Fecha del último control de hipertensión arterial (HTA)';
COMMENT ON COLUMN patients.last_dm_control_date IS 'Fecha del último control de diabetes mellitus (DM)';

-- =========================================================
-- 3. Verification queries (optional - comment out for production)
-- =========================================================

-- Verify columns exist
-- SELECT column_name, data_type FROM information_schema.columns
-- WHERE table_name = 'patients'
-- AND column_name IN ('neighborhood', 'tipo_convenio', 'last_general_control_date', 'last_3280_control_date', 'last_hta_control_date', 'last_dm_control_date');

COMMIT;
