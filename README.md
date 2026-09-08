# InsightBoard

Plataforma de analitica que permite recolectar datos, generar reportes personalizados, visualizar estadisticas interactivas con Chart.js y exportar resultados.

---

## Demo en vivo

**https://insightboard-gf27.onrender.com/**

Credenciales:
- Email: `admin@insightboard.com`
- Contrasena: `admin123`

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

## Estructura del proyecto

```
InsightBoard/
├── config/                  # Configuracion de Django
│   ├── settings/            # Ajustes del proyecto
│   ├── urls.py              # Rutas de la API
│   ├── celery_app.py        # Tareas en segundo plano
│   ├── wsgi.py              # Servidor web
│   └── asgi.py              # Servidor asincrono
├── apps/                    # Aplicaciones Django
│   ├── users/               # Manejo de usuarios
│   ├── analytics/           # Logica de analitica
│   └── core/                # Utilidades generales
├── frontend/                # Paginas web
│   ├── login.html           # Pagina de login
│   ├── index.html           # Dashboard principal
│   ├── events.html          # Registro de eventos
│   ├── reports.html         # Reportes personalizados
│   ├── css/style.css        # Estilos
│   └── js/                  # JavaScript
├── tutorials/               # Guia de tutoriales
├── docker-compose.yml       # Configuracion Docker
├── Dockerfile               # imagen Docker
├── pyproject.toml           # Dependencias Python
└── manage.py                # Comando de gestion
```

---

## Levantar el proyecto

### Con Docker (recomendado)

```bash
# 1. Clona el repositorio
git clone https://github.com/LillianaU/InsightBoard.git
cd InsightBoard

# 2. Levanta los servicios
docker-compose up -d

# 3. Aplica migraciones
docker-compose exec web uv run python manage.py migrate

# 4. Crea un superusuario
docker-compose exec web uv run python manage.py createsuperuser

# 5. Abre el navegador
# Login: http://127.0.0.1:8000/login.html
# Dashboard: http://127.0.0.1:8000/index.html
# API Docs: http://127.0.0.1:8000/api/docs/
# Admin: http://127.0.0.1:8000/admin/
```

### Sin Docker

```bash
# 1. Instala dependencias
pip install -r requirements.txt

# 2. Configura la base de datos (necesitas PostgreSQL corriendo)
# Editar config/settings/base.py con tus credenciales

# 3. Aplica migraciones
python manage.py migrate

# 4. Crea superusuario
python manage.py createsuperuser

# 5. Ejecuta el servidor
python manage.py runserver
```

---

## Credenciales de acceso

| Usuario | Contrasena | Descripcion |
|---------|-----------|-------------|
| `admin@insightboard.com` | `admin123` | Administrador del sistema |

---

## Paginas del frontend

| Pagina | URL | Descripcion |
|--------|-----|-------------|
| Login | `/login.html` | Iniciar sesion |
| Dashboard | `/index.html` | Estadisticas y graficos |
| Eventos | `/events.html` | Registrar eventos |
| Reportes | `/reports.html` | Crear reportes |
| API Docs | `/api/docs/` | Documentacion Swagger |
| Admin | `/admin/` | Panel de administracion |

---

## Endpoints principales

| Metodo | Endpoint | Descripcion | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Crear cuenta | No |
| POST | `/api/auth/login/` | Iniciar sesion | No |
| GET | `/api/auth/me/` | Usuario actual | JWT |
| POST | `/api/events/ingest/` | Crear evento | No |
| POST | `/api/events/csv/` | Importar CSV | No |
| GET | `/api/events/list/` | Listar eventos | JWT |
| GET/POST | `/api/events/sources/` | Fuentes de datos | JWT |
| GET | `/api/metrics/summary/` | Resumen general | JWT |
| GET | `/api/metrics/timeseries/` | Datos para graficos | JWT |
| GET | `/api/metrics/breakdown/` | Datos agrupados | JWT |
| GET | `/api/metrics/heatmap/` | Heatmap | JWT |
| POST | `/api/metrics/refresh/` | Refrescar metricas | JWT |
| GET/POST | `/api/reports/` | Reportes guardados | JWT |
| GET/PUT/DELETE | `/api/reports/<id>/` | Detalle reporte | JWT |
| GET | `/api/docs/` | Swagger UI | No |
| GET | `/api/health/` | Health check | No |

---

## Variables de entorno

| Variable | Descripcion | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | URL de PostgreSQL | `postgres://user:pass@host:5432/db` |
| `DJANGO_SECRET_KEY` | Clave secreta | `mi-clave-secreta-123` |
| `DEBUG` | Modo desarrollo | `True` o `False` |
| `ALLOWED_HOSTS` | Dominios permitidos | `localhost,127.0.0.1` |
| `REDIS_URL` | URL de Redis | `redis://redis:6379/0` |

---

## Desplegar en Render

1. Sube el codigo a GitHub
2. En Render, crea un **Web Service** desde tu repositorio
3. Agrega un servicio **PostgreSQL**
4. Configura las variables de entorno
5. Render desplegara automaticamente

---

## Solucion de problemas

### "No puedo acceder al frontend"
Asegurate de que el backend este corriendo y accede a `/login.html`

### "Error de conexion en el login"
Verifica que el backend este en `/api/` y que CORS este habilitado

### "Page not found (404)"
Las URLs validas son: `/login.html`, `/index.html`, `/api/docs/`, `/admin/`

### "Password hunter2 no es valida"
La contrasena de demo es `admin123`, no `hunter2`

---

## Licencia

MIT
