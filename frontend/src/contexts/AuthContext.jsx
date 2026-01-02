import React, { createContext, useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';
import { tokenManager } from '../utils/tokenManager';
import toast from 'react-hot-toast';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const refreshTimerRef = useRef(null);

  // Cargar usuario desde localStorage al iniciar
  useEffect(() => {
    initializeAuth();
  }, []);

  // Inicializar autenticación desde localStorage
  const initializeAuth = async () => {
    try {
      setIsLoading(true);

      const accessToken = tokenManager.getAccessToken();
      const savedUser = tokenManager.getUser();

      if (!accessToken || !savedUser) {
        // No hay sesión guardada
        setIsLoading(false);
        return;
      }

      // Verificar si el token está expirado
      if (tokenManager.isTokenExpired(accessToken)) {
        // Intentar refresh
        const refreshed = await handleRefreshToken();
        if (!refreshed) {
          // Refresh falló, limpiar sesión
          clearSession();
          setIsLoading(false);
          return;
        }
      }

      // Restaurar sesión
      setUser(savedUser);
      setIsAuthenticated(true);

      // Configurar auto-refresh
      scheduleTokenRefresh();

    } catch (error) {
      console.error('Error initializing auth:', error);
      clearSession();
    } finally {
      setIsLoading(false);
    }
  };

  // Login
  const login = async (username, password) => {
    try {
      setIsLoading(true);

      const response = await authService.login(username, password);

      if (!response.success) {
        throw new Error(response.message || 'Login failed');
      }

      const { access_token, refresh_token, user: userData } = response.data;

      // Guardar tokens y usuario
      tokenManager.setTokens(access_token, refresh_token);
      tokenManager.setUser(userData);

      // Actualizar estado
      setUser(userData);
      setIsAuthenticated(true);

      // Configurar auto-refresh
      scheduleTokenRefresh();

      toast.success(`Bienvenido, ${userData.full_name || userData.username}!`);

      return { success: true };
    } catch (error) {
      console.error('Login error:', error);

      let errorMessage = 'Error al iniciar sesión';

      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast.error(errorMessage);

      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  // Logout
  const logout = async () => {
    try {
      const accessToken = tokenManager.getAccessToken();
      const refreshToken = tokenManager.getRefreshToken();

      // Intentar invalidar tokens en el backend
      if (accessToken && refreshToken) {
        try {
          await authService.logout(accessToken, refreshToken);
        } catch (error) {
          console.warn('Error during logout API call:', error);
          // Continuar con logout local incluso si falla el backend
        }
      }

      // Limpiar sesión local
      clearSession();

      toast.success('Sesión cerrada exitosamente');
      navigate('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Forzar limpieza local incluso si hay error
      clearSession();
      navigate('/login');
    }
  };

  // Limpiar sesión
  const clearSession = () => {
    // Cancelar timer de refresh
    if (refreshTimerRef.current) {
      clearTimeout(refreshTimerRef.current);
      refreshTimerRef.current = null;
    }

    // Limpiar tokens y usuario
    tokenManager.clearTokens();
    tokenManager.clearUser();

    // Actualizar estado
    setUser(null);
    setIsAuthenticated(false);
  };

  // Refresh token
  const handleRefreshToken = async () => {
    try {
      const refreshToken = tokenManager.getRefreshToken();

      if (!refreshToken) {
        return false;
      }

      const response = await authService.refreshToken(refreshToken);

      if (!response.success) {
        return false;
      }

      const { access_token, refresh_token: newRefreshToken } = response.data;

      // Actualizar tokens
      tokenManager.setTokens(access_token, newRefreshToken);

      // Reprogramar auto-refresh
      scheduleTokenRefresh();

      return true;
    } catch (error) {
      console.error('Refresh token error:', error);
      return false;
    }
  };

  // Programar auto-refresh del token
  const scheduleTokenRefresh = useCallback(() => {
    // Cancelar timer anterior si existe
    if (refreshTimerRef.current) {
      clearTimeout(refreshTimerRef.current);
    }

    const accessToken = tokenManager.getAccessToken();

    if (!accessToken) {
      return;
    }

    const expiresIn = tokenManager.getTokenExpiresIn(accessToken);

    if (expiresIn <= 0) {
      // Token ya expirado, hacer refresh inmediato
      handleRefreshToken();
      return;
    }

    // Programar refresh 5 minutos antes de expirar (o a la mitad del tiempo si expira en menos de 10 min)
    const refreshTime = expiresIn > 600 ? expiresIn - 300 : expiresIn / 2;
    const refreshDelay = refreshTime * 1000; // Convertir a milisegundos

    refreshTimerRef.current = setTimeout(async () => {
      const refreshed = await handleRefreshToken();

      if (!refreshed) {
        // Refresh falló, cerrar sesión
        toast.error('Tu sesión ha expirado. Por favor inicia sesión nuevamente.');
        clearSession();
        navigate('/login');
      }
    }, refreshDelay);

  }, [navigate]);

  // Actualizar usuario (después de editar perfil)
  const updateUser = (updatedUserData) => {
    const updatedUser = { ...user, ...updatedUserData };
    setUser(updatedUser);
    tokenManager.setUser(updatedUser);
  };

  // Obtener usuario actual del backend
  const fetchCurrentUser = async () => {
    try {
      const response = await authService.getCurrentUser();

      if (response.success) {
        setUser(response.data);
        tokenManager.setUser(response.data);
        return { success: true, data: response.data };
      }

      return { success: false };
    } catch (error) {
      console.error('Error fetching current user:', error);
      return { success: false, error };
    }
  };

  // Cambiar contraseña
  const changePassword = async (currentPassword, newPassword) => {
    try {
      const response = await authService.changePassword(currentPassword, newPassword);

      if (response.success) {
        toast.success('Contraseña cambiada exitosamente');
        return { success: true };
      }

      throw new Error(response.message || 'Error al cambiar contraseña');
    } catch (error) {
      console.error('Change password error:', error);

      let errorMessage = 'Error al cambiar contraseña';

      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast.error(errorMessage);

      return { success: false, error: errorMessage };
    }
  };

  // Verificar si el usuario tiene un permiso específico
  const hasPermission = (permission) => {
    if (!user || !user.permissions) {
      return false;
    }

    // Si el usuario tiene permiso wildcard "*", tiene todos los permisos
    if (user.permissions.includes('*')) {
      return true;
    }

    return user.permissions.includes(permission);
  };

  // Verificar si el usuario tiene alguno de los permisos especificados
  const hasAnyPermission = (permissions) => {
    if (!permissions || permissions.length === 0) {
      return true;
    }

    return permissions.some(permission => hasPermission(permission));
  };

  // Verificar si el usuario tiene todos los permisos especificados
  const hasAllPermissions = (permissions) => {
    if (!permissions || permissions.length === 0) {
      return true;
    }

    return permissions.every(permission => hasPermission(permission));
  };

  // Verificar si el usuario tiene un rol específico
  const hasRole = (roleName) => {
    if (!user || !user.roles) {
      return false;
    }

    return user.roles.some(role => role.name === roleName);
  };

  const value = {
    // Estado
    user,
    isAuthenticated,
    isLoading,

    // Funciones de autenticación
    login,
    logout,
    updateUser,
    fetchCurrentUser,
    changePassword,
    refreshToken: handleRefreshToken,

    // Funciones de permisos
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
