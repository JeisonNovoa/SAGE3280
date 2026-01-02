# PLAN DETALLADO: FASE B - FRONTEND DE AUTENTICACIÓN

**Proyecto**: SAGE3280
**Fecha**: 01 de Enero de 2026
**Objetivo**: Implementar sistema completo de autenticación en Frontend React
**Duración estimada**: 2-3 semanas
**Estado actual**: Backend 100% completo, Frontend 0%

---

## CONTEXTO

El backend de autenticación está 100% completado con:
- ✅ JWT (access + refresh tokens)
- ✅ 4 roles predefinidos (admin, medico, auxiliar, operador)
- ✅ 33 permisos granulares
- ✅ Sistema de auditoría completo
- ✅ 7 endpoints de autenticación
- ✅ 21 endpoints de gestión (usuarios, roles, auditoría)

**Frontend actual**:
- ❌ NO tiene sistema de autenticación
- ❌ Todas las rutas son públicas
- ❌ No hay página de login
- ❌ No hay gestión de tokens
- ❌ API no incluye headers de autenticación

**Stack del frontend**:
- React 18.2
- React Router DOM 6.20
- Axios 1.6.2
- Tailwind CSS 3.3.6
- Vite 5.0.8
- React Hot Toast (notificaciones)
- Lucide React (iconos)

---

## ARQUITECTURA PROPUESTA

```
frontend/src/
├── contexts/
│   └── AuthContext.jsx          [B.1] - Contexto global de autenticación
├── hooks/
│   └── useAuth.js               [B.1] - Hook personalizado para auth
├── services/
│   ├── api.js                   [B.2] - Actualizar con interceptors
│   ├── authService.js           [B.2] - Servicio de autenticación
│   ├── usersService.js          [B.4] - Servicio de usuarios
│   ├── rolesService.js          [B.5] - Servicio de roles
│   └── auditService.js          [B.6] - Servicio de auditoría
├── pages/
│   ├── Login.jsx                [B.3] - Página de login
│   ├── Users.jsx                [B.4] - Gestión de usuarios
│   ├── UserForm.jsx             [B.4] - Crear/Editar usuario
│   ├── Roles.jsx                [B.5] - Gestión de roles
│   ├── RoleForm.jsx             [B.5] - Crear/Editar rol
│   └── AuditLogs.jsx            [B.6] - Logs de auditoría
├── components/
│   ├── Layout.jsx               [B.3] - Actualizar con user info + logout
│   ├── ProtectedRoute.jsx       [B.3] - Componente para proteger rutas
│   ├── PermissionGuard.jsx      [B.3] - Guard por permisos
│   ├── UserMenu.jsx             [B.3] - Menú de usuario en header
│   └── AuditFilters.jsx         [B.6] - Filtros para auditoría
├── utils/
│   ├── tokenManager.js          [B.2] - Gestión de tokens en localStorage
│   └── permissions.js           [B.3] - Helpers de permisos
└── App.jsx                      [B.7] - Actualizar con rutas protegidas
```

---

## DESGLOSE POR SUBFASES

### 📦 SUBFASE B.1: Contexto de Autenticación y Estado Global
**Duración**: 1-2 días
**Objetivo**: Crear la base del sistema de autenticación en React

#### Archivos a crear:
1. **frontend/src/contexts/AuthContext.jsx** (~200 líneas)
   - Context para manejar estado global de autenticación
   - Estado: user, isAuthenticated, isLoading, tokens
   - Funciones: login, logout, refreshToken, updateUser
   - Persistencia en localStorage
   - Recuperación automática al recargar página

2. **frontend/src/hooks/useAuth.js** (~30 líneas)
   - Hook personalizado para consumir AuthContext
   - Validación de que el hook se use dentro del provider
   - Export: useAuth()

#### Funcionalidades:
- [x] AuthProvider envuelve toda la app
- [x] Estado global: user, tokens, isAuthenticated, isLoading
- [x] Función login(username, password) → llama API y guarda tokens
- [x] Función logout() → limpia tokens y redirige a login
- [x] Función refreshAccessToken() → renueva access token
- [x] Auto-refresh de tokens antes de expirar (timer)
- [x] Recuperación de sesión desde localStorage al iniciar
- [x] Manejo de errores 401/403

#### Validación:
```bash
# Test manual:
1. Crear AuthContext con estado mockado
2. Envolver App.jsx con AuthProvider
3. Usar useAuth() en un componente para mostrar estado
4. Verificar en React DevTools que el contexto funciona
```

---

### 📦 SUBFASE B.2: Servicios de API y Gestión de Tokens
**Duración**: 1-2 días
**Objetivo**: Conectar frontend con endpoints de autenticación del backend

