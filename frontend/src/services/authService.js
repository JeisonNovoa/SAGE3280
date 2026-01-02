import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Auth Service
 * Maneja las llamadas a los endpoints de autenticación
 * Nota: Este servicio NO usa la instancia axios de api.js para evitar dependencias circulares
 */

/**
 * Login - Inicia sesión con username y password
 * @param {string} username
 * @param {string} password
 * @returns {Promise<Object>} { success, data: { access_token, refresh_token, user }, message }
 */
const login = async (username, password) => {
  try {
    const response = await axios.post(
      `${API_URL}/auth/login`,
      { username, password },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Login error:', error);

    return {
      success: false,
      message: error.response?.data?.detail || 'Error al iniciar sesión',
      error,
    };
  }
};

/**
 * Logout - Cierra sesión e invalida tokens
 * @param {string} accessToken
 * @param {string} refreshToken
 * @returns {Promise<Object>} { success, message }
 */
const logout = async (accessToken, refreshToken) => {
  try {
    const response = await axios.post(
      `${API_URL}/auth/logout`,
      { refresh_token: refreshToken },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
      }
    );

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Logout error:', error);

    return {
      success: false,
      message: error.response?.data?.detail || 'Error al cerrar sesión',
      error,
    };
  }
};

/**
 * Refresh Token - Renueva el access token usando el refresh token
 * @param {string} refreshToken
 * @returns {Promise<Object>} { success, data: { access_token, refresh_token }, message }
 */
const refreshToken = async (refreshToken) => {
  try {
    const response = await axios.post(
      `${API_URL}/auth/refresh`,
      { refresh_token: refreshToken },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Refresh token error:', error);

    return {
      success: false,
      message: error.response?.data?.detail || 'Error al renovar token',
      error,
    };
  }
};

/**
 * Get Current User - Obtiene los datos del usuario autenticado
 * Nota: El token se agrega automáticamente por el interceptor de api.js
 * @returns {Promise<Object>} { success, data: user, message }
 */
const getCurrentUser = async () => {
  try {
    const response = await axios.get(`${API_URL}/auth/me`);

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Get current user error:', error);

    return {
      success: false,
      message: error.response?.data?.detail || 'Error al obtener usuario',
      error,
    };
  }
};

/**
 * Change Password - Cambia la contraseña del usuario autenticado
 * Nota: El token se agrega automáticamente por el interceptor de api.js
 * @param {string} currentPassword
 * @param {string} newPassword
 * @returns {Promise<Object>} { success, message }
 */
const changePassword = async (currentPassword, newPassword) => {
  try {
    const response = await axios.post(
      `${API_URL}/auth/change-password`,
      {
        current_password: currentPassword,
        new_password: newPassword,
      }
    );

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Change password error:', error);

    return {
      success: false,
      message: error.response?.data?.detail || 'Error al cambiar contraseña',
      error,
    };
  }
};

/**
 * Validate Token - Verifica si un token es válido
 * @param {string} accessToken
 * @returns {Promise<Object>} { success, valid, message }
 */
const validateToken = async (accessToken) => {
  try {
    const response = await axios.get(
      `${API_URL}/auth/validate`,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      }
    );

    return {
      success: true,
      valid: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Validate token error:', error);

    return {
      success: false,
      valid: false,
      message: error.response?.data?.detail || 'Token inválido',
      error,
    };
  }
};

export const authService = {
  login,
  logout,
  refreshToken,
  getCurrentUser,
  changePassword,
  validateToken,
};
