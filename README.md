# InsightBoard

Plataforma de analitica que permite recolectar datos, generar reportes personalizados, visualizar estadisticas interactivas con Chart.js y exportar resultados.

---

## Demo en vivo

**https://insightboard-gf27.onrender.com/**

Credenciales:
- Email: `admin@insightboard.com`
- Contrasena: `admin123`

---

## Guia completa de construccion

Para aprender a construir InsightBoard desde cero, consulta la **[Guia de tutoriales](./tutorials/README.md)**.

| Cap | Titulo | Tiempo |
|-----|--------|--------|
| [C0](./tutorials/c0/README.md) | Que es InsightBoard | 10 min |
| [C1](./tutorials/c1/README.md) | Preparar tu computadora | 20 min |
| [C2](./tutorials/c2/README.md) | Docker y base de datos | 25 min |
| [C3](./tutorials/c3/README.md) | Crear el proyecto Django | 35 min |
| [C4](./tutorials/c4/README.md) | Modelos de base de datos | 30 min |
| [C5](./tutorials/c5/README.md) | API REST con DRF | 40 min |
| [C6](./tutorials/c6/README.md) | Frontend y dashboards | 35 min |
| [C7](./tutorials/c7/README.md) | Autenticacion JWT | 25 min |
| [C8](./tutorials/c8/README.md) | Probar el proyecto | 20 min |
| [C9](./tutorials/c9/README.md) | Publicar en Render | 30 min |

---

## Stack tecnico

| Capa | Tecnologia | Motivo |
|------|-----------|--------|
| Backend | Django + Django REST Framework | Rapido, seguro y profesional |
| Base de datos | PostgreSQL | Vistas materializadas, JSON, consultas complejas |
| Documentacion API | drf-spectacular (Swagger/OpenAPI) | Documentacion automatica |
| Frontend | Bootstrap 5 + Chart.js | Interfaz responsive y graficos |
| Autenticacion | JWT (SimpleJWT) | Estandar moderno |
| Container | Docker + Docker Compose | Empaquetado portable |
| Deploy | Render | Hosting gratuito con PostgreSQL |

---

## Capas de seguridad (8)

1. **SECRET_KEY** - Nunca hardcodeada, obligatoria via variable de entorno
2. **DEBUG** - Por defecto False en produccion
3. **ALLOWED_HOSTS** - Solo dominios explicitos configurados
4. **CORS** - Solo origenes permitidos (no permite todos)
5. **Rate limiting** - Throttling en endpoints de ingestion (30/hora anon, 1000/hora autenticado)
6. **JWT Seguro** - Tokens con rotacion y blacklist
7. **XSS Protection** - Frontend usa textContent en vez de innerHTML
8. **SQL Injection** - Django ORM previene inyeccion SQL automaticamente

---

## Caracteristicas

1. **Recoleccion de datos** - Endpoint para recibir eventos con JSONField, importacion de CSV
2. **Dashboards interactivos** - Graficos de lineas, barras, pasteles/donuts con Chart.js
3. **Reportes personalizados** - Crear reportes eligiendo metricas, dimensiones y filtros
4. **Exportacion** - CSV con datos agrupados
5. **Vistas materializadas en PostgreSQL** - Rendimiento optimizado para metricas

---

## Levantar el proyecto

### Con Docker (recomendado)

```bash
# 1. Clona el repositorio
git clone https://github.com/LillianaU/InsightBoard.git
cd InsightBoard

# 2. Copia el archivo de variables de entorno
cp .env.example .env

# 3. Levanta los servicios
docker-compose up -d

# 4. Aplica migraciones
docker-compose exec web uv run python manage.py migrate

# 5. Crea superusuario
docker-compose exec web uv run python manage.py createsuperuser

# 6. Abre el navegador
# Login: http://127.0.0.1:8000/login.html
# Dashboard: http://127.0.0.1:8000/index.html
# API Docs: http://127.0.0.1:8000/api/docs/
# Admin: http://127.0.0.1:8000/admin/
```

### Sin Docker

```bash
# 1. Instala dependencias
pip install -r requirements.txt

# 2. Configura PostgreSQL manualmente
# Editar config/settings/base.py

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
| `DJANGO_SECRET_KEY` | Clave secreta (obligatoria) | `mi-clave-secreta-123` |
| `DJANGO_SETTINGS_MODULE` | Modulo de settings | `config.settings.production` |
| `DEBUG` | Modo desarrollo | `True` o `False` |
| `ALLOWED_HOSTS` | Dominios permitidos | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Origenes CORS permitidos | `http://localhost:3000` |

---

## Desplegar en Render

1. Sube el codigo a GitHub
2. En Render, crea un **Web Service** desde tu repositorio
3. Agrega un servicio **PostgreSQL**
4. Configura las variables de entorno
5. Render desplegara automaticamente

Para instrucciones detalladas, ve el [Capitulo 9: Publicar en Render](./tutorials/c9/README.md).

---

## Solucion de problemas

### "No puedo acceder al frontend"
Asegurate de que el backend este corriendo y accede a `/login.html`

### "Error de conexion en el login"
Verifica que el backend este en `/api/` y que CORS este habilitado

### "Page not found (404)"
Las URLs validas son: `/login.html`, `/index.html`, `/api/docs/`, `/admin/`

### "Password validation failed"
La contrasena debe tener 8+ caracteres

---

## Licencia

MIT
