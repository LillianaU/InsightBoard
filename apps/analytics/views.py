from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.throttling import AnonRateThrottle
from .models import Event, DataSource, SavedReport, DailyMetric
from .serializers import EventSerializer, DataSourceSerializer, EventIngestSerializer, SavedReportSerializer
import csv
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


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
    parser_classes = [JSONParser, MultiPartParser, FormParser]
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
            user=request.user if request.user.is_authenticated else None
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request):
    days = int(request.query_params.get('days', 30))
    dimension = request.query_params.get('dimension', 'event_type')
    from .services import get_breakdown, get_summary

    user = request.user
    data = get_breakdown(dimension=dimension, days=days)
    summary = get_summary(days=days)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ReportTitle', parent=styles['Title'], fontSize=20, spaceAfter=10)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, spaceAfter=10, textColor=colors.HexColor('#666666'))
    heading_style = ParagraphStyle('ReportHeading', parent=styles['Heading2'], fontSize=14, spaceAfter=10)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, spaceAfter=6)

    elements = []
    elements.append(Paragraph('Reporte InsightBoard', title_style))
    elements.append(Paragraph(f'Generado por: {user.email} | Fecha: {timezone.now().strftime("%d/%m/%Y %H:%M")}', subtitle_style))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('Resumen Ejecutivo', heading_style))
    elements.append(Paragraph(f'Total de Eventos: <b>{summary["total_events"]}</b>', body_style))
    elements.append(Paragraph(f'Fuentes Activas: <b>{summary["active_sources"]}</b>', body_style))
    elements.append(Paragraph(f'Usuarios Activos: <b>{summary["active_users"]}</b>', body_style))
    elements.append(Paragraph(f'Eventos Top: <b>{len(summary["top_events"])}</b>', body_style))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph('Analisis por Dimension', heading_style))
    elements.append(Paragraph(f'Dimension: {dimension} | Dias: {days}', body_style))
    elements.append(Spacer(1, 0.3*cm))

    table_data = [[dimension.capitalize(), 'Cantidad']]
    for item in data:
        key = item.get(dimension, item.get('event_type', ''))
        table_data.append([str(key), str(item['count'])])
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f'Total de registros en esta dimension: {len(data)}', body_style))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte-{user.email}-{days}d.pdf"'
    return response
