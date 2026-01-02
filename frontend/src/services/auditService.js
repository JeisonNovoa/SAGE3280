/**
 * Audit Service - Servicio de Logs de Auditoría
 *
 * Maneja todas las operaciones relacionadas con logs de auditoría:
 * - Consulta de logs con filtros
 * - Estadísticas de auditoría
 * - Logs por usuario
 * - Limpieza de logs antiguos
 */
import api from './api';

/**
 * Categorías de auditoría disponibles
 */
export const AUDIT_CATEGORIES = {
  AUTH: 'auth',
  PATIENT: 'patient',
  UPLOAD: 'upload',
  USER: 'user',
  ROLE: 'role',
  CONTROL: 'control',
  ALERT: 'alert',
  CONFIG: 'config',
  REPORT: 'report',
  SYSTEM: 'system',
};

/**
 * Mapeo de categorías a colores para badges
 */
export const CATEGORY_COLORS = {
  auth: 'blue',
  patient: 'green',
  upload: 'purple',
  user: 'indigo',
  role: 'pink',
  control: 'yellow',
  alert: 'red',
  config: 'gray',
  report: 'orange',
  system: 'gray',
};

/**
 * Mapeo de estados a colores
 */
export const STATUS_COLORS = {
  success: 'green',
  error: 'red',
  failed: 'red',
  blocked: 'yellow',
};

/**
 * Labels legibles para categorías
 */
export const CATEGORY_LABELS = {
  auth: 'Autenticación',
  patient: 'Pacientes',
  upload: 'Cargas',
  user: 'Usuarios',
  role: 'Roles',
  control: 'Controles',
  alert: 'Alertas',
  config: 'Configuración',
  report: 'Reportes',
  system: 'Sistema',
};

/**
 * Labels para estados
 */
export const STATUS_LABELS = {
  success: 'Exitoso',
  error: 'Error',
  failed: 'Fallido',
  blocked: 'Bloqueado',
};

const auditService = {
  /**
   * Lista logs de auditoría con filtros y paginación
   *
   * @param {Object} params - Parámetros de búsqueda
   * @param {number} params.offset - Offset para paginación
   * @param {number} params.limit - Límite de resultados
   * @param {number} params.user_id - Filtrar por usuario
   * @param {string} params.action - Filtrar por acción
   * @param {string} params.category - Filtrar por categoría
   * @param {string} params.status - Filtrar por estado
   * @param {string} params.resource_type - Filtrar por tipo de recurso
   * @param {string} params.date_from - Fecha desde (ISO)
   * @param {string} params.date_to - Fecha hasta (ISO)
   * @returns {Promise<Object>} - { total, offset, limit, items }
   */
  async getLogs(params = {}) {
    try {
      const queryParams = new URLSearchParams();

      // Paginación
      queryParams.append('offset', params.offset || 0);
      queryParams.append('limit', params.limit || 50);

      // Filtros opcionales
      if (params.user_id) queryParams.append('user_id', params.user_id);
      if (params.action) queryParams.append('action', params.action);
      if (params.category) queryParams.append('category', params.category);
      if (params.status) queryParams.append('status', params.status);
      if (params.resource_type) queryParams.append('resource_type', params.resource_type);
      if (params.date_from) queryParams.append('date_from', params.date_from);
      if (params.date_to) queryParams.append('date_to', params.date_to);

      const response = await api.get(`/audit/logs?${queryParams.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      throw error;
    }
  },

  /**
   * Obtiene un log específico por ID
   *
   * @param {number} logId - ID del log
   * @returns {Promise<Object>} - Información detallada del log
   */
  async getLog(logId) {
    try {
      const response = await api.get(`/audit/logs/${logId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching audit log ${logId}:`, error);
      throw error;
    }
  },

  /**
   * Obtiene logs de un usuario específico
   *
   * @param {number} userId - ID del usuario
   * @param {number} offset - Offset para paginación
   * @param {number} limit - Límite de resultados
   * @returns {Promise<Object>} - { user_id, username, total_logs, logs }
   */
  async getUserLogs(userId, offset = 0, limit = 50) {
    try {
      const response = await api.get(`/audit/user/${userId}?offset=${offset}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching logs for user ${userId}:`, error);
      throw error;
    }
  },

  /**
   * Obtiene estadísticas de auditoría
   *
   * @param {number} days - Número de días a consultar (1-365)
   * @returns {Promise<Object>} - Estadísticas de logs
   */
  async getStats(days = 7) {
    try {
      const response = await api.get(`/audit/stats?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching audit stats:', error);
      throw error;
    }
  },

  /**
   * Obtiene metadatos de auditoría (categorías, acciones, tipos de recursos)
   *
   * @returns {Promise<Object>} - { categories, actions, resource_types, statuses }
   */
  async getMetadata() {
    try {
      const response = await api.get('/audit/metadata');
      return response.data;
    } catch (error) {
      console.error('Error fetching audit metadata:', error);
      throw error;
    }
  },

  /**
   * Limpia logs antiguos (solo Admin)
   *
   * @param {number} days - Eliminar logs más antiguos que X días
   * @param {boolean} dryRun - Si es true, solo simula la eliminación
   * @returns {Promise<Object>} - Resultado de la limpieza
   */
  async cleanupOldLogs(days = 90, dryRun = true) {
    try {
      const response = await api.delete(`/audit/cleanup?days=${days}&dry_run=${dryRun}`);
      return response.data;
    } catch (error) {
      console.error('Error cleaning up audit logs:', error);
      throw error;
    }
  },

  /**
   * Formatea una fecha para mostrar
   *
   * @param {string} isoDate - Fecha en formato ISO
   * @returns {string} - Fecha formateada
   */
  formatDate(isoDate) {
    if (!isoDate) return 'N/A';
    const date = new Date(isoDate);
    return new Intl.DateTimeFormat('es-CO', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(date);
  },

  /**
   * Formatea una fecha relativa (hace X tiempo)
   *
   * @param {string} isoDate - Fecha en formato ISO
   * @returns {string} - Fecha relativa
   */
  formatRelativeDate(isoDate) {
    if (!isoDate) return 'N/A';

    const now = new Date();
    const date = new Date(isoDate);
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'Hace menos de 1 minuto';
    if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)} minutos`;
    if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)} horas`;
    if (seconds < 604800) return `Hace ${Math.floor(seconds / 86400)} días`;
    if (seconds < 2592000) return `Hace ${Math.floor(seconds / 604800)} semanas`;
    if (seconds < 31536000) return `Hace ${Math.floor(seconds / 2592000)} meses`;
    return `Hace ${Math.floor(seconds / 31536000)} años`;
  },

  /**
   * Obtiene el color de una categoría
   *
   * @param {string} category - Categoría
   * @returns {string} - Color
   */
  getCategoryColor(category) {
    return CATEGORY_COLORS[category] || 'gray';
  },

  /**
   * Obtiene el label de una categoría
   *
   * @param {string} category - Categoría
   * @returns {string} - Label legible
   */
  getCategoryLabel(category) {
    return CATEGORY_LABELS[category] || category;
  },

  /**
   * Obtiene el color de un estado
   *
   * @param {string} status - Estado
   * @returns {string} - Color
   */
  getStatusColor(status) {
    return STATUS_COLORS[status] || 'gray';
  },

  /**
   * Obtiene el label de un estado
   *
   * @param {string} status - Estado
   * @returns {string} - Label legible
   */
  getStatusLabel(status) {
    return STATUS_LABELS[status] || status;
  },
};

export default auditService;
