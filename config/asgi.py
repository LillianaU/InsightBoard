import os
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings.production' if os.getenv('RENDER') else 'config.settings.development'
)

application = get_asgi_application()
