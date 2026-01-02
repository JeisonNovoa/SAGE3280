import React from 'react';
import { X, Calendar, User, Activity, MapPin, Monitor, FileText, AlertCircle } from 'lucide-react';
import auditService from '../services/auditService';

/**
 * AuditLogDetailsModal - Modal para mostrar detalles de un log de auditoría
 *
 * @param {Object} log - Log a mostrar
 * @param {Function} onClose - Función para cerrar el modal
 */
const AuditLogDetailsModal = ({ log, onClose }) => {
  if (!log) return null;

  const getCategoryBadgeClass = (category) => {
    const color = auditService.getCategoryColor(category);
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

  const getStatusBadgeClass = (status) => {
    const color = auditService.getStatusColor(status);
    const colors = {
      green: 'bg-green-100 text-green-800',
      red: 'bg-red-100 text-red-800',
      yellow: 'bg-yellow-100 text-yellow-800',
      gray: 'bg-gray-100 text-gray-800',
    };
    return colors[color] || colors.gray;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <FileText className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Detalles del Log de Auditoría
              </h2>
              <p className="text-sm text-gray-500">ID: {log.id}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Información Principal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Fecha y Hora */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <Calendar className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Fecha y Hora</span>
              </div>
              <p className="text-sm text-gray-900 font-mono">
                {auditService.formatDate(log.timestamp)}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {auditService.formatRelativeDate(log.timestamp)}
              </p>
            </div>

            {/* Usuario */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <User className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Usuario</span>
              </div>
              <p className="text-sm text-gray-900 font-medium">
                {log.username || 'Sistema'}
              </p>
              {log.user_id && (
                <p className="text-xs text-gray-500 mt-1">ID: {log.user_id}</p>
              )}
            </div>

            {/* Acción */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <Activity className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Acción</span>
              </div>
              <code className="text-sm bg-gray-200 px-2 py-1 rounded">
                {log.action}
              </code>
            </div>

            {/* Categoría */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <FileText className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Categoría</span>
              </div>
              {log.category ? (
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getCategoryBadgeClass(log.category)}`}>
                  {auditService.getCategoryLabel(log.category)}
                </span>
              ) : (
                <span className="text-sm text-gray-400">N/A</span>
              )}
            </div>

            {/* Estado */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <AlertCircle className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Estado</span>
              </div>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusBadgeClass(log.status)}`}>
                {auditService.getStatusLabel(log.status)}
              </span>
            </div>

            {/* IP Address */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <MapPin className="w-5 h-5 text-gray-400 mr-2" />
                <span className="text-sm font-medium text-gray-700">Dirección IP</span>
              </div>
              <p className="text-sm text-gray-900 font-mono">
                {log.ip_address || 'N/A'}
              </p>
            </div>
          </div>

          {/* Recurso Afectado */}
          {(log.resource_type || log.resource_id || log.resource_name) && (
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">
                Recurso Afectado
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {log.resource_type && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Tipo</p>
                    <p className="text-sm font-medium text-gray-900">{log.resource_type}</p>
                  </div>
                )}
                {log.resource_id && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1">ID</p>
                    <p className="text-sm font-medium text-gray-900">{log.resource_id}</p>
                  </div>
                )}
                {log.resource_name && (
                  <div className="md:col-span-3">
                    <p className="text-xs text-gray-500 mb-1">Nombre</p>
                    <p className="text-sm font-medium text-gray-900">{log.resource_name}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* User Agent */}
          {log.user_agent && (
            <div className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <Monitor className="w-5 h-5 text-gray-400 mr-2" />
                <h3 className="text-sm font-semibold text-gray-900">User Agent</h3>
              </div>
              <p className="text-xs text-gray-600 font-mono break-all">
                {log.user_agent}
              </p>
            </div>
          )}

          {/* Error Message */}
          {log.error_message && (
            <div className="border border-red-200 bg-red-50 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
                <h3 className="text-sm font-semibold text-red-900">Mensaje de Error</h3>
              </div>
              <p className="text-sm text-red-800 font-mono">
                {log.error_message}
              </p>
            </div>
          )}

          {/* Detalles Adicionales (JSON) */}
          {log.details && Object.keys(log.details).length > 0 && (
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">
                Detalles Adicionales
              </h3>
              <div className="bg-gray-900 rounded p-3 overflow-x-auto">
                <pre className="text-xs text-green-400 font-mono">
                  {JSON.stringify(log.details, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuditLogDetailsModal;
