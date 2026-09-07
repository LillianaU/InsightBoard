# C0 - Que es InsightBoard

> **Tiempo estimado:** 10 minutos  
> **Dificultad:** Solo lectura

---

## ¿Que vamos a aprender?

En este capitulo vas a entender **que es InsightBoard** y **como esta organizado** antes de escribir una sola linea de codigo.

---

## ¿Que es InsightBoard?

InsightBoard es una **plataforma de analitica** que hace 4 cosas:

1. **Recibe datos** - Le puedes decir "un usuario compro una camisa" y lo guarda
2. **Crea reportes** - Puedes pedir "muestrame las ventas de septiembre" y te los genera
3. **Muestra graficos** - Convierte numeros en graficos de lineas, barras y pasteles
4. **Exporta resultados** - Puedes descargar los datos en CSV o PDF

### Ejemplo real

Imagina que tienes una tienda online:
- InsightBoard guarda cada venta que haces
- Te muestra un grafico de cuantas vendes por dia
- Te dice cuales son los productos mas vendidos
- Te deja exportar todo a Excel

---

## Arquitectura del proyecto

Asi se ve InsightBoard por dentro:

```
                    ┌─────────────────────────┐
                    │      TU NAVEGADOR        │
                    │   (Chrome, Firefox, etc)  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      FRONTEND            │
                    │  HTML + CSS + JavaScript │
                    │  (Bootstrap + Chart.js)  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    DJANGO REST API       │
                    │  (El cerebro del server) │
                    └────┬───────────────┬────┘
                         │               │
            ┌────────────▼──┐   ┌───────▼──────────┐
            │  POSTGRESQL   │   │      REDIS        │
            │ (Base datos)  │   │ (Cache rapida)    │
            └───────────────┘   └──────────────────┘
```

---

## Las tecnologias que usamos

| Tecnologia | Que es | Analogia |
|-----------|--------|----------|
| **Python** | Lenguaje de programacion | El idioma que hablamos con la computadora |
| **Django** | Framework web | El molde para hacer paginas web rapido |
| **DRF** | Django REST Framework | Herramientas para crear APIs (puertas de entrada) |
| **PostgreSQL** | Base de datos | Un archivador gigante que guarda informacion |
| **Redis** | Cache | Una libreta rapida para apuntar cosas temporalmente |
| **Docker** | Contenedores | Cajas organizadas donde vive cada programa |
| **Bootstrap** | CSS framework | Plantillas de disenio para que las paginas se vean bonitas |
| **Chart.js** | Libreria de graficos | Herramienta para dibujar graficos en el navegador |
| **JWT** | Autenticacion | Un pase de entrada que te dice "si puedes pasar" |

---

## Las 3 apps de Django

InsightBoard tiene 3 aplicaciones principales:

### 1. `users` - Manejo de usuarios
- Crear cuentas nuevas
- Iniciar sesion (login)
- Obtener info del usuario actual

### 2. `analytics` - Analitica y eventos
- Recibir eventos (datos)
- Crear fuentes de datos
- Generar metricas y graficos
- Guardar reportes

### 3. `core` - Utilidades
- Verificar que el servidor esta vivo (health check)
- Configuracion general del admin

---

## Los 4 modelos de base de datos

```
DataSource (Fuente de Datos)
    │
    ├─── Event (Eventos) ─── payload JSON
    │
User (Usuario)
    │
    ├─── SavedReport (Reportes Guardados)
    │
DailyMetric (Metricas Diarias)
```

| Modelo | Que guarda | Ejemplo |
|--------|-----------|---------|
| **DataSource** | De donde vienen los datos | "Tienda Online", "App Movil" |
| **Event** | Cada cosa que paso | "Usuario compro camisa por $25" |
| **DailyMetric** | Resumen del dia | "Hoy hubo 42 ventas de 15 usuarios" |
| **SavedReport** | Configuracion guardada | "Grafico de barras de ventas semanales" |

---

## Flujo de datos

Asi viaja un dato desde que lo envias hasta que lo ves en un grafico:

```
1. ENVÍAS un evento
   POST /api/events/ingest/
   {"source": "tienda", "event_type": "compra", "payload": {"producto": "camisa"}}

2. DJANGO lo guarda
   INSERT INTO analytics_event ... → PostgreSQL

3. PIDES un reporte
   GET /api/metrics/summary/

4. DJANGO consulta la base de datos
   SELECT COUNT(*) FROM analytics_event ...

5. DEVUELVE los datos en JSON
   {"total_events": 42, "active_sources": 2}

6. FRONTEND dibuja el grafico
   Chart.js convierte los numeros en barras/lineas/pie
```

---

## URLs importantes

| URL | Que veras |
|-----|-----------|
| `http://127.0.0.1:8000/admin/` | Panel de administracion |
| `http://127.0.0.1:8000/api/docs/` | Documentacion de la API (Swagger) |
| `http://127.0.0.1:8000/api/health/` | Verificacion de salud |
| `http://localhost:8080` | Frontend (dashboard) |

---

## Resumen

- InsightBoard es una plataforma de analitica con API REST
- Usa Django + PostgreSQL + Redis + Docker
- Tiene 3 apps: users, analytics, core
- Tiene 4 modelos: DataSource, Event, DailyMetric, SavedReport
- Los datos viajan: Frontend → API → PostgreSQL → API → Frontend

---

**¿Listo para empezar? Sigue con el [Capitulo 1: Instalar herramientas](../c1/README.md)**
