# Diagrama del Capítulo 2 — Las cajitas de Docker

## Diagrama

```mermaid
graph TD
    subgraph VOLUMENES [📦 Volúmenes de datos]
        PGO-data[postgres_data<br/>💾 Datos de la base de datos]
        RDATA[redis_data<br/>💾 Datos rápidos de Redis]
    end

    subgraph DOCKER [🐳 Docker — tu computadora con 4 micro-computadoras]
        DB[(🟢 db<br/>PostgreSQL<br/>Guarda la información)]
        REDIS[(🟡 redis<br/>Redis<br/>Memoria rápida)]
        WEB[(🔵 web<br/>Servidor web<br/>La página)]
        WORKER[(🟣 celery<br/>Trabajador<br/>Tareas pesadas)]
    end

    DB --> PGO-data
    REDIS --> RDATA

    WEB <--> DB
    WEB <--> REDIS
    WORKER <--> DB
    WORKER <--> REDIS
```

## Explicación

Docker crea **4 micro-computadoras** dentro de tu PC, como si tuvieras 4 amiguitos trabajando juntos. La base de datos (`db`) guarda los datos en un cajón (`postgres_data`), y Redis guarda datos rápidos en otro cajón (`redis_data`).

### Conexiones

| Flecha | Significado |
|--------|-------------|
| `db --> 💾` | La base de datos guarda sus datos en el cajón `postgres_data` |
| `redis --> 💾` | Redis guarda sus datos en el cajón `redis_data` |
| `web <--> db` | El servidor web **habla** con la base de datos para leer y escribir información |
| `web <--> redis` | El servidor web usa Redis para tareas rápidas |
| `celery <--> db` | El trabajador lee y escribe datos en la base de datos |
| `celery <--> redis` | El trabajador toma tareas de la memoria rápida de Redis |
