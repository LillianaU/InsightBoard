# C3 - Crear el proyecto Django

> **Edad recomendada:** 10-11 años  
> **Tiempo estimado:** 35 minutos  
> **Dificultad:** ⭐ ⭐ ⭐ ⭐

---

## ¿Qué vamos a hacer?

Ahora vamos a **crear el proyecto Django** desde cero. Usaremos comandos mágicos de Django para generar la estructura base, luego crearemos las 3 apps y configuraremos todo para que funcione con Docker.

---

## Paso 1: Verificar que Docker está corriendo

Antes de empezar, asegúrate de que las cajitas estén encendidas:

```bash
docker-compose ps
```

Debes ver los 4 servicios en estado `Up`. Si no, enciéndelos:

```bash
docker-compose up -d
```

---

## Paso 2: Crear el proyecto Django

Django tiene un comando mágico que crea toda la estructura base del proyecto.

En la terminal, ejecuta:

```bash
uv run django-admin startproject config .
```

**¿Qué hace este comando?**
- `startproject config` = "Crea un proyecto llamado `config`"
- El `.` al final = "En la carpeta actual"

Esto crea estas carpetas y archivos automáticamente:

```
InsightBoard/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

---

## Paso 3: Ver el `manage.py`

`manage.py` es como el **control remoto** de tu proyecto. Con él puedes hacer todo.

Intenta pedirle ayuda:

```bash
uv run python manage.py help
```

Verás una lista gigante de comandos. Los que más usaremos son:
- `migrate` - Crear tablas en la base de datos
- `createsuperuser` - Crear el administrador
- `runserver` - Encender el servidor web

---

## Paso 4: Crear las 3 apps

Una **app** en Django es como una **carpeta de herramientas especializadas**.

Vamos a crear 3 apps:

### App 1: `users` (usuarios)

```bash
uv run python manage.py startapp users apps/users
```

Esto crea la carpeta `apps/users/` con todos los archivos de la app.

### App 2: `analytics` (análisis)

```bash
uv run python manage.py startapp analytics apps/analytics
```

### App 3: `core` (utilidades)

```bash
uv run python manage.py startapp core apps/core
```

---

## Paso 5: Crear carpetas extra

Algunas apps necesitan carpetas adicionales. Crea estas carpetas vacías:

**Para `analytics`:**
```bash
mkdir apps\analytics\migrations
```

**Para `users`:**
```bash
mkdir apps\users\migrations
```

**Para `core`:**
```bash
mkdir core\migrations
```

También crea archivos `__init__.py` vacíos dentro de cada `migrations`:

```bash
type nul > apps\analytics\migrations\__init__.py
type nul > apps\users\migrations\__init__.py
type nul > core\migrations\__init__.py
```

---

## Paso 6: Configurar `settings/base.py`

Ahora vamos a configurar el proyecto. Abre el archivo `config/settings/base.py` en VS Code.

### 6.1. Configurar la base de datos

Busca la sección `DATABASES` y cámbiala a:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'insightboard',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

**Nota:** Usamos `db` como host porque es el nombre del servicio en Docker.

### 6.2. Agregar las apps

Busca `INSTALLED_APPS` y agrega al final:

```python
INSTALLED_APPS = [
    # ... las apps que ya vienen ...
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_cors_headers',
    'celery',
    'apps.users',
    'apps.analytics',
    'apps.core',
]
```

### 6.3. Configurar el usuario personalizado

Agrega esto al final del archivo:

```python
AUTH_USER_MODEL = 'users.User'
```

Esto le dice a Django: "No uses el usuario por defecto, usa el nuestro".

---

## Paso 7: Configurar `config/urls.py`

Abre `config/urls.py` y cámbialo a:

```python
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/events/', include('apps.analytics.urls')),
    path('api/reports/', include('apps.analytics.report_urls')),
    path('api/metrics/', include('apps.analytics.metric_urls')),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include('apps.core.urls')),
]
```

---

## Paso 8: Crear el modelo de usuario

Abre `apps/users/models.py` y escribe:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
```

Esto crea un usuario personalizado que usa email en vez de username.

---

## Paso 9: Configurar `apps/users/admin.py`

```python
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_staff']
    search_fields = ['email', 'username']
```

---

## Paso 10: Crear el modelo de DataSource

Abre `apps/analytics/models.py` y escribe:

