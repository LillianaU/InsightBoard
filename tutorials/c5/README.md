# C5 - API REST con DRF

> **Tiempo estimado:** 40 minutos  
> **Dificultad:** ⭐ ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a crear los **endpoints** (puertas de entrada) de la API para que el frontend pueda enviar y recibir datos.

### Al final de este capitulo tendras:
- Serializers para convertir modelos a JSON
- Views para recibir peticiones HTTP
- URLs para acceder a cada endpoint
- Documentacion Swagger automatica
- Una API funcional para probar

---

## ¿Que es una API REST?

Una **API** es como un **restaurante**:

```
TU (Frontend)                    API (Mesa)                    COCINA (Base de datos)
    │                               │                               │
    │  1. Pides: "Quiero pizza"     │                               │
    │  (GET /api/events/)           │                               │
    │──────────────────────────────>│                               │
    │                               │  2. Le pide a la cocina       │
    │                               │  SELECT * FROM events         │
    │                               │──────────────────────────────>│
    │                               │                               │
    │                               │  3. Cocina devuelve los datos │
    │                               │<──────────────────────────────│
    │  4. Te sirve: JSON con datos  │                               │
    │<──────────────────────────────│                               │
```

### Metodos HTTP

| Metodo | Que hace | Ejemplo |
|--------|---------|---------|
| `GET` | Obtener datos | "Dame todos los eventos" |
| `POST` | Crear datos | "Guarda este evento nuevo" |
| `PUT` | Actualizar datos | "Cambia el nombre de este reporte" |
| `DELETE` | Borrar datos | "Elimina este reporte" |

---

## Paso 1: Crear los serializers

Los **serializers** convierten los modelos de Python a JSON (y vice versa).

Abre `apps/analytics/serializers.py` y escribe:

```python
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
```

### Que hace cada serializer

| Serializer | Modelo | Funcion |
|-----------|--------|---------|
| `DataSourceSerializer` | DataSource | Muestra/idata sources |
| `EventSerializer` | Event | Muestra eventos |
| `EventIngestSerializer` | (no modelo) | Recibe datos para crear eventos |
| `SavedReportSerializer` | SavedReport | Muestra reportes guardados |

---

## Paso 2: Crear las views de analytics

Las **views** son las que reciben las peticiones HTTP y devuelven respuestas.

Abre `apps/analytics/views.py` y escribe:

```python
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Event, DataSource, SavedReport, DailyMetric
from .serializers import EventSerializer, DataSourceSerializer, EventIngestSerializer, SavedReportSerializer
import csv
import io


class DataSourceListCreateView(generics.ListCreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]


class EventIngestView(generics.CreateAPIView):
    serializer_class = EventIngestSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

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
        days = self.request.query_params.get('days', '30')
        try:
            days = int(days)
        except ValueError:
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


class EventCSVIngestView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Archivo CSV requerido'}, status=status.HTTP_400_BAD_REQUEST)

        decoded = file_obj.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))
        created = 0
        source_name = request.data.get('source', 'csv_import')

        source, _ = DataSource.objects.get_or_create(
            name=source_name,
            defaults={'created_by': request.user if request.user.is_authenticated else None}
        )

        for row in reader:
            event_type = row.get('event_type', 'unknown')
            payload = {k: v for k, v in row.items() if k not in ('event_type',)}
            Event.objects.create(
                source=source,
                event_type=event_type,
                payload=payload,
                user=request.user if request.user.is_authenticated else None
            )
            created += 1

        return Response({'created': created}, status=status.HTTP_201_CREATED)
```

---

## Paso 3: Crear las URLs de analytics

Abre `apps/analytics/urls.py` y escribe:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('ingest/', views.EventIngestView.as_view(), name='event-ingest'),
    path('list/', views.EventListView.as_view(), name='event-list'),
    path('csv/', views.EventCSVIngestView.as_view(), name='event-csv-ingest'),
    path('sources/', views.DataSourceListCreateView.as_view(), name='datasource-list'),
]
```

---

## Paso 4: Crear las metric URLs

Crea `apps/analytics/metric_urls.py`:

```python
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
```

---

## Paso 5: Crear las report URLs

Crea `apps/analytics/report_urls.py`:

```python
from django.urls import path, include
from . import views

report_urlpatterns = [
    path('', views.SavedReportListCreateView.as_view(), name='savedreport-list'),
    path('<int:pk>/', views.SavedReportDetailView.as_view(), name='savedreport-detail'),
]

