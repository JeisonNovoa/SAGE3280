/**
 * Token Manager
 * Gestiona el almacenamiento y recuperación de tokens JWT en localStorage
 */

const ACCESS_TOKEN_KEY = 'sage3280_access_token';
const REFRESH_TOKEN_KEY = 'sage3280_refresh_token';
const USER_KEY = 'sage3280_user';

/**
 * Decodifica un JWT sin verificar la firma
 * @param {string} token - JWT a decodificar
 * @returns {Object|null} Payload del token o null si es inválido
 */
const decodeJWT = (token) => {
  try {
    if (!token) return null;

    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const payload = parts[1];
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decoded);
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
};

/**
 * Obtiene el access token de localStorage
 * @returns {string|null}
 */
const getAccessToken = () => {
  try {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  } catch (error) {
    console.error('Error getting access token:', error);
    return null;
  }
};

/**
 * Obtiene el refresh token de localStorage
 * @returns {string|null}
 */
const getRefreshToken = () => {
  try {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  } catch (error) {
    console.error('Error getting refresh token:', error);
    return null;
  }
};

/**
 * Guarda los tokens en localStorage
 * @param {string} accessToken
 * @param {string} refreshToken
 */
const setTokens = (accessToken, refreshToken) => {
  try {
    if (accessToken) {
      localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    }
    if (refreshToken) {
      localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    }
  } catch (error) {
    console.error('Error setting tokens:', error);
  }
};

/**
 * Elimina los tokens de localStorage
 */
const clearTokens = () => {
  try {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  } catch (error) {
    console.error('Error clearing tokens:', error);
  }
};

/**
 * Verifica si un token está expirado
 * @param {string} token - JWT a verificar
 * @returns {boolean} true si está expirado, false si no
 */
const isTokenExpired = (token) => {
  try {
    const decoded = decodeJWT(token);
    if (!decoded || !decoded.exp) {
      return true;
    }

    const currentTime = Date.now() / 1000; // Convertir a segundos
    return decoded.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true;
  }
};

/**
 * Obtiene el tiempo restante hasta la expiración del token en segundos
 * @param {string} token - JWT a verificar
 * @returns {number} Segundos hasta expiración (negativo si ya expiró)
 */
const getTokenExpiresIn = (token) => {
  try {
    const decoded = decodeJWT(token);
    if (!decoded || !decoded.exp) {
      return 0;
    }

    const currentTime = Date.now() / 1000; // Convertir a segundos
    return decoded.exp - currentTime;
  } catch (error) {
    console.error('Error getting token expiration time:', error);
    return 0;
  }
};

/**
 * Obtiene información del usuario desde el token
 * @param {string} token - JWT del cual extraer info
 * @returns {Object|null} Info del usuario o null
 */
const getUserFromToken = (token) => {
  try {
    const decoded = decodeJWT(token);
    if (!decoded) return null;

    return {
      user_id: decoded.sub,
      username: decoded.username,
      email: decoded.email,
      exp: decoded.exp,
      iat: decoded.iat,
    };
  } catch (error) {
    console.error('Error getting user from token:', error);
    return null;
  }
};

/**
 * Obtiene el usuario guardado en localStorage
 * @returns {Object|null}
 */
const getUser = () => {
  try {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;

    return JSON.parse(userStr);
  } catch (error) {
    console.error('Error getting user:', error);
    return null;
  }
};

/**
 * Guarda el usuario en localStorage
 * @param {Object} user - Datos del usuario
 */
const setUser = (user) => {
  try {
    if (!user) return;

    localStorage.setItem(USER_KEY, JSON.stringify(user));
  } catch (error) {
    console.error('Error setting user:', error);
  }
};

/**
 * Elimina el usuario de localStorage
 */
const clearUser = () => {
  try {
    localStorage.removeItem(USER_KEY);
  } catch (error) {
    console.error('Error clearing user:', error);
  }
};

/**
 * Verifica si hay una sesión válida
 * @returns {boolean}
 */
const hasValidSession = () => {
  const accessToken = getAccessToken();
  if (!accessToken) return false;

  return !isTokenExpired(accessToken);
};

/**
 * Obtiene todos los datos de sesión
 * @returns {Object} { accessToken, refreshToken, user, isValid }
 */
const getSession = () => {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();
  const user = getUser();
  const isValid = hasValidSession();

  return {
    accessToken,
    refreshToken,
    user,
    isValid,
  };
};

/**
 * Limpia toda la sesión (tokens + usuario)
 */
const clearSession = () => {
  clearTokens();
  clearUser();
};

export const tokenManager = {
  // Tokens
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,

  // Usuario
  getUser,
  setUser,
  clearUser,

  // Validación
  isTokenExpired,
  getTokenExpiresIn,
  hasValidSession,

  // Utilidades
  decodeJWT,
  getUserFromToken,
  getSession,
  clearSession,
};
