"""
Generador de informe PDF de InsightBoard
Ejecuta: uv run python generate_report.py
"""
import os
import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)


def build_report():
    filename = "InsightBoard_Informe.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], fontSize=24, spaceAfter=20
    )
    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading1"], fontSize=16, spaceAfter=10, spaceBefore=20
    )
    subheading_style = ParagraphStyle(
        "CustomSubHeading", parent=styles["Heading2"], fontSize=13, spaceAfter=8, spaceBefore=12
    )
    body_style = ParagraphStyle(
        "CustomBody", parent=styles["BodyText"], fontSize=10, leading=14, spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "CustomBullet", parent=body_style, leftIndent=20, bulletIndent=10
    )

    elements = []

    # Portada
    elements.append(Spacer(1, 4*cm))
    elements.append(Paragraph("InsightBoard", title_style))
    elements.append(Paragraph("Informe Completo del Proyecto", heading_style))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", body_style))
    elements.append(Paragraph("Version: 1.0.0", body_style))
    elements.append(Paragraph("Autor: LillianaU", body_style))
    elements.append(Spacer(1, 2*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        "Plataforma de analitica con recoleccion de datos, reportes personalizados "
        "y visualizaciones interactivas construida con Django REST Framework.",
        body_style
    ))
    elements.append(PageBreak())

    # Indice
    elements.append(Paragraph("Indice", heading_style))
    indice = [
        "1. Resumen ejecutivo",
        "2. Arquitectura del sistema",
        "3. Stack tecnologico",
        "4. Estructura del proyecto",
        "5. Capas de seguridad",
        "6. Endpoints de la API",
        "7. Modelos de base de datos",
        "8. Frontend",
        "9. Testing",
        "10. Despliegue",
        "11. Credenciales de prueba",
        "12. Tutoriales (C0-C9)",
    ]
    for item in indice:
        elements.append(Paragraph(item, bullet_style))
    elements.append(PageBreak())

    # 1. Resumen ejecutivo
    elements.append(Paragraph("1. Resumen ejecutivo", heading_style))
    elements.append(Paragraph(
        "InsightBoard es una plataforma de analitica web que permite recolectar eventos, "
        "generar metricas automaticas, crear reportes personalizados y visualizar datos "
        "interactivos con graficos Chart.js. El proyecto esta construido con Django 6.1 "
        "y Django REST Framework, desplegado en Render con PostgreSQL.",
        body_style
    ))

    # 2. Arquitectura
    elements.append(Paragraph("2. Arquitectura del sistema", heading_style))
    elements.append(Paragraph(
        "El sistema sigue una arquitectura cliente-servidor con API REST:",
        body_style
    ))
    arch_data = [
        ["Componente", "Tecnologia", "Funcion"],
        ["Frontend", "HTML + Bootstrap + Chart.js", "Interfaz de usuario"],
        ["Backend", "Django 6.1 + DRF", "API REST y logica"],
        ["Base de datos", "PostgreSQL 17", "Almacenamiento"],
        ["Cache/Tasks", "Redis + Celery", "Tareas en segundo plano"],
        ["Auth", "JWT (SimpleJWT)", "Autenticacion segura"],
        ["Deploy", "Render (Free Tier)", "Hosting en la nube"],
    ]
    arch_table = Table(arch_data, colWidths=[4*cm, 5*cm, 6*cm])
    arch_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(arch_table)
    elements.append(Spacer(1, 0.5*cm))

    # 3. Stack tecnologico
    elements.append(Paragraph("3. Stack tecnologico", heading_style))
    stack_data = [
        ["Capa", "Tecnologia", "Version"],
        ["Backend", "Django", "6.1.1"],
        ["API REST", "Django REST Framework", "3.18.0"],
        ["Documentacion", "drf-spectacular (Swagger)", "0.30.0"],
        ["Auth", "djangorestframework-simplejwt", "5.5.1"],
        ["CORS", "django-cors-headers", "4.9.0"],
        ["Base de datos", "psycopg2-binary", "2.9.12"],
        ["Cache", "redis", "8.1.0"],
        ["Tareas", "celery", "5.6.3"],
        ["Frontend", "Bootstrap 5 + Chart.js", "-"],
        ["Container", "Docker + Docker Compose", "-"],
        ["Servidor", "gunicorn", "26.2.0"],
        ["Testing", "pytest + pytest-django", "9.1.1"],
        ["Reportes PDF", "reportlab", "5.0.1"],
        ["Excel", "openpyxl", "3.1.5"],
    ]
    stack_table = Table(stack_data, colWidths=[4*cm, 6*cm, 3*cm])
    stack_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(stack_table)
    elements.append(Spacer(1, 0.5*cm))

    # 4. Estructura del proyecto
    elements.append(Paragraph("4. Estructura del proyecto", heading_style))
    estructura = """
<b>InsightBoard/</b><br/>
├── config/                  # Configuracion de Django<br/>
│   ├── settings/            # base.py, development.py, production.py<br/>
│   ├── urls.py              # Rutas de la API<br/>
│   ├── celery_app.py        # Tareas en segundo plano<br/>
│   └── wsgi.py / asgi.py    # Servidores web<br/>
├── apps/                    # Aplicaciones Django<br/>
│   ├── analytics/           # Modelos, views, serializers, services<br/>
│   ├── users/               # Autenticacion y usuarios<br/>
│   └── core/                # Utilidades generales<br/>
├── frontend/                # Paginas web<br/>
│   ├── login.html           # Pagina de login<br/>
│   ├── index.html           # Dashboard principal<br/>
│   ├── events.html          # Registro de eventos<br/>
│   ├── reports.html         # Reportes personalizados<br/>
│   ├── css/style.css        # Estilos<br/>
│   └── js/auth.js, app.js   # JavaScript<br/>
├── tutorials/               # Libro de tutoriales (C0-C9)<br/>
├── Dockerfile               # Imagen Docker<br/>
├── docker-compose.yml       # Servicios Docker<br/>
├── pyproject.toml           # Dependencias Python<br/>
├── conftest.py              # Configuracion pytest<br/>
└── manage.py                # Comando de gestion<br/>
"""
    elements.append(Paragraph(estructura, body_style))

    # 5. Capas de seguridad
    elements.append(PageBreak())
    elements.append(Paragraph("5. Capas de seguridad (8)", heading_style))
    security_data = [
        ["#", "Capa", "Descripcion"],
        ["1", "SECRET_KEY", "Nunca hardcodeada, obligatoria via variable de entorno"],
        ["2", "DEBUG", "Por defecto False en produccion"],
        ["3", "ALLOWED_HOSTS", "Solo dominios explicitos configurados"],
        ["4", "CORS", "Solo origenes permitidos (no permite todos)"],
        ["5", "Rate limiting", "30/hora anon, 1000/hora autenticado"],
        ["6", "JWT Seguro", "Tokens con rotacion y blacklist"],
        ["7", "XSS Protection", "Frontend usa textContent en vez de innerHTML"],
        ["8", "SQL Injection", "Django ORM previene inyeccion SQL"],
    ]
    sec_table = Table(security_data, colWidths=[1*cm, 3.5*cm, 10*cm])
    sec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e74c3c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fdf0f0")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(sec_table)

    # 6. Endpoints
    elements.append(Paragraph("6. Endpoints de la API", heading_style))
    endpoints_data = [
        ["Metodo", "Endpoint", "Auth"],
        ["POST", "/api/auth/register/", "No"],
        ["POST", "/api/auth/login/", "No"],
        ["GET", "/api/auth/me/", "JWT"],
        ["POST", "/api/events/ingest/", "No"],
        ["POST", "/api/events/csv/", "No"],
        ["GET", "/api/events/list/", "JWT"],
        ["GET/POST", "/api/events/sources/", "JWT"],
        ["GET", "/api/metrics/summary/", "JWT"],
        ["GET", "/api/metrics/timeseries/", "JWT"],
        ["GET", "/api/metrics/breakdown/", "JWT"],
        ["GET", "/api/metrics/heatmap/", "JWT"],
        ["POST", "/api/metrics/refresh/", "JWT"],
        ["GET/POST", "/api/reports/", "JWT"],
        ["GET/PUT/DELETE", "/api/reports/<id>/", "JWT"],
        ["GET", "/api/docs/", "No"],
        ["GET", "/api/health/", "No"],
    ]
    ep_table = Table(endpoints_data, colWidths=[3*cm, 7*cm, 2*cm])
    ep_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#27ae60")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdf4")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(ep_table)

    # 7. Modelos
    elements.append(PageBreak())
    elements.append(Paragraph("7. Modelos de base de datos", heading_style))

    models_info = [
        ("User (apps.users)", [
            "email (EmailField, unique, PK via USERNAME_FIELD)",
            "username (CharField)",
            "is_staff, is_superuser (BooleanField)",
        ]),
        ("DataSource (apps.analytics)", [
            "name (CharField)",
            "description (TextField)",
            "created_by (FK -> User, nullable)",
            "created_at (DateTimeField, auto)",
        ]),
        ("Event (apps.analytics)", [
            "source (FK -> DataSource)",
            "event_type (CharField)",
            "payload (JSONField)",
            "user (FK -> User, nullable)",
            "created_at (DateTimeField, auto)",
        ]),
        ("DailyMetric (apps.analytics)", [
            "date (DateField)",
            "event_type (CharField)",
            "count (BigIntegerField)",
            "unique_users (BigIntegerField)",
        ]),
        ("SavedReport (apps.analytics)", [
            "user (FK -> User)",
            "name (CharField)",
            "config (JSONField)",
            "created_at (DateTimeField, auto)",
        ]),
    ]

    for model_name, fields in models_info:
        elements.append(Paragraph(f"<b>{model_name}</b>", subheading_style))
        for field in fields:
            elements.append(Paragraph(f"  - {field}", bullet_style))
        elements.append(Spacer(1, 0.3*cm))

    # 8. Frontend
    elements.append(Paragraph("8. Frontend", heading_style))
    fe_data = [
        ["Pagina", "URL", "Funcion"],
        ["Login", "/login.html", "Iniciar sesion con JWT"],
        ["Dashboard", "/index.html", "Estadisticas y graficos interactivos"],
        ["Eventos", "/events.html", "Registrar y listar eventos"],
        ["Reportes", "/reports.html", "Crear reportes personalizados"],
        ["API Docs", "/api/docs/", "Documentacion Swagger"],
        ["Admin", "/admin/", "Panel de administracion Django"],
    ]
    fe_table = Table(fe_data, colWidths=[3*cm, 4*cm, 7*cm])
    fe_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#9b59b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f0fc")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(fe_table)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        "<b>Seguridad XSS:</b> Todo el frontend usa textContent en vez de innerHTML "
        "para evitar ataques de inyeccion de scripts. Las funciones escapeHtml() "
        "sanitizan cualquier dato dinamico.",
        body_style
    ))

    # 9. Testing
    elements.append(Paragraph("9. Testing", heading_style))
    elements.append(Paragraph(
        "El proyecto incluye pruebas automatizadas con pytest y pytest-django:",
        body_style
    ))
    test_data = [
        ["Archivo", "Que prueba", "Tests"],
        ["apps/users/tests.py", "Modelo User (crear, super, unico)", "4"],
        ["apps/analytics/tests.py", "DataSource, Event, DailyMetric, SavedReport", "10"],
        ["apps/analytics/api_tests.py", "Register, Login, Events, Metrics (API)", "9"],
        ["TOTAL", "", "23"],
    ]
    test_table = Table(test_data, colWidths=[5*cm, 7*cm, 2*cm])
    test_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f39c12")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef9e7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(test_table)
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("<b>Ejecutar pruebas:</b>", body_style))
    elements.append(Paragraph("  uv run pytest -v", bullet_style))

    # 10. Despliegue
    elements.append(Paragraph("10. Despliegue", heading_style))
    elements.append(Paragraph("<b>Produccion:</b> Render (Free Tier)", body_style))
    elements.append(Paragraph("  URL: https://insightboard-gf27.onrender.com/", bullet_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("<b>Local con Docker:</b>", body_style))
    deploy_steps = [
        "1. git clone https://github.com/LillianaU/InsightBoard.git",
        "2. cd InsightBoard",
        "3. cp .env.example .env",
        "4. docker-compose up -d",
        "5. docker-compose exec web uv run python manage.py migrate",
        "6. docker-compose exec web uv run python manage.py createsuperuser",
    ]
    for step in deploy_steps:
        elements.append(Paragraph(f"  {step}", bullet_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("<b>Local sin Docker:</b>", body_style))
    local_steps = [
        "1. uv venv && uv sync",
        "2. Crear PostgreSQL: CREATE DATABASE insightboard;",
        "3. cp .env.example .env (editar DATABASE_URL)",
        "4. uv run python manage.py migrate",
        "5. uv run python manage.py createsuperuser",
        "6. uv run python manage.py runserver",
    ]
    for step in local_steps:
        elements.append(Paragraph(f"  {step}", bullet_style))

    # 11. Credenciales
    elements.append(PageBreak())
    elements.append(Paragraph("11. Credenciales de prueba", heading_style))
    cred_data = [
        ["Usuario", "Contrasena", "Descripcion"],
        ["admin@insightboard.com", "admin123", "Administrador del sistema"],
    ]
    cred_table = Table(cred_data, colWidths=[5*cm, 4*cm, 5*cm])
    cred_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(cred_table)

    # 12. Tutoriales
    elements.append(Paragraph("12. Tutoriales (C0-C9)", heading_style))
    elements.append(Paragraph(
        "El proyecto incluye un libro completo de 10 capitulos que ensena a construir "
        "InsightBoard desde cero:",
        body_style
    ))
    tutoriales_data = [
        ["Cap", "Titulo", "Tiempo"],
        ["C0", "Que es InsightBoard", "10 min"],
        ["C1", "Preparar tu computadora", "20 min"],
        ["C2", "Docker y base de datos", "25 min"],
        ["C3", "Crear el proyecto Django", "35 min"],
        ["C4", "Modelos de base de datos", "30 min"],
        ["C5", "API REST con DRF", "40 min"],
        ["C6", "Frontend y dashboards", "35 min"],
        ["C7", "Autenticacion JWT", "25 min"],
        ["C8", "Probar el proyecto", "20 min"],
        ["C9", "Publicar en Render", "30 min"],
        ["", "TOTAL", "~5 horas"],
    ]
    tut_table = Table(tutoriales_data, colWidths=[2*cm, 7*cm, 3*cm])
    tut_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1abc9c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f8f5")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#1abc9c")),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
    ]))
    elements.append(tut_table)

    # Pie de pagina
    elements.append(Spacer(1, 2*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        f"Informe generado automaticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        body_style
    ))
    elements.append(Paragraph(
        "Repositorio: https://github.com/LillianaU/InsightBoard",
        body_style
    ))

    doc.build(elements)
    print(f"PDF generado: {os.path.abspath(filename)}")
    return filename


if __name__ == "__main__":
    build_report()
