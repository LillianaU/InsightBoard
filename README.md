# InsightBoard

Plataforma de analítica que permite recolectar datos, generar reportes personalizados, visualizar estadísticas interactivas con D3.js y exportar resultados.

## Stack técnico

| Capa | Tecnología | Motivo |
|------|-----------|--------|
| Backend | Django + Django REST Framework | Rápido, seguro y profesional |
| Base de datos | PostgreSQL | Vistas materializadas, JSON, consultas complejas |
| Documentación API | drf-spectacular (Swagger/OpenAPI) | Documentación automática |
| Frontend | Bootstrap 5 + Chart.js | Interfaz responsive y gráficos |
| Autenticación | JWT (SimpleJWT) | Estándar moderno |
| Exportación | openpyxl / ReportLab / csv | Excel, PDF y CSV |
| Despliegue | Railway / Render + Vercel | Fácil de mostrar en vivo |

## Características

1. **Recolección de datos** - Endpoint para recibir eventos con JSONField, importación de CSV/Excel
2. **Dashboards interactivos** - Gráficos de líneas, barras, pasteles/donuts con Chart.js
3. **Reportes personalizados** - Crear reportes eligiendo métricas, dimensiones y filtros
4. **Exportación** - Excel, PDF y CSV con gráficos incluidos
5. **Vistas materializadas en PostgreSQL** - Rendimiento optimizado para métricas

## Frontend

El frontend está construido con **Bootstrap 5** y **Chart.js**. Incluye:

- **Dashboard** (`frontend/index.html`) - Estadísticas generales y gráficos
- **Eventos** (`frontend/events.html`) - Formulario para registrar eventos
- **Reportes** (`frontend/reports.html`) - Crear y visualizar reportes personalizados

Para abrir el frontend:

```bash
# Opción 1: Abrir directamente
start frontend/index.html

# Opción 2: Servir con Python
cd frontend
python -m http.server 8080
```

**Nota:** Asegúrate de que el backend esté corriendo en `http://127.0.0.1:8000`.

## Levantar el proyecto

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/InsightBoard.git
cd InsightBoard

# 2. Levanta los servicios con Docker Compose
docker-compose up -d

# 3. Aplica migraciones
docker-compose exec web uv run python manage.py migrate

# 4. Crea un superusuario
docker-compose exec web uv run python manage.py createsuperuser

# 5. Abre el navegador en:
#    - Frontend: http://localhost:8080
#    - API Docs: http://127.0.0.1:8000/api/docs/
#    - Admin: http://127.0.0.1:8000/admin/
```

## Credenciales de acceso

| Usuario | Contraseña | Descripción |
|---------|-----------|-------------|
| `admin` | `admin123` | Administrador del sistema |

Estas credenciales se crean al ejecutar `createsuperuser`.

## Acceder al sistema

1. Abre el frontend: `http://localhost:8080`
2. Ingresa con `admin` / `admin123`
3. Verás el dashboard con estadísticas

## Solución de problemas frontend

### "No puedo acceder al frontend"
Sirve el frontend con un servidor local:
```bash
cd frontend
python -m http.server 8080
```

### "Error de conexión en el login"
Asegúrate de que el backend esté corriendo:
```bash
docker-compose ps
```

### "No veo el login"
Abre directamente: `frontend/login.html` o `http://localhost:8080/login.html`

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/events/ingest/` | Recibir nuevos datos |
| GET | `/api/events/list/` | Listar eventos |
| POST | `/api/events/csv/` | Importar CSV |
| GET | `/api/metrics/summary/` | Resumen general |
| GET | `/api/metrics/timeseries/` | Datos para gráficos de línea |
| GET | `/api/metrics/breakdown/` | Datos agrupados (barras/pie) |
| GET | `/api/metrics/heatmap/` | Datos para heatmap |
| POST | `/api/metrics/refresh/` | Refrescar vista materializada |
| POST | `/api/reports/` | Crear reporte personalizado |
| GET | `/api/reports/{id}/` | Detalle de reporte |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/health/` | Health check |

## Licencia

MIT
