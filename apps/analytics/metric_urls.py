from django.urls import path
from . import views
from .services import get_summary, get_timeseries, get_breakdown, get_heatmap_data, build_materialized_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_summary(request):
    days = int(request.query_params.get('days', 30))
    return Response(get_summary(days=days))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_timeseries(request):
    event_type = request.query_params.get('event_type')
    days = int(request.query_params.get('days', 30))
    return Response(get_timeseries(event_type=event_type, days=days))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_breakdown(request):
    dimension = request.query_params.get('dimension', 'event_type')
    days = int(request.query_params.get('days', 30))
    return Response(get_breakdown(dimension=dimension, days=days))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metrics_heatmap(request):
    days = int(request.query_params.get('days', 30))
    return Response(get_heatmap_data(days=days))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_materialized(request):
    rows = build_materialized_view()
    return Response({'refreshed': rows})


metric_urlpatterns = [
    path('summary/', metrics_summary, name='metrics-summary'),
    path('timeseries/', metrics_timeseries, name='metrics-timeseries'),
    path('breakdown/', metrics_breakdown, name='metrics-breakdown'),
    path('heatmap/', metrics_heatmap, name='metrics-heatmap'),
    path('refresh/', refresh_materialized, name='metrics-refresh'),
]

urlpatterns = metric_urlpatterns
