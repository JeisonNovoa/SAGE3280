import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Check, X } from 'lucide-react';
import { PERMISSION_CATEGORIES, getCategoryColor } from '../services/rolesService';

/**
 * PermissionsTable
 * Componente para mostrar y gestionar permisos organizados por categorías
 *
 * @param {Object} props
 * @param {Array<string>} props.selectedPermissions - Permisos seleccionados
 * @param {Function} props.onChange - Callback cuando cambian los permisos (solo en modo edit)
 * @param {string} props.mode - 'view' o 'edit' (default: 'view')
 */
const PermissionsTable = ({
  selectedPermissions = [],
  onChange,
  mode = 'view'
}) => {
  const [expandedCategories, setExpandedCategories] = useState(() => {
    // Expandir todas las categorías por defecto en modo edit
    if (mode === 'edit') {
      return Object.keys(PERMISSION_CATEGORIES).reduce((acc, key) => {
        acc[key] = true;
        return acc;
      }, {});
    }
    return {};
  });

  const isEditable = mode === 'edit';

  const toggleCategory = (categoryKey) => {
    setExpandedCategories(prev => ({
      ...prev,
      [categoryKey]: !prev[categoryKey]
    }));
  };

  const handlePermissionToggle = (permission) => {
    if (!isEditable || !onChange) return;

    const newPermissions = selectedPermissions.includes(permission)
      ? selectedPermissions.filter(p => p !== permission)
      : [...selectedPermissions, permission];

    onChange(newPermissions);
  };

  const handleSelectAllInCategory = (categoryKey) => {
    if (!isEditable || !onChange) return;

    const categoryPermissions = PERMISSION_CATEGORIES[categoryKey].permissions;
    const allSelected = categoryPermissions.every(p => selectedPermissions.includes(p));

    let newPermissions;
    if (allSelected) {
      // Deseleccionar todos de esta categoría
      newPermissions = selectedPermissions.filter(p => !categoryPermissions.includes(p));
    } else {
      // Seleccionar todos de esta categoría
      const toAdd = categoryPermissions.filter(p => !selectedPermissions.includes(p));
      newPermissions = [...selectedPermissions, ...toAdd];
    }

    onChange(newPermissions);
  };

  const handleSelectAll = () => {
    if (!isEditable || !onChange) return;

    const allPermissions = Object.values(PERMISSION_CATEGORIES).flatMap(cat => cat.permissions);
    const allSelected = allPermissions.every(p => selectedPermissions.includes(p));

    if (allSelected) {
      onChange([]);
    } else {
      onChange(allPermissions);
    }
  };

  const getCategoryStats = (categoryKey) => {
    const categoryPermissions = PERMISSION_CATEGORIES[categoryKey].permissions;
    const selected = categoryPermissions.filter(p => selectedPermissions.includes(p)).length;
    const total = categoryPermissions.length;
    return { selected, total };
  };

  const allPermissionsCount = Object.values(PERMISSION_CATEGORIES).reduce(
    (acc, cat) => acc + cat.permissions.length,
    0
  );
  const selectedCount = selectedPermissions.length;

  const getCategoryColorClass = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-800 border-blue-300',
      green: 'bg-green-100 text-green-800 border-green-300',
      purple: 'bg-purple-100 text-purple-800 border-purple-300',
      yellow: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      indigo: 'bg-indigo-100 text-indigo-800 border-indigo-300',
      pink: 'bg-pink-100 text-pink-800 border-pink-300',
      red: 'bg-red-100 text-red-800 border-red-300',
      gray: 'bg-gray-100 text-gray-800 border-gray-300',
      orange: 'bg-orange-100 text-orange-800 border-orange-300',
    };
    return colors[color] || colors.gray;
  };

  return (
    <div className="space-y-4">
      {/* Header with Select All */}
      {isEditable && (
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-600">
            <span className="font-semibold">{selectedCount}</span> de{' '}
            <span className="font-semibold">{allPermissionsCount}</span> permisos seleccionados
          </div>
          <button
            type="button"
            onClick={handleSelectAll}
            className="px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
          >
            {selectedCount === allPermissionsCount ? 'Deseleccionar todos' : 'Seleccionar todos'}
          </button>
        </div>
      )}

      {/* Categories */}
      <div className="space-y-3">
        {Object.entries(PERMISSION_CATEGORIES).map(([categoryKey, category]) => {
          const isExpanded = expandedCategories[categoryKey];
          const stats = getCategoryStats(categoryKey);
          const allCategorySelected = stats.selected === stats.total;

          return (
            <div
              key={categoryKey}
              className="border border-gray-200 rounded-lg overflow-hidden"
            >
              {/* Category Header */}
              <div className="bg-gray-50 p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-1">
                    <button
                      type="button"
                      onClick={() => toggleCategory(categoryKey)}
                      className="p-1 hover:bg-gray-200 rounded transition-colors"
                    >
                      {isExpanded ? (
                        <ChevronUp className="w-4 h-4 text-gray-600" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-gray-600" />
                      )}
                    </button>

                    <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getCategoryColorClass(category.color)}`}>
                      {category.label}
                    </span>

                    <span className="text-sm text-gray-600">
                      {stats.selected}/{stats.total} seleccionados
                    </span>
                  </div>

                  {isEditable && (
                    <button
                      type="button"
                      onClick={() => handleSelectAllInCategory(categoryKey)}
                      className="px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-200 rounded transition-colors"
                    >
                      {allCategorySelected ? (
                        <span className="flex items-center">
                          <X className="w-3 h-3 mr-1" />
                          Deseleccionar
                        </span>
                      ) : (
                        <span className="flex items-center">
                          <Check className="w-3 h-3 mr-1" />
                          Seleccionar todos
                        </span>
                      )}
                    </button>
                  )}
                </div>
              </div>

              {/* Category Permissions */}
              {isExpanded && (
                <div className="p-4 bg-white">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {category.permissions.map((permission) => {
                      const isSelected = selectedPermissions.includes(permission);

                      return (
                        <label
                          key={permission}
                          className={`flex items-center p-3 rounded-lg border transition-colors ${
                            isEditable
                              ? 'cursor-pointer hover:bg-gray-50'
                              : 'cursor-default'
                          } ${
                            isSelected
                              ? 'border-blue-300 bg-blue-50'
                              : 'border-gray-200'
                          }`}
                        >
                          {isEditable ? (
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={() => handlePermissionToggle(permission)}
                              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                            />
                          ) : (
                            isSelected && (
                              <div className="w-4 h-4 bg-blue-600 rounded flex items-center justify-center">
                                <Check className="w-3 h-3 text-white" />
                              </div>
                            )
                          )}

                          <span className={`ml-3 text-sm ${
                            isSelected ? 'font-medium text-gray-900' : 'text-gray-700'
                          }`}>
                            {permission}
                          </span>
                        </label>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary */}
      {!isEditable && selectedCount === 0 && (
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-center">
          <p className="text-sm text-gray-500 italic">
            No hay permisos asignados a este rol
          </p>
        </div>
      )}
    </div>
  );
};

export default PermissionsTable;
