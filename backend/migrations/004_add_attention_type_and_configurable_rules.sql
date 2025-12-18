-- Migration: Add Attention Type and Configurable Rules
-- Date: 2025-12-15
-- Description: Implements Grupo C classification and configurable rules system
--   - Adds attention_type field to patients (Grupo A/B/C)
--   - Creates control_rules table for configurable control generation
--   - Creates alert_rules table for configurable alert generation
--   - Creates rias_guidelines table for official RIAS documentation

-- =========================================================
-- 1. Add attention_type to patients table (Grupo A/B/C)
-- =========================================================

-- Create enum type for attention_type
DO $$ BEGIN
    CREATE TYPE attention_type_enum AS ENUM ('grupo_a', 'grupo_b', 'grupo_c');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Add attention_type column
ALTER TABLE patients
ADD COLUMN IF NOT EXISTS attention_type attention_type_enum;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_patients_attention_type ON patients(attention_type);

-- Add comment
COMMENT ON COLUMN patients.attention_type IS 'Tipo de atención: grupo_a (RIAS preventivo), grupo_b (crónico), grupo_c (consulta externa general)';

-- =========================================================
-- 2. Create control_rules table
-- =========================================================

CREATE TABLE IF NOT EXISTS control_rules (
    id SERIAL PRIMARY KEY,

    -- Identificación
    rule_code VARCHAR(100) NOT NULL UNIQUE,
    rule_name VARCHAR(200) NOT NULL,
    description TEXT,

    -- Control configuration
    control_type VARCHAR(100) NOT NULL,
    criteria JSONB NOT NULL,  -- Criterios de aplicación

    -- Frecuencia y urgencia
    frequency_days INTEGER,
    is_urgent_if_overdue BOOLEAN DEFAULT TRUE,
    overdue_threshold_days INTEGER,

    -- Prioridad
    priority INTEGER DEFAULT 50,  -- 0-100

    -- RIAS information
    rias_stage VARCHAR(50),
    rias_description TEXT,
    normative_reference VARCHAR(200),

    -- Estado
    is_active BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(200),
    updated_by VARCHAR(200),
    notes TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_control_rules_code ON control_rules(rule_code);
CREATE INDEX IF NOT EXISTS idx_control_rules_type ON control_rules(control_type);
CREATE INDEX IF NOT EXISTS idx_control_rules_active ON control_rules(is_active);
CREATE INDEX IF NOT EXISTS idx_control_rules_rias_stage ON control_rules(rias_stage);
CREATE INDEX IF NOT EXISTS idx_control_rules_criteria ON control_rules USING GIN (criteria);

-- Add comments
COMMENT ON TABLE control_rules IS 'Reglas configurables para generación de controles médicos';
COMMENT ON COLUMN control_rules.rule_code IS 'Código único identificador de la regla (e.g., CONTROL_HTA_MENSUAL)';
COMMENT ON COLUMN control_rules.criteria IS 'Criterios de aplicación en formato JSON (edad, sexo, condiciones, etc.)';
COMMENT ON COLUMN control_rules.frequency_days IS 'Frecuencia recomendada del control en días';
COMMENT ON COLUMN control_rules.rias_description IS 'Descripción oficial según RIAS';

-- =========================================================
-- 3. Create alert_rules table
-- =========================================================

CREATE TABLE IF NOT EXISTS alert_rules (
    id SERIAL PRIMARY KEY,

    -- Identificación
    rule_code VARCHAR(100) NOT NULL UNIQUE,
    rule_name VARCHAR(200) NOT NULL,
    description TEXT,

    -- Alert configuration
    alert_type VARCHAR(100) NOT NULL,
    criteria JSONB NOT NULL,  -- Criterios de aplicación

    -- Frecuencia y periodicidad
    frequency_days INTEGER,
    due_date_calculation VARCHAR(50) DEFAULT 'frequency',

    -- Prioridad
    priority VARCHAR(20) NOT NULL,  -- AlertPriorityEnum
    priority_score INTEGER DEFAULT 50,  -- 0-100

    -- Umbrales (si aplica)
    threshold_config JSONB,

    -- Mensaje
    reason_template TEXT,

    -- Información normativa
    normative_reference VARCHAR(200),
    clinical_guidelines TEXT,

    -- Estado
    is_active BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(200),
    updated_by VARCHAR(200),
    notes TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_alert_rules_code ON alert_rules(rule_code);
CREATE INDEX IF NOT EXISTS idx_alert_rules_type ON alert_rules(alert_type);
CREATE INDEX IF NOT EXISTS idx_alert_rules_active ON alert_rules(is_active);
CREATE INDEX IF NOT EXISTS idx_alert_rules_priority ON alert_rules(priority);
CREATE INDEX IF NOT EXISTS idx_alert_rules_criteria ON alert_rules USING GIN (criteria);

-- Add comments
COMMENT ON TABLE alert_rules IS 'Reglas configurables para generación de alertas médicas';
COMMENT ON COLUMN alert_rules.rule_code IS 'Código único identificador de la regla (e.g., ALERT_HBA1C_DIABETES)';
COMMENT ON COLUMN alert_rules.criteria IS 'Criterios de aplicación en formato JSON (edad, sexo, condiciones, etc.)';
COMMENT ON COLUMN alert_rules.threshold_config IS 'Umbrales para alertas basadas en valores de laboratorio';
COMMENT ON COLUMN alert_rules.reason_template IS 'Plantilla del mensaje de la alerta';

-- =========================================================
-- 4. Create rias_guidelines table
-- =========================================================

CREATE TABLE IF NOT EXISTS rias_guidelines (
    id SERIAL PRIMARY KEY,

    -- Identificación
    guideline_code VARCHAR(100) NOT NULL UNIQUE,
    guideline_name VARCHAR(200) NOT NULL,

    -- Etapa del curso de vida
    life_stage VARCHAR(50) NOT NULL,

    -- Descripción oficial
    official_description TEXT NOT NULL,
    objectives TEXT,

    -- Parámetros de edad
    age_min INTEGER,
    age_max INTEGER,

    -- Actividades recomendadas
    recommended_controls JSONB,
    screening_activities JSONB,

    -- Referencias normativas
    normative_reference VARCHAR(300) NOT NULL,
    additional_references TEXT,

    -- Notas clínicas
    clinical_notes TEXT,
    special_considerations TEXT,

    -- Estado
    is_active BOOLEAN DEFAULT TRUE,
    version VARCHAR(20) DEFAULT '1.0',

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(200),
    updated_by VARCHAR(200)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_rias_guidelines_code ON rias_guidelines(guideline_code);
CREATE INDEX IF NOT EXISTS idx_rias_guidelines_stage ON rias_guidelines(life_stage);
CREATE INDEX IF NOT EXISTS idx_rias_guidelines_active ON rias_guidelines(is_active);

-- Add comments
COMMENT ON TABLE rias_guidelines IS 'Guías oficiales RIAS (Rutas Integrales de Atención en Salud) según Resolución 3280 de 2018';
COMMENT ON COLUMN rias_guidelines.life_stage IS 'Etapa del curso de vida (primera_infancia, infancia, adolescencia, juventud, adultez, vejez)';
COMMENT ON COLUMN rias_guidelines.official_description IS 'Descripción oficial de la atención en esta etapa según normativa';
COMMENT ON COLUMN rias_guidelines.recommended_controls IS 'Controles y actividades recomendadas en formato JSON estructurado';

-- =========================================================
-- 5. Create update triggers
-- =========================================================

-- Trigger for control_rules
DROP TRIGGER IF EXISTS update_control_rules_updated_at ON control_rules;
CREATE TRIGGER update_control_rules_updated_at
    BEFORE UPDATE ON control_rules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for alert_rules
DROP TRIGGER IF EXISTS update_alert_rules_updated_at ON alert_rules;
CREATE TRIGGER update_alert_rules_updated_at
    BEFORE UPDATE ON alert_rules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for rias_guidelines
DROP TRIGGER IF EXISTS update_rias_guidelines_updated_at ON rias_guidelines;
CREATE TRIGGER update_rias_guidelines_updated_at
    BEFORE UPDATE ON rias_guidelines
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMIT;
