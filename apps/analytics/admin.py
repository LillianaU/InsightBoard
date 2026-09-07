from django.contrib import admin
from .models import Event, DataSource, SavedReport, DailyMetric


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'event_type', 'created_at', 'user']
    list_filter = ['event_type', 'source', 'created_at']
    search_fields = ['event_type']
    date_hierarchy = 'created_at'


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    search_fields = ['name']


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user']


@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ['date', 'event_type', 'count', 'unique_users']
    list_filter = ['event_type', 'date']
