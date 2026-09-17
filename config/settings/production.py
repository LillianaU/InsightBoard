import os
from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = False

# ============================================================================
# ALLOWED HOSTS - Dominios explicitos + dominio automatico de Render
# ============================================================================
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]

_render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME', '').strip()
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

# ============================================================================
# SECRET KEY - Obligatoria en produccion (falla rapido si falta)
# ============================================================================
if not SECRET_KEY or SECRET_KEY.startswith('django-insecure-'):
    raise ImproperlyConfigured(
        'DJANGO_SECRET_KEY no esta definida. Configurala en el dashboard de Render '
        'antes de desplegar en produccion.'
    )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================================
# SEGURIDAD HTTPS (Render termina TLS en el proxy)
# ============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ============================================================================
# CACHE - Redis para throttling compartido entre workers (si esta disponible)
# ============================================================================
_redis_url = os.getenv('REDIS_URL')
if _redis_url:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': _redis_url,
        }
    }
