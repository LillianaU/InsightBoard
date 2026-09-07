from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
