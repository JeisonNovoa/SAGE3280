import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Phone, Mail, MapPin, AlertCircle, FileText, CheckCircle, X, Calendar, MessageSquare, XCircle } from 'lucide-react';
import { patientsService, controlsService, alertsService } from '../services/api';
import toast from 'react-hot-toast';

const PatientDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);

  // Contact modal state
  const [showContactModal, setShowContactModal] = useState(false);
  const [contactStatus, setContactStatus] = useState('');
  const [contactNotes, setContactNotes] = useState('');

  // Control modal state
  const [showControlModal, setShowControlModal] = useState(false);
  const [selectedControl, setSelectedControl] = useState(null);
  const [controlStatus, setControlStatus] = useState('');
  const [scheduledDate, setScheduledDate] = useState('');
  const [controlNotes, setControlNotes] = useState('');

  // Alert modal state
  const [showAlertModal, setShowAlertModal] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [alertStatus, setAlertStatus] = useState('');
  const [alertNotes, setAlertNotes] = useState('');

  useEffect(() => {
    loadPatient();
  }, [id]);

  const loadPatient = async () => {
    try {
      const data = await patientsService.getPatient(id);
      setPatient(data);
    } catch (error) {
      console.error('Error loading patient:', error);
      toast.error('Error al cargar paciente');
    } finally {
      setLoading(false);
    }
  };

  // ================== CONTACT MANAGEMENT ==================
  const handleOpenContactModal = () => {
    setContactStatus(patient.contact_status || '');
    setContactNotes('');
    setShowContactModal(true);
  };

  const handleUpdateContact = async () => {
    try {
      await patientsService.updateContactStatus(id, contactStatus, contactNotes);
      toast.success('Estado de contacto actualizado');
      setShowContactModal(false);
      loadPatient(); // Reload to get updated data
    } catch (error) {
      console.error('Error updating contact:', error);
      toast.error('Error al actualizar contacto');
    }
  };

  // ================== CONTROL MANAGEMENT ==================
  const handleOpenControlModal = (control) => {
    setSelectedControl(control);
    setControlStatus(control.status);
    setScheduledDate(control.scheduled_date || '');
    setControlNotes(control.notes || '');
    setShowControlModal(true);
  };

  const handleUpdateControl = async () => {
    try {
      const updateData = {
        status: controlStatus,
        notes: controlNotes,
      };

      if (scheduledDate) {
        updateData.scheduled_date = scheduledDate;
      }

      if (controlStatus === 'completado') {
        updateData.completed_date = new Date().toISOString().split('T')[0];
      }

      await controlsService.updateControl(selectedControl.id, updateData);
      toast.success('Control actualizado');
      setShowControlModal(false);
      loadPatient(); // Reload to get updated data
    } catch (error) {
      console.error('Error updating control:', error);
      toast.error('Error al actualizar control');
    }
  };

  // ================== ALERT MANAGEMENT ==================
  const handleOpenAlertModal = (alert) => {
    setSelectedAlert(alert);
    setAlertStatus(alert.status);
    setAlertNotes(alert.notes || '');
    setShowAlertModal(true);
  };

  const handleUpdateAlert = async () => {
    try {
      const updateData = {
        status: alertStatus,
        notes: alertNotes,
      };

      if (alertStatus === 'completada') {
        updateData.completed_date = new Date().toISOString().split('T')[0];
      }

      await alertsService.updateAlert(selectedAlert.id, updateData);
      toast.success('Alerta actualizada');
      setShowAlertModal(false);
      loadPatient(); // Reload to get updated data
    } catch (error) {
      console.error('Error updating alert:', error);
      toast.error('Error al actualizar alerta');
    }
  };

  const handleDismissAlert = async (alertId) => {
    if (!confirm('¿Está seguro de descartar esta alerta?')) return;

    try {
      await alertsService.dismissAlert(alertId);
      toast.success('Alerta descartada');
      loadPatient(); // Reload to get updated data
    } catch (error) {
      console.error('Error dismissing alert:', error);
      toast.error('Error al descartar alerta');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-800">Paciente no encontrado</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/patients')}
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-5 w-5 mr-1" />
          Volver
        </button>

        {/* Contact Button */}
        <button
          onClick={handleOpenContactModal}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <Phone className="h-4 w-4 mr-2" />
          Registrar Contacto
        </button>
      </div>

      {/* Patient Info */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center">
            <div className="bg-primary-100 p-3 rounded-full">
              <User className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <h2 className="text-2xl font-bold text-gray-900">{patient.full_name}</h2>
              <p className="text-sm text-gray-500">CC: {patient.document_number}</p>
            </div>
          </div>
          <div className="space-y-2">
            {patient.is_contacted && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                Contactado
              </span>
            )}
            {patient.contact_status && (
              <div className="text-sm text-gray-600">
                Estado: <span className="font-medium capitalize">{patient.contact_status}</span>
              </div>
            )}
            {patient.contact_attempts > 0 && (
              <div className="text-sm text-gray-600">
                Intentos: <span className="font-medium">{patient.contact_attempts}</span>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <p className="text-sm text-gray-600 mb-1">Edad</p>
            <p className="text-lg font-semibold text-gray-900">{patient.age} años</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Sexo</p>
            <p className="text-lg font-semibold text-gray-900">
              {patient.sex === 'M' ? 'Masculino' : patient.sex === 'F' ? 'Femenino' : 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Grupo Etario</p>
            <p className="text-lg font-semibold text-gray-900 capitalize">
              {patient.age_group?.replace('_', ' ')}
            </p>
          </div>
        </div>
      </div>

      {/* Contact Info */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Información de Contacto</h3>
        <div className="space-y-3">
          {patient.phone && (
            <div className="flex items-center">
              <Phone className="h-5 w-5 text-gray-400 mr-3" />
              <span className="text-gray-900">{patient.phone}</span>
            </div>
          )}
          {patient.email && (
            <div className="flex items-center">
              <Mail className="h-5 w-5 text-gray-400 mr-3" />
              <span className="text-gray-900">{patient.email}</span>
            </div>
          )}
          {patient.address && (
            <div className="flex items-center">
              <MapPin className="h-5 w-5 text-gray-400 mr-3" />
              <span className="text-gray-900">{patient.address}</span>
            </div>
          )}
        </div>
      </div>

      {/* Health Conditions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Condiciones de Salud</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className={`p-4 rounded-lg ${patient.is_hypertensive ? 'bg-red-50' : 'bg-gray-50'}`}>
            <p className="text-sm text-gray-600 mb-1">Hipertensión</p>
            <p className={`text-lg font-semibold ${patient.is_hypertensive ? 'text-red-700' : 'text-gray-700'}`}>
              {patient.is_hypertensive ? 'Sí' : 'No'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${patient.is_diabetic ? 'bg-orange-50' : 'bg-gray-50'}`}>
            <p className="text-sm text-gray-600 mb-1">Diabetes</p>
            <p className={`text-lg font-semibold ${patient.is_diabetic ? 'text-orange-700' : 'text-gray-700'}`}>
              {patient.is_diabetic ? 'Sí' : 'No'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${patient.is_pregnant ? 'bg-pink-50' : 'bg-gray-50'}`}>
            <p className="text-sm text-gray-600 mb-1">Gestante</p>
            <p className={`text-lg font-semibold ${patient.is_pregnant ? 'text-pink-700' : 'text-gray-700'}`}>
              {patient.is_pregnant ? 'Sí' : 'No'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${patient.has_cardiovascular_risk ? 'bg-purple-50' : 'bg-gray-50'}`}>
            <p className="text-sm text-gray-600 mb-1">Riesgo Cardiovascular</p>
            <p className={`text-lg font-semibold ${patient.has_cardiovascular_risk ? 'text-purple-700' : 'text-gray-700'}`}>
              {patient.has_cardiovascular_risk ? patient.cardiovascular_risk_level || 'Sí' : 'No'}
            </p>
          </div>
        </div>
      </div>

      {/* Controls */}
      {patient.controls && patient.controls.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            <FileText className="inline h-5 w-5 mr-2" />
            Controles Requeridos
          </h3>
          <div className="space-y-3">
            {patient.controls.map((control) => (
              <div
                key={control.id}
                className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{control.control_name}</p>
                  <div className="flex items-center gap-3 mt-1">
                    <span className={`text-sm capitalize px-2 py-1 rounded ${
                      control.status === 'completado' ? 'bg-green-100 text-green-800' :
                      control.status === 'programado' ? 'bg-blue-100 text-blue-800' :
                      control.status === 'vencido' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {control.status}
                    </span>
                    {control.scheduled_date && (
                      <span className="text-sm text-gray-500">
                        Programado: {new Date(control.scheduled_date).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                  {control.notes && (
                    <p className="text-sm text-gray-600 mt-1">{control.notes}</p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {control.is_urgent && (
                    <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800">
                      Urgente
                    </span>
                  )}
                  <button
                    onClick={() => handleOpenControlModal(control)}
                    className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700"
                  >
                    Gestionar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alerts */}
      {patient.alerts && patient.alerts.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            <AlertCircle className="inline h-5 w-5 mr-2" />
            Alertas Activas
          </h3>
          <div className="space-y-3">
            {patient.alerts.map((alert) => {
              const priorityColors = {
                urgente: 'border-red-500 bg-red-50',
                alta: 'border-orange-500 bg-orange-50',
                media: 'border-yellow-500 bg-yellow-50',
                baja: 'border-green-500 bg-green-50',
              };

              return (
                <div
                  key={alert.id}
                  className={`p-4 border-l-4 rounded ${priorityColors[alert.priority] || 'border-gray-500 bg-gray-50'}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-gray-900">{alert.alert_name}</p>
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium capitalize ${
                          alert.priority === 'urgente' ? 'bg-red-100 text-red-800' :
                          alert.priority === 'alta' ? 'bg-orange-100 text-orange-800' :
                          alert.priority === 'media' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {alert.priority}
                        </span>
                        <span className={`text-xs capitalize px-2 py-1 rounded ${
                          alert.status === 'completada' ? 'bg-green-100 text-green-800' :
                          alert.status === 'programada' ? 'bg-blue-100 text-blue-800' :
                          alert.status === 'notificada' ? 'bg-purple-100 text-purple-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {alert.status}
                        </span>
                      </div>
                      {alert.reason && (
                        <p className="text-sm text-gray-600 mt-1">{alert.reason}</p>
                      )}
                      {alert.notes && (
                        <p className="text-sm text-gray-500 mt-1 italic">Nota: {alert.notes}</p>
                      )}
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <button
                        onClick={() => handleOpenAlertModal(alert)}
                        className="px-3 py-1 text-sm bg-primary-600 text-white rounded hover:bg-primary-700"
                      >
                        Gestionar
                      </button>
                      {alert.status === 'activa' && (
                        <button
                          onClick={() => handleDismissAlert(alert.id)}
                          className="px-2 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                          title="Descartar alerta"
                        >
                          <XCircle className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ==================== CONTACT MODAL ==================== */}
      {showContactModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Registrar Contacto</h3>
              <button onClick={() => setShowContactModal(false)} className="text-gray-400 hover:text-gray-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado del Contacto
                </label>
                <select
                  value={contactStatus}
                  onChange={(e) => setContactStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="">Seleccionar...</option>
                  <option value="contactado">Contactado</option>
                  <option value="no_contesta">No contesta</option>
                  <option value="numero_errado">Número errado</option>
                  <option value="programado">Programado</option>
                  <option value="no_interesado">No interesado</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas
                </label>
                <textarea
                  value={contactNotes}
                  onChange={(e) => setContactNotes(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Detalles del contacto..."
                />
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={handleUpdateContact}
                disabled={!contactStatus}
                className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-300"
              >
                Guardar
              </button>
              <button
                onClick={() => setShowContactModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==================== CONTROL MODAL ==================== */}
      {showControlModal && selectedControl && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Gestionar Control</h3>
              <button onClick={() => setShowControlModal(false)} className="text-gray-400 hover:text-gray-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="mb-4">
              <p className="font-medium text-gray-900">{selectedControl.control_name}</p>
              <p className="text-sm text-gray-500 capitalize">Estado actual: {selectedControl.status}</p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nuevo Estado
                </label>
                <select
                  value={controlStatus}
                  onChange={(e) => setControlStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="pendiente">Pendiente</option>
                  <option value="programado">Programado</option>
                  <option value="completado">Completado</option>
                  <option value="vencido">Vencido</option>
                  <option value="cancelado">Cancelado</option>
                </select>
              </div>

              {(controlStatus === 'programado' || scheduledDate) && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fecha Programada
                  </label>
                  <input
                    type="date"
                    value={scheduledDate}
                    onChange={(e) => setScheduledDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas
                </label>
                <textarea
                  value={controlNotes}
                  onChange={(e) => setControlNotes(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Observaciones..."
                />
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={handleUpdateControl}
                className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                Actualizar
              </button>
              <button
                onClick={() => setShowControlModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==================== ALERT MODAL ==================== */}
      {showAlertModal && selectedAlert && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Gestionar Alerta</h3>
              <button onClick={() => setShowAlertModal(false)} className="text-gray-400 hover:text-gray-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="mb-4">
              <p className="font-medium text-gray-900">{selectedAlert.alert_name}</p>
              <p className="text-sm text-gray-500">Prioridad: <span className="capitalize font-medium">{selectedAlert.priority}</span></p>
              <p className="text-sm text-gray-500 capitalize">Estado actual: {selectedAlert.status}</p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nuevo Estado
                </label>
                <select
                  value={alertStatus}
                  onChange={(e) => setAlertStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="activa">Activa</option>
                  <option value="notificada">Notificada</option>
                  <option value="programada">Programada</option>
                  <option value="completada">Completada</option>
                  <option value="ignorada">Ignorada</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas
                </label>
                <textarea
                  value={alertNotes}
                  onChange={(e) => setAlertNotes(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Acción tomada u observaciones..."
                />
              </div>
            </div>

            <div className="mt-6 flex gap-3">
              <button
                onClick={handleUpdateAlert}
                className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                Actualizar
              </button>
              <button
                onClick={() => setShowAlertModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientDetail;
