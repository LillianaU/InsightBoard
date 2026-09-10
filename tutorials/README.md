# InsightBoard - Guia Completa de Construccion

> **Libro para aprender a construir una plataforma de analitica desde cero**
> **Nivel:** Principiante a Intermedio
> **Duracion total:** ~6 horas

---

## Tabla de contenido

| Cap | Titulo | Que aprenderas | Tiempo |
|-----|--------|---------------|--------|
| [C0](./c0/README.md) | **Que es InsightBoard** | Vista general del proyecto y arquitectura | 10 min |
| [C1](./c1/README.md) | **Preparar tu computadora** | Instalar Python, VS Code, Git, uv | 20 min |
| [C2](./c2/README.md) | **Docker y base de datos** | Docker Desktop, PostgreSQL, Redis | 25 min |
| [C3](./c3/README.md) | **Crear el proyecto Django** | startproject, apps, settings, migraciones | 35 min |
| [C4](./c4/README.md) | **Modelos de base de datos** | DataSource, Event, DailyMetric, SavedReport | 30 min |
| [C5](./c5/README.md) | **API REST con DRF** | Serializers, views, endpoints, Swagger | 40 min |
| [C6](./c6/README.md) | **Frontend y dashboards** | HTML, Chart.js, Bootstrap, consumo de API | 35 min |
| [C7](./c7/README.md) | **Autenticacion JWT** | Login, registro, tokens, proteccion de rutas | 25 min |
| [C8](./c8/README.md) | **Probar el proyecto** | Pruebas locales, troubleshooting | 20 min |
| [C9](./c9/README.md) | **Publicar en Render** | Deploy, variables de entorno, superusuario | 30 min |
| [C10](./c10/README.md) | **Arquitectura y Variables de Entorno** | Entender la estructura, .env, configuracion | 20 min |

---

## Como usar este libro

1. Lee cada capitulo **en orden** (del C0 al C9)
2. Haz **cada paso exactamente como se indica**
3. **Verifica** que funciono antes de pasar al siguiente paso
4. Si algo falla, revisa la seccion "Solucion de problemas" del capitulo

---

## Que construiremos

InsightBoard es una plataforma de analitica que:
- **Recibe datos** mediante una API REST
- **Guarda eventos** en PostgreSQL
- **Crea graficos** interactivos con Chart.js
- **Permite reportes** personalizados
- **Se despliega** en la nube con Render

---

## Arquitectura del proyecto

```
Browser (Frontend)  --[JWT]-->  Django REST API  --[psycopg2]-->  PostgreSQL
                                      |
                                      +--[Celery]-->  Redis  -->  Background tasks
```

---

## Estructura final del proyecto

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
│   └── js/                  # JavaScript (auth.js, app.js)
├── tutorials/               # Este libro
├── docker-compose.yml       # Configuracion Docker
├── Dockerfile               # Imagen Docker
├── pyproject.toml           # Dependencias Python
└── manage.py                # Comando de gestion
```

---

## Requisitos previos

- Una computadora con **Windows** (tambien funciona en Mac/Linux)
- Conexion a **Internet**
- Ganas de aprender

---

## Credenciales de prueba

| Usuario | Contrasena | Descripcion |
|---------|-----------|-------------|
| `admin@insightboard.com` | `admin123` | Administrador del sistema |

---

**Empieza con el [Capitulo 0: Que es InsightBoard](./c0/README.md)**

powershel
uv venv

uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver


docker-compose down -v
docker volume rm insightboard_venv_data 2>$null
docker-compose up -d --build
docker-compose exec web uv run python manage.py migrate
docker-compose exec web uv run python manage.py createsuperuser