from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve as static_serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.core.views import health_check
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/events/', include('apps.analytics.urls')),
    path('api/reports/', include('apps.analytics.report_urls')),
    path('api/metrics/', include('apps.analytics.metric_urls')),
    path('api/health/', health_check, name='api-health'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include('apps.core.urls')),
]

FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'frontend')

frontend_urlpatterns = [
    re_path(r'^(?P<path>login\.html)$', static_serve, {'document_root': FRONTEND_DIR}),
    re_path(r'^(?P<path>index\.html)$', static_serve, {'document_root': FRONTEND_DIR}),
    re_path(r'^(?P<path>events\.html)$', static_serve, {'document_root': FRONTEND_DIR}),
    re_path(r'^(?P<path>reports\.html)$', static_serve, {'document_root': FRONTEND_DIR}),
    re_path(r'^css/(?P<path>.*)$', static_serve, {'document_root': os.path.join(FRONTEND_DIR, 'css')}),
    re_path(r'^js/(?P<path>.*)$', static_serve, {'document_root': os.path.join(FRONTEND_DIR, 'js')}),
]

urlpatterns = frontend_urlpatterns + urlpatterns

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.STATIC_ROOT}),
    ]
