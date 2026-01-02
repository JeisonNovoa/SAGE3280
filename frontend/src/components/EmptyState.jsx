import React from 'react';
import { FileText, Plus } from 'lucide-react';

/**
 * EmptyState - Componente para mostrar cuando no hay datos
 *
 * @param {ReactNode} icon - Icono a mostrar (default: FileText)
 * @param {string} title - Título
 * @param {string} description - Descripción
 * @param {Function} action - Acción a ejecutar (opcional)
 * @param {string} actionText - Texto del botón de acción (opcional)
 * @param {ReactNode} actionIcon - Icono del botón de acción (default: Plus)
 */
const EmptyState = ({
  icon: Icon = FileText,
  title,
  description,
  action,
  actionText,
  actionIcon: ActionIcon = Plus,
}) => {
  return (
    <div className="text-center py-12">
      <div className="flex justify-center mb-4">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
          <Icon className="w-8 h-8 text-gray-400" />
        </div>
      </div>

      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>

      {description && (
        <p className="text-sm text-gray-500 mb-6 max-w-md mx-auto">
          {description}
        </p>
      )}

      {action && actionText && (
        <button
          onClick={action}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <ActionIcon className="w-4 h-4 mr-2" />
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
