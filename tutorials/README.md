# Tutoriales InsightBoard

Guia paso a paso para construir **InsightBoard** desde cero.

> **Nivel:** Principiante  
> **Duracion total:** ~4 horas  
> **Requisito:** Una computadora con Windows y conexion a Internet

---

## Tabla de contenido

| Cap | Tema | Que aprenderas | Tiempo |
|-----|------|---------------|--------|
| [C0](./c0/README.md) | [Que es InsightBoard](./c0/README.md) | Vista general del proyecto, arquitectura y tecnologias | 10 min |
| [C1](./c1/README.md) | [Instalar herramientas](./c1/README.md) | Python, VS Code, Git, uv | 20 min |
| [C2](./c2/README.md) | [Docker y base de datos](./c2/README.md) | Docker Desktop, PostgreSQL, Redis | 25 min |
| [C3](./c3/README.md) | [Crear proyecto Django](./c3/README.md) | startproject, apps, settings, migraciones | 35 min |
| [C4](./c4/README.md) | [Modelos de base de datos](./c4/README.md) | DataSource, Event, DailyMetric, SavedReport | 30 min |
| [C5](./c5/README.md) | [API REST con DRF](./c5/README.md) | Serializers, views, endpoints, Swagger | 40 min |
| [C6](./c6/README.md) | [Frontend y dashboards](./c6/README.md) | HTML, Chart.js, Bootstrap, consumo de API | 35 min |
| [C7](./c7/README.md) | [Autenticacion JWT](./c7/README.md) | Login, registro, tokens, proteccion de rutas | 25 min |
| [C8](./c8/README.md) | [Probar y deploy](./c8/README.md) | Pruebas, troubleshooting, despliegue | 20 min |

---

## Como usar estos tutoriales

1. Lee cada capitulo **en orden** (del C0 al C8)
2. Haz **cada paso exactamente como se indica**
3. **Verifica** que funciono antes de pasar al siguiente paso (cada paso tiene una prueba)
4. Si algo falla, revisa la seccion "Solucion de problemas" del capitulo

---

## Arquitectura del proyecto

```
Browser (Frontend)  --[JWT]-->  Django REST API  --[psycopg2]-->  PostgreSQL
                                      |
                                      +--[Celery]-->  Redis  -->  Background tasks
```

| Capa | Tecnologia | Para que sirve |
|------|-----------|----------------|
| Backend | Django + DRF | Crear la API y logica del servidor |
| Base de datos | PostgreSQL | Guardar eventos, usuarios, reportes |
| Cache | Redis | Memoria rapida para tareas en segundo plano |
| Frontend | Bootstrap 5 + Chart.js | Paginas web con graficos interactivos |
| Auth | JWT (SimpleJWT) | Login seguro con tokens |
| Container | Docker | Empaquetar todo para que funcione igual en cualquier computadora |

---

## Requisitos previos

- Una computadora con **Windows**
- Conexion a **Internet**
- Ganas de aprender

---

## Estructura final del proyecto

```
InsightBoard/
├── config/                  # Configuracion de Django (el cerebro)
│   ├── settings/            # Ajustes del proyecto
│   ├── urls.py              # Rutas de la API
│   ├── celery_app.py        # Configuracion de tareas en segundo plano
│   ├── wsgi.py              # Servidor web
│   └── asgi.py              # Servidor web asincrono
├── apps/                    # Aplicaciones de Django
│   ├── users/               # Manejo de usuarios
│   ├── analytics/           # Logica de analitica y eventos
│   └── core/                # Utilidades generales
├── frontend/                # Paginas web (HTML/CSS/JS)
│   ├── index.html           # Dashboard principal
│   ├── events.html          # Registro de eventos
│   ├── reports.html         # Reportes personalizados
│   ├── login.html           # Pagina de login
│   ├── css/style.css        # Estilos
│   └── js/                  # JavaScript (auth.js, app.js)
├── tutorials/               # Estos tutoriales
├── docker-compose.yml       # Configuracion de Docker
├── requirements.txt         # Dependencias de Python
└── manage.py                # Comando de gestion de Django
```

---

## Ejecutar el proyecto (paso a paso)