urlpatterns = [
    path('reports/', include(report_urlpatterns)),
]
```

---

## Paso 6: Crear el services.py

Crea `apps/analytics/services.py` (la logica de negocio):

```python
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncHour, ExtractWeekDay
from django.utils import timezone
from datetime import timedelta
from typing import Dict, Any, List, Optional
from .models import Event, DailyMetric


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
```

---

## Paso 7: Crear las URLs de usuarios

Abre `apps/users/urls.py` y escribe:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('me/', views.me_view, name='me'),
]
```

---

## Paso 8: Crear las views de usuarios

Abre `apps/users/views.py` y escribe:

```python
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)
```

---

## Paso 9: Crear los serializers de usuarios

Abre `apps/users/serializers.py` y escribe:

```python
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales invalidas')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
```

---

## Paso 10: Reiniciar el servidor

Para que los cambios tomen efecto:

```bash
docker-compose restart web
```

Espera unos segundos y verifica:

```bash
docker-compose ps
```

El servicio `web` debe estar en `Up`.

---

## Paso 11: Probar la API con Swagger

1. Abre http://127.0.0.1:8000/api/docs/
2. Veras la documentacion interactiva de todos los endpoints
3. Haz clic en un endpoint
4. Haz clic en **"Try it out"**
5. Entra con tu usuario si te lo pide

---

## Paso 12: Probar la API con curl

### Obtener token de login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"admin@insightboard.com\", \"password\": \"admin123\"}"
```

Copia el valor de `"access"` del resultado.

### Crear un evento

Reemplaza `TU_TOKEN` con el token que copiaste:

```bash
curl -X POST http://127.0.0.1:8000/api/events/ingest/ -H "Content-Type: application/json" -H "Authorization: Bearer TU_TOKEN" -d "{\"source\": \"tienda\", \"event_type\": \"compra\", \"payload\": {\"producto\": \"camisa\", \"precio\": 25}}"
```

**Resultado esperado:** Devuelve el evento creado con un `id`.

### Ver el resumen de metricas

```bash
curl -H "Authorization: Bearer TU_TOKEN" http://127.0.0.1:8000/api/metrics/summary/
```

**Resultado esperado:** JSON con `total_events`, `active_sources`, etc.

---

## Tabla de endpoints

| Metodo | Endpoint | Autenticacion | Descripcion |
|--------|----------|--------------|-------------|
| POST | `/api/auth/register/` | No | Crear cuenta nueva |
| POST | `/api/auth/login/` | No | Obtener token JWT |
| GET | `/api/auth/me/` | JWT | Ver usuario actual |
| POST | `/api/events/ingest/` | No | Crear un evento |
| POST | `/api/events/csv/` | No | Importar CSV |
| GET | `/api/events/list/` | JWT | Listar eventos |
| GET/POST | `/api/events/sources/` | JWT | Listar/crear fuentes |
| GET | `/api/metrics/summary/` | JWT | Resumen general |
| GET | `/api/metrics/timeseries/` | JWT | Datos para graficos de linea |
| GET | `/api/metrics/breakdown/` | JWT | Datos agrupados |
| GET | `/api/metrics/heatmap/` | JWT | Datos para heatmap |
| POST | `/api/metrics/refresh/` | JWT | Refrescar metricas |
| GET/POST | `/api/reports/` | JWT | Listar/crear reportes |
| GET/PUT/DELETE | `/api/reports/<id>/` | JWT | Editar/eliminar reporte |
| GET | `/api/docs/` | No | Documentacion Swagger |

---

## Solucion de problemas

### "No route found for path"
- Verifica que `config/urls.py` tiene todas las rutas correctas
- Reinicia el servidor: `docker-compose restart web`

### "ModuleNotFoundError"
- Verifica que creaste todos los archivos en los pasos anteriores
- Verifica que los archivos `__init__.py` existen

### "401 Unauthorized"
- Necesitas un token JWT para acceder a endpoints protegidos
- Primero haz login en `/api/auth/login/`

---

## Resumen del paso

| Paso | Que hicimos | Verificacion |
|------|------------|-------------|
| 1 | Serializers | Archivos creados |
| 2 | Views de analytics | Archivo views.py escrito |
| 3 | URLs de analytics | Archivo urls.py escrito |
| 4 | Metric URLs | Archivo metric_urls.py creado |
| 5 | Report URLs | Archivo report_urls.py creado |
| 6 | Services | Logica de negocio creada |
| 7-9 | Users (URLs, views, serializers) | Usuarios funcionando |
| 10 | Reiniciar servidor | `web` en `Up` |
| 11 | Probar Swagger | http://127.0.0.1:8000/api/docs/ |
| 12 | Probar con curl | Respuestas correctas |

---

**¿La API funciona? Sigue con el [Capitulo 6: Frontend y dashboards](../c6/README.md)**