#### Archivos a crear/modificar:

1. **frontend/src/utils/tokenManager.js** (~100 líneas)
   - Funciones para gestionar tokens en localStorage
   - `getAccessToken()`, `getRefreshToken()`
   - `setTokens(access, refresh)`, `clearTokens()`
   - `getUser()`, `setUser(user)`, `clearUser()`
   - Validación de expiración de tokens
   - Decodificación de JWT para extraer datos

2. **frontend/src/services/authService.js** (~150 líneas)
   - `login(username, password)` → POST /api/auth/login
   - `logout(accessToken, refreshToken)` → POST /api/auth/logout
   - `refreshToken(refreshToken)` → POST /api/auth/refresh
   - `getCurrentUser()` → GET /api/auth/me
   - `changePassword(currentPassword, newPassword)` → POST /api/auth/change-password
   - Manejo de errores específicos de auth

3. **frontend/src/services/api.js** - ACTUALIZAR (~250 líneas)
   - Agregar interceptor de REQUEST:
     * Inyectar `Authorization: Bearer {token}` en cada request
     * Obtener token desde tokenManager
   - Agregar interceptor de RESPONSE:
     * Detectar 401 (token expirado)
     * Intentar refresh automático
     * Si refresh falla → logout y redirect a login
     * Reintentar request original con nuevo token
   - Queue de requests durante refresh (evitar race conditions)

#### Funcionalidades:
- [x] Login envía credenciales y recibe tokens
- [x] Tokens se guardan en localStorage
- [x] Refresh automático cuando access token expira
- [x] Logout invalida tokens en backend
- [x] Interceptor agrega Authorization header automáticamente
- [x] Manejo de errores 401 con refresh automático
- [x] Si refresh falla, redirigir a login

#### Validación:
```bash
# Test con Postman/Thunder Client:
1. Login exitoso → guardar tokens
2. Llamar endpoint protegido con token válido
3. Esperar 30 min → token expira → refresh automático
4. Logout → tokens se limpian
5. Intentar endpoint protegido sin token → redirect a login

# Test en navegador:
1. Login desde UI
2. Inspeccionar localStorage → ver tokens
3. Recargar página → sesión persiste
4. Esperar expiración → auto-refresh
5. Logout → localStorage limpio
```

---

### 📦 SUBFASE B.3: UI de Login y Protección de Rutas
**Duración**: 2-3 días
**Objetivo**: Crear página de login y proteger rutas existentes

#### Archivos a crear/modificar:

1. **frontend/src/pages/Login.jsx** (~250 líneas)
   - Formulario de login con validación
   - Campos: username, password
   - Botón de submit con loading state
   - Manejo de errores (credenciales incorrectas, cuenta bloqueada)
   - Mensajes de error amigables
   - Diseño responsive con Tailwind
   - Recuerda usuario (opcional checkbox)
   - Logo SAGE3280 y branding

2. **frontend/src/components/ProtectedRoute.jsx** (~80 líneas)
   - Componente wrapper para rutas protegidas
   - Props: children, requiredPermission (opcional)
   - Verifica si usuario está autenticado
   - Si no autenticado → redirect a /login
   - Si autenticado pero sin permiso → mostrar error 403
   - Muestra loading mientras verifica sesión

3. **frontend/src/components/PermissionGuard.jsx** (~50 líneas)
   - Componente para mostrar/ocultar elementos según permisos
   - Props: permission, children, fallback
   - Ejemplo: `<PermissionGuard permission="users.create"><Button/></PermissionGuard>`
   - Útil para botones, menús, secciones

4. **frontend/src/components/UserMenu.jsx** (~150 líneas)
   - Dropdown menu en header con info del usuario
   - Muestra: nombre, email, rol(es)
   - Opciones: Mi Perfil, Cambiar Contraseña, Cerrar Sesión
   - Indicador visual de sesión activa (avatar, badge)
   - Diseño con Tailwind + Lucide icons

5. **frontend/src/components/Layout.jsx** - ACTUALIZAR (~200 líneas)
   - Agregar UserMenu en header
   - Mostrar solo si usuario autenticado
   - Actualizar navegación según permisos:
     * Dashboard: todos
     * Carga: solo con permiso upload.create
     * Pacientes: todos autenticados
     * Admin DB: solo admin
     * Usuarios: solo admin
     * Roles: solo admin
     * Auditoría: admin y medico

6. **frontend/src/utils/permissions.js** (~80 líneas)
   - Helpers para verificar permisos
   - `hasPermission(user, permission)` → boolean
   - `hasAnyPermission(user, permissions[])` → boolean
   - `hasAllPermissions(user, permissions[])` → boolean
   - `hasRole(user, role)` → boolean
   - Manejo de wildcard "*"

