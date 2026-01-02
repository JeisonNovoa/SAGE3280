import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { canAccessRoute } from '../utils/permissions';

/**
 * ProtectedRoute
 * Componente wrapper para proteger rutas que requieren autenticación
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Componente a renderizar si tiene acceso
 * @param {string|Array<string>} props.requiredPermission - Permiso(s) requerido(s)
 * @param {string|Array<string>} props.requiredRole - Rol(es) requerido(s)
 * @param {React.ReactNode} props.fallback - Componente a mostrar si no tiene acceso (opcional)
 *
 * @example
 * <ProtectedRoute requiredPermission="users.read">
 *   <UsersPage />
 * </ProtectedRoute>
 */
const ProtectedRoute = ({
  children,
  requiredPermission = null,
  requiredRole = null,
  fallback = null
}) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  // Si no está autenticado, redirigir a login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Verificar permisos/roles si se especificaron
  if (requiredPermission || requiredRole) {
    const hasAccess = canAccessRoute(user, requiredPermission, requiredRole);

    if (!hasAccess) {
      // Si se proporciona un fallback, mostrarlo
      if (fallback) {
        return fallback;
      }

      // Mostrar página de acceso denegado
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
            <div className="mb-4">
              <svg
                className="mx-auto h-16 w-16 text-red-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Acceso Denegado
            </h2>
            <p className="text-gray-600 mb-6">
              No tienes permisos para acceder a esta página.
            </p>
            <button
              onClick={() => window.history.back()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Volver
            </button>
          </div>
        </div>
      );
    }
  }

  // Usuario autenticado y con permisos, renderizar children
  return children;
};

export default ProtectedRoute;
