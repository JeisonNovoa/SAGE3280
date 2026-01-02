import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { canAccessRoute } from '../utils/permissions';

/**
 * PermissionGuard
 * Componente para mostrar/ocultar elementos basado en permisos o roles
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Elemento a mostrar si tiene acceso
 * @param {string|Array<string>} props.permission - Permiso(s) requerido(s)
 * @param {string|Array<string>} props.role - Rol(es) requerido(s)
 * @param {React.ReactNode} props.fallback - Elemento a mostrar si no tiene acceso (opcional)
 *
 * @example
 * <PermissionGuard permission="users.create">
 *   <button>Crear Usuario</button>
 * </PermissionGuard>
 *
 * @example
 * <PermissionGuard role="admin" fallback={<p>Solo admins</p>}>
 *   <AdminPanel />
 * </PermissionGuard>
 */
const PermissionGuard = ({
  children,
  permission = null,
  role = null,
  fallback = null
}) => {
  const { user, isAuthenticated } = useAuth();

  // Si no está autenticado, no mostrar nada (o fallback)
  if (!isAuthenticated) {
    return fallback || null;
  }

  // Verificar permisos/roles
  const hasAccess = canAccessRoute(user, permission, role);

  // Si no tiene acceso, mostrar fallback o nada
  if (!hasAccess) {
    return fallback || null;
  }

  // Tiene acceso, renderizar children
  return children;
};

export default PermissionGuard;
