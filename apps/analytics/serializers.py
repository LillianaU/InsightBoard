from rest_framework import serializers
from .models import Event, DataSource, SavedReport


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'source', 'event_type', 'payload', 'created_at', 'user']
        read_only_fields = ['id', 'created_at']


class EventIngestSerializer(serializers.Serializer):
    source = serializers.CharField()
    event_type = serializers.CharField()
    payload = serializers.DictField()
    user_id = serializers.IntegerField(required=False, allow_null=True)


class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = ['id', 'name', 'config', 'created_at']
        read_only_fields = ['id', 'created_at']
