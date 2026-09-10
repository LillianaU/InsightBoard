# C10 - Arquitectura y Variables de Entorno

> **Tiempo estimado:** 20 minutos
> **Dificultad:** ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a entender **como esta organizado InsightBoard por dentro**, que son las **variables de entorno** y como configurarlas para que funcione en cualquier lugar (tu computadora, Render, Docker).

---

## ¿Que es la arquitectura de un proyecto?

La arquitectura es como se construye un edificio: tiene cimientos, paredes, tuberias y electricidad. InsightBoard tiene una arquitectura clara:

```
                    ┌─────────────────────────┐
                    │      TU NAVEGADOR        │
                    │   (Chrome, Firefox, etc)  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      FRONTEND            │
                    │  HTML + CSS + JavaScript │
                    │  (Bootstrap + Chart.js)  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    DJANGO REST API       │
                    │  (El cerebro del server) │
                    └────┬───────────────┬────┘
                         │               │
             ┌────────────▼──┐   ┌───────▼──────────┐
             │  POSTGRESQL   │   │      REDIS        │
             │ (Base datos)  │   │ (Cache/Colas)     │
             └───────────────┘   └───────────────────┘
```

### ¿Que hace cada parte?

| Componente | Que hace | Analogia |
|------------|----------|----------|
| **Navegador** | Muestra la pagina | El salón de ventas |
| **Frontend** | Páginas HTML con graficos | El escaparate de la tienda |
| **Django REST API** | Procesa peticiones y responde | El cajero del banco |
| **PostgreSQL** | Guarda todos los datos | El archivo enorme |
| **Redis** | Cache rapido y tareas en cola | La libreta del cajero |

---

## Estructura del proyecto

```
InsightBoard/
├── config/                  # Configuracion de Django
│   ├── settings/            # Ajustes del proyecto
│   │   ├── __init__.py
│   │   ├── base.py          # Configuracion BASE (todos los entornos)
│   │   ├── development.py   # Configuracion para tu PC local
│   │   └── production.py    # Configuracion para Render (internet)
│   ├── urls.py              # Rutas de la API
│   ├── celery_app.py        # Tareas en segundo plano
│   ├── wsgi.py              # Servidor web (produccion)
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
├── docker-compose.yml       # Configuracion Docker (local)
├── Dockerfile               # Imagen Docker (produccion)
├── pyproject.toml           # Dependencias Python
├── manage.py                # Comando de gestion de Django
└── .env                     # Variables de entorno LOCAL (NO subir a GitHub)
```

---

## ¿Que son las variables de entorno?

Una **variable de entorno** es un valor que tu aplicacion lee del sistema operativo en vez de tenerlo escrito en el codigo.

### ¿Por que es importante?

Imagina que tu contraseña del banco esta escrita en un papel pegado en la puerta. Si alguien entra a tu casa, la tiene. Pero si esta en tu billetera, solo tu la tienes.

Las variables de entorno son como tu billetera: **no estan en el codigo, estan en el entorno donde corre la aplicacion**.

### Ejemplo en `base.py`

```python
# MAL: La clave esta escrita en el codigo
SECRET_KEY = "mi-clave-secreta"

# BIEN: La clave viene del entorno
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')
```

La segunda forma:
- Busca la variable `DJANGO_SECRET_KEY` en el entorno
- Si no la encuentra, usa `'django-insecure-clave-temporal-desarrollo'` como respaldo para desarrollo
- En producción (Render), se pone la clave real en las variables de entorno de Render

---

## Las 3 capas de configuracion

InsightBoard tiene **3 archivos de configuracion** que se complementan:

```
base.py (configuracion base - se usa en todos lados)
     │
     ├── development.py (tu PC local)
     │     └── DEBUG=True, base de datos local
     │
     └── production.py (Render - internet)
           └── DEBUG=False, HSTS, SSL, WhiteNoise
```

### `base.py` - Configuracion Base

Tiene **8 capas de seguridad**:

| Capa | Que protege | Variable de entorno |
|------|-------------|---------------------|
| 1 | SECRET_KEY | `DJANGO_SECRET_KEY` |
| 2 | DEBUG | `DEBUG` |
| 3 | ALLOWED_HOSTS | `ALLOWED_HOSTS` |
| 4 | Apps instaladas | - |
| 5 | Middleware de seguridad | - |
| 6 | Base de datos | `DATABASE_URL`, `POSTGRES_*` |
| 7 | DRF (autenticacion) | `CORS_ALLOWED_ORIGINS` |
| 8 | JWT | - |

### `development.py` - Tu PC local

```python
from .base import *

DEBUG = True
# Usa SQLite o PostgreSQL local
# No necesita SSL
```

### `production.py` - Render (produccion)

```python
from .base import *

# Seguridad extra para internet
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## El archivo `.env`

El archivo `.env` guarda todas las variables de entorno para tu computadora local.

### Crear tu `.env`

En la carpeta raiz del proyecto, crea un archivo llamado `.env`:

```env
# === SECRETO ===
DJANGO_SECRET_KEY=clave-secreta-muy-larga-para-desarrollo