Si ya tienes el codigo y solo quieres correrlo, sigue estos pasos **en orden**:

1. **Abre Docker Desktop** y espera a que la ballena indique que esta corriendo
2. **Levanta los servicios:**
   ```bash
   docker-compose up -d
   docker-compose ps
   ```
3. **Aplica migraciones:**
   ```bash
   docker-compose exec web uv run python manage.py migrate
   ```
4. **Crea un superusuario** (solo la primera vez):
   ```bash
   docker-compose exec web uv run python manage.py createsuperuser
   ```
5. **Inicia el frontend** (en una segunda terminal):
   ```bash
   cd frontend
   python -m http.server 8080
   ```
6. **Abre en el navegador:**
   - Frontend: http://localhost:8080
   - API Docs (Swagger): http://127.0.0.1:8000/api/docs/
   - Admin: http://127.0.0.1:8000/admin/

> Tienes la version extendida con todos los detalles en el [Paso 0 del Cap 8](./c8/README.md#paso-0-ejecutar-el-proyecto-por-primera-vez).

---

## Como se construye (de cero)

El tutorial construye el proyecto paso a paso en cada capitulo:

| Cap | Que se construye |
|-----|------------------|
| C2 | Docker Compose, PostgreSQL, Redis |
| C3 | Proyecto Django, apps, settings, migraciones |
| C4 | Modelos de datos (DataSource, Event, DailyMetric, SavedReport) |
| C5 | API REST, serializers, views, Swagger |
| C6 | Frontend con Bootstrap 5 y Chart.js |
| C7 | Autenticacion JWT |

---

## Arquitectura del proyecto

### Tipo de arquitectura: **Monolito modular con contenedores**

InsightBoard es un **monolitico (single codebase)** organizado por **apps de Django** (`users`, `analytics`, `core`). No es microservicios: todo el backend corre como un solo proceso, lo que lo hace mas simple de desplegar y mantener. La separacion en apps modulares permite crecer sin reescribir todo.

```
Browser (Frontend)  --[JWT]-->  Django REST API  --[psycopg2]-->  PostgreSQL
                                      |
                                      +--[Celery]-->  Redis  -->  Background tasks
```

| Capa | Tecnologia | Funcion |
|------|-----------|---------|
| Frontend | Bootstrap 5 + Chart.js | Interfaz responsive con graficos |
| Backend | Django + DRF | API REST y logica del servidor |
| Base de datos | PostgreSQL | Vistas materializadas, JSON, consultas |
| Cache / Colas | Redis + Celery | Tareas en segundo plano |
| Contenedores | Docker Compose | Mismo entorno en cualquier maquina |

### Mejoras futuras

| Mejora | Beneficio |
|--------|-----------|
| Separar Celery worker en un servicio propio escalable | Escalar tareas pesadas de forma independiente |
| Migrar a microservicios (analytics, auth, reports) | Aislamiento y despliegue independiente |
| Cachear endpoints con Redis (DRF caching) | Respuestas mas rapidas en dashboards |
| Rate limiting en `/api/events/ingest/` | Proteger la API de abuso |
| Tests automatizados (pytest + CI) | Evitar regresiones |
| Paginacion y filtros avanzados en eventos | Manejar volumenes grandes |
| Desplegar con CDN (Cloudflare) | Entregar el frontend mas rapido |
| Logging centralizado y monitoreo (Sentry) | Detectar errores en produccion |
| Autenticacion social (Google/GitHub OAuth) | Login mas comodo |
| Modo oscuro y tema personalizable | Mejor experiencia de usuario |

---

## Credenciales de prueba

| Usuario | Contrasena | Descripcion |
|---------|-----------|-------------|
| `admin@insightboard.com` | `admin123` | Administrador del sistema |

---

## ¿Te trabaste?

- Revisa el capitulo de nuevo, especialmente los pasos numerados
- Asegurate de tener **Docker Desktop** corriendo (icono de ballena en la barra de tareas)
- Revisa la seccion de **Solucion de problemas** de cada capitulo
- Busca el mensaje de error en Google

---

**¡Empieza con el [Capitulo 0: Que es InsightBoard](./c0/README.md)!**
