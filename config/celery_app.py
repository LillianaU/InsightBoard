import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings.production' if os.getenv('RENDER') else 'config.settings.development'
)

app = Celery('insightboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
