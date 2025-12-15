-- Migration: Complete Grupo A (RIAS) and Grupo B (Chronic Conditions) Implementation
-- Date: 2025-12-15
-- Description: Adds all new fields for complete RIAS implementation and chronic conditions tracking
--   - New chronic conditions (hypothyroidism, COPD, asthma, CKD, cardiovascular disease)
--   - Clinical indicators (BP, glucose, HbA1c, lipid profile, etc.)
--   - Disease stratification fields
--   - Medications table for complete medication tracking

-- =========================================================
-- 1. Add new chronic condition fields to patients table
-- =========================================================

ALTER TABLE patients
ADD COLUMN IF NOT EXISTS has_hypothyroidism BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_copd BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_asthma BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_ckd BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_cardiovascular_disease BOOLEAN DEFAULT FALSE;

-- =========================================================
-- 2. Add disease stratification fields
-- =========================================================

ALTER TABLE patients
ADD COLUMN IF NOT EXISTS hypertension_stage VARCHAR(20),
ADD COLUMN IF NOT EXISTS diabetes_complications BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS metabolic_control VARCHAR(20);

-- =========================================================
-- 3. Add clinical indicators (last measured values)
-- =========================================================

ALTER TABLE patients
ADD COLUMN IF NOT EXISTS last_systolic_bp INTEGER,
ADD COLUMN IF NOT EXISTS last_diastolic_bp INTEGER,
ADD COLUMN IF NOT EXISTS last_bp_date DATE,
ADD COLUMN IF NOT EXISTS last_glucose FLOAT,
ADD COLUMN IF NOT EXISTS last_glucose_date DATE,
ADD COLUMN IF NOT EXISTS last_hba1c FLOAT,
ADD COLUMN IF NOT EXISTS last_hba1c_date DATE,
ADD COLUMN IF NOT EXISTS last_cholesterol FLOAT,
ADD COLUMN IF NOT EXISTS last_hdl FLOAT,
ADD COLUMN IF NOT EXISTS last_ldl FLOAT,
ADD COLUMN IF NOT EXISTS last_lipid_profile_date DATE,
ADD COLUMN IF NOT EXISTS last_creatinine FLOAT,
ADD COLUMN IF NOT EXISTS last_creatinine_date DATE,
ADD COLUMN IF NOT EXISTS is_smoker BOOLEAN DEFAULT FALSE;

-- =========================================================
-- 4. Create medications table
-- =========================================================

CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,

    -- Medication info
    medication_name VARCHAR(200) NOT NULL,
    generic_name VARCHAR(200),
    presentation VARCHAR(100),  -- Tableta, jarabe, inyección, etc.
    concentration VARCHAR(50),  -- 500mg, 10mg/ml, etc.

    -- Dosage
    dose VARCHAR(100) NOT NULL,  -- 1 tableta, 5ml, etc.
    frequency VARCHAR(100) NOT NULL,  -- Cada 8 horas, 2 veces al día, etc.
    route VARCHAR(50),  -- Oral, IV, IM, etc.

    -- Indication
    indication VARCHAR(200),  -- Para qué se prescribió
    prescriber VARCHAR(200),  -- Médico que prescribió

    -- Dates
    start_date DATE NOT NULL,
    end_date DATE,  -- Null si es tratamiento indefinido
    last_refill_date DATE,  -- Última vez que renovó
    next_refill_date DATE,  -- Próxima renovación programada

    -- Status
    status VARCHAR(20) DEFAULT 'activo',  -- activo, suspendido, completado
    adherence VARCHAR(20) DEFAULT 'no_evaluado',  -- buena, regular, mala, no_evaluado

    -- Refill info
    refill_frequency_days INTEGER,  -- Cada cuántos días debe renovar
    requires_refill_alert BOOLEAN DEFAULT TRUE,  -- Si se debe alertar cuando necesite renovar

    -- Notes
    notes TEXT,
    side_effects TEXT,  -- Efectos secundarios reportados

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(200)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_medications_patient_id ON medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_medications_status ON medications(status);
CREATE INDEX IF NOT EXISTS idx_medications_next_refill_date ON medications(next_refill_date);

-- =========================================================
-- 5. Update trigger for medications updated_at
-- =========================================================

DROP TRIGGER IF EXISTS update_medications_updated_at ON medications;
CREATE TRIGGER update_medications_updated_at
    BEFORE UPDATE ON medications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =========================================================
-- 6. Comments for documentation
-- =========================================================

