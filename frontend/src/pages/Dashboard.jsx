import { useState, useEffect } from 'react';
import { Users, FileText, AlertTriangle, CheckCircle, Phone } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { statsService } from '../services/api';
import toast from 'react-hot-toast';

const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await statsService.getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
      toast.error('Error al cargar estadísticas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <p className="text-yellow-800">
          No hay datos disponibles. Por favor, carga un archivo Excel primero.
        </p>
      </div>
    );
  }

  const summaryCards = [
    {
      title: 'Total Pacientes',
      value: stats.total_patients,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      title: 'Controles Pendientes',
      value: stats.total_controls_pending,
      icon: FileText,
      color: 'bg-orange-500',
    },
    {
      title: 'Alertas Activas',
      value: stats.total_active_alerts,
      icon: AlertTriangle,
      color: 'bg-red-500',
    },
    {
      title: 'Tasa de Contacto',
      value: `${stats.contact_stats.contact_rate}%`,
      icon: Phone,
      color: 'bg-green-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-2 text-sm text-gray-600">
          Última actualización: {stats.last_upload_date}
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {summaryCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.title} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{card.title}</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{card.value}</p>
                </div>
                <div className={`${card.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Age Group Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Distribución por Grupo Etario
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats.patients_by_age_group}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.name}: ${entry.count}`}
              >
                {stats.patients_by_age_group.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Sex Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Distribución por Sexo
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats.patients_by_sex}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.name}: ${entry.count} (${entry.percentage}%)`}
              >
                {stats.patients_by_sex.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Risk Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Pacientes con Factores de Riesgo
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-red-50 p-4 rounded-lg">
            <p className="text-sm text-red-600 mb-1">Hipertensos</p>
            <p className="text-2xl font-bold text-red-700">{stats.risk_stats.hypertensive}</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <p className="text-sm text-orange-600 mb-1">Diabéticos</p>
            <p className="text-2xl font-bold text-orange-700">{stats.risk_stats.diabetic}</p>
          </div>
          <div className="bg-pink-50 p-4 rounded-lg">
            <p className="text-sm text-pink-600 mb-1">Gestantes</p>
            <p className="text-2xl font-bold text-pink-700">{stats.risk_stats.pregnant}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm text-purple-600 mb-1">Riesgo CV</p>
            <p className="text-2xl font-bold text-purple-700">{stats.risk_stats.cardiovascular_risk}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Total Riesgos</p>
            <p className="text-2xl font-bold text-gray-700">{stats.risk_stats.total_with_risks}</p>
          </div>
        </div>
      </div>

      {/* Controls by Type */}
      {stats.controls_by_type && stats.controls_by_type.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Controles por Tipo
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={stats.controls_by_type}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="control_type" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="pending" fill="#f59e0b" name="Pendientes" />
              <Bar dataKey="completed" fill="#10b981" name="Completados" />
              <Bar dataKey="overdue" fill="#ef4444" name="Vencidos" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Alerts Priority */}
      {stats.alerts_by_priority && Object.keys(stats.alerts_by_priority).length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Alertas por Prioridad
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(stats.alerts_by_priority).map(([priority, count]) => {
              const priorityColors = {
                urgente: 'bg-red-50 text-red-700',
                alta: 'bg-orange-50 text-orange-700',
                media: 'bg-yellow-50 text-yellow-700',
                baja: 'bg-green-50 text-green-700',
              };

              return (
                <div key={priority} className={`p-4 rounded-lg ${priorityColors[priority] || 'bg-gray-50 text-gray-700'}`}>
                  <p className="text-sm mb-1 capitalize">{priority}</p>
                  <p className="text-2xl font-bold">{count}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Contact Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Estado de Contacto
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-green-600 mb-1">Contactados</p>
            <p className="text-3xl font-bold text-green-700">{stats.contact_stats.contacted}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">No Contactados</p>
            <p className="text-3xl font-bold text-gray-700">{stats.contact_stats.not_contacted}</p>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-600 mb-1">Tasa de Contacto</p>
            <p className="text-3xl font-bold text-blue-700">{stats.contact_stats.contact_rate}%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
