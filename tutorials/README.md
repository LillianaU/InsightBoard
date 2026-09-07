# Tutoriales InsightBoard

Guia paso a paso para construir **InsightBoard** desde cero.

> **Nivel:** Principiante  
> **Duracion total:** ~4 horas  
> **Requisito:** Una computadora con Windows y conexion a Internet

---

## Tabla de contenido

| Cap | Tema | Que aprenderas | Tiempo |
|-----|------|---------------|--------|
| [C0](./c0/README.md) | [Que es InsightBoard](./c0/README.md) | Vista general del proyecto, arquitectura y tecnologias | 10 min |
| [C1](./c1/README.md) | [Instalar herramientas](./c1/README.md) | Python, VS Code, Git, uv | 20 min |
| [C2](./c2/README.md) | [Docker y base de datos](./c2/README.md) | Docker Desktop, PostgreSQL, Redis | 25 min |
| [C3](./c3/README.md) | [Crear proyecto Django](./c3/README.md) | startproject, apps, settings, migraciones | 35 min |
| [C4](./c4/README.md) | [Modelos de base de datos](./c4/README.md) | DataSource, Event, DailyMetric, SavedReport | 30 min |
| [C5](./c5/README.md) | [API REST con DRF](./c5/README.md) | Serializers, views, endpoints, Swagger | 40 min |
| [C6](./c6/README.md) | [Frontend y dashboards](./c6/README.md) | HTML, Chart.js, Bootstrap, consumo de API | 35 min |
| [C7](./c7/README.md) | [Autenticacion JWT](./c7/README.md) | Login, registro, tokens, proteccion de rutas | 25 min |
| [C8](./c8/README.md) | [Probar y deploy](./c8/README.md) | Pruebas, troubleshooting, despliegue | 20 min |

---

## Como usar estos tutoriales

1. Lee cada capitulo **en orden** (del C0 al C8)
2. Haz **cada paso exactamente como se indica**
3. **Verifica** que funciono antes de pasar al siguiente paso (cada paso tiene una prueba)
4. Si algo falla, revisa la seccion "Solucion de problemas" del capitulo

---

## Arquitectura del proyecto

```
Browser (Frontend)  --[JWT]-->  Django REST API  --[psycopg2]-->  PostgreSQL
                                      |
                                      +--[Celery]-->  Redis  -->  Background tasks
```

| Capa | Tecnologia | Para que sirve |
|------|-----------|----------------|
| Backend | Django + DRF | Crear la API y logica del servidor |
| Base de datos | PostgreSQL | Guardar eventos, usuarios, reportes |
| Cache | Redis | Memoria rapida para tareas en segundo plano |
| Frontend | Bootstrap 5 + Chart.js | Paginas web con graficos interactivos |
| Auth | JWT (SimpleJWT) | Login seguro con tokens |
| Container | Docker | Empaquetar todo para que funcione igual en cualquier computadora |

---

## Requisitos previos

- Una computadora con **Windows**
- Conexion a **Internet**
- Ganas de aprender

---

## Estructura final del proyecto

```
InsightBoard/
├── config/                  # Configuracion de Django (el cerebro)
│   ├── settings/            # Ajustes del proyecto
│   ├── urls.py              # Rutas de la API
│   ├── celery_app.py        # Configuracion de tareas en segundo plano
│   ├── wsgi.py              # Servidor web
│   └── asgi.py              # Servidor web asincrono
├── apps/                    # Aplicaciones de Django
│   ├── users/               # Manejo de usuarios
│   ├── analytics/           # Logica de analitica y eventos
│   └── core/                # Utilidades generales
├── frontend/                # Paginas web (HTML/CSS/JS)
│   ├── index.html           # Dashboard principal
│   ├── events.html          # Registro de eventos
│   ├── reports.html         # Reportes personalizados
│   ├── login.html           # Pagina de login
│   ├── css/style.css        # Estilos
│   └── js/                  # JavaScript (auth.js, app.js)
├── tutorials/               # Estos tutoriales
├── docker-compose.yml       # Configuracion de Docker
├── requirements.txt         # Dependencias de Python
└── manage.py                # Comando de gestion de Django
```

---

## Credenciales de prueba

| Usuario | Contrasena | Descripcion |
|---------|-----------|-------------|
| `admin@insightboard.com` | `admin123` | Administrador del sistema |

---

## ¿Te trabaste?

- Revisa el capitulo de nuevo, especialmente los pasos numerados
- Asegurate de tener **Docker Desktop** corriendo (icono de ballena en la barra de tareas)
- Revisa la seccion de **Solucion de problemas** de cada capitulo
- Busca el mensaje de error en Google

---

**¡Empieza con el [Capitulo 0: Que es InsightBoard](./c0/README.md)!**
