import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Save, X, ArrowLeft, Shield } from 'lucide-react';
import toast from 'react-hot-toast';
import rolesService from '../services/rolesService';
import PermissionsTable from '../components/PermissionsTable';

const RoleForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = !!id;

  const [loading, setLoading] = useState(isEditMode);
  const [saving, setSaving] = useState(false);
  const [roleData, setRoleData] = useState(null);

  const [formData, setFormData] = useState({
    name: '',
    display_name: '',
    description: '',
    permissions: [],
    is_active: true,
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (isEditMode) {
      loadRole();
    }
  }, [id]);

  const loadRole = async () => {
    try {
      setLoading(true);
      const role = await rolesService.getRole(id);

      // No permitir editar roles del sistema
      if (role.is_system_role) {
        toast.error('No se pueden editar roles del sistema');
        navigate('/roles');
        return;
      }

      setRoleData(role);
      setFormData({
        name: role.name,
        display_name: role.display_name,
        description: role.description || '',
        permissions: role.permissions || [],
        is_active: role.is_active,
      });
    } catch (error) {
      console.error('Error loading role:', error);
      toast.error('Error al cargar rol');
      navigate('/roles');
    } finally {
      setLoading(false);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Name validation (solo en modo create)
    if (!isEditMode) {
      if (!formData.name.trim()) {
        newErrors.name = 'El nombre es requerido';
      } else if (formData.name.length < 3) {
        newErrors.name = 'El nombre debe tener al menos 3 caracteres';
      } else if (!/^[a-z0-9_]+$/.test(formData.name)) {
        newErrors.name = 'Solo se permiten letras minúsculas, números y guiones bajos';
      }
    }

    // Display name validation
    if (!formData.display_name.trim()) {
      newErrors.display_name = 'El nombre para mostrar es requerido';
    }

    // Permissions validation
    if (formData.permissions.length === 0) {
      newErrors.permissions = 'Debes asignar al menos un permiso';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Limpiar error del campo
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handlePermissionsChange = (selectedPermissions) => {
    setFormData(prev => ({
      ...prev,
      permissions: selectedPermissions
    }));

    // Limpiar error de permissions
    if (errors.permissions) {
      setErrors(prev => ({
        ...prev,
        permissions: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      toast.error('Por favor corrige los errores en el formulario');
      return;
    }

    setSaving(true);

    try {
      const payload = {
        display_name: formData.display_name,
        description: formData.description,
        permissions: formData.permissions,
        is_active: formData.is_active,
      };

      if (!isEditMode) {
        payload.name = formData.name;
      }

      if (isEditMode) {
        await rolesService.updateRole(id, payload);
        toast.success('Rol actualizado exitosamente');
      } else {
        await rolesService.createRole(payload);
        toast.success('Rol creado exitosamente');
      }

      navigate('/roles');
    } catch (error) {
      console.error('Error saving role:', error);
      const errorMessage = error.response?.data?.detail || 'Error al guardar rol';
      toast.error(errorMessage);

      // Manejar errores específicos del backend
      if (error.response?.data?.detail?.includes('name')) {
        setErrors(prev => ({ ...prev, name: 'Este nombre ya existe' }));
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/roles"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          Volver a roles
        </Link>
        <div className="flex items-center">
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
            <Shield className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {isEditMode ? 'Editar Rol' : 'Crear Nuevo Rol'}
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              {isEditMode
                ? `Actualiza la información del rol "${formData.display_name}"`
                : 'Completa la información para crear un nuevo rol custom'}
            </p>
          </div>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info Card */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Información Básica
          </h2>

          <div className="space-y-4">
            {/* Name (solo en modo create) */}
            {!isEditMode && (
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre (identificador) <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className={`block w-full px-3 py-2 border ${
                    errors.name ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="supervisor_calidad"
                />
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600">{errors.name}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  Solo minúsculas, números y guiones bajos (ej: supervisor_calidad)
                </p>
              </div>
            )}

            {/* Display Name */}
            <div>
              <label htmlFor="display_name" className="block text-sm font-medium text-gray-700 mb-2">
                Nombre para Mostrar <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="display_name"
                name="display_name"
                value={formData.display_name}
                onChange={handleChange}
                className={`block w-full px-3 py-2 border ${
                  errors.display_name ? 'border-red-300' : 'border-gray-300'
                } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                placeholder="Supervisor de Calidad"
              />
              {errors.display_name && (
                <p className="mt-1 text-sm text-red-600">{errors.display_name}</p>
              )}
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                id="description"
                name="description"
                rows="3"
                value={formData.description}
                onChange={handleChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Describe el propósito de este rol..."
              />
            </div>

            {/* Active Status */}
            <div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Rol activo
                </span>
              </label>
              <p className="mt-1 text-xs text-gray-500 ml-6">
                Los roles inactivos no pueden ser asignados a usuarios
              </p>
            </div>
          </div>
        </div>

        {/* Permissions Card */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">
                Permisos <span className="text-red-500">*</span>
              </h2>
              <p className="text-sm text-gray-500 mt-1">
                Selecciona los permisos que tendrá este rol ({formData.permissions.length} seleccionados)
              </p>
            </div>
          </div>

          {errors.permissions && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{errors.permissions}</p>
            </div>
          )}

          <PermissionsTable
            selectedPermissions={formData.permissions}
            onChange={handlePermissionsChange}
            mode="edit"
          />
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 bg-white rounded-lg shadow p-6">
          <button
            type="button"
            onClick={() => navigate('/roles')}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <X className="w-4 h-4 inline mr-2" />
            Cancelar
          </button>
          <button
            type="submit"
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? (
              <>
                <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Guardando...
              </>
            ) : (
              <>
                <Save className="w-4 h-4 inline mr-2" />
                {isEditMode ? 'Actualizar Rol' : 'Crear Rol'}
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RoleForm;