```python
from django.db import models
from django.conf import settings


class DataSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

## Paso 11: Crear el modelo de Event

En el mismo archivo `apps/analytics/models.py`, agrega:

```python
class Event(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
```

---

## Paso 12: Crear el modelo de SavedReport

En el mismo archivo, agrega:

```python
class SavedReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_reports')
    name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

## Paso 13: Crear el modelo de DailyMetric

```python
class DailyMetric(models.Model):
    date = models.DateField()
    event_type = models.CharField(max_length=50)
    count = models.BigIntegerField()
    unique_users = models.BigIntegerField()

    class Meta:
        indexes = [models.Index(fields=['date', 'event_type'])]

    def __str__(self):
        return f"{self.date} - {self.event_type}: {self.count}"
```

---

## Paso 14: Configurar el admin de analytics

Abre `apps/analytics/admin.py` y escribe:

```python
from django.contrib import admin
from .models import Event, DataSource, SavedReport, DailyMetric


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'event_type', 'created_at']
    list_filter = ['event_type', 'source']


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']


@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ['date', 'event_type', 'count', 'unique_users']
```

---

## Paso 15: Configurar el core app

Crea `apps/core/views.py`:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})
```

Crea `apps/core/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
]
```

Crea `apps/core/apps.py`:

```python
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
```

Crea `apps/core/__init__.py` (vacío).

---

## Paso 16: Configurar Celery

Crea `config/celery_app.py`:

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('insightboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

---

## Paso 17: Archivos de settings

### `config/settings/__init__.py` (vacío)

```bash
type nul > config\settings\__init__.py
```

### `config/settings/base.py`

```python
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_cors_headers',
    'celery',
    'apps.users',
    'apps.analytics',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'insightboard'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'InsightBoard API',
    'DESCRIPTION': 'Plataforma de analítica con recolección de datos, reportes personalizados y visualizaciones D3.js',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOW_ALL_ORIGINS = True

CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
```

### `config/settings/development.py`

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/events/', include('apps.analytics.urls')),
    path('api/reports/', include('apps.analytics.report_urls')),
    path('api/metrics/', include('apps.analytics.metric_urls')),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include('apps.core.urls')),
]
```

### `config/wsgi.py`

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_wsgi_application()
```

### `config/asgi.py`

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_asgi_application()
```

### `manage.py`

```python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
```

---

## Paso 18: Crear el archivo `.env`

Crea `.env` en la carpeta principal:

```
DEBUG=True
DJANGO_SECRET_KEY=django-insecure-change-me-in-production
POSTGRES_DB=insightboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Paso 19: Crear migraciones

Django va a crear los "planos" de las tablas:

```bash
docker-compose exec web uv run python manage.py makemigrations
```

Verás algo como:
```
Migrations for 'analytics':
  apps\analytics\migrations\0001_initial.py
Migrations for 'users':
  apps\users\migrations\0001_initial.py
```

---

## Paso 20: Aplicar migraciones

Ahora construye las tablas en la base de datos:

```bash
docker-compose exec web uv run python manage.py migrate
```

Verás:
```
Applying users.0001_initial... OK
Applying analytics.0001_initial... OK
...
```

---

## Paso 21: Crear superusuario

```bash
docker-compose exec web uv run python manage.py createsuperuser
```

Ingresa:
- Usuario: `admin`
- Email: `admin@insightboard.com`
- Contraseña: `admin123`

---

## Paso 22: Verificar que funciona

Abre el navegador en:

| URL | Qué verás |
|-----|-----------|
| [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Panel de administración |
| [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) | Documentación Swagger |
| [http://127.0.0.1:8000/api/health/](http://127.0.0.1:8000/api/health/) | `{"status": "ok"}` |

---

## ¿Qué sigue?

Ahora que tienes el proyecto armado, en el siguiente capítulo vamos a explicar **qué son los modelos** y cómo funcionan las piezas que acabamos de crear.

> **Ejercicio para casa:** Entra al panel de admin y crea una "Fuente de Datos" llamada "Tienda Online". No te preocupes si no entiendes todo todavía, solo practica hacer clics.

---

## Resumen del capítulo C3

✅ Creamos el proyecto Django con `startproject`  
✅ Creamos 3 apps (`users`, `analytics`, `core`)  
✅ Configuramos settings, URLs, WSGI, ASGI  
✅ Creamos los modelos de usuario y eventos  
✅ Configuramos el panel de administración  
✅ Creamos las migraciones y aplicamos  
✅ Creamos el superusuario  
✅ Verificamos que el servidor funciona  

**¡Tu proyecto Django ya está vivo!** 🧠⚡
