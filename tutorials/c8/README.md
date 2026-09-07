# C8 - Probar y deploy

> **Tiempo estimado:** 20 minutos
> **Dificultad:** ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a hacer las **pruebas finales** de todo el proyecto y aprender a **desplegarlo** en internet.

---

## Paso 0: Ejecutar el proyecto por primera vez

Si tienes el codigo de InsightBoard (clonado o descargado) y quieres correrlo, sigue estos pasos **en orden**.

### 0.1 Arranca Docker Desktop

Abre **Docker Desktop** y espera a que el icono de la ballena en la barra de tareas indique que esta corriendo.

### 0.2 Levanta los servicios con Docker Compose

Desde la carpeta raiz del proyecto:

```bash
docker-compose up -d
```

Esto enciende los 4 servicios: `web`, `db`, `redis` y `worker`. Verifica que todos esten `Up`:

```bash
docker-compose ps
```

### 0.3 Aplica las migraciones de la base de datos

```bash
docker-compose exec web uv run python manage.py migrate
```

### 0.4 Crea un superusuario (solo la primera vez)

```bash
docker-compose exec web uv run python manage.py createsuperuser
```

Usa el email y la contrasena que quieras (o las credenciales de prueba: `admin@insightboard.com` / `admin123`).

### 0.5 Carga datos de ejemplo (opcional)

Para que el dashboard muestre estadisticas, registra algunos eventos (ver el **Paso 2** mas abajo).

### 0.6 Inicia el frontend (segunda terminal)

Abre una **nueva terminal** y ejecuta:

```bash
cd frontend
python -m http.server 8080
```

### 0.7 Abre el proyecto en el navegador

| Pagina | URL |
|--------|-----|
| Frontend (login) | http://localhost:8080/login.html |
| Frontend (dashboard) | http://localhost:8080 |
| API Docs (Swagger) | http://127.0.0.1:8000/api/docs/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## Paso 1: Prueba completa del backend

Asegurate de que Docker esta corriendo:

```bash
docker-compose ps
```

Todos los servicios deben estar en `Up`.

### 1.1 Health check

```bash
curl http://127.0.0.1:8000/health/
```

**Resultado esperado:** `{"status": "ok"}`

### 1.2 Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"admin@insightboard.com\", \"password\": \"admin123\"}"
```

**Resultado esperado:** JSON con `access` y `user`.

### 1.3 Crear evento

```bash
curl -X POST http://127.0.0.1:8000/api/events/ingest/ -H "Content-Type: application/json" -d "{\"source\": \"test\", \"event_type\": \"prueba\", \"payload\": {\"mensaje\": \"funciona\"}}"
```

**Resultado esperado:** JSON con el evento creado.

### 1.4 Ver metricas

Copia el token del login y ejecuta:

```bash
curl -H "Authorization: Bearer TU_TOKEN" http://127.0.0.1:8000/api/metrics/summary/
```

**Resultado esperado:** JSON con `total_events >= 1`.

---

## Paso 2: Prueba completa del frontend

### 2.1 Iniciar servidor frontend

Abre una **nueva terminal**:

```bash
cd frontend
python -m http.server 8080
```

### 2.2 Probar cada pagina

| Pagina | URL | Que verificar |
|--------|-----|--------------|
| Login | http://localhost:8080/login.html | Puedes ingresar |
| Dashboard | http://localhost:8080 | Ves estadisticas |
| Eventos | http://localhost:8080/events.html | Puedes crear eventos |
| Reportes | http://localhost:8080/reports.html | Puedes generar graficos |

### 2.3 Prueba de eventos

1. Ve a http://localhost:8080/events.html
2. Crea 3-4 eventos de prueba:

| Source | Event Type | Payload |
|--------|-----------|---------|
| tienda | compra | `{"producto": "camisa", "precio": 25}` |
| tienda | compra | `{"producto": "pantalon", "precio": 40}` |
| app | visita | `{"pagina": "inicio"}` |
| tienda | click | `{"boton": "comprar"}` |

3. Verifica que aparecen en la tabla

### 2.4 Prueba del dashboard

1. Ve a http://localhost:8080
2. Verifica que los numeros cambiaron
3. Verifica que los graficos muestran datos

---

## Paso 3: Prueba de Swagger

1. Ve a http://127.0.0.1:8000/api/docs/
2. Haz clic en **"Authorize"** (arriba a la derecha)
3. Pega tu token: `Bearer TU_TOKEN`
4. Haz clic en "Authorize"
5. Prueba varios endpoints haciendo clic en ellos y luego en "Try it out"

---

## Paso 4: Lista de verificacion final

Marca cada item con una X cuando lo verifiques:

```
[ ] Docker esta corriendo (4 servicios Up)
[ ] Health check responde {"status": "ok"}
[ ] Login funciona (obtienes token)
[ ] Crear evento funciona
[ ] Metricas muestran datos
[ ] Frontend carga en el navegador
[ ] Login en frontend funciona
[ ] Dashboard muestra graficos
[ ] Puedes crear eventos desde el frontend
[ ] Puedes generar reportes
[ ] Swagger muestra todos los endpoints
[ ] Puedes cerrar sesion
```

---

## Paso 5: Desplegar en la nube

> **Requisito previo:** el codigo debe estar en un repositorio de GitHub.
> ```bash
> git init
> git add .
> git commit -m "Deploy InsightBoard"
> git branch -M main
> git remote add origin https://github.com/TU_USUARIO/InsightBoard.git
> git push -u origin main
> ```

> **Nota sobre el puerto:** el proyecto ya esta preparado para produccion. El `Dockerfile`
> arranca con `gunicorn` en el puerto `$PORT` (que inyecta el proveedor) y corre las migraciones solo:
> ```dockerfile
> CMD uv run python manage.py migrate && uv run gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000}
> ```
> Y los settings aceptan `DATABASE_URL` ademas de las variables `POSTGRES_*`.

### Opcion 1: Railway (recomendada para principiantes)

1. Ve a **https://railway.app** e inicia sesion con GitHub.
2. **New Project** > **Deploy from GitHub repo** > selecciona `InsightBoard`.
3. Railway detecta el `Dockerfile` automaticamente y empieza a construir.
4. Agrega los servicios de datos:
   - **New** > **Database** > **PostgreSQL**
   - **New** > **Database** > **Redis** (para Celery)
5. En el servicio web, pestana **Variables**, agrega:
   ```
   DJANGO_SECRET_KEY=clave-secreta-larga
   DEBUG=False
   ALLOWED_HOSTS=tu-app.up.railway.app
   ```
   Y las credenciales de la base de datos (abre el plugin PostgreSQL > Variables y copia al servicio web):
   ```
   POSTGRES_DB=...
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   POSTGRES_HOST=...
   POSTGRES_PORT=5432
   REDIS_URL=redis://<host-redis>:6379/0
   ```
6. Railway ejecuta `migrate` y `gunicorn` solo (gracias al `Dockerfile`).
7. Entra al **Shell** del servicio web y crea el superusuario:
   ```bash
   uv run python manage.py createsuperuser
   ```
8. Railway te da una URL publica. Listo.

### Opcion 2: Render

1. Ve a **https://render.com** > **New** > **Web Service**.
2. Conecta tu repositorio de GitHub y selecciona `InsightBoard`.
3. Render detecta el `Dockerfile`. Region: la mas cercana.
4. Agrega los servicios de datos:
   - **New** > **PostgreSQL** (copia su **Internal Database URL**)
   - **New** > **Redis** (copia su **Internal Connection String**)
5. En el Web Service, pestana **Environment**, agrega:
   ```
   DJANGO_SECRET_KEY=clave-secreta-larga
   DEBUG=False
   ALLOWED_HOSTS=insightboard.onrender.com
   DATABASE_URL=postgres://...   (del paso 4)
   REDIS_URL=redis://...         (del paso 4)
   ```
6. **Start Command** (opcional, el `Dockerfile` ya lo hace, pero asi es explicito):
   ```bash
   uv run python manage.py migrate && uv run gunicorn config.wsgi --bind 0.0.0.0:$PORT
   ```
7. Clic en **Create Web Service**. Render construye y despliega.
8. Crea el superusuario desde la pestana **Shell**:
   ```bash
   uv run python manage.py createsuperuser
   ```
9. URL publica: `https://insightboard.onrender.com` (Swagger en `/api/docs/`).

