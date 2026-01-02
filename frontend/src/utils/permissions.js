/**
 * Permissions Utilities
 * Funciones helper para verificar permisos de usuarios
 */

/**
 * Verifica si un usuario tiene un permiso específico
 * @param {Object} user - Usuario con array de permissions
 * @param {string} permission - Permiso a verificar (ej: "users.create")
 * @returns {boolean}
 */
export const hasPermission = (user, permission) => {
  if (!user || !user.permissions || !Array.isArray(user.permissions)) {
    return false;
  }

  // Si el usuario tiene el wildcard "*", tiene todos los permisos
  if (user.permissions.includes('*')) {
    return true;
  }

  return user.permissions.includes(permission);
};

/**
 * Verifica si un usuario tiene al menos uno de los permisos especificados
 * @param {Object} user - Usuario con array de permissions
 * @param {Array<string>} permissions - Array de permisos (OR logic)
 * @returns {boolean}
 */
export const hasAnyPermission = (user, permissions) => {
  if (!permissions || !Array.isArray(permissions) || permissions.length === 0) {
    return true; // Sin restricciones
  }

  return permissions.some(permission => hasPermission(user, permission));
};

/**
 * Verifica si un usuario tiene todos los permisos especificados
 * @param {Object} user - Usuario con array de permissions
 * @param {Array<string>} permissions - Array de permisos (AND logic)
 * @returns {boolean}
 */
export const hasAllPermissions = (user, permissions) => {
  if (!permissions || !Array.isArray(permissions) || permissions.length === 0) {
    return true; // Sin restricciones
  }

  return permissions.every(permission => hasPermission(user, permission));
};

/**
 * Verifica si un usuario tiene un rol específico
 * @param {Object} user - Usuario con array de roles
 * @param {string} roleName - Nombre del rol (ej: "admin", "medico")
 * @returns {boolean}
 */
export const hasRole = (user, roleName) => {
  if (!user || !user.roles || !Array.isArray(user.roles)) {
    return false;
  }

  return user.roles.some(role => role.name === roleName);
};

/**
 * Verifica si un usuario tiene al menos uno de los roles especificados
 * @param {Object} user - Usuario con array de roles
 * @param {Array<string>} roleNames - Array de nombres de roles (OR logic)
 * @returns {boolean}
 */
export const hasAnyRole = (user, roleNames) => {
  if (!roleNames || !Array.isArray(roleNames) || roleNames.length === 0) {
    return true; // Sin restricciones
  }

  return roleNames.some(roleName => hasRole(user, roleName));
};

/**
 * Verifica si un usuario tiene todos los roles especificados
 * @param {Object} user - Usuario con array de roles
 * @param {Array<string>} roleNames - Array de nombres de roles (AND logic)
 * @returns {boolean}
 */
export const hasAllRoles = (user, roleNames) => {
  if (!roleNames || !Array.isArray(roleNames) || roleNames.length === 0) {
    return true; // Sin restricciones
  }

  return roleNames.every(roleName => hasRole(user, roleName));
};

/**
 * Obtiene los nombres de los roles de un usuario
 * @param {Object} user - Usuario con array de roles
 * @returns {Array<string>}
 */
export const getUserRoleNames = (user) => {
  if (!user || !user.roles || !Array.isArray(user.roles)) {
    return [];
  }

  return user.roles.map(role => role.name);
};

/**
 * Obtiene los display names de los roles de un usuario
 * @param {Object} user - Usuario con array de roles
 * @returns {Array<string>}
 */
export const getUserRoleDisplayNames = (user) => {
  if (!user || !user.roles || !Array.isArray(user.roles)) {
    return [];
  }

  return user.roles.map(role => role.display_name || role.name);
};

/**
 * Verifica si un usuario es administrador
 * @param {Object} user - Usuario
 * @returns {boolean}
 */
export const isAdmin = (user) => {
  return hasRole(user, 'admin') || hasPermission(user, '*');
};

/**
 * Verifica si un usuario puede acceder a una ruta
 * @param {Object} user - Usuario
 * @param {string|Array<string>} requiredPermission - Permiso(s) requerido(s)
 * @param {string|Array<string>} requiredRole - Rol(es) requerido(s)
 * @returns {boolean}
 */
export const canAccessRoute = (user, requiredPermission = null, requiredRole = null) => {
  // Si no hay restricciones, permitir acceso
  if (!requiredPermission && !requiredRole) {
    return true;
  }

  // Verificar permisos
  if (requiredPermission) {
    if (Array.isArray(requiredPermission)) {
      if (!hasAnyPermission(user, requiredPermission)) {
        return false;
      }
    } else {
      if (!hasPermission(user, requiredPermission)) {
        return false;
      }
    }
  }

  // Verificar roles
  if (requiredRole) {
    if (Array.isArray(requiredRole)) {
      if (!hasAnyRole(user, requiredRole)) {
        return false;
      }
    } else {
      if (!hasRole(user, requiredRole)) {
        return false;
      }
    }
  }

  return true;
};
