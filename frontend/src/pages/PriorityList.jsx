import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertTriangle, Phone, User, Calendar } from 'lucide-react';
import { patientsService } from '../services/api';
import toast from 'react-hot-toast';

const PriorityList = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [minPriority, setMinPriority] = useState(50);

  useEffect(() => {
    loadPriorityPatients();
  }, [minPriority]);

  const loadPriorityPatients = async () => {
    try {
      setLoading(true);
      const data = await patientsService.getPriorityList(100, minPriority);
      // The API returns { total, patients }, so we need to extract the patients array
      setPatients(data.patients || []);
    } catch (error) {
      console.error('Error loading priority patients:', error);
      toast.error('Error al cargar lista de prioridad');
      setPatients([]);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (score) => {
    if (score >= 80) return 'bg-red-100 text-red-800 border-red-300';
    if (score >= 60) return 'bg-orange-100 text-orange-800 border-orange-300';
    if (score >= 40) return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    return 'bg-green-100 text-green-800 border-green-300';
  };

  const getPriorityLabel = (score) => {
    if (score >= 80) return 'Urgente';
    if (score >= 60) return 'Alta';
    if (score >= 40) return 'Media';
    return 'Normal';
  };

  const handleViewPatient = (patientId) => {
    navigate(`/patients/${patientId}`);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Lista de Prioridad</h1>
          <p className="mt-2 text-sm text-gray-600">
            Pacientes ordenados por prioridad de contacto
          </p>
        </div>

        {/* Priority Filter */}
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-700">
            Prioridad mínima:
          </label>
          <select
            value={minPriority}
            onChange={(e) => setMinPriority(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value={0}>Todos</option>
            <option value={40}>Media o mayor (40+)</option>
            <option value={60}>Alta o mayor (60+)</option>
            <option value={80}>Urgente (80+)</option>
          </select>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total en Lista</p>
              <p className="text-2xl font-semibold text-gray-900">{patients.length}</p>
            </div>
            <User className="h-8 w-8 text-gray-400" />
          </div>
        </div>

        <div className="bg-red-50 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-red-700">Urgentes (80+)</p>
              <p className="text-2xl font-semibold text-red-900">
                {patients.filter(p => p.priority_score >= 80).length}
              </p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-500" />
          </div>
        </div>

        <div className="bg-orange-50 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-orange-700">Alta (60-79)</p>
              <p className="text-2xl font-semibold text-orange-900">
                {patients.filter(p => p.priority_score >= 60 && p.priority_score < 80).length}
              </p>
            </div>
            <AlertTriangle className="h-8 w-8 text-orange-500" />
          </div>
        </div>

        <div className="bg-yellow-50 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-yellow-700">Media (40-59)</p>
              <p className="text-2xl font-semibold text-yellow-900">
                {patients.filter(p => p.priority_score >= 40 && p.priority_score < 60).length}
              </p>
            </div>
            <AlertTriangle className="h-8 w-8 text-yellow-500" />
          </div>
        </div>
      </div>

      {/* Patients Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Prioridad
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Paciente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Edad / Sexo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contacto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Factores de Riesgo
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
              {patients.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-gray-500">
                    No hay pacientes con este nivel de prioridad
                  </td>
                </tr>
              ) : (
                patients.map((patient) => (
                  <tr key={patient.id} className="hover:bg-gray-50">
                    {/* Priority Score */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span
                          className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border ${getPriorityColor(
                            patient.priority_score
                          )}`}
                        >
                          {patient.priority_score}
                        </span>
                        <span className="ml-2 text-xs text-gray-500">
                          {getPriorityLabel(patient.priority_score)}
                        </span>
                      </div>
                    </td>

                    {/* Patient Name */}
                    <td className="px-6 py-4">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {patient.full_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          CC: {patient.document_number}
                        </div>
                      </div>
                    </td>

                    {/* Age / Sex */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{patient.age} años</div>
                      <div className="text-sm text-gray-500 capitalize">
                        {patient.sex === 'M' ? 'Masculino' : 'Femenino'}
                      </div>
                    </td>

                    {/* Contact */}
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">
                        {patient.phone || 'Sin teléfono'}
                      </div>
                      {patient.contact_attempts > 0 && (
                        <div className="text-xs text-gray-500">
                          {patient.contact_attempts} intento(s)
                        </div>
                      )}
                    </td>

                    {/* Risk Factors */}
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {patient.is_pregnant && (
                          <span className="px-2 py-1 text-xs bg-pink-100 text-pink-800 rounded">
                            Gestante
                          </span>
                        )}
                        {patient.is_hypertensive && (
                          <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded">
                            HTA
                          </span>
                        )}
                        {patient.is_diabetic && (
                          <span className="px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded">
                            DM
                          </span>
                        )}
                        {patient.has_cardiovascular_risk && (
                          <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">
                            Riesgo CV
                          </span>
                        )}
                        {!patient.is_pregnant &&
                          !patient.is_hypertensive &&
                          !patient.is_diabetic &&
                          !patient.has_cardiovascular_risk && (
                            <span className="text-xs text-gray-500">Sin factores</span>
                          )}
                      </div>
                    </td>

                    {/* Contact Status */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      {patient.is_contacted ? (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">
                          Contactado
                        </span>
                      ) : (
                        <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded">
                          Pendiente
                        </span>
                      )}
                      {patient.contact_status && (
                        <div className="text-xs text-gray-500 mt-1 capitalize">
                          {patient.contact_status}
                        </div>
                      )}
                    </td>

                    {/* Actions */}
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => handleViewPatient(patient.id)}
                        className="text-primary-600 hover:text-primary-900 mr-3"
                      >
                        Ver detalles
                      </button>
                      {patient.phone && (
                        <a
                          href={`tel:${patient.phone}`}
                          className="text-green-600 hover:text-green-900"
                        >
                          <Phone className="h-4 w-4 inline" />
                        </a>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <AlertTriangle className="h-5 w-5 text-blue-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">
              Cómo se calcula la prioridad
            </h3>
            <div className="mt-2 text-sm text-blue-700">
              <p>El puntaje de prioridad (0-100) se calcula considerando:</p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>Edad del paciente (niños y adultos mayores tienen mayor prioridad)</li>
                <li>Gestantes (+25 puntos)</li>
                <li>Enfermedades crónicas (Diabetes +15, Hipertensión +15)</li>
                <li>Nivel de riesgo cardiovascular (+5 a +20)</li>
                <li>Tiempo desde el último control (hasta +20 puntos)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PriorityList;