---

## Paso 6: Comandos utiles

| Comando | Que hace |
|---------|----------|
| `docker-compose up -d` | Encender todo |
| `docker-compose down` | Apagar todo (guardar datos) |
| `docker-compose logs -f` | Ver logs en tiempo real |
| `docker-compose restart web` | Reiniciar solo el servidor |
| `docker-compose exec web bash` | Entrar al servidor |
| `docker-compose exec web uv run python manage.py migrate` | Aplicar migraciones |
| `docker-compose exec web uv run python manage.py createsuperuser` | Crear admin |

---

## Solucion de problemas

### "El servidor web no inicia"

```bash
# Ver logs del servidor
docker-compose logs web

# Reiniciar el servidor
docker-compose restart web
```

### "La base de datos no conecta"

```bash
# Verificar que PostgreSQL esta corriendo
docker-compose ps db

# Entrar a la base de datos
docker-compose exec db psql -U postgres insightboard
```

### "El frontend no carga graficos"

1. Abre la consola del navegador (F12)
2. Busca errores en la pestana "Console"
3. Verifica que `http://127.0.0.1:8000` esta accesible

### "Error CORS"

Verifica que `CORS_ALLOW_ALL_ORIGINS = True` en `config/settings/base.py`.

### "Token expirado"

Vuelve a hacer login para obtener un token nuevo.

---

## Resumen del curso

| Capitulo | Que aprendiste |
|----------|---------------|
| C0 | Que es InsightBoard y como esta organizado |
| C1 | Instalar Python, VS Code, Git, uv |
| C2 | Docker, PostgreSQL, Redis |
| C3 | Crear proyecto Django, apps, settings |
| C4 | Modelos de base de datos |
| C5 | API REST con DRF (serializers, views, endpoints) |
| C6 | Frontend con Bootstrap y Chart.js |
| C7 | Autenticacion JWT |
| C8 | Pruebas y deploy |

---

## ¿Que sigue?

Ahora que tienes InsightBoard funcionando, puedes:

1. **Agregar mas funcionalidades** - Exportar PDF, filtros avanzados, modo oscuro
2. **Mejorar el frontend** - Agregar animaciones, mejorar el diseno
3. **Crear tu propia app** - Usa lo que aprendiste para construir algo nuevo
4. **Compartir** - Muestra tu proyecto a tus amigos o en tu portafolio

---

## Felicidades

Has completado el tutorial de InsightBoard. Ahora tienes:

- Un proyecto completo de analitica
- Conocimientos de Django, DRF, PostgreSQL, Docker
- Experiencia creando APIs REST
- Experiencia construyendo frontends interactivos

**¡Sigue aprendiendo y construyendo!**
