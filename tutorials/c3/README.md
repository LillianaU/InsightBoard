# C3 - Crear proyecto Django

> **Tiempo estimado:** 35 minutos  
> **Dificultad:** ⭐ ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a crear el proyecto Django desde cero, configurar las apps, los settings, las URLs y levantar el servidor.

### Al final de este capitulo tendras:
- Un proyecto Django funcionando
- 3 apps configuradas (users, analytics, core)
- La base de datos conectada
- El panel de admin funcionando
- El servidor web corriendo

---

## Paso 1: Verificar que Docker esta corriendo

```bash
docker-compose ps
```

Debes ver los 4 servicios en `Up`. Si no:

```bash
docker-compose up -d
```

---

## Paso 2: Crear el proyecto Django

Ejecuta este comando en la terminal:

```bash
uv run django-admin startproject config .
```

**¿Que hace?**
- `startproject config` = Crea un proyecto llamado "config"
- El `.` = En la carpeta actual

**Estructura que se crea:**

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

### Verificar

```bash
dir config
```

Debes ver los archivos: `__init__.py`, `asgi.py`, `settings.py`, `urls.py`, `wsgi.py`

---

## Paso 3: Crear las 3 apps

Una **app** en Django es una pieza especializada. Vamos a crear 3:

### App 1: users (usuarios)

```bash
uv run python manage.py startapp users apps/users
```

### App 2: analytics (analitica)

```bash
uv run python manage.py startapp analytics apps/analytics
```

### App 3: core (utilidades)

```bash
uv run python manage.py startapp core apps/core
```

### Verificar

```bash
dir apps
```

Debes ver 3 carpetas: `analytics/`, `core/`, `users/`

---

## Paso 4: Crear carpetas de migraciones

```bash
mkdir apps\analytics\migrations
mkdir apps\users\migrations
mkdir apps\core\migrations
```

Crear archivos `__init__.py` vacios:

```bash
type nul > apps\analytics\migrations\__init__.py
type nul > apps\users\migrations\__init__.py
type nul > apps\core\migrations\__init__.py
```

### Verificar

```bash
dir apps\analytics\migrations
```

Debes ver `__init__.py`

---

## Paso 5: Crear la estructura de settings

Django genera un solo `settings.py`, pero nosotros queremos separar en base y desarrollo.

Primero crea la carpeta:

```bash
mkdir config\settings
```

Mueve el settings original:

```bash
move config\settings.py config\settings\base.py
```

Crea el archivo de desarrollo:

```bash
type nul > config\settings\__init__.py
```

---

## Paso 6: Configurar config/settings/base.py

Abre `config/settings/base.py` en VS Code y reemplaza TODO el contenido con:

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
    'DESCRIPTION': 'Plataforma de analitica con recoleccion de datos, reportes personalizados y visualizaciones interactivas',
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

---

## Paso 7: Configurar config/settings/development.py

Abre `config/settings/development.py` y escribe:

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Paso 8: Crear el archivo .env

Crea un archivo `.env` en la carpeta raiz del proyecto:

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

## Paso 9: Configurar manage.py

Abre `manage.py` y reemplaza el contenido con:

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

## Paso 10: Configurar config/wsgi.py

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_wsgi_application()
```

---

## Paso 11: Configurar config/asgi.py

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_asgi_application()
```

---

## Paso 12: Configurar Celery

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

## Paso 13: Configurar URLs

Abre `config/urls.py` y escribe:

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

## Paso 14: Crear el modelo de usuario

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

---

## Paso 15: Configurar admin de users

Abre `apps/users/admin.py` y escribe:

```python
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_staff']
    search_fields = ['email', 'username']
```

---

## Paso 16: Crear los modelos de analytics

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


class SavedReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_reports')
    name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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

## Paso 17: Configurar admin de analytics

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

## Paso 18: Configurar core app

Crea `apps/core/__init__.py` (vacio).

Crea `apps/core/apps.py`:

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
```

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

---

## Paso 19: Crear las migraciones

Django va a crear los "planos" de las tablas:

```bash
docker-compose exec web uv run python manage.py makemigrations
```

Debes ver:

```
Migrations for 'analytics':
  apps\analytics\migrations\0001_initial.py
Migrations for 'users':
  apps\users\migrations\0001_initial.py
```

---

## Paso 20: Aplicar las migraciones

Construye las tablas en la base de datos:

```bash
docker-compose exec web uv run python manage.py migrate
```

Debes ver `OK` en cada migracion:

```
Applying auth.0001_initial... OK
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
- Email: `admin@insightboard.com`
- Username: `admin`
- Contrasena: `admin123`

---

## Paso 22: Verificar que funciona

Abre el navegador en estas URLs:

| URL | Que debes ver |
|-----|--------------|
| http://127.0.0.1:8000/admin/ | Panel de administracion (login) |
| http://127.0.0.1:8000/api/docs/ | Documentacion Swagger de la API |
| http://127.0.0.1:8000/health/ | `{"status": "ok"}` |

### Prueba completa

1. Ve a http://127.0.0.1:8000/admin/
2. Ingresa con `admin@insightboard.com` y `admin123`
3. Si ves el panel de administracion con Users y Analytics, **¡funciono!**

---

## Solucion de problemas

### "No se pudo conectar a la base de datos"
- Verifica que Docker esta corriendo: `docker-compose ps`
- Verifica que el servicio `db` esta en `Up`

### "ModuleNotFoundError: No module named 'apps'"
- Asegurate de que `apps/` tiene `__init__.py` en cada subcarpeta
- Verifica que `INSTALLED_APPS` incluye `'apps.users'`, `'apps.analytics'`, `'apps.core'`

### "OperationalError: FATAL: password authentication failed"
- Verifica que las credenciales en `.env` coinciden con las de `docker-compose.yml`

---

## Resumen del paso

| Paso | Que hicimos | Verificacion |
|------|------------|-------------|
| 2 | Crear proyecto Django | `dir config` muestra archivos |
| 3 | Crear 3 apps | `dir apps` muestra 3 carpetas |
| 6-8 | Configurar settings | Archivos creados correctamente |
| 14-16 | Crear modelos | Archivos models.py escritos |
| 19 | Crear migraciones | Mensajes de "Migrations for..." |
| 20 | Aplicar migraciones | Mensajes de "OK" |
| 21 | Crear superusuario | Puedes ingresar al admin |
| 22 | Verificar | Admin, Swagger y health funcionan |

---

**¿Todo funciono? Sigue con el [Capitulo 4: Modelos de base de datos](../c4/README.md)**