# === ENTORNO ===
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# === BASE DE DATOS ===
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/insightboard
POSTGRES_DB=insightboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# === REDIS ===
REDIS_URL=redis://localhost:6379/0

# === CORS ===
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### ⚠️ **Regla de oro**

**NUNCA** subas tu archivo `.env` a GitHub. Ya está en `.gitignore`.

Si quieres que otros sepan que variables necesita el proyecto, usa `.env.example`:

```env
# Archivo .env.example (SÍ se sube a GitHub)
DJANGO_SECRET_KEY=
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
REDIS_URL=
CORS_ALLOWED_ORIGINS=
```

---

## Configuracion en Render

Cuando haces deploy en Render, las variables de entorno se configuran en el dashboard:

```
Render Dashboard
  → Tu Web Service
    → Environment
      → Environment Variables
```

Agrega estas variables:

| Variable | Valido en Render | Descripcion |
|----------|-----------------|-------------|
| `DJANGO_SECRET_KEY` | Clave larga aleatoria | Seguridad de Django |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | Usa configuracion de produccion |
| `DEBUG` | `False` | Sin errores detallados |
| `ALLOWED_HOSTS` | `insightboard.onrender.com` | Dominio permitido |
| `DATABASE_URL` | `postgresql://...` | URL de tu PostgreSQL de Render |
| `REDIS_URL` | `redis://...` | URL de tu Redis de Render |
| `CORS_ALLOWED_ORIGINS` | `https://insightboard.onrender.com` | Origen del frontend |

---

## Como Django lee las variables de entorno

El flujo es asi:

```
1. Archivo .env (tu PC)
   │
   ▼
2. base.py lee con os.getenv()
   │
   ▼
3. development.py o production.py selecciona configuracion
   │
   ▼
4. Django arranca correctamente
```

En `base.py`, la clave SEQUENCE_KEY funciona asi:

```python
# Esta funcion busca DJANGO_SECRET_KEY en el entorno
# Si no la encuentra, usa el respaldo para desarrollo
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')
```

Esto significa:
- **En tu PC local**: Si `.env` tiene `DJANGO_SECRET_KEY`, lo usa. Si no, usa el respaldo.
- **En Render**: Usa el valor que pusiste en las variables de entorno de Render.
- **Nunca se crash**: Siempre tiene un valor, nunca está vacío.

---

## Variables de entorno importantes resumidas

### Para desarrollo local (`.env`)

```env
DJANGO_SECRET_KEY=clave-temporal
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/insightboard
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Para produccion (Render)

```env
DJANGO_SECRET_KEY=clave-secreta-muy-larga
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
ALLOWED_HOSTS=insightboard.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
CORS_ALLOWED_ORIGINS=https://insightboard.onrender.com
```

---

## Como cambiar entre entornos

Solo cambias `DJANGO_SETTINGS_MODULE`:

| Entorno | `DJANGO_SETTINGS_MODULE` | Archivo que usa |
|---------|--------------------------|-----------------|
| Tu PC local | `config.settings.development` | `development.py` |
| Docker local | `config.settings.development` | `development.py` |
| Render | `config.settings.production` | `production.py` |

El `Dockerfile` para Render tiene:
```dockerfile
ENV DJANGO_SETTINGS_MODULE=config.settings.production
```

---

## Solucion de problemas

### "La aplicacion crasha con ValueError de SECRET_KEY"

Ya esta fijo. `base.py` ahora tiene un respaldo (fallback):
```python
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-temporal-desarrollo')
```

Si no hay `DJANGO_SECRET_KEY` en el entorno, usa el respaldo temporal.

### "Render no conecta a la base de datos"

Verifica que `DATABASE_URL` este configurada en Render con la URL interna de tu PostgreSQL.

### "CORS bloqueado en el frontend"

Verifica que `CORS_ALLOWED_ORIGINS` incluya la URL de tu frontend (ej: `http://localhost:8080` para desarrollo).

### "El frontend carga pero los graficos no aparecen"

Verifica que el frontend puede llegar a `http://127.0.0.1:8000` (local) o a tu dominio de Render (produccion).

### "¿Como sé que estoy usando el settings correcto?"

Agrega este print temporal en `base.py`:
```python
print(f"USANDO SETTINGS: {os.getenv('DJANGO_SETTINGS_MODULE')}")
```

Los logs de Render/Docker te dirán qué archivo de configuración está usando.

---

## Resumen

- InsightBoard tiene una arquitectura de 4 capas: Navegador → API → Base de datos → Cache
- Las **variables de entorno** mantienen los secretos fuera del código
- Hay **3 archivos de configuración**: `base.py`, `development.py`, `production.py`
- El archivo `.env` guarda variables locales (nunca subir a GitHub)
- Render necesita las variables configuradas en su dashboard
- `DJANGO_SECRET_KEY` siempre tiene un respaldo para desarrollo

---

**¿Listo para el siguiente paso? Ya tienes todo listo para usar y desplegar InsightBoard correctamente.**
