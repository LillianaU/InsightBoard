from django.urls import path
from . import views

urlpatterns = [
    path('ingest/', views.EventIngestView.as_view(), name='event-ingest'),
    path('list/', views.EventListView.as_view(), name='event-list'),
    path('csv/', views.EventCSVIngestView.as_view(), name='event-csv-ingest'),
    path('sources/', views.DataSourceListCreateView.as_view(), name='datasource-list'),
]
