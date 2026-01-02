-- ============================================================================
-- MIGRACIÓN 004: Poblar catálogo de EPS (Entidades Promotoras de Salud)
-- ============================================================================
-- Descripción: Inserta las 27 EPS oficiales autorizadas para operar en Colombia
-- Fuente: Ministerio de Salud y Protección Social - Junio 2025
-- Fecha: Diciembre 2025
-- Autor: SAGE3280
-- ============================================================================

-- Esta migración es IDEMPOTENTE: puede ejecutarse múltiples veces sin duplicar datos
-- Usa ON CONFLICT para actualizar registros existentes en lugar de fallar

BEGIN;

-- ============================================================================
-- RÉGIMEN CONTRIBUTIVO - EPS PRINCIPALES
-- ============================================================================

INSERT INTO eps_catalog (code, name, short_name, nit, regime_type, is_active, phone, email, website, coverage_nationwide, departments, notes, created_at, updated_at)
VALUES
    ('EPS002', 'SALUD TOTAL S.A. EPS', 'Salud Total', '800130907-4', 'contributivo', true, '01 8000 116 699', NULL, 'https://www.saludtotal.com.co', true, 'Nacional', 'Una de las EPS más grandes del país', NOW(), NOW()),
    ('EPS005', 'EPS SANITAS S.A.', 'Sanitas', '800251440-6', 'contributivo', true, '01 8000 123 414', 'servicioalcliente@colsanitas.com', 'https://www.colsanitas.com', true, 'Nacional', 'Parte del grupo Keralty (anteriormente Colsanitas)', NOW(), NOW()),
    ('EPS008', 'COMPENSAR ENTIDAD PROMOTORA DE SALUD', 'Compensar', '860066942-7', 'contributivo', true, '444 4234', 'epscompensarcajadecompensacionfamiliar@compensar.com', 'https://www.compensar.com', false, 'Bogotá D.C., Cundinamarca', 'EPS de Caja de Compensación Familiar Compensar', NOW(), NOW()),
    ('EPS010', 'EPS SURA', 'SURA', '800088702-2', 'contributivo', true, '01 8000 51 7872', 'servicioalcliente@eps.sura.com.co', 'https://www.epssura.com', true, 'Nacional', 'EPS del grupo SURA', NOW(), NOW()),
    ('EPS016', 'COOMEVA ENTIDAD PROMOTORA DE SALUD S.A.', 'Coomeva EPS', '805000427-1', 'contributivo', false, '01 8000 052 666', NULL, 'https://www.coomeva.com.co', true, 'Nacional', 'EN LIQUIDACIÓN - Proceso iniciado en 2024', NOW(), NOW()),
    ('EPS017', 'EPS FAMISANAR LTDA', 'Famisanar', '830003564-7', 'contributivo', true, '01 8000 426 600', 'servicioalcliente@famisanar.com.co', 'https://www.famisanar.com.co', true, 'Nacional', 'EPS cooperativa con amplia cobertura', NOW(), NOW()),
    ('EPS037', 'NUEVA EPS S.A.', 'Nueva EPS', '900156264-2', 'contributivo', true, '01 8000 113 110', 'servicioalcliente@nuevaeps.com.co', 'https://www.nuevaeps.com.co', true, 'Nacional', 'Estuvo bajo intervención administrativa hasta abril 2025. Ahora opera ambos regímenes (EPS037/EPSS41)', NOW(), NOW()),
    ('EPS001', 'ALIANSALUD EPS', 'Aliansalud', '830113831-0', 'contributivo', true, '01 8000 110 102', NULL, 'https://www.aliansalud.com.co', false, 'Cauca, Nariño, Valle del Cauca', 'EPS regional del sur occidente colombiano', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    short_name = EXCLUDED.short_name,
    nit = EXCLUDED.nit,
    regime_type = EXCLUDED.regime_type,
    is_active = EXCLUDED.is_active,
    phone = EXCLUDED.phone,
    email = EXCLUDED.email,
    website = EXCLUDED.website,
    coverage_nationwide = EXCLUDED.coverage_nationwide,
    departments = EXCLUDED.departments,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- RÉGIMEN CONTRIBUTIVO - EPS REGIONALES Y ESPECIALES
-- ============================================================================

INSERT INTO eps_catalog (code, name, short_name, nit, regime_type, is_active, phone, email, website, coverage_nationwide, departments, notes, created_at, updated_at)
VALUES
    ('EPS014', 'CAFESALUD ENTIDAD PROMOTORA DE SALUD S.A.', 'Cafesalud', '817000083-0', 'contributivo', false, NULL, NULL, NULL, true, 'Nacional', 'LIQUIDADA - Integrada a Nueva EPS en 2016', NOW(), NOW()),
    ('EPS025', 'SERVICIO OCCIDENTAL DE SALUD S.A.', 'SOS', '805024488-6', 'contributivo', true, '01 8000 117 717', NULL, 'https://www.sos.com.co', false, 'Valle del Cauca, Cauca, Nariño, Chocó', 'EPS regional del Valle del Cauca', NOW(), NOW()),
    ('EPS022', 'FUNDACIÓN SALUD MIA', 'Fundación Salud Mía', '830037939-0', 'contributivo', true, NULL, NULL, NULL, false, 'Antioquia, Valle del Cauca', 'EPS regional', NOW(), NOW()),
    ('EPS033', 'MALLAMAS ENTIDAD PROMOTORA DE SALUD S.A.S.', 'Mallamas', '900815725-8', 'contributivo', true, NULL, NULL, NULL, false, 'Nariño', 'EPS regional de Nariño', NOW(), NOW()),
    ('EPS023', 'CRUZ BLANCA ENTIDAD PROMOTORA DE SALUD S.A.', 'Cruz Blanca', '860011153-6', 'contributivo', true, '601 3077777', NULL, 'https://www.cruzblanca.com.co', false, 'Bogotá D.C., Cundinamarca', 'EPS regional de Bogotá y Cundinamarca', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    short_name = EXCLUDED.short_name,
    nit = EXCLUDED.nit,
    regime_type = EXCLUDED.regime_type,
    is_active = EXCLUDED.is_active,
    phone = EXCLUDED.phone,
    email = EXCLUDED.email,
    website = EXCLUDED.website,
    coverage_nationwide = EXCLUDED.coverage_nationwide,
    departments = EXCLUDED.departments,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- RÉGIMEN SUBSIDIADO - EPS PRINCIPALES
-- ============================================================================

INSERT INTO eps_catalog (code, name, short_name, nit, regime_type, is_active, phone, email, website, coverage_nationwide, departments, notes, created_at, updated_at)
VALUES
    ('ESS024', 'COOSALUD ENTIDAD PROMOTORA DE SALUD S.A.', 'Coosalud', '900226715-4', 'subsidiado', true, '01 8000 413 225', 'pqr@coosalud.com.co', 'https://www.coosalud.com.co', true, 'Nacional', 'Opera en ambos regímenes: ESS024 (subsidiado) y EPS042 (contributivo)', NOW(), NOW()),
    ('ESS207', 'ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD', 'Mutual Ser', '806008394-6', 'subsidiado', true, '01 8000 115 544', 'servicioalcliente@mutualser.com', 'https://www.mutualser.com', true, 'Nacional', 'Opera en ambos regímenes: ESS207 (subsidiado) y EPS048 (contributivo)', NOW(), NOW()),
    ('EPSS46', 'SALUD MIA EPS SAS', 'Salud Mía', '900914254-5', 'subsidiado', true, '01 8000 422 220', NULL, 'https://www.saludmia.com.co', false, 'Antioquia, Atlántico, Bogotá, Bolívar, Caldas, Cesar, Córdoba, Cundinamarca, La Guajira, Magdalena, Meta, Santander, Sucre, Valle del Cauca', 'Opera principalmente en régimen subsidiado, expandiendo a contributivo', NOW(), NOW()),
    ('EPSC34', 'CAPITAL SALUD ENTIDAD PROMOTORA DE SALUD DEL REGIMEN SUBSIDIADO S.A.S.', 'Capital Salud', '900298372-9', 'subsidiado', true, '601 3649666', 'info@capitalsalud.gov.co', 'https://www.capitalsalud.gov.co', false, 'Bogotá D.C., Cundinamarca (Soacha), Meta', 'EPS territorial de Bogotá para régimen subsidiado', NOW(), NOW()),
    ('ESS025', 'ASOCIACIÓN INDÍGENA DEL CAUCA', 'AIC', '817002683-1', 'subsidiado', true, NULL, NULL, NULL, false, 'Cauca', 'EPS indígena del Cauca - Régimen subsidiado', NOW(), NOW()),
    ('ESS033', 'ANAS WAYUU ENTIDAD PROMOTORA DE SALUD INDIGENA', 'Anas Wayuu', '824005387-6', 'subsidiado', true, NULL, NULL, NULL, false, 'La Guajira, Cesar', 'EPS indígena para comunidad Wayuu', NOW(), NOW()),
    ('ESS117', 'COMFACOR ENTIDAD PROMOTORA DE SALUD S.A.', 'Comfacor', '891480160-1', 'subsidiado', true, NULL, NULL, NULL, false, 'Córdoba', 'EPS regional de Córdoba', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    short_name = EXCLUDED.short_name,
    nit = EXCLUDED.nit,
    regime_type = EXCLUDED.regime_type,
    is_active = EXCLUDED.is_active,
    phone = EXCLUDED.phone,
    email = EXCLUDED.email,
    website = EXCLUDED.website,
    coverage_nationwide = EXCLUDED.coverage_nationwide,
    departments = EXCLUDED.departments,
    notes = EXCLUDED.notes,
    updated_at = NOW();

-- ============================================================================
-- REGÍMENES ESPECIALES
-- ============================================================================

INSERT INTO eps_catalog (code, name, short_name, nit, regime_type, is_active, phone, email, website, coverage_nationwide, departments, notes, created_at, updated_at)
VALUES
    ('ESE001', 'FONDO DE PASIVO SOCIAL DE FERROCARRILES NACIONALES DE COLOMBIA', 'Ferrocarriles', '800215381-9', 'especial', true, NULL, NULL, NULL, true, 'Nacional', 'Régimen especial para ex-empleados de Ferrocarriles Nacionales', NOW(), NOW()),
    ('ESE002', 'CAJA DE COMPENSACIÓN FAMILIAR CAJACOPI ATLÁNTICO', 'Cajacopi', '890102018-4', 'especial', true, NULL, NULL, NULL, false, 'Atlántico', 'Régimen especial - Caja de Compensación', NOW(), NOW()),
    ('ESEM01', 'DIRECCIÓN DE SANIDAD DEL EJÉRCITO NACIONAL', 'DISAN Ejército', '800197268-4', 'especial', true, NULL, NULL, NULL, true, 'Nacional', 'Régimen especial - Fuerzas Militares (Ejército Nacional)', NOW(), NOW()),
    ('ESEM02', 'DIRECCIÓN GENERAL DE SANIDAD DE LA POLICÍA NACIONAL', 'DISAN Policía', '899999026-6', 'especial', true, NULL, NULL, NULL, true, 'Nacional', 'Régimen especial - Policía Nacional', NOW(), NOW()),
    ('ESEM03', 'DIRECCIÓN GENERAL DE SANIDAD MILITAR', 'DISAN Militar', '899999115-7', 'especial', true, NULL, NULL, NULL, true, 'Nacional', 'Régimen especial - Fuerzas Militares', NOW(), NOW()),
    ('ESEE01', 'ECOPETROL S.A. - RÉGIMEN ESPECIAL DE SALUD', 'Ecopetrol Salud', '899999068-1', 'especial', true, NULL, NULL, NULL, true, 'Nacional', 'Régimen especial - Empleados de Ecopetrol', NOW(), NOW()),
    ('ESEMC', 'UNIVERSIDAD DEL VALLE - PLAN DE SALUD', 'Univalle Salud', '890399010-6', 'especial', true, NULL, NULL, NULL, false, 'Valle del Cauca', 'Régimen especial - Empleados Universidad del Valle', NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    short_name = EXCLUDED.short_name,
    nit = EXCLUDED.nit,
    regime_type = EXCLUDED.regime_type,
    is_active = EXCLUDED.is_active,
    phone = EXCLUDED.phone,
    email = EXCLUDED.email,
    website = EXCLUDED.website,
    coverage_nationwide = EXCLUDED.coverage_nationwide,
    departments = EXCLUDED.departments,
    notes = EXCLUDED.notes,
    updated_at = NOW();

COMMIT;

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================

-- Contar registros insertados
SELECT
    regime_type,
    COUNT(*) as total,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as activas,
    SUM(CASE WHEN NOT is_active THEN 1 ELSE 0 END) as inactivas
FROM eps_catalog
GROUP BY regime_type
ORDER BY regime_type;

-- Mostrar todas las EPS activas
SELECT code, short_name, regime_type, coverage_nationwide
FROM eps_catalog
WHERE is_active = true
ORDER BY regime_type, code;