-- New chronic conditions
COMMENT ON COLUMN patients.has_hypothyroidism IS 'Paciente con hipotiroidismo';
COMMENT ON COLUMN patients.has_copd IS 'Paciente con EPOC (Enfermedad Pulmonar Obstructiva Crónica)';
COMMENT ON COLUMN patients.has_asthma IS 'Paciente con asma';
COMMENT ON COLUMN patients.has_ckd IS 'Paciente con IRC (Insuficiencia Renal Crónica)';
COMMENT ON COLUMN patients.has_cardiovascular_disease IS 'Paciente con enfermedad cardiovascular establecida (IAM, ICC, ECV)';

-- Disease stratification
COMMENT ON COLUMN patients.hypertension_stage IS 'Estadio de hipertensión (I, II, III)';
COMMENT ON COLUMN patients.diabetes_complications IS 'Diabetes con complicaciones (retinopatía, nefropatía, neuropatía)';
COMMENT ON COLUMN patients.metabolic_control IS 'Control metabólico del paciente (controlado, no_controlado)';

-- Clinical indicators
COMMENT ON COLUMN patients.last_systolic_bp IS 'Última presión arterial sistólica (PAS) en mmHg';
COMMENT ON COLUMN patients.last_diastolic_bp IS 'Última presión arterial diastólica (PAD) en mmHg';
COMMENT ON COLUMN patients.last_bp_date IS 'Fecha de última toma de presión arterial';
COMMENT ON COLUMN patients.last_glucose IS 'Última glicemia en ayunas en mg/dL';
COMMENT ON COLUMN patients.last_glucose_date IS 'Fecha de última glicemia';
COMMENT ON COLUMN patients.last_hba1c IS 'Última HbA1c en %';
COMMENT ON COLUMN patients.last_hba1c_date IS 'Fecha de última HbA1c';
COMMENT ON COLUMN patients.last_cholesterol IS 'Último colesterol total en mg/dL';
COMMENT ON COLUMN patients.last_hdl IS 'Último HDL en mg/dL';
COMMENT ON COLUMN patients.last_ldl IS 'Último LDL en mg/dL';
COMMENT ON COLUMN patients.last_lipid_profile_date IS 'Fecha de último perfil lipídico';
COMMENT ON COLUMN patients.last_creatinine IS 'Última creatinina en mg/dL';
COMMENT ON COLUMN patients.last_creatinine_date IS 'Fecha de última creatinina';
COMMENT ON COLUMN patients.is_smoker IS 'Paciente fumador activo';

-- Medications table
COMMENT ON TABLE medications IS 'Registro de medicamentos activos y pasados del paciente';
COMMENT ON COLUMN medications.medication_name IS 'Nombre comercial del medicamento';
COMMENT ON COLUMN medications.generic_name IS 'Nombre genérico (DCI)';
COMMENT ON COLUMN medications.presentation IS 'Forma farmacéutica (tableta, jarabe, inyectable)';
COMMENT ON COLUMN medications.concentration IS 'Concentración (500mg, 10mg/ml, etc.)';
COMMENT ON COLUMN medications.dose IS 'Dosis prescrita (1 tableta, 5ml, etc.)';
COMMENT ON COLUMN medications.frequency IS 'Frecuencia de administración (cada 8 horas, 2 veces al día)';
COMMENT ON COLUMN medications.route IS 'Vía de administración (oral, IV, IM, tópica)';
COMMENT ON COLUMN medications.indication IS 'Indicación o diagnóstico para el cual se prescribió';
COMMENT ON COLUMN medications.prescriber IS 'Médico que prescribió';
COMMENT ON COLUMN medications.start_date IS 'Fecha de inicio del tratamiento';
COMMENT ON COLUMN medications.end_date IS 'Fecha de fin del tratamiento (NULL si es indefinido)';
COMMENT ON COLUMN medications.last_refill_date IS 'Fecha de última renovación de la prescripción';
COMMENT ON COLUMN medications.next_refill_date IS 'Fecha programada para próxima renovación';
COMMENT ON COLUMN medications.status IS 'Estado del medicamento (activo, suspendido, completado)';
COMMENT ON COLUMN medications.adherence IS 'Nivel de adherencia (buena, regular, mala, no_evaluado)';
COMMENT ON COLUMN medications.refill_frequency_days IS 'Cada cuántos días debe renovar la prescripción';
COMMENT ON COLUMN medications.requires_refill_alert IS 'Si se debe generar alerta cuando necesite renovar';
COMMENT ON COLUMN medications.side_effects IS 'Efectos adversos reportados por el paciente';

COMMIT;
