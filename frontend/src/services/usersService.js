import api from './api';

/**
 * Users Service
 * Servicio para gestión de usuarios
 */

/**
 * Obtiene lista de usuarios con paginación y filtros
 * @param {Object} params - Parámetros de búsqueda
 * @param {number} params.offset - Offset para paginación (default: 0)
 * @param {number} params.limit - Límite de resultados (default: 50)
 * @param {string} params.search - Búsqueda por username o email
 * @param {string} params.role - Filtrar por rol
 * @param {boolean} params.is_active - Filtrar por estado activo/inactivo
 * @returns {Promise<Object>} { users, total, offset, limit }
 */
export const getUsers = async (params = {}) => {
  const response = await api.get('/users', { params });
  // Backend returns { total, items }, transform to { users, total }
  return {
    users: response.data.items || [],
    total: response.data.total || 0
  };
};

/**
 * Obtiene un usuario por ID
 * @param {number} userId - ID del usuario
 * @returns {Promise<Object>} Usuario
 */
export const getUser = async (userId) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

/**
 * Crea un nuevo usuario
 * @param {Object} userData - Datos del usuario
 * @param {string} userData.username - Username (único)
 * @param {string} userData.email - Email (único)
 * @param {string} userData.full_name - Nombre completo
 * @param {string} userData.password - Contraseña
 * @param {Array<number>} userData.role_ids - IDs de roles a asignar
 * @param {boolean} userData.is_active - Usuario activo (default: true)
 * @returns {Promise<Object>} Usuario creado
 */
export const createUser = async (userData) => {
  const response = await api.post('/users', userData);
  return response.data;
};

/**
 * Actualiza un usuario existente
 * @param {number} userId - ID del usuario
 * @param {Object} userData - Datos a actualizar
 * @param {string} userData.email - Email (opcional)
 * @param {string} userData.full_name - Nombre completo (opcional)
 * @param {Array<number>} userData.role_ids - IDs de roles (opcional)
 * @param {boolean} userData.is_active - Estado activo (opcional)
 * @returns {Promise<Object>} Usuario actualizado
 */
export const updateUser = async (userId, userData) => {
  const response = await api.put(`/users/${userId}`, userData);
  return response.data;
};

/**
 * Elimina un usuario
 * @param {number} userId - ID del usuario
 * @returns {Promise<Object>} Mensaje de confirmación
 */
export const deleteUser = async (userId) => {
  const response = await api.delete(`/users/${userId}`);
  return response.data;
};

/**
 * Activa o desactiva un usuario
 * @param {number} userId - ID del usuario
 * @param {boolean} activate - true para activar, false para desactivar
 * @returns {Promise<Object>} Usuario actualizado
 */
export const toggleUserActive = async (userId, activate) => {
  const response = await api.put(`/users/${userId}/activate`, { activate });
  return response.data;
};

/**
 * Resetea la contraseña de un usuario (solo admin)
 * @param {number} userId - ID del usuario
 * @param {string} newPassword - Nueva contraseña
 * @returns {Promise<Object>} Mensaje de confirmación
 */
export const resetUserPassword = async (userId, newPassword) => {
  const response = await api.post(`/users/${userId}/reset-password`, {
    new_password: newPassword
  });
  return response.data;
};

/**
 * Obtiene roles disponibles
 * @returns {Promise<Array>} Lista de roles
 */
export const getRoles = async () => {
  const response = await api.get('/roles');
  // Backend returns { total, items }, extract items array
  return response.data.items || [];
};

/**
 * Verifica si un username está disponible
 * @param {string} username - Username a verificar
 * @returns {Promise<boolean>} true si está disponible
 */
export const checkUsernameAvailable = async (username) => {
  try {
    const response = await api.get(`/users/check-username/${username}`);
    return response.data.available;
  } catch (error) {
    return false;
  }
};

/**
 * Verifica si un email está disponible
 * @param {string} email - Email a verificar
 * @returns {Promise<boolean>} true si está disponible
 */
export const checkEmailAvailable = async (email) => {
  try {
    const response = await api.get(`/users/check-email/${email}`);
    return response.data.available;
  } catch (error) {
    return false;
  }
};

const usersService = {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
  toggleUserActive,
  resetUserPassword,
  getRoles,
  checkUsernameAvailable,
  checkEmailAvailable,
};

export default usersService;
