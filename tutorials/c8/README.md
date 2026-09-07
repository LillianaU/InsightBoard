# C8 - Probar y deploy

> **Tiempo estimado:** 20 minutos
> **Dificultad:** ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a hacer las **pruebas finales** de todo el proyecto y aprender a **desplegarlo** en internet.

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

### Opcion 1: Railway (recomendada para principiantes)

1. Ve a **https://railway.app**
2. Crea una cuenta con GitHub
3. Haz clic en "New Project" > "Deploy from GitHub repo"
4. Selecciona tu repositorio de InsightBoard
5. Railway detectara el `Dockerfile` automaticamente
6. Agrega las variables de entorno en la pestana "Variables":

```
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
POSTGRES_DB=insightboard
POSTGRES_USER=tu-usuario
POSTGRES_PASSWORD=tu-contrasena
POSTGRES_HOST=tu-host-de-railway
POSTGRES_PORT=5432
REDIS_URL=tu-url-de-redis
ALLOWED_HOSTS=tu-app.railway.app
DEBUG=False
```

7. Railway desplegara automaticamente

### Opcion 2: Render

1. Ve a **https://render.com**
2. Crea un "Web Service" desde tu repositorio de GitHub
3. Configura:
   - **Build Command:** `docker-compose build`
   - **Start Command:** `docker-compose up`
4. Agrega las variables de entorno
5. Haz clic en "Create Web Service"

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
