import api from './api';

/**
 * Roles Service
 * Servicio para gestión de roles y permisos
 */

/**
 * Obtiene lista de roles con paginación y filtros
 * @param {Object} params - Parámetros de búsqueda
 * @param {number} params.offset - Offset para paginación (default: 0)
 * @param {number} params.limit - Límite de resultados (default: 50)
 * @param {string} params.search - Búsqueda por nombre
 * @returns {Promise<Object>} { roles, total, offset, limit }
 */
export const getRoles = async (params = {}) => {
  const response = await api.get('/roles', { params });
  // Backend returns { total, items }, transform to { roles, total }
  return {
    roles: response.data.items || [],
    total: response.data.total || 0
  };
};

/**
 * Obtiene un rol por ID
 * @param {number} roleId - ID del rol
 * @returns {Promise<Object>} Rol con permisos
 */
export const getRole = async (roleId) => {
  const response = await api.get(`/roles/${roleId}`);
  return response.data;
};

/**
 * Crea un nuevo rol custom
 * @param {Object} roleData - Datos del rol
 * @param {string} roleData.name - Nombre del rol (único, snake_case)
 * @param {string} roleData.display_name - Nombre para mostrar
 * @param {string} roleData.description - Descripción del rol
 * @param {Array<string>} roleData.permissions - Array de permisos
 * @param {boolean} roleData.is_active - Rol activo (default: true)
 * @returns {Promise<Object>} Rol creado
 */
export const createRole = async (roleData) => {
  const response = await api.post('/roles', roleData);
  return response.data;
};

/**
 * Actualiza un rol custom existente
 * @param {number} roleId - ID del rol
 * @param {Object} roleData - Datos a actualizar
 * @param {string} roleData.display_name - Nombre para mostrar (opcional)
 * @param {string} roleData.description - Descripción (opcional)
 * @param {Array<string>} roleData.permissions - Permisos (opcional)
 * @param {boolean} roleData.is_active - Estado activo (opcional)
 * @returns {Promise<Object>} Rol actualizado
 */
export const updateRole = async (roleId, roleData) => {
  const response = await api.put(`/roles/${roleId}`, roleData);
  return response.data;
};

/**
 * Elimina un rol custom
 * @param {number} roleId - ID del rol
 * @returns {Promise<Object>} Mensaje de confirmación
 */
export const deleteRole = async (roleId) => {
  const response = await api.delete(`/roles/${roleId}`);
  return response.data;
};

/**
 * Obtiene la lista de permisos disponibles
 * @returns {Promise<Array>} Lista de permisos con categorías
 */
export const getAvailablePermissions = async () => {
  const response = await api.get('/roles/permissions/list');
  return response.data;
};

/**
 * Obtiene los permisos de un rol específico
 * @param {number} roleId - ID del rol
 * @returns {Promise<Array>} Array de permisos
 */
export const getRolePermissions = async (roleId) => {
  const response = await api.get(`/roles/${roleId}/permissions`);
  return response.data;
};

/**
 * Obtiene estadísticas de un rol (cantidad de usuarios)
 * @param {number} roleId - ID del rol
 * @returns {Promise<Object>} { users_count, ... }
 */
export const getRoleStats = async (roleId) => {
  const response = await api.get(`/roles/${roleId}/stats`);
  return response.data;
};

/**
 * Lista de categorías de permisos para agrupar en UI
 * Esta es una estructura local para organizar los 33 permisos
 */
export const PERMISSION_CATEGORIES = {
  patients: {
    label: 'Pacientes',
    color: 'blue',
    permissions: [
      'patients.read',
      'patients.create',
      'patients.update',
      'patients.delete',
      'patients.read_all',
      'patients.export',
      'patients.import',
      'patients.contact_update'
    ]
  },
  consultations: {
    label: 'Consultas',
    color: 'green',
    permissions: [
      'consultations.read',
      'consultations.create',
      'consultations.update',
      'consultations.delete',
      'consultations.read_all',
      'consultations.export'
    ]
  },
  controls: {
    label: 'Controles',
    color: 'purple',
    permissions: [
      'controls.read',
      'controls.create',
      'controls.update',
      'controls.delete',
      'controls.read_all',
      'controls.export'
    ]
  },
  alerts: {
    label: 'Alertas',
    color: 'yellow',
    permissions: [
      'alerts.read',
      'alerts.create',
      'alerts.update',
      'alerts.dismiss',
      'alerts.read_all'
    ]
  },
  reports: {
    label: 'Reportes',
    color: 'indigo',
    permissions: [
      'reports.read',
      'reports.create',
      'reports.export'
    ]
  },
  users: {
    label: 'Usuarios',
    color: 'pink',
    permissions: [
      'users.read',
      'users.create',
      'users.update',
      'users.delete'
    ]
  },
  roles: {
    label: 'Roles',
    color: 'red',
    permissions: [
      'roles.read',
      'roles.create',
      'roles.update',
      'roles.delete'
    ]
  },
  audit: {
    label: 'Auditoría',
    color: 'gray',
    permissions: [
      'audit.read',
      'audit.export'
    ]
  },
  upload: {
    label: 'Cargas',
    color: 'orange',
    permissions: [
      'upload.create',
      'upload.read',
      'upload.delete'
    ]
  }
};

/**
 * Obtiene el color de badge para una categoría
 * @param {string} category - Nombre de la categoría
 * @returns {string} Clase de Tailwind para el color
 */
export const getCategoryColor = (category) => {
  const colors = {
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
    purple: 'bg-purple-100 text-purple-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    indigo: 'bg-indigo-100 text-indigo-800',
    pink: 'bg-pink-100 text-pink-800',
    red: 'bg-red-100 text-red-800',
    gray: 'bg-gray-100 text-gray-800',
    orange: 'bg-orange-100 text-orange-800',
  };

  const categoryData = Object.values(PERMISSION_CATEGORIES).find(
    cat => cat.permissions.includes(category) || cat.label.toLowerCase() === category.toLowerCase()
  );

  const color = categoryData?.color || 'gray';
  return colors[color] || colors.gray;
};

const rolesService = {
  getRoles,
  getRole,
  createRole,
  updateRole,
  deleteRole,
  getAvailablePermissions,
  getRolePermissions,
  getRoleStats,
  PERMISSION_CATEGORIES,
  getCategoryColor,
};

export default rolesService;
