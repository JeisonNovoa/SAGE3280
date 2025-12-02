import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload as UploadIcon, FileSpreadsheet, CheckCircle, XCircle, Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { uploadService } from '../services/api';

const Upload = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadStats, setUploadStats] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];

    // Validate file type
    const validTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
      'text/csv'
    ];

    if (!validTypes.includes(file.type) && !file.name.match(/\.(xlsx|xls|csv)$/i)) {
      toast.error('Por favor selecciona un archivo Excel (.xlsx, .xls) o CSV');
      return;
    }

    setUploading(true);
    setUploadResult(null);
    setUploadStats(null);

    try {
      const result = await uploadService.uploadFile(file);
      setUploadResult(result);
      toast.success('Archivo subido correctamente. Procesando...');

      // Poll for upload status
      pollUploadStatus(result.id);
    } catch (error) {
      console.error('Error uploading file:', error);
      toast.error('Error al subir el archivo');
      setUploading(false);
    }
  }, []);

  const pollUploadStatus = async (uploadId) => {
    const maxAttempts = 60; // 1 minute max
    let attempts = 0;

    const interval = setInterval(async () => {
      try {
        const status = await uploadService.getUploadStatus(uploadId);
        setUploadResult(status);

        if (status.status === 'completed') {
          clearInterval(interval);
          setUploading(false);
          toast.success(`Procesamiento completado: ${status.success_rows} pacientes procesados`);

          // Get stats
          const stats = await uploadService.getUploadStats(uploadId);
          setUploadStats(stats);
        } else if (status.status === 'failed') {
          clearInterval(interval);
          setUploading(false);
          toast.error('Error al procesar el archivo');
        }

        attempts++;
        if (attempts >= maxAttempts) {
          clearInterval(interval);
          setUploading(false);
        }
      } catch (error) {
        clearInterval(interval);
        setUploading(false);
        console.error('Error checking upload status:', error);
      }
    }, 1000);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    multiple: false,
    disabled: uploading
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Cargar Base de Datos</h2>
        <p className="mt-2 text-sm text-gray-600">
          Sube un archivo Excel o CSV con la información de los pacientes
        </p>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-gray-400'}
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center">
          {uploading ? (
            <Loader className="h-12 w-12 text-primary-500 animate-spin mb-4" />
          ) : (
            <UploadIcon className="h-12 w-12 text-gray-400 mb-4" />
          )}

          <p className="text-lg font-medium text-gray-900 mb-2">
            {uploading
              ? 'Procesando archivo...'
              : isDragActive
              ? 'Suelta el archivo aquí'
              : 'Arrastra y suelta un archivo aquí, o haz clic para seleccionar'
            }
          </p>

          <p className="text-sm text-gray-500">
            Formatos soportados: .xlsx, .xls, .csv (máx. 50MB)
          </p>
        </div>
      </div>

      {/* Upload Result */}
      {uploadResult && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Estado del Procesamiento
            </h3>
            {uploadResult.status === 'completed' && (
              <CheckCircle className="h-6 w-6 text-green-500" />
            )}
            {uploadResult.status === 'failed' && (
              <XCircle className="h-6 w-6 text-red-500" />
            )}
            {uploadResult.status === 'processing' && (
              <Loader className="h-6 w-6 text-primary-500 animate-spin" />
            )}
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Archivo:</span>
              <span className="font-medium text-gray-900">{uploadResult.original_filename}</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Total de filas:</span>
              <span className="font-medium text-gray-900">{uploadResult.total_rows}</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Procesadas:</span>
              <span className="font-medium text-gray-900">{uploadResult.processed_rows}</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Exitosas:</span>
              <span className="font-medium text-green-600">{uploadResult.success_rows}</span>
            </div>

            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Errores:</span>
              <span className="font-medium text-red-600">{uploadResult.error_rows}</span>
            </div>

            {uploadResult.error_message && (
              <div className="mt-4 p-3 bg-red-50 rounded-md">
                <p className="text-sm text-red-700">{uploadResult.error_message}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Upload Stats */}
      {uploadStats && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Resumen del Procesamiento
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Pacientes</p>
              <p className="text-3xl font-bold text-gray-900">{uploadStats.total_patients}</p>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <p className="text-sm text-green-600 mb-1">Controles Generados</p>
              <p className="text-3xl font-bold text-green-700">{uploadStats.controls_generated}</p>
            </div>

            <div className="bg-orange-50 p-4 rounded-lg">
              <p className="text-sm text-orange-600 mb-1">Alertas Generadas</p>
              <p className="text-3xl font-bold text-orange-700">{uploadStats.alerts_generated}</p>
            </div>
          </div>

          {uploadStats.patients_by_age_group && Object.keys(uploadStats.patients_by_age_group).length > 0 && (
            <div className="mt-6">
              <h4 className="text-sm font-medium text-gray-700 mb-3">Distribución por Grupo Etario</h4>
              <div className="space-y-2">
                {Object.entries(uploadStats.patients_by_age_group).map(([group, count]) => (
                  <div key={group} className="flex justify-between text-sm">
                    <span className="text-gray-600 capitalize">{group.replace('_', ' ')}</span>
                    <span className="font-medium text-gray-900">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          Formato del Archivo
        </h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>El archivo Excel debe contener al menos las siguientes columnas:</p>
          <ul className="list-disc list-inside ml-4 space-y-1">
            <li><strong>Documento:</strong> Número de identificación del paciente</li>
            <li><strong>Nombre/Apellido:</strong> Nombres y apellidos</li>
            <li><strong>Edad o Fecha de Nacimiento:</strong> Para calcular grupo etario</li>
            <li><strong>Sexo:</strong> M/F (Masculino/Femenino)</li>
            <li><strong>Teléfono:</strong> Número de contacto</li>
          </ul>
          <p className="mt-3">
            Columnas opcionales: Email, Dirección, Ciudad, EPS, Diagnósticos, Fecha Último Control
          </p>
        </div>
      </div>
    </div>
  );
};

export default Upload;
