import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

export default api;
