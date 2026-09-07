from django.db.models import Count, Sum, Avg, Min, Max, F, Q
from django.db.models.functions import TruncDate, TruncHour, ExtractWeekDay
from django.utils import timezone
from datetime import timedelta, date
from typing import Dict, Any, List, Optional
from .models import Event, DataSource, DailyMetric


def get_summary(days: int = 30) -> Dict[str, Any]:
    since = timezone.now() - timedelta(days=days)
    qs = Event.objects.filter(created_at__gte=since)
    total_events = qs.count()
    active_sources = qs.values('source').distinct().count()
    active_users = qs.filter(user__isnull=False).values('user').distinct().count()

    top_events = (
        qs.values('event_type')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    daily_counts = (
        qs.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    return {
        'total_events': total_events,
        'active_sources': active_sources,
        'active_users': active_users,
        'top_events': list(top_events),
        'daily_counts': list(daily_counts),
    }


def get_timeseries(event_type: Optional[str] = None, days: int = 30) -> List[Dict[str, Any]]:
    since = timezone.now() - timedelta(days=days)
    qs = Event.objects.filter(created_at__gte=since)
    if event_type:
        qs = qs.filter(event_type=event_type)

    return list(
        qs.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'), unique_users=Count('user', distinct=True))
        .order_by('day')
    )


def get_breakdown(dimension: str = 'event_type', days: int = 30) -> List[Dict[str, Any]]:
    since = timezone.now() - timedelta(days=days)
    qs = Event.objects.filter(created_at__gte=since)
    if dimension == 'event_type':
        return list(
            qs.values('event_type')
            .annotate(count=Count('id'))
            .order_by('-count')[:50]
        )
    elif dimension == 'source':
        return list(
            qs.values('source__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:50]
        )
    elif dimension == 'weekday':
        return list(
            qs.annotate(weekday=ExtractWeekDay('created_at'))
            .values('weekday')
            .annotate(count=Count('id'))
            .order_by('weekday')
        )
    return []


def get_heatmap_data(days: int = 30) -> List[Dict[str, Any]]:
    since = timezone.now() - timedelta(days=days)
    qs = Event.objects.filter(created_at__gte=since)

    return list(
        qs.annotate(hour=TruncHour('created_at'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )


def build_materialized_view():
    DailyMetric.objects.all().delete()
    qs = Event.objects.annotate(day=TruncDate('created_at')).values('day', 'event_type')
    qs = qs.annotate(count=Count('id'), unique_users=Count('user', distinct=True))

    rows = []
    for row in qs:
        rows.append(DailyMetric(
            date=row['day'],
            event_type=row['event_type'],
            count=row['count'],
            unique_users=row['unique_users'],
        ))
    DailyMetric.objects.bulk_create(rows, batch_size=1000)
    return len(rows)
