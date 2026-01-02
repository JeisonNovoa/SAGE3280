import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Save, X, ArrowLeft, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';
import usersService from '../services/usersService';

const UserForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = !!id;

  const [loading, setLoading] = useState(isEditMode);
  const [saving, setSaving] = useState(false);
  const [roles, setRoles] = useState([]);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    confirmPassword: '',
    role_ids: [],
    is_active: true,
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    loadRoles();
    if (isEditMode) {
      loadUser();
    }
  }, [id]);

  const loadRoles = async () => {
    try {
      const data = await usersService.getRoles();
      setRoles(data);
    } catch (error) {
      console.error('Error loading roles:', error);
      toast.error('Error al cargar roles');
    }
  };

  const loadUser = async () => {
    try {
      setLoading(true);
      const user = await usersService.getUser(id);
      setFormData({
        username: user.username,
        email: user.email,
        full_name: user.full_name || '',
        password: '',
        confirmPassword: '',
        role_ids: user.roles ? user.roles.map(r => r.id) : [],
        is_active: user.is_active,
      });
    } catch (error) {
      console.error('Error loading user:', error);
      toast.error('Error al cargar usuario');
      navigate('/users');
    } finally {
      setLoading(false);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Username validation (solo en modo create)
    if (!isEditMode) {
      if (!formData.username.trim()) {
        newErrors.username = 'El usuario es requerido';
      } else if (formData.username.length < 3) {
        newErrors.username = 'El usuario debe tener al menos 3 caracteres';
      } else if (!/^[a-zA-Z0-9._-]+$/.test(formData.username)) {
        newErrors.username = 'Solo se permiten letras, números, puntos, guiones y guiones bajos';
      }
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    // Full name validation
    if (!formData.full_name.trim()) {
      newErrors.full_name = 'El nombre completo es requerido';
    }

    // Password validation (solo en modo create o si se ingresó password en edit)
    if (!isEditMode || formData.password) {
      if (!formData.password) {
        newErrors.password = 'La contraseña es requerida';
      } else if (formData.password.length < 8) {
        newErrors.password = 'La contraseña debe tener al menos 8 caracteres';
      } else if (!/[A-Z]/.test(formData.password)) {
        newErrors.password = 'La contraseña debe contener al menos una mayúscula';
      } else if (!/[a-z]/.test(formData.password)) {
        newErrors.password = 'La contraseña debe contener al menos una minúscula';
      } else if (!/[0-9]/.test(formData.password)) {
        newErrors.password = 'La contraseña debe contener al menos un número';
      }

      if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Las contraseñas no coinciden';
      }
    }

    // Role validation
    if (formData.role_ids.length === 0) {
      newErrors.roles = 'Debes asignar al menos un rol';
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

  const handleRoleToggle = (roleId) => {
    setFormData(prev => ({
      ...prev,
      role_ids: prev.role_ids.includes(roleId)
        ? prev.role_ids.filter(id => id !== roleId)
        : [...prev.role_ids, roleId]
    }));

    // Limpiar error de roles
    if (errors.roles) {
      setErrors(prev => ({
        ...prev,
        roles: ''
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
        email: formData.email,
        full_name: formData.full_name,
        role_ids: formData.role_ids,
        is_active: formData.is_active,
      };

      if (!isEditMode) {
        payload.username = formData.username;
        payload.password = formData.password;
      }

      if (isEditMode) {
        await usersService.updateUser(id, payload);
        toast.success('Usuario actualizado exitosamente');
      } else {
        await usersService.createUser(payload);
        toast.success('Usuario creado exitosamente');
      }

      navigate('/users');
    } catch (error) {
      console.error('Error saving user:', error);
      const errorMessage = error.response?.data?.detail || 'Error al guardar usuario';
      toast.error(errorMessage);

      // Manejar errores específicos del backend
      if (error.response?.data?.detail?.includes('username')) {
        setErrors(prev => ({ ...prev, username: 'Este usuario ya existe' }));
      }
      if (error.response?.data?.detail?.includes('email')) {
        setErrors(prev => ({ ...prev, email: 'Este email ya está en uso' }));
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
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/users"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          Volver a usuarios
        </Link>
        <h1 className="text-3xl font-bold text-gray-900">
          {isEditMode ? 'Editar Usuario' : 'Crear Nuevo Usuario'}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {isEditMode
            ? `Actualiza la información del usuario @${formData.username}`
            : 'Completa la información para crear un nuevo usuario'}
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 space-y-6">
        {/* Username (solo en modo create) */}
        {!isEditMode && (
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
              Usuario <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className={`block w-full px-3 py-2 border ${
                errors.username ? 'border-red-300' : 'border-gray-300'
              } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
              placeholder="usuario123"
            />
            {errors.username && (
              <p className="mt-1 text-sm text-red-600">{errors.username}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              Solo letras, números, puntos, guiones y guiones bajos
            </p>
          </div>
        )}

        {/* Email */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Email <span className="text-red-500">*</span>
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={`block w-full px-3 py-2 border ${
              errors.email ? 'border-red-300' : 'border-gray-300'
            } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
            placeholder="usuario@ejemplo.com"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email}</p>
          )}
        </div>

        {/* Full Name */}
        <div>
          <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
            Nombre Completo <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            className={`block w-full px-3 py-2 border ${
              errors.full_name ? 'border-red-300' : 'border-gray-300'
            } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
            placeholder="Juan Pérez"
          />
          {errors.full_name && (
            <p className="mt-1 text-sm text-red-600">{errors.full_name}</p>
          )}
        </div>

        {/* Password (solo en modo create) */}
        {!isEditMode && (
          <>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Contraseña <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={`block w-full px-3 py-2 pr-10 border ${
                    errors.password ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Mínimo 8 caracteres, con mayúsculas, minúsculas y números
              </p>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                Confirmar Contraseña <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={`block w-full px-3 py-2 pr-10 border ${
                    errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
              )}
            </div>
          </>
        )}

        {/* Roles */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Roles <span className="text-red-500">*</span>
          </label>
          <div className="space-y-2 p-4 border border-gray-300 rounded-lg bg-gray-50">
            {roles.map((role) => (
              <label
                key={role.id}
                className="flex items-center p-2 hover:bg-gray-100 rounded cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={formData.role_ids.includes(role.id)}
                  onChange={() => handleRoleToggle(role.id)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-3 flex-1">
                  <span className="block text-sm font-medium text-gray-900">
                    {role.display_name}
                  </span>
                  {role.description && (
                    <span className="block text-xs text-gray-500">
                      {role.description}
                    </span>
                  )}
                </span>
              </label>
            ))}
          </div>
          {errors.roles && (
            <p className="mt-1 text-sm text-red-600">{errors.roles}</p>
          )}
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
              Usuario activo
            </span>
          </label>
          <p className="mt-1 text-xs text-gray-500 ml-6">
            Los usuarios inactivos no pueden iniciar sesión
          </p>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 pt-4 border-t">
          <button
            type="button"
            onClick={() => navigate('/users')}
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
                {isEditMode ? 'Actualizar Usuario' : 'Crear Usuario'}
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserForm;
