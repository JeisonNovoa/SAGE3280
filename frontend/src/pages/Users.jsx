import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  UserPlus,
  Edit,
  Trash2,
  Search,
  Filter,
  CheckCircle,
  XCircle,
  Key,
  RefreshCw
} from 'lucide-react';
import toast from 'react-hot-toast';
import usersService from '../services/usersService';
import { useAuth } from '../hooks/useAuth';
import PermissionGuard from '../components/PermissionGuard';
import ResetPasswordModal from '../components/ResetPasswordModal';

const Users = () => {
  const { hasPermission } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);

  // Filtros
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [roles, setRoles] = useState([]);

  // Paginación
  const [offset, setOffset] = useState(0);
  const [limit] = useState(50);

  // Modal de reset password
  const [resetPasswordUser, setResetPasswordUser] = useState(null);

  // Cargar roles
  useEffect(() => {
    loadRoles();
  }, []);

  // Cargar usuarios cuando cambian los filtros
  useEffect(() => {
    loadUsers();
  }, [search, roleFilter, statusFilter, offset]);

  const loadRoles = async () => {
    try {
      const data = await usersService.getRoles();
      setRoles(data);
    } catch (error) {
      console.error('Error loading roles:', error);
    }
  };

  const loadUsers = async () => {
    try {
      setLoading(true);

      const params = {
        offset,
        limit,
      };

      if (search) {
        params.search = search;
      }

      if (roleFilter) {
        params.role = roleFilter;
      }

      if (statusFilter !== 'all') {
        params.is_active = statusFilter === 'active';
      }

      const data = await usersService.getUsers(params);
      setUsers(data.users || data);
      setTotal(data.total || data.length);
    } catch (error) {
      console.error('Error loading users:', error);
      toast.error('Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (userId, currentStatus) => {
    try {
      await usersService.toggleUserActive(userId, !currentStatus);
      toast.success(currentStatus ? 'Usuario desactivado' : 'Usuario activado');
      loadUsers();
    } catch (error) {
      console.error('Error toggling user status:', error);
      toast.error('Error al cambiar estado del usuario');
    }
  };

  const handleDeleteUser = async (userId, username) => {
    if (!confirm(`¿Estás seguro de eliminar al usuario "${username}"?\n\nEsta acción no se puede deshacer.`)) {
      return;
    }

    try {
      await usersService.deleteUser(userId);
      toast.success('Usuario eliminado exitosamente');
      loadUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar usuario');
    }
  };

  const getRoleBadgeColor = (roleName) => {
    const colors = {
      admin: 'bg-purple-100 text-purple-800',
      medico: 'bg-blue-100 text-blue-800',
      auxiliar: 'bg-green-100 text-green-800',
      operador: 'bg-yellow-100 text-yellow-800',
    };
    return colors[roleName] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Usuarios</h1>
          <p className="mt-1 text-sm text-gray-500">
            Administra usuarios, roles y permisos del sistema
          </p>
        </div>

        <PermissionGuard permission="users.create">
          <Link
            to="/users/new"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <UserPlus className="w-5 h-5 mr-2" />
            Crear Usuario
          </Link>
        </PermissionGuard>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar por usuario o email..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setOffset(0);
              }}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Role Filter */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Filter className="h-5 w-5 text-gray-400" />
            </div>
            <select
              value={roleFilter}
              onChange={(e) => {
                setRoleFilter(e.target.value);
                setOffset(0);
              }}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todos los roles</option>
              {roles.map((role) => (
                <option key={role.id} value={role.name}>
                  {role.display_name}
                </option>
              ))}
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setOffset(0);
              }}
              className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Todos los estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>
        </div>

        {/* Active filters summary */}
        {(search || roleFilter || statusFilter !== 'all') && (
          <div className="mt-3 flex items-center text-sm text-gray-600">
            <span>Filtros activos:</span>
            {search && <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded">Búsqueda: {search}</span>}
            {roleFilter && <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded">Rol: {roleFilter}</span>}
            {statusFilter !== 'all' && (
              <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-800 rounded">
                Estado: {statusFilter === 'active' ? 'Activos' : 'Inactivos'}
              </span>
            )}
            <button
              onClick={() => {
                setSearch('');
                setRoleFilter('');
                setStatusFilter('all');
                setOffset(0);
              }}
              className="ml-2 text-blue-600 hover:text-blue-800"
            >
              Limpiar filtros
            </button>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="text-sm text-gray-600">
          Mostrando <span className="font-semibold">{users.length}</span> de{' '}
          <span className="font-semibold">{total}</span> usuarios
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Cargando usuarios...</p>
          </div>
        ) : users.length === 0 ? (
          <div className="text-center py-12">
            <UserPlus className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No hay usuarios</h3>
            <p className="mt-1 text-sm text-gray-500">
              {search || roleFilter || statusFilter !== 'all'
                ? 'No se encontraron usuarios con los filtros aplicados'
                : 'Comienza creando un nuevo usuario'}
            </p>
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Roles
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {user.full_name}
                      </div>
                      <div className="text-sm text-gray-500">@{user.username}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {user.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex flex-wrap gap-1">
                      {user.roles && user.roles.length > 0 ? (
                        user.roles.map((role, index) => (
                          <span
                            key={index}
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeColor(role.name)}`}
                          >
                            {role.display_name}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-gray-400">Sin roles</span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {user.is_active ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Activo
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        <XCircle className="w-3 h-3 mr-1" />
                        Inactivo
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex justify-end space-x-2">
                      {/* Edit */}
                      <PermissionGuard permission="users.update">
                        <Link
                          to={`/users/${user.id}/edit`}
                          className="text-blue-600 hover:text-blue-900"
                          title="Editar"
                        >
                          <Edit className="w-4 h-4" />
                        </Link>
                      </PermissionGuard>

                      {/* Reset Password */}
                      <PermissionGuard permission="users.update">
                        <button
                          onClick={() => setResetPasswordUser(user)}
                          className="text-yellow-600 hover:text-yellow-900"
                          title="Resetear contraseña"
                        >
                          <Key className="w-4 h-4" />
                        </button>
                      </PermissionGuard>

                      {/* Toggle Active */}
                      <PermissionGuard permission="users.update">
                        <button
                          onClick={() => handleToggleActive(user.id, user.is_active)}
                          className={user.is_active ? 'text-orange-600 hover:text-orange-900' : 'text-green-600 hover:text-green-900'}
                          title={user.is_active ? 'Desactivar' : 'Activar'}
                        >
                          <RefreshCw className="w-4 h-4" />
                        </button>
                      </PermissionGuard>

                      {/* Delete */}
                      <PermissionGuard permission="users.delete">
                        <button
                          onClick={() => handleDeleteUser(user.id, user.username)}
                          className="text-red-600 hover:text-red-900"
                          title="Eliminar"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </PermissionGuard>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Reset Password Modal */}
      {resetPasswordUser && (
        <ResetPasswordModal
          isOpen={!!resetPasswordUser}
          user={resetPasswordUser}
          onClose={() => setResetPasswordUser(null)}
          onSuccess={() => {
            setResetPasswordUser(null);
            toast.success('Contraseña reseteada exitosamente');
          }}
        />
      )}
    </div>
  );
};

export default Users;
