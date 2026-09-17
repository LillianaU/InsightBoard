import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings.production' if os.getenv('RENDER') else 'config.settings.development'
)

application = get_wsgi_application()