7. **frontend/src/App.jsx** - ACTUALIZAR (~150 líneas)
   - Agregar ruta pública `/login`
   - Envolver rutas existentes con `<ProtectedRoute>`
   - Agregar redirect: si autenticado y va a /login → redirect a /
   - Agregar rutas para Users, Roles, AuditLogs

#### Funcionalidades:
- [x] Página de login funcional y atractiva
- [x] Validación de formulario (frontend)
- [x] Login exitoso → guardar sesión → redirect a dashboard
- [x] Manejo de errores de login (UI)
- [x] Todas las rutas protegidas excepto /login
- [x] Redirect automático a /login si no autenticado
- [x] UserMenu en header con datos del usuario
- [x] Botón de logout funcional
- [x] Navegación oculta/mostrada según permisos
- [x] Persistencia de sesión al recargar página

#### Validación:
```bash
# Tests funcionales:
1. Usuario NO autenticado:
   - Ir a / → redirect a /login
   - Ir a /patients → redirect a /login
   - Ir a /admin → redirect a /login

2. Usuario autenticado (medico):
   - Login exitoso → redirect a /
   - Ver UserMenu con su nombre
   - Navegar a /patients → acceso OK
   - Navegar a /admin → acceso OK (ver DB stats)
   - NO ver opción "Usuarios" en menú
   - NO ver opción "Roles" en menú
   - SÍ ver opción "Auditoría" en menú

3. Usuario autenticado (admin):
   - Ver TODAS las opciones en menú
   - Acceso a /users, /roles, /audit

4. Logout:
   - Click en "Cerrar Sesión"
   - Redirect a /login
   - Intentar volver a / → redirect a /login
   - localStorage limpio

5. Recargar página:
   - Login → navegar → F5
   - Sesión persiste
   - Usuario sigue autenticado
```

---

### 📦 SUBFASE B.4: Gestión de Usuarios (UI)
**Duración**: 2-3 días
**Objetivo**: CRUD completo de usuarios desde la UI

#### Archivos a crear:

1. **frontend/src/services/usersService.js** (~200 líneas)
   - `getUsers(offset, limit, search, role, isActive)` → GET /api/users
   - `getUser(userId)` → GET /api/users/{id}
   - `createUser(userData)` → POST /api/users
   - `updateUser(userId, userData)` → PUT /api/users/{id}
   - `deleteUser(userId)` → DELETE /api/users/{id}
   - `activateUser(userId, activate)` → PUT /api/users/{id}/activate
   - `resetPassword(userId, newPassword)` → POST /api/users/{id}/reset-password
   - `changeMyPassword(currentPassword, newPassword)` → POST /api/auth/change-password

2. **frontend/src/pages/Users.jsx** (~400 líneas)
   - Lista de usuarios con paginación
   - Tabla: username, email, roles, estado (activo/inactivo), acciones
   - Filtros:
     * Búsqueda por username/email
     * Filtro por rol (dropdown)
     * Filtro por estado (activo/inactivo/todos)
   - Botón "Crear Usuario" (modal o ruta)
   - Acciones por usuario:
     * Ver/Editar
     * Activar/Desactivar
     * Resetear contraseña
     * Eliminar (con confirmación)
   - Indicadores visuales (badges para roles, estado)
   - Loading states
   - Empty states (no hay usuarios)

3. **frontend/src/pages/UserForm.jsx** (~350 líneas)
   - Formulario para crear/editar usuario
   - Modo: create vs edit (detectar por route param)
   - Campos:
     * Username (solo create)
     * Email
     * Full Name
     * Password (solo create, validación de fortaleza)
     * Confirm Password (solo create)
     * Roles (multi-select con checkboxes)
     * Is Active (toggle)
   - Validaciones frontend:
     * Username: min 3 chars, solo alfanumérico + ._-
     * Email: formato válido
     * Password: min 8 chars, 1 mayúscula, 1 minúscula, 1 número
     * Passwords match
   - Mostrar errores de backend (username duplicado, etc.)
   - Botones: Guardar, Cancelar
   - Breadcrumbs: Usuarios > Nuevo Usuario / Editar {username}

4. **frontend/src/components/PasswordChangeModal.jsx** (~200 líneas)
   - Modal para cambiar contraseña (propio usuario)
   - Campos: Contraseña Actual, Nueva Contraseña, Confirmar
   - Validación de fortaleza
   - Accesible desde UserMenu
   - Cierra automáticamente al success

5. **frontend/src/components/ResetPasswordModal.jsx** (~150 líneas)
   - Modal para resetear contraseña de otro usuario (admin)
   - Campos: Nueva Contraseña, Confirmar
   - Validación
   - Confirmación antes de resetear

