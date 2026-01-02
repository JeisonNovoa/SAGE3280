import axios from 'axios';
import { tokenManager } from '../utils/tokenManager';
import { authService } from './authService';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Variable para controlar refresh en progreso (evitar race conditions)
let isRefreshing = false;
// Cola de requests que esperan el refresh
let refreshQueue = [];

/**
 * Procesa la cola de requests después de un refresh exitoso
 * @param {string} token - Nuevo access token
 */
const processQueue = (error, token = null) => {
  refreshQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else {
      promise.resolve(token);
    }
  });

  refreshQueue = [];
};

// REQUEST INTERCEPTOR: Agregar token de autorización
api.interceptors.request.use(
  (config) => {
    const accessToken = tokenManager.getAccessToken();

    if (accessToken && !config.headers['Authorization']) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// RESPONSE INTERCEPTOR: Manejo de errores 401 y auto-refresh
api.interceptors.response.use(
  (response) => {
    // Respuesta exitosa, retornar directamente
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Si no es un error 401, o ya se intentó refresh, rechazar
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    // Si ya hay un refresh en progreso, agregar a la cola
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({ resolve, reject });
      })
        .then((token) => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          return api(originalRequest);
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    }

    // Marcar que se intentará refresh
    originalRequest._retry = true;
    isRefreshing = true;

    const refreshToken = tokenManager.getRefreshToken();

    if (!refreshToken) {
      // No hay refresh token, limpiar sesión y rechazar
      isRefreshing = false;
      tokenManager.clearSession();
      processQueue(new Error('No refresh token available'));

      // Redirigir a login si estamos en el navegador
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }

      return Promise.reject(error);
    }

    try {
      // Intentar refresh
      const response = await authService.refreshToken(refreshToken);

      if (!response.success) {
        throw new Error('Refresh failed');
      }

      const { access_token, refresh_token: newRefreshToken } = response.data;

      // Guardar nuevos tokens
      tokenManager.setTokens(access_token, newRefreshToken);

      // Procesar cola de requests
      processQueue(null, access_token);

      // Reintentar request original con nuevo token
      originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
      return api(originalRequest);
    } catch (refreshError) {
      // Refresh falló, limpiar sesión
      processQueue(refreshError);
      tokenManager.clearSession();

      // Redirigir a login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }

      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

// Upload service
export const uploadService = {
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getUploadStatus: async (uploadId) => {
    const response = await api.get(`/upload/${uploadId}`);
    return response.data;
  },

  getUploadStats: async (uploadId) => {
    const response = await api.get(`/upload/${uploadId}/stats`);
    return response.data;
  },
};

// Patients service
export const patientsService = {
  getPatients: async (params = {}) => {
    const response = await api.get('/patients/', { params });
    return response.data;
  },

  getPatient: async (patientId) => {
    const response = await api.get(`/patients/${patientId}`);
    return response.data;
  },

  getPatientByDocument: async (documentNumber) => {
    const response = await api.get(`/patients/document/${documentNumber}`);
    return response.data;
  },

  updateContactStatus: async (patientId, contactStatus, notes = null) => {
    const response = await api.put(`/patients/${patientId}/contact`, {
      contact_status: contactStatus,
      notes,
    });
    return response.data;
  },

  getPriorityList: async (limit = 100, minPriority = 50) => {
    const response = await api.get('/patients/list/priority', {
      params: { limit, min_priority: minPriority },
    });
    return response.data;
  },
};

// Stats service
export const statsService = {
  getDashboardStats: async () => {
    const response = await api.get('/stats/dashboard');
    return response.data;
  },

  getSummaryStats: async () => {
    const response = await api.get('/stats/summary');
    return response.data;
  },
};

// Controls service
export const controlsService = {
  getControls: async (params = {}) => {
    const response = await api.get('/controls/', { params });
    return response.data;
  },

  getControl: async (controlId) => {
    const response = await api.get(`/controls/${controlId}`);
    return response.data;
  },

  updateControl: async (controlId, data) => {
    const response = await api.put(`/controls/${controlId}`, data);
    return response.data;
  },

  getControlsStats: async () => {
    const response = await api.get('/controls/stats/summary');
    return response.data;
  },
};

// Alerts service
export const alertsService = {
  getAlerts: async (params = {}) => {
    const response = await api.get('/alerts/', { params });
    return response.data;
  },

  getAlert: async (alertId) => {
    const response = await api.get(`/alerts/${alertId}`);
    return response.data;
  },

  updateAlert: async (alertId, data) => {
    const response = await api.put(`/alerts/${alertId}`, data);
    return response.data;
  },

  dismissAlert: async (alertId) => {
    const response = await api.delete(`/alerts/${alertId}`);
    return response.data;
  },

  getAlertsStats: async () => {
    const response = await api.get('/alerts/stats/summary');
    return response.data;
  },
};

// Export service
export const exportService = {
  exportPatients: async (params = {}) => {
    const response = await api.get('/export/patients', {
      params,
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const filename = params.format === 'csv'
      ? 'pacientes_sage3280.csv'
      : 'pacientes_sage3280.xlsx';

    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  exportControls: async (controlType, params = {}) => {
    const response = await api.get('/export/controls', {
      params: { control_type: controlType, ...params },
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const filename = params.format === 'csv'
      ? `controles_${controlType}_sage3280.csv`
      : `controles_${controlType}_sage3280.xlsx`;

    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  exportAlerts: async (alertType, params = {}) => {
    const response = await api.get('/export/alerts', {
      params: { alert_type: alertType, ...params },
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const filename = params.format === 'csv'
      ? `alertas_${alertType}_sage3280.csv`
      : `alertas_${alertType}_sage3280.xlsx`;

    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};

// Admin service
export const adminService = {
  getDatabaseStats: async () => {
    const response = await api.get('/admin/database-stats');
    return response.data;
  },

  listUploads: async () => {
    const response = await api.get('/admin/uploads');
    return response.data;
  },

  deleteAllPatients: async () => {
    const response = await api.delete('/admin/patients/all', {
      params: { confirm: 'YES_DELETE_ALL_PATIENTS' },
    });
    return response.data;
  },

  deletePatientsByUpload: async (uploadId) => {
    const response = await api.delete(`/admin/patients/upload/${uploadId}`);
    return response.data;
  },

  clearDatabase: async () => {
    const response = await api.delete('/admin/clear-database', {
      params: { confirm: 'YES_DELETE_ALL_DATA' },
    });
    return response.data;
  },
};

export default api;
