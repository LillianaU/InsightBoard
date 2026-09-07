# C2 - Docker y base de datos

> **Tiempo estimado:** 25 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a instalar Docker y levantar los servicios que InsightBoard necesita para funcionar:
- **PostgreSQL** - Donde se guardan los datos
- **Redis** - Memoria rapida para tareas en segundo plano
- **Web** - El servidor de Django
- **Celery** - Trabajador de tareas pesadas

---

## ¿Que es Docker?

Docker es como **tener varias computadoras dentro de tu computadora**.

En vez de instalar PostgreSQL, Redis, etc. una por una y pelear con configuraciones, Docker nos da "cajitas" listas para usar:

```
┌─────────────────────────────────────────────────┐
│                TU COMPUTADORA                    │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │    db     │  │  redis   │  │   web    │      │
│  │ PostgreSQL│  │  Cache   │  │  Django  │      │
│  │  :5432   │  │  :6379   │  │  :8000   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                  │
│  ┌──────────┐                                   │
│  │ celery   │                                   │
│  │ Trabajador│                                   │
│  └──────────┘                                   │
└─────────────────────────────────────────────────┘
```

---

## Paso 1: Instalar Docker Desktop

1. Ve a **https://www.docker.com/products/docker-desktop/**
2. Haz clic en **"Download for Windows"**
3. Ejecuta el instalador
4. Marca todas las casillas que aparezcan
5. Haz clic en **"Finish"**
6. **REINICIA tu computadora** (esto es obligatorio)

### Verificar que funciono

Despues de reiniciar, busca una **ballena** en tu barra de tareas (esquina inferior derecha). Si la ves, Docker esta vivo.

Abre la terminal y escribe:

```bash
docker --version
```

**Resultado esperado:** `Docker version 24.x.x` o similar

---

## Paso 2: Entender docker-compose.yml

En la carpeta del proyecto hay un archivo `docker-compose.yml`. Este archivo es la **lista de compras** de Docker: le dice exactamente que necesitamos.

```yaml
services:
  db:          # PostgreSQL - guarda los datos
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: insightboard
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  redis:       # Redis - memoria rapida
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:         # Django - el servidor web
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  celery:      # Celery - tareas en segundo plano
    build: .
    command: celery -A config.celery_app worker
    depends_on:
      - redis
```

### Explicacion de cada servicio

| Servicio | Puerto | Que hace |
|----------|--------|----------|
| `db` | 5432 | Guarda usuarios, eventos, reportes |
| `redis` | 6379 | Memoria cache para Celery |
| `web` | 8000 | Sirve la API y el admin de Django |
| `celery` | - | Ejecuta tareas pesadas sin bloquear el servidor |

---

## Paso 3: Levantar los servicios

En la terminal, navega a la carpeta del proyecto:

```bash
cd C:\Users\LILLYU\Documents\GitHub\InsightBoard
```

Ejecuta:

```bash
docker-compose up -d
```

Espera unos minutos. Veras algo como:

```
 ✔ Container insightboard-db-1       Started
 ✔ Container insightboard-redis-1    Started
 ✔ Container insightboard-web-1      Started
 ✔ Container insightboard-celery-1   Started
```

**Si ves 4 "Started", ¡funciono!**

---

## Paso 4: Verificar que estan corriendo

```bash
docker-compose ps
```

Debes ver los 4 servicios con estado `Up`:

```
Name                    Command               State           Ports
---------------------------------------------------------------------------
insightboard-db-1       docker-entrypoint.sh postgres   Up   0.0.0.0:5432->5432
insightboard-redis-1    docker-entrypoint.sh redis ...   Up   0.0.0.0:6379->6379
insightboard-web-1      uv run python manage.py run...   Up   0.0.0.0:8000->8000
insightboard-celery-1   uv run celery -A config.cel...   Up
```

> **¿Alguno no esta en `Up`?** Ejecuta `docker-compose logs` para ver que paso.

---

## Paso 5: Probar la base de datos

Vamos a entrar a PostgreSQL para confirmar que funciona:

```bash
docker-compose exec db psql -U postgres insightboard
```

Dentro de la consola de PostgreSQL escribe:

```sql
\l
```

Esto muestra todas las bases de datos. Debes ver `insightboard` en la lista.

Para salir escribe:

```sql
\q
```

---

## Paso 6: Entender los volúmenes

Los datos se guardan en **volumenes de Docker**. Son como "cajones" persistentes.

| Accion | ¿Se pierden los datos? |
|--------|------------------------|
| Apagar la computadora | **No** |
| `docker-compose down` | **No** |
| `docker-compose down -v` | **SI** (borra todo) |

> **Regla de oro:** Nunca uses `docker-compose down -v` a menos que quieras borrar todos los datos intencionalmente.

---

## Paso 7: Comandos utiles de Docker

| Comando | Que hace |
|---------|----------|
| `docker-compose up -d` | Enciende todos los servicios |
| `docker-compose down` | Apaga los servicios (guarda datos) |
| `docker-compose ps` | Muestra el estado de los servicios |
| `docker-compose logs -f` | Muestra los logs en tiempo real |
| `docker-compose exec web bash` | Entra a la consola del servidor web |
| `docker-compose restart web` | Reinicia solo el servidor web |

---

## Solucion de problemas

### "Docker no inicia despues de reiniciar"
- Abre Docker Desktop manualmente
- Espera a que la ballena se ponga verde

### "Puerto 5432 ya esta en uso"
- Cierra cualquier otro PostgreSQL que tengas instalado
- O cambia el puerto en `docker-compose.yml`: `"5433:5432"`

### "Error de permisos"
- Ejecuta Docker Desktop como administrador

---

## Resumen del paso

| Paso | Comando | Resultado esperado |
|------|---------|-------------------|
| Instalar Docker | Descargar e instalar | Ballena en la barra de tareas |
| Verificar | `docker --version` | `Docker version 24.x.x` |
| Levantar | `docker-compose up -d` | 4 servicios Started |
| Verificar estado | `docker-compose ps` | Todos en `Up` |
| Probar DB | `docker-compose exec db psql -U postgres insightboard` | Entra a la consola |

---

**¿Todo funciono? Sigue con el [Capitulo 3: Crear proyecto Django](../c3/README.md)**