#### Funcionalidades:
- [x] Listar todos los usuarios con paginación
- [x] Buscar usuarios por username/email
- [x] Filtrar por rol y estado
- [x] Crear nuevo usuario con asignación de roles
- [x] Editar usuario existente (email, nombre, roles, estado)
- [x] Activar/Desactivar cuenta de usuario
- [x] Resetear contraseña de usuario (admin)
- [x] Eliminar usuario (con confirmación)
- [x] Cambiar mi propia contraseña
- [x] Validaciones frontend + manejo de errores backend
- [x] UI/UX responsiva y amigable
- [x] Loading states y feedback visual

#### Validación:
```bash
# Tests funcionales:
1. Listar usuarios:
   - Ver tabla con 4 usuarios default
   - Paginación funciona (si hay >50)
   - Buscar "admin" → encuentra admin
   - Filtrar por rol "medico" → solo dr.martinez
   - Filtrar "inactivos" → ninguno (todos activos)

2. Crear usuario:
   - Click "Crear Usuario"
   - Llenar formulario válido
   - Asignar rol "auxiliar"
   - Submit → usuario creado
   - Aparece en lista

3. Validaciones:
   - Username corto → error
   - Email inválido → error
   - Password sin mayúscula → error
   - Passwords no coinciden → error
   - Username duplicado → error backend

4. Editar usuario:
   - Click editar en dr.martinez
   - Cambiar email
   - Agregar rol "admin"
   - Guardar → cambios aplicados

5. Resetear contraseña:
   - Click resetear en usuario
   - Ingresar nueva contraseña válida
   - Confirmar → contraseña cambiada
   - Logout → login con nueva contraseña

6. Desactivar usuario:
   - Click desactivar
   - Usuario marcado como inactivo
   - Intentar login con ese usuario → error

7. Eliminar usuario:
   - Click eliminar
   - Confirmar
   - Usuario eliminado de lista

8. Cambiar mi contraseña:
   - UserMenu → Cambiar Contraseña
   - Ingresar contraseña actual (incorrecta) → error
   - Ingresar correcta + nueva válida
   - Guardar → success
   - Logout → login con nueva contraseña
```

---

### 📦 SUBFASE B.5: Gestión de Roles (UI)
**Duración**: 2-3 días
**Objetivo**: CRUD completo de roles desde la UI

#### Archivos a crear:

1. **frontend/src/services/rolesService.js** (~150 líneas)
   - `getRoles(offset, limit, search)` → GET /api/roles
   - `getRole(roleId)` → GET /api/roles/{id}
   - `createRole(roleData)` → POST /api/roles
   - `updateRole(roleId, roleData)` → PUT /api/roles/{id}
   - `deleteRole(roleId)` → DELETE /api/roles/{id}
   - `getAvailablePermissions()` → GET /api/roles/permissions/list
   - `getRolePermissions(roleId)` → GET /api/roles/{id}/permissions

2. **frontend/src/pages/Roles.jsx** (~350 líneas)
   - Lista de roles en cards o tabla
   - Info por rol:
     * Nombre y Display Name
     * Descripción
     * Cantidad de usuarios
     * Cantidad de permisos
     * Badge "Sistema" si es rol del sistema
     * Estado (activo/inactivo)
   - Botón "Crear Rol" (solo roles custom, no sistema)
   - Acciones:
     * Ver permisos (expandir/modal)
     * Editar (solo roles custom)
     * Activar/Desactivar (solo custom)
     * Eliminar (solo custom sin usuarios)
   - Advertencia: roles del sistema no editables
   - Búsqueda por nombre

3. **frontend/src/pages/RoleForm.jsx** (~400 líneas)
   - Formulario para crear/editar rol custom
   - Campos:
     * Name (identificador único)
     * Display Name (nombre para mostrar)
     * Description (textarea)
     * Permissions (lista de checkboxes agrupados por categoría)
     * Is Active (toggle)
   - Permisos agrupados por categoría:
     * Patients (8 permisos)
     * Consultations (6 permisos)
     * Controls (6 permisos)
     * Alerts (5 permisos)
     * Reports (3 permisos)
     * Users (4 permisos)
     * Etc. (total 33)
   - Helpers:
     * "Seleccionar todos" por categoría
     * "Deseleccionar todos"
     * Contador de permisos seleccionados
   - Validaciones:
     * Name único
     * Al menos 1 permiso seleccionado
   - Preview de permisos seleccionados

