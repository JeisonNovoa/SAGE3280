import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Shield,
  Plus,
  Edit,
  Trash2,
  Search,
  ChevronDown,
  ChevronUp,
  Users as UsersIcon,
  Lock,
  Unlock,
  AlertTriangle
} from 'lucide-react';
import toast from 'react-hot-toast';
import rolesService from '../services/rolesService';
import { useAuth } from '../hooks/useAuth';
import PermissionGuard from '../components/PermissionGuard';

const Roles = () => {
  const { hasPermission } = useAuth();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [expandedRole, setExpandedRole] = useState(null);
  const [roleStats, setRoleStats] = useState({});

  useEffect(() => {
    loadRoles();
  }, [search]);

  const loadRoles = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) {
        params.search = search;
      }

      const data = await rolesService.getRoles(params);
      setRoles(data.roles || data);

      // Cargar estadísticas de usuarios por rol
      await loadRoleStats(data.roles || data);
    } catch (error) {
      console.error('Error loading roles:', error);
      toast.error('Error al cargar roles');
    } finally {
      setLoading(false);
    }
  };

  const loadRoleStats = async (rolesList) => {
    const stats = {};
    for (const role of rolesList) {
      try {
        const roleStat = await rolesService.getRoleStats(role.id);
        stats[role.id] = roleStat;
      } catch (error) {
        stats[role.id] = { users_count: 0 };
      }
    }
    setRoleStats(stats);
  };

  const handleDeleteRole = async (roleId, roleName, isSystemRole) => {
    if (isSystemRole) {
      toast.error('No se pueden eliminar roles del sistema');
      return;
    }

    const usersCount = roleStats[roleId]?.users_count || 0;
    if (usersCount > 0) {
      toast.error(`No se puede eliminar. ${usersCount} usuario(s) tienen este rol`);
      return;
    }

    if (!confirm(`¿Estás seguro de eliminar el rol "${roleName}"?\n\nEsta acción no se puede deshacer.`)) {
      return;
    }

    try {
      await rolesService.deleteRole(roleId);
      toast.success('Rol eliminado exitosamente');
      loadRoles();
    } catch (error) {
      console.error('Error deleting role:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar rol');
    }
  };

  const toggleExpanded = (roleId) => {
    setExpandedRole(expandedRole === roleId ? null : roleId);
  };

  const getRoleBadgeColor = (roleName) => {
    const colors = {
      admin: 'bg-purple-100 text-purple-800 border-purple-300',
      medico: 'bg-blue-100 text-blue-800 border-blue-300',
      auxiliar: 'bg-green-100 text-green-800 border-green-300',
      operador: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    };
    return colors[roleName] || 'bg-gray-100 text-gray-800 border-gray-300';
  };

  const getPermissionCategoryColor = (permission) => {
    const category = permission.split('.')[0];
    return rolesService.getCategoryColor(category);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Roles</h1>
          <p className="mt-1 text-sm text-gray-500">
            Administra roles y permisos del sistema (33 permisos disponibles)
          </p>
        </div>

        <PermissionGuard permission="roles.create">
          <Link
            to="/roles/new"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5 mr-2" />
            Crear Rol
          </Link>
        </PermissionGuard>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Buscar por nombre de rol..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Roles List */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Cargando roles...</p>
        </div>
      ) : roles.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <Shield className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay roles</h3>
          <p className="mt-1 text-sm text-gray-500">
            {search ? 'No se encontraron roles con ese nombre' : 'Comienza creando un nuevo rol'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {roles.map((role) => {
            const isSystemRole = role.is_system_role;
            const isExpanded = expandedRole === role.id;
            const usersCount = roleStats[role.id]?.users_count || 0;
            const permissionsCount = role.permissions?.length || 0;
            const hasWildcard = role.permissions?.includes('*');

            return (
              <div
                key={role.id}
                className="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
              >
                {/* Role Header */}
                <div className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getRoleBadgeColor(role.name)}`}>
                          <Shield className="w-5 h-5" />
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            {role.display_name}
                          </h3>
                          <p className="text-sm text-gray-500">@{role.name}</p>
                        </div>
                        {isSystemRole && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                            <Lock className="w-3 h-3 mr-1" />
                            Sistema
                          </span>
                        )}
                        {!role.is_active && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Inactivo
                          </span>
                        )}
                      </div>

                      {role.description && (
                        <p className="mt-2 text-sm text-gray-600">
                          {role.description}
                        </p>
                      )}

                      <div className="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                        <span className="flex items-center">
                          <UsersIcon className="w-4 h-4 mr-1" />
                          {usersCount} {usersCount === 1 ? 'usuario' : 'usuarios'}
                        </span>
                        <span className="flex items-center">
                          <Shield className="w-4 h-4 mr-1" />
                          {hasWildcard ? 'Todos los permisos (*)' : `${permissionsCount} permisos`}
                        </span>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center space-x-2 ml-4">
                      {/* Ver permisos */}
                      <button
                        onClick={() => toggleExpanded(role.id)}
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                        title={isExpanded ? 'Ocultar permisos' : 'Ver permisos'}
                      >
                        {isExpanded ? (
                          <ChevronUp className="w-5 h-5" />
                        ) : (
                          <ChevronDown className="w-5 h-5" />
                        )}
                      </button>

                      {/* Edit (solo roles custom) */}
                      {!isSystemRole && (
                        <PermissionGuard permission="roles.update">
                          <Link
                            to={`/roles/${role.id}/edit`}
                            className="p-2 text-blue-600 hover:text-blue-800 transition-colors"
                            title="Editar"
                          >
                            <Edit className="w-5 h-5" />
                          </Link>
                        </PermissionGuard>
                      )}

                      {/* Delete (solo roles custom sin usuarios) */}
                      {!isSystemRole && (
                        <PermissionGuard permission="roles.delete">
                          <button
                            onClick={() => handleDeleteRole(role.id, role.display_name, isSystemRole)}
                            className="p-2 text-red-600 hover:text-red-800 transition-colors disabled:opacity-50"
                            disabled={usersCount > 0}
                            title={usersCount > 0 ? `No se puede eliminar (${usersCount} usuarios)` : 'Eliminar'}
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </PermissionGuard>
                      )}

                      {/* Lock icon for system roles */}
                      {isSystemRole && (
                        <div className="p-2 text-gray-400" title="Rol del sistema (no editable)">
                          <Lock className="w-5 h-5" />
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Warning if role has users */}
                  {!isSystemRole && usersCount > 0 && (
                    <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start">
                      <AlertTriangle className="w-4 h-4 text-yellow-600 mr-2 mt-0.5" />
                      <p className="text-sm text-yellow-800">
                        Este rol tiene {usersCount} usuario(s) asignado(s). No se puede eliminar mientras tenga usuarios.
                      </p>
                    </div>
                  )}
                </div>

                {/* Expanded Permissions */}
                {isExpanded && (
                  <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
                    <h4 className="text-sm font-medium text-gray-900 mb-3">
                      Permisos asignados:
                    </h4>

                    {hasWildcard ? (
                      <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
                        <Shield className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-purple-900">
                          Acceso Total (*)
                        </p>
                        <p className="text-xs text-purple-700 mt-1">
                          Este rol tiene acceso a todos los permisos del sistema
                        </p>
                      </div>
                    ) : permissionsCount === 0 ? (
                      <p className="text-sm text-gray-500 italic">
                        No tiene permisos asignados
                      </p>
                    ) : (
                      <div className="flex flex-wrap gap-2">
                        {role.permissions.map((permission, index) => (
                          <span
                            key={index}
                            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getPermissionCategoryColor(permission)}`}
                          >
                            {permission}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Info */}
      {!loading && roles.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <Shield className="h-5 w-5 text-blue-600" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-900">
                Información sobre roles
              </h3>
              <div className="mt-2 text-sm text-blue-800">
                <ul className="list-disc list-inside space-y-1">
                  <li>Los roles del sistema (Admin, Médico, Auxiliar, Operador) no se pueden editar ni eliminar</li>
                  <li>Los roles custom pueden ser editados y eliminados si no tienen usuarios asignados</li>
                  <li>El permiso wildcard (*) otorga acceso total al sistema</li>
                  <li>Hay 33 permisos disponibles organizados en 9 categorías</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Roles;
