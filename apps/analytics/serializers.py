import json

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
    source = serializers.CharField(max_length=100)
    event_type = serializers.CharField(max_length=50)
    payload = serializers.DictField()

    def validate_payload(self, value):
        if len(json.dumps(value)) > 10000:
            raise serializers.ValidationError('Payload demasiado grande (maximo 10KB)')
        return value


class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = ['id', 'name', 'config', 'created_at']
        read_only_fields = ['id', 'created_at']