4. **frontend/src/components/PermissionsTable.jsx** (~200 líneas)
   - Componente reutilizable para mostrar permisos
   - Modo lectura: mostrar permisos asignados (en Roles.jsx)
   - Modo edición: checkboxes para seleccionar (en RoleForm.jsx)
   - Agrupación por categoría con expand/collapse
   - Badges de colores por categoría

#### Funcionalidades:
- [x] Listar todos los roles (sistema + custom)
- [x] Ver permisos de cada rol
- [x] Crear nuevo rol custom con permisos
- [x] Editar rol custom (nombre, permisos, estado)
- [x] Activar/Desactivar rol custom
- [x] Eliminar rol custom (solo si no tiene usuarios)
- [x] No permitir editar/eliminar roles del sistema
- [x] Validaciones frontend + backend
- [x] UI clara para gestión de 33 permisos

#### Validación:
```bash
# Tests funcionales:
1. Listar roles:
   - Ver 4 roles del sistema
   - Cada rol muestra cantidad de usuarios
   - Rol "admin" tiene 33 permisos (*)
   - Rol "medico" tiene ~20 permisos

2. Ver permisos de rol:
   - Click en "Ver permisos" de "medico"
   - Expandir → ver lista de permisos
   - Agrupados por categoría

3. Crear rol custom:
   - Click "Crear Rol"
   - Name: "supervisor"
   - Display: "Supervisor de Calidad"
   - Descripción: "Revisa indicadores"
   - Seleccionar permisos:
     * reports.read
     * reports.export
     * patients.read
     * controls.read
   - Guardar → rol creado
   - Aparece en lista

4. Editar rol custom:
   - Click editar en "supervisor"
   - Agregar permiso alerts.read
   - Guardar → cambios aplicados

5. Intentar editar rol sistema:
   - Rol "admin" NO tiene botón editar
   - Rol "medico" NO editable
   - Solo visualización

6. Eliminar rol sin usuarios:
   - Crear rol "test" sin asignar a nadie
   - Eliminar → success

7. Intentar eliminar rol con usuarios:
   - Rol "medico" tiene 1 usuario
   - Intentar eliminar → error
   - Mensaje: "No se puede eliminar, tiene N usuarios"

8. Asignar rol custom a usuario:
   - Ir a Users → crear usuario
   - Asignar rol "supervisor"
   - Guardar → usuario tiene permisos de supervisor
```

---

### 📦 SUBFASE B.6: Visualización de Logs de Auditoría
**Duración**: 2-3 días
**Objetivo**: Interfaz para ver y filtrar logs de auditoría

#### Archivos a crear:

1. **frontend/src/services/auditService.js** (~120 líneas)
   - `getLogs(offset, limit, filters)` → GET /api/audit/logs
   - `getLogDetail(logId)` → GET /api/audit/logs/{id}
   - `getStats(days)` → GET /api/audit/stats
   - `cleanupOldLogs(days, dryRun)` → DELETE /api/audit/cleanup
   - `exportLogs(filters, format)` → GET /api/audit/export

2. **frontend/src/pages/AuditLogs.jsx** (~500 líneas)
   - Tabla de logs con paginación
   - Columnas:
     * Timestamp (fecha/hora)
     * Usuario
     * Acción (create_user, login, update_patient, etc.)
     * Categoría (auth, users, patients, etc.)
     * Estado (success/error)
     * IP Address
     * Detalles (expandible)
   - Filtros avanzados:
     * Rango de fechas (date_from, date_to)
     * Usuario (dropdown)
     * Acción (dropdown)
     * Categoría (dropdown)
     * Estado (success/error/all)
   - Botón "Limpiar filtros"
   - Botón "Exportar" (CSV/Excel)
   - Indicadores visuales:
     * Badge verde para success
     * Badge rojo para error
     * Íconos por categoría
   - Detalle expandible:
     * JSON formateado de request/response
     * User-agent
     * Duración

3. **frontend/src/pages/AuditStats.jsx** (~350 líneas)
   - Dashboard de estadísticas de auditoría
   - Métricas principales:
     * Total de logs (último día/semana/mes)
     * Logs por categoría (gráfico de barras)
     * Logs por usuario (top 10)
     * Logs por acción (top 10)
     * Tasa de errores (%)
     * Acciones más frecuentes
   - Filtro por período (último día, 7 días, 30 días, custom)
   - Gráficos con Recharts:
     * Timeline de actividad
     * Distribución por categoría (pie chart)
     * Top usuarios (bar chart)
   - Exportar estadísticas

4. **frontend/src/components/AuditFilters.jsx** (~200 líneas)
   - Componente de filtros reutilizable
   - Date pickers para rango
   - Dropdowns para usuario, acción, categoría
   - Estado (radio buttons o select)
   - Botones: Aplicar, Limpiar
   - Contador de filtros activos

