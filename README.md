# SAGE3280™

**Sistema de Gestión de Atención Primaria en Salud - Resolución 3280**

SAGE3280 es una aplicación de inteligencia artificial para Atención Primaria en Salud (APS) que automatiza la gestión de pacientes, controles médicos y alertas preventivas según la Resolución 3280 de Colombia.

## Características Principales

- ✅ **Carga y Procesamiento de Excel**: Sube bases de datos poblacionales y procesa automáticamente miles de registros
- ✅ **Clasificación Automática**: Clasifica pacientes por grupos etarios y condiciones de salud
- ✅ **Generación de Controles**: Determina qué controles médicos necesita cada paciente según normativa
- ✅ **Alertas Preventivas**: Genera alertas para exámenes y procedimientos según edad, sexo y riesgos
- ✅ **Dashboard Interactivo**: Visualiza estadísticas, métricas y cobertura en tiempo real
- ✅ **Exportación de Listas**: Exporta listas filtradas a Excel para gestión de contactos
- ✅ **Gestión de Pacientes**: Busca, filtra y visualiza información detallada de cada paciente

## Tecnologías

### Backend
- **Python 3.11**
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **PostgreSQL**: Base de datos relacional
- **Pandas**: Procesamiento de datos Excel
- **Pydantic**: Validación de datos

### Frontend
- **React 18**: Librería UI
- **Vite**: Build tool ultra rápido
- **TailwindCSS**: Framework CSS utility-first
- **Recharts**: Gráficas y visualizaciones
- **Axios**: Cliente HTTP
- **React Router**: Navegación

### Infraestructura
- **Docker & Docker Compose**: Containerización
- **PostgreSQL**: Base de datos
- **Nginx**: Servidor web para frontend

## Requisitos Previos

- Docker y Docker Compose instalados
- Git (opcional)

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

1. Clona o descarga el repositorio:
```bash
git clone <repository-url>
cd SAGE3280
```

2. Copia el archivo de variables de entorno:
```bash
cp backend/.env.example backend/.env
```

3. Inicia los servicios con Docker Compose:
```bash
docker-compose up -d
```

4. Accede a la aplicación:
- **Frontend**: http://localhost
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/api/docs

5. Para detener los servicios:
```bash
docker-compose down
```

### Opción 2: Sin Docker (Desarrollo Local)

#### Backend

1. Instala Python 3.11+ y PostgreSQL

2. Crea un entorno virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

5. Inicia el servidor:
```bash
uvicorn app.main:app --reload
```

#### Frontend

1. Instala Node.js 18+

2. Instala dependencias:
```bash
cd frontend
npm install
```

3. Inicia el servidor de desarrollo:
```bash
npm run dev
```

4. Accede a: http://localhost:3000

## Uso

### 1. Cargar Base de Datos

1. Ve a la sección **"Cargar Excel"**
2. Arrastra o selecciona un archivo Excel/CSV con la información de pacientes
3. Espera a que el sistema procese los datos
4. Visualiza el resumen del procesamiento

**Formato del archivo Excel:**

Columnas requeridas:
- `Documento`: Número de identificación
- `Nombre/Apellido`: Nombres y apellidos del paciente
- `Edad` o `Fecha de Nacimiento`
- `Sexo`: M/F
- `Teléfono`: Número de contacto

Columnas opcionales:
- Email, Dirección, Ciudad, EPS, Diagnósticos, Fecha Último Control

### 2. Ver Dashboard

El dashboard muestra:
- Total de pacientes y métricas clave
- Distribución por grupos etarios y sexo
- Pacientes con factores de riesgo
- Controles pendientes por tipo
- Alertas activas por prioridad
- Tasa de contacto

### 3. Gestionar Pacientes

- **Buscar**: Por nombre o documento
- **Filtrar**: Por grupo etario, sexo, estado de contacto
- **Ver Detalles**: Haz clic en "Ver detalles" para ver información completa
- **Exportar**: Descarga listas filtradas en Excel o CSV

### 4. Exportar Listas

1. Aplica los filtros deseados en la lista de pacientes
2. Haz clic en "Exportar"
3. Selecciona el formato (Excel o CSV)
4. El archivo se descargará automáticamente

## Estructura del Proyecto

