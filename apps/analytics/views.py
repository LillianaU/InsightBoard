from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.throttling import AnonRateThrottle
from .models import Event, DataSource, SavedReport, DailyMetric
from .serializers import EventSerializer, DataSourceSerializer, EventIngestSerializer, SavedReportSerializer
import csv
import io


MAX_CSV_SIZE = 5 * 1024 * 1024  # 5MB


class DataSourceListCreateView(generics.ListCreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]


class EventIngestThrottle(AnonRateThrottle):
    rate = '30/hour'


class EventIngestView(generics.CreateAPIView):
    serializer_class = EventIngestSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [EventIngestThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        source, _ = DataSource.objects.get_or_create(
            name=data['source'],
            defaults={'created_by': request.user if request.user.is_authenticated else None}
        )

        event = Event.objects.create(
            source=source,
            event_type=data['event_type'],
            payload=data['payload'],
            user_id=data.get('user_id')
        )

        return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Event.objects.select_related('source', 'user')
        event_type = self.request.query_params.get('event_type')
        source_id = self.request.query_params.get('source')
        try:
            days = int(self.request.query_params.get('days', '30'))
        except (ValueError, TypeError):
            days = 30
        since = timezone.now() - timedelta(days=days)
        qs = qs.filter(created_at__gte=since)
        if event_type:
            qs = qs.filter(event_type=event_type)
        if source_id:
            qs = qs.filter(source_id=source_id)
        return qs


class SavedReportListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedReport.objects.filter(user=self.request.user)


class CSVIngestThrottle(AnonRateThrottle):
    rate = '10/hour'


class EventCSVIngestView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    throttle_classes = [CSVIngestThrottle]

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Archivo CSV requerido'}, status=status.HTTP_400_BAD_REQUEST)

        if file_obj.size > MAX_CSV_SIZE:
            return Response({'detail': 'Archivo muy grande (maximo 5MB)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded = file_obj.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({'detail': 'Archivo no es UTF-8 valido'}, status=status.HTTP_400_BAD_REQUEST)

        reader = csv.DictReader(io.StringIO(decoded))
        source_name = request.data.get('source', 'csv_import')

        source, _ = DataSource.objects.get_or_create(
            name=source_name,
            defaults={'created_by': request.user if request.user.is_authenticated else None}
        )

        events = []
        for row in reader:
            event_type = row.get('event_type', 'unknown')
            payload = {k: v for k, v in row.items() if k != 'event_type'}
            events.append(Event(
                source=source,
                event_type=event_type,
                payload=payload,
                user=request.user if request.user.is_authenticated else None
            ))

        Event.objects.bulk_create(events, batch_size=500)

        return Response({'created': len(events)}, status=status.HTTP_201_CREATED)
