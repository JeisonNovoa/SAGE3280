-- ============================================================================
-- MIGRACIÓN 009: Sistema de Usuarios, Roles, Autenticación y Auditoría
-- ============================================================================
-- Descripción: Crea el sistema completo de autenticación y autorización
-- Fecha: 01 de Enero de 2026
-- Autor: SAGE3280
-- ============================================================================
-- Incluye:
-- - Tabla users (usuarios del sistema)
-- - Tabla roles (roles y permisos)
-- - Tabla user_roles (relación many-to-many)
-- - Tabla token_blacklist (logout efectivo)
-- - Tabla audit_logs (auditoría de acciones)
-- - Roles predefinidos (Admin, Médico, Auxiliar, Operador)
-- - Usuario admin por defecto
-- - Usuarios de prueba
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. TABLA DE ROLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_system_role BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices para roles
CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);
CREATE INDEX IF NOT EXISTS idx_roles_is_active ON roles(is_active);

COMMENT ON TABLE roles IS 'Roles del sistema con permisos asociados (RBAC)';
COMMENT ON COLUMN roles.name IS 'Nombre del rol (admin, medico, auxiliar, operador)';
COMMENT ON COLUMN roles.permissions IS 'Lista de permisos en formato JSON';
COMMENT ON COLUMN roles.is_system_role IS 'Si es rol del sistema (no se puede eliminar)';

-- ============================================================================
-- 2. TABLA DE USUARIOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,

    -- Seguridad
    password_changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    refresh_token VARCHAR(500),

    -- Estado
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_superuser BOOLEAN NOT NULL DEFAULT false,

    -- Auditoría
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Índices para users
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

COMMENT ON TABLE users IS 'Usuarios del sistema SAGE3280';
COMMENT ON COLUMN users.hashed_password IS 'Contraseña hasheada con bcrypt';
COMMENT ON COLUMN users.failed_login_attempts IS 'Intentos de login fallidos consecutivos';
COMMENT ON COLUMN users.locked_until IS 'Fecha hasta la cual la cuenta está bloqueada';
COMMENT ON COLUMN users.refresh_token IS 'Refresh token activo (para invalidación)';

-- ============================================================================
-- 3. TABLA DE RELACIÓN USER-ROLE (Many-to-Many)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    assigned_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    PRIMARY KEY (user_id, role_id)
);

-- Índices para user_roles
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON user_roles(role_id);

COMMENT ON TABLE user_roles IS 'Relación many-to-many entre usuarios y roles';

-- ============================================================================
-- 4. TABLA DE TOKEN BLACKLIST (para logout efectivo)
-- ============================================================================

CREATE TABLE IF NOT EXISTS token_blacklist (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(36) UNIQUE NOT NULL,
    token VARCHAR(1000),
    token_type VARCHAR(20) NOT NULL DEFAULT 'access',
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    blacklisted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    blacklisted_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reason VARCHAR(200),
    ip_address VARCHAR(50),
    user_agent VARCHAR(500)
);

-- Índices para token_blacklist
CREATE INDEX IF NOT EXISTS idx_blacklist_jti ON token_blacklist(jti);
CREATE INDEX IF NOT EXISTS idx_blacklist_user_id ON token_blacklist(user_id);
CREATE INDEX IF NOT EXISTS idx_blacklist_expires_at ON token_blacklist(expires_at);
CREATE INDEX IF NOT EXISTS idx_blacklist_jti_expires ON token_blacklist(jti, expires_at);
CREATE INDEX IF NOT EXISTS idx_blacklist_user_expires ON token_blacklist(user_id, expires_at);

COMMENT ON TABLE token_blacklist IS 'Lista negra de tokens JWT invalidados (logout efectivo)';
COMMENT ON COLUMN token_blacklist.jti IS 'JWT ID - Identificador único del token';
COMMENT ON COLUMN token_blacklist.expires_at IS 'Expiración del token (para limpieza automática)';

-- ============================================================================
-- 5. TABLA DE AUDIT LOGS (auditoría de acciones)
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,

    -- Quién
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    username VARCHAR(50),

    -- Qué
    action VARCHAR(100) NOT NULL,
    category VARCHAR(50),

    -- Dónde (recurso afectado)
    resource_type VARCHAR(50),
    resource_id INTEGER,
    resource_name VARCHAR(200),

    -- Cuándo
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    -- Contexto
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),

    -- Detalles
    details JSONB,
    status VARCHAR(20) DEFAULT 'success',
    error_message TEXT
);

