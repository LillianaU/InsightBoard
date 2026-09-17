from django.http import JsonResponse
from django.db import connection


def health_check(request):
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({'status': 'error', 'database': 'error'}, status=503)
    return JsonResponse({'status': 'ok', 'database': 'ok'})