```
SAGE3280/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── upload.py      # Endpoints de carga de archivos
│   │   │       ├── patients.py    # Endpoints de pacientes
│   │   │       ├── stats.py       # Endpoints de estadísticas
│   │   │       └── export.py      # Endpoints de exportación
│   │   ├── models/
│   │   │   ├── patient.py         # Modelo de paciente
│   │   │   ├── control.py         # Modelo de controles
│   │   │   ├── alert.py           # Modelo de alertas
│   │   │   └── upload.py          # Modelo de cargas
│   │   ├── services/
│   │   │   ├── excel_processor.py # Procesamiento de Excel
│   │   │   ├── classifier.py      # Clasificación de pacientes
│   │   │   └── alert_generator.py # Generación de alertas
│   │   ├── schemas/               # Schemas Pydantic
│   │   ├── utils/                 # Utilidades
│   │   ├── config.py              # Configuración
│   │   ├── database.py            # Configuración DB
│   │   └── main.py                # Aplicación principal
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx         # Layout principal
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx      # Página dashboard
│   │   │   ├── Upload.jsx         # Página carga de archivos
│   │   │   ├── Patients.jsx       # Listado de pacientes
│   │   │   └── PatientDetail.jsx  # Detalle de paciente
│   │   ├── services/
│   │   │   └── api.js             # Cliente API
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## API Endpoints

### Upload
- `POST /api/upload/` - Subir archivo Excel
- `GET /api/upload/{upload_id}` - Estado de la carga
- `GET /api/upload/{upload_id}/stats` - Estadísticas de la carga

### Patients
- `GET /api/patients/` - Listar pacientes (con filtros y paginación)
- `GET /api/patients/{id}` - Obtener paciente por ID
- `GET /api/patients/document/{document}` - Buscar por documento
- `PUT /api/patients/{id}/contact` - Actualizar estado de contacto
- `GET /api/patients/list/priority` - Lista priorizada para contacto

### Stats
- `GET /api/stats/dashboard` - Estadísticas completas del dashboard
- `GET /api/stats/summary` - Resumen rápido de métricas

### Export
- `GET /api/export/patients` - Exportar pacientes filtrados
- `GET /api/export/controls` - Exportar controles por tipo
- `GET /api/export/alerts` - Exportar alertas por tipo

## Configuración

### Variables de Entorno (Backend)

```env
# Database
DATABASE_URL=postgresql://sage_user:sage_password@db:5432/sage3280_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# File Upload
MAX_UPLOAD_SIZE=52428800
ALLOWED_EXTENSIONS=xlsx,xls,csv
```

## Próximas Funcionalidades (Roadmap)

- [ ] Integración con WhatsApp Business API
- [ ] Envío automático de mensajes SMS
- [ ] Sistema de agendamiento de citas
- [ ] Registro automático de asistencias
- [ ] Multi-tenancy (múltiples IPS)
- [ ] Sistema de usuarios y roles
- [ ] Reportes avanzados para EPS
- [ ] Integración con Historia Clínica Electrónica

## Desarrollo

### Ejecutar tests (Backend)
```bash
cd backend
pytest
```

### Linting
```bash
# Backend
cd backend
flake8 app/

# Frontend
cd frontend
npm run lint
```

### Build Frontend
```bash
cd frontend
npm run build
```

## Contribuciones

Este es un proyecto privado. Para contribuir, contacta al equipo de desarrollo.

## Licencia

© 2024 SAGE3280. Todos los derechos reservados.

## Soporte

Para soporte o preguntas, contacta a: [tu-email@ejemplo.com]

## Notas Importantes

- **Lógica de Clasificación**: La lógica de filtrado detallada según la guía de Resolución 3280 debe ser implementada en `backend/app/services/classifier.py` y `alert_generator.py` una vez que se proporcione el PDF con las especificaciones completas.

- **Datos de Prueba**: Para probar el sistema, puedes crear un archivo Excel de ejemplo con datos ficticios siguiendo el formato especificado.

- **Seguridad**: En producción, asegúrate de:
  - Cambiar todas las contraseñas por defecto
  - Configurar SECRET_KEY con un valor seguro
  - Usar HTTPS
  - Configurar firewall adecuadamente
  - Hacer backups regulares de la base de datos

---

**SAGE3280™** - Sistema de Gestión APS | Resolución 3280 - 2023