5. **frontend/src/components/AuditLogDetail.jsx** (~150 líneas)
   - Modal o panel expandible para ver detalles
   - Info completa del log:
     * Timestamp
     * Usuario (nombre, email, rol)
     * Acción y categoría
     * IP y User-Agent
     * Request data (JSON viewer)
     * Response data (JSON viewer)
     * Error message (si aplica)
   - JSON syntax highlighting (opcional)
   - Botón copiar JSON

#### Funcionalidades:
- [x] Listar todos los logs con paginación
- [x] Filtros avanzados por fecha, usuario, acción, categoría, estado
- [x] Ver detalles de cada log
- [x] Exportar logs a CSV/Excel
- [x] Dashboard de estadísticas de auditoría
- [x] Gráficos visuales de actividad
- [x] Cleanup de logs antiguos (admin only)
- [x] Auto-refresh opcional (cada 30s)
- [x] Acceso para admin y medico (no auxiliar/operador)

#### Validación:
```bash
# Tests funcionales:
1. Listar logs:
   - Ver tabla con todos los logs
   - Ordenados por fecha DESC (más recientes primero)
   - Paginación funciona

2. Filtros:
   - Filtrar por usuario "admin" → solo logs de admin
   - Filtrar por acción "login" → solo logins
   - Filtrar por categoría "auth" → autenticación
   - Filtrar por estado "error" → solo errores
   - Filtrar por rango de fechas → logs en ese rango
   - Combinar filtros → AND logic

3. Ver detalle:
   - Click en un log de "create_user"
   - Ver JSON del request (usuario creado)
   - Ver response (success)
   - Ver IP y user-agent

4. Estadísticas:
   - Ir a AuditStats
   - Ver gráfico de actividad (último 7 días)
   - Ver top usuarios (admin aparece arriba)
   - Ver distribución por categoría
   - Cambiar período a "último mes"

5. Exportar:
   - Aplicar filtros
   - Click "Exportar a Excel"
   - Descarga archivo con logs filtrados

6. Permisos:
   - Login como admin → acceso completo
   - Login como medico → acceso solo lectura
   - Login como auxiliar → NO ver opción Auditoría
   - Login como operador → NO ver opción Auditoría

7. Cleanup (solo admin):
   - Ir a configuración de auditoría
   - Cleanup logs > 90 días
   - Dry run → mostrar cantidad a eliminar
   - Confirmar → logs eliminados
```

---

### 📦 SUBFASE B.7: Integración Final y Pulido
**Duración**: 2-3 días
**Objetivo**: Integrar todo, testing end-to-end, mejoras UX

#### Tareas:

1. **Integración de todas las partes**
   - Verificar que todos los componentes funcionen juntos
   - Probar flujos completos end-to-end
   - Resolver conflictos de rutas o estados

2. **Actualizar navegación principal** (~100 líneas)
   - Menú lateral/header con links condicionales:
     * Dashboard (todos)
     * Carga (upload.create)
     * Pacientes (todos autenticados)
     * Controles (todos autenticados)
     * Alertas (todos autenticados)
     * Prioridades (todos autenticados)
     * Reportes (reports.read)
     * Admin DB (admin)
     * ─────────── (separador)
     * Usuarios (users.read)
     * Roles (roles.read)
     * Auditoría (audit.read)
   - Íconos de Lucide React
   - Badge de "Admin" en secciones administrativas
   - Active link highlighting

3. **Mejorar UX/UI general**
   - Loading skeletons en lugar de spinners
   - Transiciones suaves entre páginas
   - Toasts informativos para acciones (success/error)
   - Confirmaciones antes de acciones destructivas
   - Empty states con ilustraciones y mensajes útiles
   - Error boundaries para capturar errores React
   - 404 page para rutas no encontradas

4. **Responsive design**
   - Verificar todas las páginas en mobile/tablet
   - Menú responsive (hamburger en mobile)
   - Tablas responsive (scroll horizontal o cards en mobile)
   - Modales adaptados a pantallas pequeñas

5. **Mejoras de seguridad frontend**
   - Sanitizar inputs (prevenir XSS)
   - No almacenar datos sensibles en localStorage (solo tokens)
   - Timeout de sesión por inactividad (opcional)
   - Confirmación de salida si hay cambios sin guardar

6. **Testing end-to-end**
   - Flujo completo de admin:
     1. Login como admin
     2. Crear nuevo usuario
     3. Asignar rol
     4. Verificar en auditoría
     5. Editar usuario
     6. Verificar cambios
     7. Logout
   - Flujo de medico:
     1. Login como dr.martinez
     2. Ver pacientes
     3. Ver controles
     4. Ver auditoría
     5. Intentar acceder a usuarios → 403
     6. Logout
   - Flujo de auxiliar:
     1. Login como aux.garcia
     2. Ver pacientes
     3. Marcar contacto
     4. NO ver auditoría
     5. Logout
   - Flujo de operador:
     1. Login como op.lopez
     2. Cargar archivo Excel
     3. Ver progreso
     4. NO ver usuarios/roles/auditoría
     5. Logout

