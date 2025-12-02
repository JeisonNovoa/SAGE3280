# Inicio Rápido - SAGE3280

## Iniciar el Sistema

### Paso 1: Configurar el entorno

```bash
cd C:\Users\jeiso\Desktop\SAGE3280
cp backend\.env.example backend\.env
```

### Paso 2: Iniciar con Docker

```bash
docker-compose up -d
```

Espera unos segundos a que los servicios se inicien.

### Paso 3: Acceder a la aplicación

Abre tu navegador y ve a:
- **Aplicación**: http://localhost
- **API Docs**: http://localhost:8000/api/docs

## Uso Básico

### 1. Cargar tu primera base de datos

1. Haz clic en "Cargar Excel" en el menú superior
2. Arrastra o selecciona tu archivo Excel con los pacientes
3. Espera a que se procese (verás una barra de progreso)
4. Listo! Ya puedes ver el dashboard

### 2. Ver el Dashboard

Haz clic en "Dashboard" para ver:
- Total de pacientes
- Distribución por edades
- Controles pendientes
- Alertas activas

### 3. Buscar Pacientes

1. Haz clic en "Pacientes"
2. Usa los filtros para buscar:
   - Por nombre o documento
   - Por grupo de edad
   - Por sexo
   - Por estado de contacto

### 4. Exportar Listas

1. En la página de Pacientes, aplica los filtros que necesites
2. Haz clic en "Exportar"
3. El archivo Excel se descargará automáticamente

## Formato del Archivo Excel

Tu archivo debe tener estas columnas (mínimo):

| Documento | Nombre  | Apellido | Edad | Sexo | Teléfono   |
|-----------|---------|----------|------|------|------------|
| 12345678  | Juan    | Pérez    | 45   | M    | 3001234567 |
| 87654321  | María   | García   | 32   | F    | 3007654321 |

Columnas opcionales: Email, Dirección, Ciudad, EPS, Diagnósticos

## Comandos Útiles

### Ver logs del sistema
```bash
docker-compose logs -f
```

### Detener el sistema
```bash
docker-compose down
```

### Reiniciar el sistema
```bash
docker-compose restart
```

### Borrar todos los datos (¡CUIDADO!)
```bash
docker-compose down -v
```

## Solución de Problemas

### El puerto 80 ya está en uso
Si el puerto 80 está ocupado, edita `docker-compose.yml` y cambia:
```yaml
frontend:
  ports:
    - "8080:80"  # Cambia 80 por otro puerto como 8080
```

### No se puede conectar al backend
Verifica que los 3 servicios estén corriendo:
```bash
docker-compose ps
```

Deberías ver:
- sage3280_db (up)
- sage3280_backend (up)
- sage3280_frontend (up)

### Error al procesar Excel
- Verifica que el archivo tenga al menos las columnas requeridas
- Asegúrate de que los datos estén en el formato correcto
- Revisa los logs: `docker-compose logs backend`

## Próximos Pasos

1. **Implementar la lógica de filtrado completa**: Una vez que proporciones el PDF con la guía de Resolución 3280, se completará la lógica de clasificación en:
   - `backend/app/services/classifier.py`
   - `backend/app/services/alert_generator.py`

2. **Configurar WhatsApp/SMS**: Para envío automático de mensajes

3. **Personalizar alertas**: Según las necesidades específicas de tu IPS

## Contacto

¿Necesitas ayuda? Contacta al equipo de desarrollo.

---

🚀 **SAGE3280** - Simplificando la gestión de APS
