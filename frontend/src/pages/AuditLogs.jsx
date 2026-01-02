import React, { useState, useEffect } from 'react';
import { FileText, Filter, X, ChevronDown, ChevronUp, Eye, Calendar, User, Activity, AlertCircle, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import auditService from '../services/auditService';
import AuditLogDetailsModal from '../components/AuditLogDetailsModal';
import AuditStatsPanel from '../components/AuditStatsPanel';

/**
 * AuditLogs - Página de visualización de logs de auditoría
 *
 * Características:
 * - Listado de logs con paginación
 * - Filtros avanzados (usuario, categoría, acción, estado, fechas)
 * - Vista de detalles de log
 * - Panel de estadísticas
 */
const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(50);

  // Filtros
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    user_id: '',
    action: '',
    category: '',
    status: '',
    resource_type: '',
    date_from: '',
    date_to: '',
  });

  // Metadatos
  const [metadata, setMetadata] = useState({
    categories: [],
    actions: [],
    resource_types: [],
    statuses: [],
  });

  // Modal de detalles
  const [selectedLog, setSelectedLog] = useState(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  // Panel de estadísticas
  const [showStats, setShowStats] = useState(false);

  useEffect(() => {
    loadLogs();
    loadMetadata();
  }, [currentPage, filters]);

  const loadLogs = async () => {
    try {
      setLoading(true);
      const offset = (currentPage - 1) * pageSize;
      const params = {
        offset,
        limit: pageSize,
        ...filters,
      };

      // Filtrar parámetros vacíos
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === null || params[key] === undefined) {
          delete params[key];
        }
      });

      const data = await auditService.getLogs(params);
      setLogs(data.items);
      setTotal(data.total);
    } catch (error) {
      console.error('Error loading audit logs:', error);
      toast.error('Error al cargar logs de auditoría');
    } finally {
      setLoading(false);
    }
  };

  const loadMetadata = async () => {
    try {
      const data = await auditService.getMetadata();
      setMetadata(data);
    } catch (error) {
      console.error('Error loading metadata:', error);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    setCurrentPage(1); // Reset a primera página
  };

  const clearFilters = () => {
    setFilters({
      user_id: '',
      action: '',
      category: '',
      status: '',
      resource_type: '',
      date_from: '',
      date_to: '',
    });
    setCurrentPage(1);
  };

  const handleViewDetails = async (log) => {
    try {
      const fullLog = await auditService.getLog(log.id);
      setSelectedLog(fullLog);
      setShowDetailsModal(true);
    } catch (error) {
      console.error('Error loading log details:', error);
      toast.error('Error al cargar detalles del log');
    }
  };

  const totalPages = Math.ceil(total / pageSize);
  const hasActiveFilters = Object.values(filters).some(v => v !== '');

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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mr-4">
              <FileText className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Logs de Auditoría</h1>
              <p className="mt-1 text-sm text-gray-500">
                Registro de acciones y eventos del sistema
              </p>
            </div>
          </div>
        </div>

        <div className="flex space-x-3">
          <button
            onClick={() => setShowStats(!showStats)}
            className={`px-4 py-2 border rounded-lg transition-colors ${
              showStats
                ? 'bg-blue-50 border-blue-300 text-blue-700'
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Activity className="w-4 h-4 inline mr-2" />
            Estadísticas
          </button>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`px-4 py-2 border rounded-lg transition-colors ${
              showFilters || hasActiveFilters
                ? 'bg-blue-50 border-blue-300 text-blue-700'
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Filter className="w-4 h-4 inline mr-2" />
            Filtros
            {hasActiveFilters && (
              <span className="ml-2 px-2 py-0.5 bg-blue-600 text-white text-xs rounded-full">
                {Object.values(filters).filter(v => v !== '').length}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Stats Panel */}
      {showStats && <AuditStatsPanel />}

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Filtros de búsqueda</h3>
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                <X className="w-4 h-4 inline mr-1" />
                Limpiar filtros
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Categoría */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Categoría
              </label>
              <select
                name="category"
                value={filters.category}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todas las categorías</option>
                {metadata.categories.map(cat => (
                  <option key={cat} value={cat}>
                    {auditService.getCategoryLabel(cat)}
                  </option>
                ))}
              </select>
            </div>

            {/* Estado */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estado
              </label>
              <select
                name="status"
                value={filters.status}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los estados</option>
                {metadata.statuses.map(status => (
                  <option key={status} value={status}>
                    {auditService.getStatusLabel(status)}
                  </option>
                ))}
              </select>
            </div>

            {/* Tipo de recurso */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de recurso
              </label>
              <select
                name="resource_type"
                value={filters.resource_type}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los tipos</option>
                {metadata.resource_types.map(type => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>

            {/* Acción */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Acción
              </label>
              <input
                type="text"
                name="action"
                value={filters.action}
                onChange={handleFilterChange}
                placeholder="Buscar acción..."
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Fecha desde */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha desde
              </label>
              <input
                type="datetime-local"
                name="date_from"
                value={filters.date_from}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Fecha hasta */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha hasta
              </label>
              <input
                type="datetime-local"
                name="date_to"
                value={filters.date_to}
                onChange={handleFilterChange}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Mostrando <span className="font-semibold">{logs.length}</span> de{' '}
            <span className="font-semibold">{total}</span> logs
          </div>
          {hasActiveFilters && (
            <div className="text-sm text-blue-600">
              <Filter className="w-4 h-4 inline mr-1" />
              Filtros activos
            </div>
          )}
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Cargando logs...</p>
          </div>
        ) : logs.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2 text-gray-500">
              {hasActiveFilters ? 'No se encontraron logs con los filtros aplicados' : 'No hay logs de auditoría'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Usuario
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acción
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Categoría
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Recurso
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 text-gray-400 mr-2" />
                        <div>
                          <div>{auditService.formatDate(log.timestamp).split(' ')[0]}</div>
                          <div className="text-xs text-gray-500">
                            {auditService.formatDate(log.timestamp).split(' ')[1]}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <User className="w-4 h-4 text-gray-400 mr-2" />
                        <div className="text-sm">
                          <div className="font-medium text-gray-900">
                            {log.username || 'Sistema'}
                          </div>
                          {log.user_id && (
                            <div className="text-xs text-gray-500">ID: {log.user_id}</div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      <code className="px-2 py-1 bg-gray-100 rounded text-xs">
                        {log.action}
                      </code>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {log.category && (
                        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getCategoryBadgeClass(log.category)}`}>
                          {auditService.getCategoryLabel(log.category)}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {log.resource_type && (
                        <div>
                          <div className="font-medium">{log.resource_type}</div>
                          {log.resource_name && (
                            <div className="text-xs text-gray-500 truncate max-w-xs">
                              {log.resource_name}
                            </div>
                          )}
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusBadgeClass(log.status)}`}>
                        {auditService.getStatusLabel(log.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button
                        onClick={() => handleViewDetails(log)}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                        title="Ver detalles"
                      >
                        <Eye className="w-5 h-5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {!loading && totalPages > 1 && (
          <div className="bg-gray-50 px-4 py-3 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-700">
                Página <span className="font-medium">{currentPage}</span> de{' '}
                <span className="font-medium">{totalPages}</span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 border border-gray-300 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                >
                  Anterior
                </button>
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 border border-gray-300 rounded-lg text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                >
                  Siguiente
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Details Modal */}
      {showDetailsModal && selectedLog && (
        <AuditLogDetailsModal
          log={selectedLog}
          onClose={() => setShowDetailsModal(false)}
        />
      )}
    </div>
  );
};

export default AuditLogs;