7. **Documentación**
   - README del frontend actualizado
   - Guía de uso para cada rol
   - Screenshots de las pantallas principales
   - Instrucciones de desarrollo local

8. **Performance**
   - Lazy loading de rutas (React.lazy)
   - Code splitting por rutas
   - Memoización de componentes pesados
   - Optimizar re-renders innecesarios

#### Archivos a crear/modificar:

1. **frontend/src/App.jsx** - FINAL (~200 líneas)
   - Todas las rutas configuradas
   - Lazy loading de páginas
   - Error boundary
   - 404 page

2. **frontend/src/components/ErrorBoundary.jsx** (~100 líneas)
   - Captura errores de React
   - Muestra UI amigable
   - Log de errores

3. **frontend/src/pages/NotFound.jsx** (~80 líneas)
   - Página 404
   - Link para volver al dashboard

4. **frontend/src/components/LoadingSkeleton.jsx** (~100 líneas)
   - Skeletons para tablas, cards, forms
   - Reutilizable

5. **frontend/README.md** - ACTUALIZAR
   - Guía de instalación
   - Usuarios de prueba
   - Permisos por rol
   - Estructura del proyecto

#### Validación final:
```bash
# Tests de regresión:
1. Todas las páginas existentes siguen funcionando
2. Upload de archivos funciona con auth
3. Dashboard stats funcionan
4. Exportaciones funcionan

# Tests de autenticación:
5. Login/logout funcional
6. Refresh automático de tokens
7. Persistencia de sesión
8. Protección de rutas

# Tests de permisos:
9. Admin ve todo
10. Medico ve pacientes + auditoría, NO usuarios
11. Auxiliar NO ve auditoría ni usuarios
12. Operador solo ve upload

# Tests de CRUD:
13. Crear/editar/eliminar usuarios
14. Crear/editar/eliminar roles
15. Ver/filtrar/exportar auditoría

# Tests de UX:
16. Navegación intuitiva
17. Feedback visual de acciones
18. Manejo de errores amigable
19. Responsive en mobile

# Tests de performance:
20. Primera carga < 3s
21. Navegación entre páginas < 500ms
22. Lazy loading funciona
```

---

## RESUMEN DE ENTREGABLES

### Archivos nuevos a crear: 25
```
contexts/
  └── AuthContext.jsx                    [B.1]
hooks/
  └── useAuth.js                         [B.1]
utils/
  ├── tokenManager.js                    [B.2]
  └── permissions.js                     [B.3]
services/
  ├── authService.js                     [B.2]
  ├── usersService.js                    [B.4]
  ├── rolesService.js                    [B.5]
  └── auditService.js                    [B.6]
pages/
  ├── Login.jsx                          [B.3]
  ├── Users.jsx                          [B.4]
  ├── UserForm.jsx                       [B.4]
  ├── Roles.jsx                          [B.5]
  ├── RoleForm.jsx                       [B.5]
  ├── AuditLogs.jsx                      [B.6]
  ├── AuditStats.jsx                     [B.6]
  └── NotFound.jsx                       [B.7]
components/
  ├── ProtectedRoute.jsx                 [B.3]
  ├── PermissionGuard.jsx                [B.3]
  ├── UserMenu.jsx                       [B.3]
  ├── PasswordChangeModal.jsx            [B.4]
  ├── ResetPasswordModal.jsx             [B.4]
  ├── PermissionsTable.jsx               [B.5]
  ├── AuditFilters.jsx                   [B.6]
  ├── AuditLogDetail.jsx                 [B.6]
  ├── ErrorBoundary.jsx                  [B.7]
  └── LoadingSkeleton.jsx                [B.7]
```

### Archivos a modificar: 4
```
services/api.js                          [B.2] - Interceptors
components/Layout.jsx                    [B.3] - UserMenu + navegación
App.jsx                                  [B.7] - Rutas + lazy loading
README.md                                [B.7] - Documentación
```

### Total de líneas estimadas: ~5,500 líneas

---

## CRONOGRAMA PROPUESTO

### Semana 1: Fundamentos (B.1, B.2, B.3)
**Días 1-2**: B.1 - AuthContext y hooks
**Días 3-4**: B.2 - Servicios de API y tokens
**Días 5-7**: B.3 - Login UI y protección de rutas

