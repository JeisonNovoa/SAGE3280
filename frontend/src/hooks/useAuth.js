import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

/**
 * Hook personalizado para acceder al contexto de autenticación
 *
 * @returns {Object} Contexto de autenticación con:
 *   - user: Usuario actual
 *   - isAuthenticated: Boolean indicando si hay sesión activa
 *   - isLoading: Boolean indicando si se está cargando la sesión
 *   - login: Función para iniciar sesión
 *   - logout: Función para cerrar sesión
 *   - updateUser: Función para actualizar datos del usuario
 *   - fetchCurrentUser: Función para obtener usuario actual del backend
 *   - changePassword: Función para cambiar contraseña
 *   - refreshToken: Función para renovar el access token
 *   - hasPermission: Función para verificar si tiene un permiso
 *   - hasAnyPermission: Función para verificar si tiene alguno de varios permisos
 *   - hasAllPermissions: Función para verificar si tiene todos los permisos
 *   - hasRole: Función para verificar si tiene un rol específico
 *
 * @throws {Error} Si se usa fuera del AuthProvider
 *
 * @example
 * const { user, login, logout, hasPermission } = useAuth();
 *
 * if (hasPermission('users.create')) {
 *   // Mostrar botón crear usuario
 * }
 */
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      'useAuth must be used within an AuthProvider. ' +
      'Make sure your component is wrapped with <AuthProvider>.'
    );
  }

  return context;
};
