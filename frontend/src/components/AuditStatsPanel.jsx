import React, { useState, useEffect } from 'react';
import { BarChart3, PieChart, TrendingUp, Users, AlertTriangle, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';
import auditService from '../services/auditService';

/**
 * AuditStatsPanel - Panel de estadísticas de auditoría
 *
 * Muestra estadísticas de logs de auditoría:
 * - Total de logs en el período
 * - Distribución por categoría
 * - Top 10 acciones
 * - Top 10 usuarios más activos
 * - Errores recientes
 * - Distribución por estado
 */
const AuditStatsPanel = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState(7); // Días

  useEffect(() => {
    loadStats();
  }, [period]);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await auditService.getStats(period);
      setStats(data);
    } catch (error) {
      console.error('Error loading audit stats:', error);
      toast.error('Error al cargar estadísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Cargando estadísticas...</p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  const getCategoryColor = (category) => {
    const color = auditService.getCategoryColor(category);
    const colors = {
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      purple: 'bg-purple-500',
      yellow: 'bg-yellow-500',
      indigo: 'bg-indigo-500',
      pink: 'bg-pink-500',
      red: 'bg-red-500',
      gray: 'bg-gray-500',
      orange: 'bg-orange-500',
    };
    return colors[color] || colors.gray;
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <BarChart3 className="w-6 h-6 text-blue-600 mr-2" />
          <h2 className="text-lg font-semibold text-gray-900">
            Estadísticas de Auditoría
          </h2>
        </div>

        {/* Period Selector */}
        <div className="flex items-center space-x-2">
          <Calendar className="w-4 h-4 text-gray-500" />
          <select
            value={period}
            onChange={(e) => setPeriod(Number(e.target.value))}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={1}>Último día</option>
            <option value={7}>Últimos 7 días</option>
            <option value={30}>Últimos 30 días</option>
            <option value={90}>Últimos 90 días</option>
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Total Logs */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium">Total de Logs</p>
              <p className="text-2xl font-bold text-blue-900 mt-1">
                {stats.total_logs.toLocaleString()}
              </p>
            </div>
            <TrendingUp className="w-8 h-8 text-blue-400" />
          </div>
        </div>

        {/* Success Rate */}
        {stats.by_status && stats.by_status.length > 0 && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">Exitosos</p>
                <p className="text-2xl font-bold text-green-900 mt-1">
                  {(
                    ((stats.by_status.find(s => s.status === 'success')?.count || 0) /
                      stats.total_logs) *
                    100
                  ).toFixed(1)}%
                </p>
              </div>
              <PieChart className="w-8 h-8 text-green-400" />
            </div>
          </div>
        )}

        {/* Active Users */}
        {stats.top_users && stats.top_users.length > 0 && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-600 font-medium">Usuarios Activos</p>
                <p className="text-2xl font-bold text-purple-900 mt-1">
                  {stats.top_users.length}
                </p>
              </div>
              <Users className="w-8 h-8 text-purple-400" />
            </div>
          </div>
        )}

        {/* Errors */}
        {stats.recent_errors && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-600 font-medium">Errores Recientes</p>
                <p className="text-2xl font-bold text-red-900 mt-1">
                  {stats.recent_errors.length}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-400" />
            </div>
          </div>
        )}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* By Category */}
        {stats.by_category && stats.by_category.length > 0 && (
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-4">
              Por Categoría
            </h3>
            <div className="space-y-2">
              {stats.by_category
                .sort((a, b) => b.count - a.count)
                .slice(0, 8)
                .map((item) => {
                  const percentage = (item.count / stats.total_logs) * 100;
                  return (
                    <div key={item.category}>
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span className="text-gray-700">
                          {auditService.getCategoryLabel(item.category)}
                        </span>
                        <span className="font-medium text-gray-900">
                          {item.count} ({percentage.toFixed(1)}%)
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getCategoryColor(item.category)}`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}

        {/* Top Actions */}
        {stats.by_action && stats.by_action.length > 0 && (
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-4">
              Top 10 Acciones
            </h3>
            <div className="space-y-2">
              {stats.by_action.slice(0, 10).map((item, index) => {
                const percentage = (item.count / stats.total_logs) * 100;
                return (
                  <div key={item.action} className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-2 flex-1 min-w-0">
                      <span className="text-gray-500 font-medium w-6 text-right">
                        {index + 1}.
                      </span>
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded truncate">
                        {item.action}
                      </code>
                    </div>
                    <span className="font-medium text-gray-900 ml-2">
                      {item.count} ({percentage.toFixed(1)}%)
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Top Users */}
        {stats.top_users && stats.top_users.length > 0 && (
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-4">
              Top 10 Usuarios Activos
            </h3>
            <div className="space-y-2">
              {stats.top_users.map((item, index) => {
                const percentage = (item.count / stats.total_logs) * 100;
                return (
                  <div key={item.username} className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-2 flex-1">
                      <span className="text-gray-500 font-medium w-6 text-right">
                        {index + 1}.
                      </span>
                      <Users className="w-4 h-4 text-gray-400" />
                      <span className="text-gray-700 font-medium">{item.username}</span>
                    </div>
                    <span className="font-medium text-gray-900">
                      {item.count} ({percentage.toFixed(1)}%)
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Recent Errors */}
        {stats.recent_errors && stats.recent_errors.length > 0 && (
          <div className="border border-red-200 bg-red-50 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-red-900 mb-4 flex items-center">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Errores Recientes
            </h3>
            <div className="space-y-3">
              {stats.recent_errors.map((error) => (
                <div key={error.id} className="bg-white border border-red-200 rounded p-3">
                  <div className="flex items-start justify-between mb-1">
                    <code className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                      {error.action}
                    </code>
                    <span className="text-xs text-gray-500">
                      {auditService.formatRelativeDate(error.timestamp)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-700 mt-1">
                    <span className="font-medium">Usuario:</span> {error.username || 'N/A'}
                  </p>
                  {error.error_message && (
                    <p className="text-xs text-red-700 mt-1 font-mono">
                      {error.error_message}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditStatsPanel;