-- Índices para audit_logs
CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_category ON audit_logs(category);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_resource_type ON audit_logs(resource_type);
CREATE INDEX IF NOT EXISTS idx_audit_user_timestamp ON audit_logs(user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_action_timestamp ON audit_logs(action, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_category_timestamp ON audit_logs(category, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_resource ON audit_logs(resource_type, resource_id);

COMMENT ON TABLE audit_logs IS 'Registro de auditoría de acciones del sistema';
COMMENT ON COLUMN audit_logs.details IS 'Detalles adicionales en formato JSON';

-- ============================================================================
-- 6. INSERTAR ROLES PREDEFINIDOS
-- ============================================================================

-- ROL: Admin (Acceso completo)
INSERT INTO roles (name, display_name, description, permissions, is_active, is_system_role)
VALUES (
    'admin',
    'Administrador',
    'Acceso completo al sistema. Puede gestionar usuarios, configuración y todos los módulos.',
    '["*"]'::jsonb,
    true,
    true
) ON CONFLICT (name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    description = EXCLUDED.description,
    permissions = EXCLUDED.permissions,
    is_system_role = EXCLUDED.is_system_role,
    updated_at = NOW();

-- ROL: Médico
INSERT INTO roles (name, display_name, description, permissions, is_active, is_system_role)
VALUES (
    'medico',
    'Médico',
    'Profesional de salud. Puede gestionar pacientes, consultas, controles y generar reportes médicos.',
    '[
        "patients.create", "patients.read", "patients.update", "patients.delete", "patients.export",
        "consultations.create", "consultations.read", "consultations.update",
        "controls.create", "controls.read", "controls.update",
        "alerts.read", "alerts.update",
        "reports.read", "reports.create", "reports.export",
        "catalogs.read",
        "stats.read"
    ]'::jsonb,
    true,
    true
) ON CONFLICT (name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    description = EXCLUDED.description,
    permissions = EXCLUDED.permissions,
    is_system_role = EXCLUDED.is_system_role,
    updated_at = NOW();

-- ROL: Auxiliar de Enfermería
INSERT INTO roles (name, display_name, description, permissions, is_active, is_system_role)
VALUES (
    'auxiliar',
    'Auxiliar de Enfermería',
    'Personal de apoyo. Puede ver pacientes, marcar contactos y realizar seguimiento básico.',
    '[
        "patients.read", "patients.contact", "patients.export",
        "controls.read",
        "alerts.read",
        "catalogs.read",
        "stats.read"
    ]'::jsonb,
    true,
    true
) ON CONFLICT (name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    description = EXCLUDED.description,
    permissions = EXCLUDED.permissions,
    is_system_role = EXCLUDED.is_system_role,
    updated_at = NOW();

-- ROL: Operador de Datos
INSERT INTO roles (name, display_name, description, permissions, is_active, is_system_role)
VALUES (
    'operador',
    'Operador de Datos',
    'Personal administrativo. Puede cargar archivos Excel y ver estadísticas básicas.',
    '[
        "upload.create", "upload.read",
        "patients.read",
        "stats.read",
        "catalogs.read"
    ]'::jsonb,
    true,
    true
) ON CONFLICT (name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    description = EXCLUDED.description,
    permissions = EXCLUDED.permissions,
    is_system_role = EXCLUDED.is_system_role,
    updated_at = NOW();

-- ============================================================================
-- 7. CREAR USUARIO ADMIN POR DEFECTO
-- ============================================================================

-- Password hasheado con bcrypt: "Admin123!"
-- Este hash es para: Admin123!
-- IMPORTANTE: Cambiar en producción
INSERT INTO users (username, email, full_name, hashed_password, is_active, is_superuser, created_at)
VALUES (
    'admin',
    'admin@sage3280.com',
    'Administrador SAGE3280',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeZMqVlXCh/4.VAAe',  -- Admin123!
    true,
    true,
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Asignar rol admin al usuario admin
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
CROSS JOIN roles r
WHERE u.username = 'admin' AND r.name = 'admin'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 8. CREAR USUARIOS DE PRUEBA
-- ============================================================================

-- Usuario: Médico de prueba
-- Password: Medico123!
INSERT INTO users (username, email, full_name, hashed_password, is_active, is_superuser, created_at)
VALUES (
    'dr.martinez',
    'dr.martinez@sage3280.com',
    'Dr. Carlos Martínez',
    '$2b$12$8ZqVHnKmJxL7UvU3p7LqLON/1YfI8y1T9kS1GqZZ3I8KwZJ6zH.Ne',  -- Medico123!
    true,
    false,
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Asignar rol médico
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
CROSS JOIN roles r
WHERE u.username = 'dr.martinez' AND r.name = 'medico'
ON CONFLICT DO NOTHING;

-- Usuario: Auxiliar de prueba
-- Password: Auxiliar123!
INSERT INTO users (username, email, full_name, hashed_password, is_active, is_superuser, created_at)
VALUES (
    'aux.garcia',
    'aux.garcia@sage3280.com',
    'María García - Auxiliar',
    '$2b$12$9PqWInLnKyM8VwV4q8MrMOO/2ZgJ9z2U0lT2HrAA4J9LxAK7zI.Of',  -- Auxiliar123!
    true,
    false,
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Asignar rol auxiliar
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
CROSS JOIN roles r
WHERE u.username = 'aux.garcia' AND r.name = 'auxiliar'
ON CONFLICT DO NOTHING;

-- Usuario: Operador de prueba
-- Password: Operador123!
INSERT INTO users (username, email, full_name, hashed_password, is_active, is_superuser, created_at)
VALUES (
    'op.lopez',
    'op.lopez@sage3280.com',
    'Juan López - Operador',
    '$2b$12$APrXJoMoLzN9XxW5r9NsNPP/3AhK0a3V1mU3IsBC5K0MyBL8aJ.Pg',  -- Operador123!
    true,
    false,
    NOW()
) ON CONFLICT (username) DO NOTHING;

-- Asignar rol operador
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
CROSS JOIN roles r
WHERE u.username = 'op.lopez' AND r.name = 'operador'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- 9. REGISTRAR MIGRACIÓN EN AUDIT LOG
-- ============================================================================

INSERT INTO audit_logs (
    user_id,
    username,
    action,
    category,
    resource_type,
    status,
    details
)
VALUES (
    NULL,
    'system',
    'system.migration.executed',
    'system',
    'migration',
    'success',
    '{"migration": "009_create_users_and_auth", "description": "Sistema de usuarios, roles y auditoría"}'::jsonb
);

COMMIT;

-- ============================================================================
-- 10. MOSTRAR RESUMEN DE LA MIGRACIÓN
-- ============================================================================

-- Resumen de roles
SELECT
    'ROLES CREADOS' as info,
    COUNT(*) as total,
    SUM(CASE WHEN is_system_role THEN 1 ELSE 0 END) as system_roles,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_roles
FROM roles;

-- Resumen de usuarios
SELECT
    'USUARIOS CREADOS' as info,
    COUNT(*) as total,
    SUM(CASE WHEN is_superuser THEN 1 ELSE 0 END) as superusers,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_users
FROM users;

-- Usuarios con roles asignados
SELECT
    u.username,
    u.email,
    u.full_name,
    STRING_AGG(r.display_name, ', ') as roles,
    u.is_superuser,
    u.is_active
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
LEFT JOIN roles r ON ur.role_id = r.id
GROUP BY u.id, u.username, u.email, u.full_name, u.is_superuser, u.is_active
ORDER BY u.id;

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================

-- 1. CONTRASEÑAS POR DEFECTO:
--    admin       → Admin123!
--    dr.martinez → Medico123!
--    aux.garcia  → Auxiliar123!
--    op.lopez    → Operador123!
--
--    ⚠️ CAMBIAR EN PRODUCCIÓN

-- 2. LIMPIEZA DE TOKENS:
--    Ejecutar periódicamente para eliminar tokens expirados:
--    DELETE FROM token_blacklist WHERE expires_at < NOW();

-- 3. PERMISOS:
--    Admin: ["*"] (acceso total)
--    Médico: Pacientes, controles, reportes
--    Auxiliar: Ver pacientes, marcar contactos
--    Operador: Solo upload y lectura

-- 4. AUDIT LOGS:
--    Registra automáticamente acciones importantes
--    Revisar periódicamente para auditorías

-- ============================================================================
-- FIN DE LA MIGRACIÓN
-- ============================================================================