**Checkpoint Semana 1**:
- ✅ Login funcional
- ✅ Rutas protegidas
- ✅ Tokens persistentes
- ✅ UserMenu con logout

### Semana 2: Gestión de Entidades (B.4, B.5)
**Días 8-10**: B.4 - Gestión de Usuarios completa
**Días 11-13**: B.5 - Gestión de Roles completa

**Checkpoint Semana 2**:
- ✅ CRUD usuarios completo
- ✅ CRUD roles completo
- ✅ Asignación de roles a usuarios
- ✅ Validaciones frontend

### Semana 3: Auditoría y Pulido (B.6, B.7)
**Días 14-16**: B.6 - Logs de Auditoría
**Días 17-21**: B.7 - Integración, testing, pulido

**Checkpoint Semana 3**:
- ✅ Auditoría funcional con filtros
- ✅ Estadísticas visuales
- ✅ Testing end-to-end completo
- ✅ UX/UI pulida
- ✅ Documentación actualizada

---

## TECNOLOGÍAS Y LIBRERÍAS

### Ya instaladas:
- ✅ React 18.2
- ✅ React Router DOM 6.20
- ✅ Axios 1.6.2
- ✅ Tailwind CSS 3.3.6
- ✅ Recharts 2.10.3 (gráficos)
- ✅ Lucide React 0.294.0 (iconos)
- ✅ React Hot Toast 2.4.1 (notificaciones)

### A instalar:
```bash
# Date pickers para filtros de auditoría
npm install react-datepicker

# JWT decode para extraer info del token
npm install jwt-decode

# JSON viewer para auditoría (opcional)
npm install react-json-view

# Tablas avanzadas (opcional, solo si es necesario)
npm install @tanstack/react-table
```

---

## RIESGOS Y MITIGACIONES

### Riesgo 1: Refresh tokens no funcionan correctamente
**Mitigación**: Implementar queue de requests durante refresh para evitar race conditions

### Riesgo 2: Tokens expiran mientras usuario está activo
**Mitigación**: Auto-refresh antes de expiración (timer) + refresh en interceptor 401

### Riesgo 3: Usuario pierde cambios si token expira durante edición
**Mitigación**: Guardar draft en localStorage + advertencia antes de salir

### Riesgo 4: Performance con muchos permisos (33 checkboxes)
**Mitigación**: Lazy loading de permisos + virtualization si es necesario

### Riesgo 5: Mobile UX pobre en tablas complejas
**Mitigación**: Cards en mobile en lugar de tablas + scroll horizontal

---

## CRITERIOS DE ÉXITO

### Funcionales:
- [x] Login/Logout funcionan correctamente
- [x] Tokens se renuevan automáticamente
- [x] Rutas protegidas según permisos
- [x] CRUD completo de usuarios
- [x] CRUD completo de roles
- [x] Auditoría visible y filtrable
- [x] Navegación adaptada a cada rol
- [x] Sesión persiste al recargar

### No funcionales:
- [x] Primera carga < 3 segundos
- [x] Navegación fluida < 500ms
- [x] Responsive en mobile/tablet
- [x] No errores en consola
- [x] Código limpio y mantenible
- [x] 100% de endpoints de auth utilizados

### UX:
- [x] Interfaz intuitiva
- [x] Feedback visual de acciones
- [x] Errores mostrados de forma amigable
- [x] Loading states en todas las operaciones
- [x] Confirmaciones antes de acciones destructivas

---

## SIGUIENTES PASOS

Una vez completada la FASE B (Frontend de Autenticación), el sistema estará:
- ✅ 100% funcional end-to-end
- ✅ Totalmente usable por usuarios finales
- ✅ Seguro y con auditoría completa
- ✅ Preparado para escalar

**Progreso del proyecto pasará de 82% a ~90%**

**Opciones para continuar después de FASE B**:
1. **FASE C**: Sistema de WhatsApp/Mensajería (8-10 semanas) - GAP #1 CRÍTICO
2. **FASE D**: Reportes Regulatorios (2 semanas) - GAP #6
3. **FASE E**: Multi-tenancy (2 semanas) - GAP #4
4. **FASE F**: Integraciones HCE (3-4 semanas) - GAP #5

---

## NOTAS FINALES

- Este plan está diseñado para implementarse **paso a paso**
- Cada subfase es **independiente y testable**
- Se puede pausar después de cualquier subfase
- Prioriza **funcionalidad sobre perfección** en primera iteración
- Iteraciones de mejora UX pueden hacerse después

**Recomendación**: Seguir el orden B.1 → B.2 → B.3 → B.4 → B.5 → B.6 → B.7 sin saltar pasos.

---

**FIN DEL PLAN DETALLADO FASE B**
