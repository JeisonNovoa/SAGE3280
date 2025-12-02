-- Migration: Add Exam model and new fields to Control model
-- Date: 2025-12-01
-- Description: Implements Point 4 and Point 5 improvements
--   - Adds exams table to track patient exam history
--   - Adds recommended_frequency_days and description fields to controls table

-- =========================================================
-- 1. Create exams table
-- =========================================================

CREATE TABLE IF NOT EXISTS exams (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,

    -- Exam info
    exam_type VARCHAR(100) NOT NULL,
    exam_name VARCHAR(200) NOT NULL,

    -- Dates
    exam_date DATE NOT NULL,
    ordered_date DATE,
    result_date DATE,

    -- Result
    result_status VARCHAR(50) DEFAULT 'pendiente_resultado',
    result_value VARCHAR(200),
    result_numeric FLOAT,
    result_notes TEXT,

    -- Provider info
    provider VARCHAR(200),
    ordered_by VARCHAR(200),

    -- Follow-up
    requires_followup VARCHAR(10),
    followup_notes TEXT,

    -- Integration
    alert_id INTEGER REFERENCES alerts(id) ON DELETE SET NULL,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(200)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_exams_patient_id ON exams(patient_id);
CREATE INDEX IF NOT EXISTS idx_exams_exam_type ON exams(exam_type);
CREATE INDEX IF NOT EXISTS idx_exams_exam_date ON exams(exam_date);

-- =========================================================
-- 2. Add new fields to controls table
-- =========================================================

ALTER TABLE controls
ADD COLUMN IF NOT EXISTS recommended_frequency_days INTEGER,
ADD COLUMN IF NOT EXISTS description VARCHAR(500);

-- =========================================================
-- 3. Comments for documentation
-- =========================================================

COMMENT ON TABLE exams IS 'Stores patient exam history to track completed screenings and prevent duplicate alerts';
COMMENT ON COLUMN exams.recommended_frequency_days IS 'Frequency in days for this type of control per Resolución 3280/412';
COMMENT ON COLUMN controls.description IS 'Description of the control according to RIAS guidelines';
COMMENT ON COLUMN controls.recommended_frequency_days IS 'Recommended frequency in days per Resolución 3280/412';

-- =========================================================
-- 4. Update trigger for updated_at
-- =========================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_exams_updated_at ON exams;
CREATE TRIGGER update_exams_updated_at
    BEFORE UPDATE ON exams
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =========================================================
-- 5. Verification queries (optional - comment out for production)
-- =========================================================

-- Verify tables exist
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('exams', 'controls');

-- Verify columns exist
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'controls' AND column_name IN ('recommended_frequency_days', 'description');

-- Verify indexes exist
-- SELECT indexname FROM pg_indexes WHERE tablename = 'exams';

COMMIT;
