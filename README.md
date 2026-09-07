# InsightBoard

Plataforma de analitica que permite recolectar datos, generar reportes personalizados, visualizar estadisticas interactivas con Chart.js y exportar resultados.

---

## Tutoriales

Para aprender a construir InsightBoard desde cero, consulta la **[Guia de tutoriales](./tutorials/README.md)**.

| Cap | Tema | Tiempo |
|-----|------|--------|
| [C0](./tutorials/c0/README.md) | Que es InsightBoard | 10 min |
| [C1](./tutorials/c1/README.md) | Instalar herramientas | 20 min |
| [C2](./tutorials/c2/README.md) | Docker y base de datos | 25 min |
| [C3](./tutorials/c3/README.md) | Crear proyecto Django | 35 min |
| [C4](./tutorials/c4/README.md) | Modelos de base de datos | 30 min |
| [C5](./tutorials/c5/README.md) | API REST con DRF | 40 min |
| [C6](./tutorials/c6/README.md) | Frontend y dashboards | 35 min |
| [C7](./tutorials/c7/README.md) | Autenticacion JWT | 25 min |
| [C8](./tutorials/c8/README.md) | Probar y deploy | 20 min |

---

## Stack tecnico

| Capa | Tecnologia | Motivo |
|------|-----------|--------|
| Backend | Django + Django REST Framework | Rapido, seguro y profesional |
| Base de datos | PostgreSQL | Vistas materializadas, JSON, consultas complejas |
| Documentacion API | drf-spectacular (Swagger/OpenAPI) | Documentacion automatica |
| Frontend | Bootstrap 5 + Chart.js | Interfaz responsive y graficos |
| Autenticacion | JWT (SimpleJWT) | Estandar moderno |
| Exportacion | openpyxl / ReportLab / csv | Excel, PDF y CSV |
| Container | Docker + Docker Compose | Empaquetado portable |

---

## Caracteristicas

1. **Recoleccion de datos** - Endpoint para recibir eventos con JSONField, importacion de CSV
2. **Dashboards interactivos** - Graficos de lineas, barras, pasteles/donuts con Chart.js
3. **Reportes personalizados** - Crear reportes eligiendo metricas, dimensiones y filtros
4. **Exportacion** - Excel, PDF y CSV con graficos incluidos
5. **Vistas materializadas en PostgreSQL** - Rendimiento optimizado para metricas

---

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

---

## Credenciales de acceso

| Usuario | Contrasena | Descripcion |
|---------|-----------|-------------|
| `admin@insightboard.com` | `admin123` | Administrador del sistema |

---

## Frontend

El frontend esta construido con **Bootstrap 5** y **Chart.js**. Incluye:

- **Dashboard** (`frontend/index.html`) - Estadisticas generales y graficos
- **Eventos** (`frontend/events.html`) - Formulario para registrar eventos
- **Reportes** (`frontend/reports.html`) - Crear y visualizar reportes personalizados

Para abrir el frontend:

```bash
cd frontend
python -m http.server 8080
```

---

## Endpoints principales

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | `/api/events/ingest/` | Recibir nuevos datos |
| GET | `/api/events/list/` | Listar eventos |
| POST | `/api/events/csv/` | Importar CSV |
| GET | `/api/metrics/summary/` | Resumen general |
| GET | `/api/metrics/timeseries/` | Datos para graficos de linea |
| GET | `/api/metrics/breakdown/` | Datos agrupados (barras/pie) |
| GET | `/api/metrics/heatmap/` | Datos para heatmap |
| POST | `/api/metrics/refresh/` | Refrescar vista materializada |
| POST | `/api/reports/` | Crear reporte personalizado |
| GET | `/api/reports/{id}/` | Detalle de reporte |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/health/` | Health check |

---

## Solucion de problemas

### "No puedo acceder al frontend"
Sirve el frontend con un servidor local:
```bash
cd frontend
python -m http.server 8080
```

### "Error de conexion en el login"
Asegurate de que el backend este corriendo:
```bash
docker-compose ps
```

### "No veo el login"
Abre directamente: `frontend/login.html` o `http://localhost:8080/login.html`

---

## Licencia

MIT
