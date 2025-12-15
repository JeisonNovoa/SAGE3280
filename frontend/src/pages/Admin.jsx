import { useState, useEffect } from 'react';
import { adminService } from '../services/api';

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [uploads, setUploads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsData, uploadsData] = await Promise.all([
        adminService.getDatabaseStats(),
        adminService.listUploads(),
      ]);
      setStats(statsData);
      setUploads(uploadsData.uploads);
    } catch (error) {
      console.error('Error loading admin data:', error);
      setMessage({ type: 'error', text: 'Error al cargar datos de administración' });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAllPatients = async () => {
    if (!window.confirm('⚠️ ¿Estás seguro de que deseas eliminar TODOS los pacientes? Esta acción no se puede deshacer.')) {
      return;
    }

    try {
      setActionLoading(true);
      const result = await adminService.deleteAllPatients();
      setMessage({
        type: 'success',
        text: `✅ ${result.message}. Eliminados: ${result.deleted.patients} pacientes, ${result.deleted.controls} controles, ${result.deleted.alerts} alertas.`
      });
      await loadData();
    } catch (error) {
      console.error('Error deleting patients:', error);
      setMessage({ type: 'error', text: 'Error al eliminar pacientes: ' + (error.response?.data?.detail || error.message) });
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteUpload = async (uploadId, filename) => {
    if (!window.confirm(`¿Estás seguro de que deseas eliminar todos los pacientes del archivo "${filename}"?`)) {
      return;
    }

    try {
      setActionLoading(true);
      const result = await adminService.deletePatientsByUpload(uploadId);
      setMessage({
        type: 'success',
        text: `✅ ${result.message}. Eliminados: ${result.deleted.patients} pacientes.`
      });
      await loadData();
    } catch (error) {
      console.error('Error deleting upload patients:', error);
      setMessage({ type: 'error', text: 'Error al eliminar pacientes: ' + (error.response?.data?.detail || error.message) });
    } finally {
      setActionLoading(false);
    }
  };

  const handleClearDatabase = async () => {
    if (!window.confirm('🚨 PELIGRO: ¿Estás seguro de que deseas ELIMINAR TODA LA BASE DE DATOS? Esto incluye pacientes, controles, alertas, exámenes Y registros de uploads. Esta acción NO se puede deshacer.')) {
      return;
    }

    if (!window.confirm('⚠️ ÚLTIMA CONFIRMACIÓN: Esto eliminará ABSOLUTAMENTE TODO. ¿Continuar?')) {
      return;
    }

    try {
      setActionLoading(true);
      const result = await adminService.clearDatabase();
      setMessage({
        type: 'success',
        text: `✅ Base de datos limpiada completamente.`
      });
      await loadData();
    } catch (error) {
      console.error('Error clearing database:', error);
      setMessage({ type: 'error', text: 'Error al limpiar base de datos: ' + (error.response?.data?.detail || error.message) });
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Administración</h1>
        <p className="mt-2 text-gray-600">Gestiona la base de datos y los archivos cargados</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${message.type === 'error' ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'}`}>
          <p>{message.text}</p>
          <button
            onClick={() => setMessage(null)}
            className="mt-2 text-sm underline"
          >
            Cerrar
          </button>
        </div>
      )}

      {/* Estadísticas */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Estadísticas de la Base de Datos</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{stats?.patients || 0}</div>
            <div className="text-sm text-gray-600 mt-1">Pacientes</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600">{stats?.controls || 0}</div>
            <div className="text-sm text-gray-600 mt-1">Controles</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-3xl font-bold text-yellow-600">{stats?.alerts || 0}</div>
            <div className="text-sm text-gray-600 mt-1">Alertas</div>
          </div>
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-3xl font-bold text-purple-600">{stats?.uploads || 0}</div>
            <div className="text-sm text-gray-600 mt-1">Uploads</div>
          </div>
          <div className="text-center p-4 bg-pink-50 rounded-lg">
            <div className="text-3xl font-bold text-pink-600">{stats?.exams || 0}</div>
            <div className="text-sm text-gray-600 mt-1">Exámenes</div>
          </div>
        </div>
      </div>

      {/* Uploads */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Archivos Cargados</h2>
        {uploads.length === 0 ? (
          <p className="text-gray-500">No hay archivos cargados</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Archivo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pacientes</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {uploads.map((upload) => (
                  <tr key={upload.id}>
                    <td className="px-4 py-3 text-sm text-gray-900">{upload.id}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{upload.filename}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {new Date(upload.created_at).toLocaleString('es-CO')}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        upload.status === 'completed' ? 'bg-green-100 text-green-800' :
                        upload.status === 'failed' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {upload.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">{upload.current_patient_count}</td>
                    <td className="px-4 py-3">
                      {upload.current_patient_count > 0 && (
                        <button
                          onClick={() => handleDeleteUpload(upload.id, upload.filename)}
                          disabled={actionLoading}
                          className="text-red-600 hover:text-red-800 text-sm font-medium disabled:opacity-50"
                        >
                          Eliminar pacientes
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Acciones Peligrosas */}
      <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-red-900 mb-4">⚠️ Zona de Peligro</h2>
        <p className="text-red-700 mb-4">Estas acciones son irreversibles. Usa con precaución.</p>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-white rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Eliminar Todos los Pacientes</h3>
              <p className="text-sm text-gray-600">Elimina todos los pacientes, controles, alertas y exámenes. Mantiene registros de uploads.</p>
            </div>
            <button
              onClick={handleDeleteAllPatients}
              disabled={actionLoading || (stats?.patients || 0) === 0}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {actionLoading ? 'Procesando...' : 'Eliminar Pacientes'}
            </button>
          </div>

          <div className="flex items-center justify-between p-4 bg-white rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Limpiar Base de Datos Completa</h3>
              <p className="text-sm text-gray-600">🚨 Elimina TODO: pacientes, controles, alertas, exámenes Y uploads.</p>
            </div>
            <button
              onClick={handleClearDatabase}
              disabled={actionLoading}
              className="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-900 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {actionLoading ? 'Procesando...' : 'Limpiar Todo'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
