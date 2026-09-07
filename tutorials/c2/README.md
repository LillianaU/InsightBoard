# C2 - Encender el taller: Docker y la base de datos

> **Edad recomendada:** 10-11 años  
> **Tiempo estimado:** 25 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Qué vamos a hacer?

En este capítulo vamos a **encender la base de datos** para que esté lista cuando empecemos a programar. No escribiremos código todavía, solo prepararemos el "escenario de juego".

---

## ¿Qué es Docker? (versión rápida)

Docker es como **tener varias computadoras dentro de tu computadora**.

En vez de instalar PostgreSQL, Redis, etc. una por una y pelear con configuraciones, Docker nos da:
- Una "cajita" con PostgreSQL
- Una "cajita" con Redis
- Una "cajita" con nuestro servidor web

Todas se comunican entre sí sin instalarlas manualmente.

---

## Paso 1: Instalar Docker Desktop

1. Ve a [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Descarga la versión para **Windows**
3. Ejecuta el instalador y marca todas las casillas
4. Clic en **"Finish"**
5. **Reinicia tu computadora** (importante)

Cuando vuelvas a encenderla, busca una **ballena 🐳** en tu barra de tareas. Eso significa que Docker está vivo.

---

## Paso 2: Verificar que Docker funciona

Abre la terminal de Windows (`Windows + R`, escribe `cmd`, Enter) y escribe:

```bash
docker --version
```

Si ves `Docker version 24.0.5`, ¡perfecto! 🎉

---

## Paso 3: Entender el archivo `docker-compose.yml`

Ya tienes este archivo en tu proyecto. Es como la **lista de compras** de un supermercado: le dice a Docker exactamente qué necesitamos.

Las "cajitas" que necesitamos son:

| Cajita | ¿Qué es? | ¿Para qué sirve? |
|--------|----------|------------------|
| `db` | PostgreSQL | Guardar todos los datos (eventos, usuarios, reportes) |
| `redis` | Redis | Memoria rápida para tareas en segundo plano |
| `web` | Nuestro servidor | Donde vivirá la página web y la API |
| `celery` | Trabajador | Hace tareas pesadas sin detener el servidor |

---

## Paso 4: Levantar las cajitas

En la terminal, en la carpeta del proyecto:

```bash
docker-compose up -d
```

Verás muchas líneas. Las importantes son al final:

```
 ✔ Container insightboard-db-1       Started
 ✔ Container insightboard-redis-1    Started
 ✔ Container insightboard-web-1      Started
 ✔ Container insightboard-celery-1   Started
```

**¡Eso significa que ya tienes 4 computadoras funcionando dentro de tu computadora!** 🚀

---

## Paso 5: Verificar que están vivas

```bash
docker-compose ps
```

Debes ver algo como:

```
     Name                   Command               State           Ports
----------------------------------------------------------------------------
insightboard-db-1       docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
insightboard-redis-1    docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
insightboard-web-1      uv run python manage.py run...   Up      0.0.0.0:8000->8000/tcp
insightboard-celery-1   uv run celery -A config.cel...   Up
```

Si todas están en `Up`, estás listo.

---

## Paso 6: ¿Dónde se guardan los datos?

Los datos se guardan en **volúmenes de Docker**. Son como "cajones" que Docker administra.

### Regla de oro

| Acción | ¿Se pierden los datos? |
|--------|------------------------|
| Apagar la computadora | **No** |
| `docker-compose down` | **No** |
| `docker-compose down -v` | **Sí** |

Así que **nunca** uses `down -v` a menos que quieras borrar todo intencionalmente.

### Hacer respaldos (opcional pero recomendado)

Si quieres guardar una copia de tus datos:

```bash
docker-compose exec db pg_dump -U postgres insightboard > respaldo.sql
```

Esto crea un archivo `respaldo.sql` en tu carpeta del proyecto.

---

## Paso 7: Probar la base de datos

Vamos a entrar a PostgreSQL para ver que funciona:

```bash
docker-compose exec db psql -U postgres insightboard
```

Dentro de psql, escribe:

```sql
\l
```

Esto muestra las bases de datos. Deberías ver `insightboard`.

Para salir:

```sql
\q
```

---

## ¿Qué sigue?

Ya tenemos la base de datos encendida. En el siguiente capítulo vamos a **crear el proyecto Django** y conectar todo.

> **Ejercicio para casa:** Dibuja en un papel las 4 cajitas (db, redis, web, celery) y conéctalas con flechas. ¿Por qué crees que `web` necesita a `db`?

---

## Resumen del capítulo C2

✅ Instalamos Docker Desktop  
✅ Levantamos 4 servicios con `docker-compose up -d`  
✅ Verificamos que están corriendo  
✅ Aprendimos que los datos se guardan en volúmenes  
✅ Probamos la base de datos con `psql`  

**¡Tu taller ya tiene luz, agua y electricidad!** 🔌
