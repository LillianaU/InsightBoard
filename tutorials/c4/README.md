# C4 - Armar las piezas: Modelos de base de datos

> **Edad recomendada:** 10-11 años  
> **Tiempo estimado:** 30 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Qué vamos a hacer?

Ya tenemos el proyecto Django corriendo. Ahora vamos a **entender las piezas que acabamos de crear** y por qué las armamos así.

---

## ¿Qué es un modelo?

Un **modelo** es como la **instrucción de armado de LEGO**. Nos dice:
- ¿Qué piezas necesito?
- ¿Cómo se conectan entre sí?
- ¿Qué forma tiene cada pieza?

En programación, un modelo es un archivo que describe **cómo se guarda la información** en la base de datos.

---

## Nuestros 4 modelos principales

### 🧱 1. DataSource (Fuente de Datos)

```python
class DataSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Analogía:** Es como una **caja de almacenamiento con etiqueta**.

| Pieza LEGO | Campo | Ejemplo |
|-----------|-------|---------|
| Nombre en la etiqueta | `name` | "Ventas de septiembre" |
| Nota adhesiva | `description` | "Datos de la tienda online" |
| Dueño de la caja | `created_by` | El usuario que la creó |
| Fecha de compra | `created_at` | Cuándo se creó |

---

### 🧱 2. Event (Evento)

```python
class Event(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
```

**Analogía:** Es como una **ficha individual** que registra algo que pasó.

| Pieza LEGO | Campo | Ejemplo |
|-----------|-------|---------|
| ¿De qué caja viene? | `source` | "Ventas de septiembre" |
| Tipo de evento | `event_type` | "compra", "visita", "click" |
| Datos extra | `payload` | `{"producto": "camisa", "precio": 25}` |
| Cuándo pasó | `created_at` | "2026-09-06 14:30" |
| Quién lo hizo | `user` | Usuario #123 (opcional) |

**¿Qué es `payload`?** Es una **cajita mágica** donde guardamos cualquier información extra. Piensa en ella como una **mochila** que puede llevar lo que quieras.

---

### 🧱 3. DailyMetric (Métrica Diaria)

```python
class DailyMetric(models.Model):
    date = models.DateField()
    event_type = models.CharField(max_length=50)
    count = models.BigIntegerField()
    unique_users = models.BigIntegerField()
```

**Analogía:** Es como un **reporte pre-armado** que dice "en este día pasó X".

| Pieza LEGO | Campo | Ejemplo |
|-----------|-------|---------|
| Fecha del reporte | `date` | "2026-09-06" |
| Tipo de evento | `event_type` | "compra" |
| Cuántos eventos | `count` | 42 |
| Cuántas personas únicas | `unique_users` | 15 |

**¿Por qué existe?** Para que los gráficos se vean rápidos sin tener que contar todos los eventos de nuevo cada vez.

---

### 🧱 4. SavedReport (Reporte Guardado)

```python
class SavedReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_reports')
    name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Analogía:** Es como **guardar una partida en un videojuego**.

| Pieza LEGO | Campo | Ejemplo |
|-----------|-------|---------|
| Quién lo guardó | `user` | "maria@gmail.com" |
| Nombre del reporte | `name` | "Ventas de septiembre" |
| Configuración | `config` | `{"tipo": "barras", "filtros": {...}}` |
| Cuándo lo guardó | `created_at` | "2026-09-06" |

---

## ¿Cómo se conectan los LEGOs?

```
DataSource (1) ────┐
                   ├─── Event (muchos)
User (1) ──────────┘
                   ├─── Event (muchos)
                   ├─── DataSource (muchos)
                   └─── SavedReport (muchos)
```

**Regla de oro:** Una `DataSource` puede tener **muchos** `Event`, pero un `Event` pertenece a **una sola** `DataSource`.

Esto se llama **relación uno a muchos** (ForeignKey).

---

## ¿Qué es un `JSONField`?

Imagina que tienes una **cajita mágica** donde puedes guardar cualquier cosa:
- Un número: `42`
- Un texto: `"camisa azul"`
- Una lista: `["rojo", "azul", "verde"]`
- Un diccionario: `{"talla": "M", "color": "azul"}`

Esa cajita mágica es el `JSONField`. Nos sirve para guardar datos flexibles sin tener que crear campos nuevos cada vez.

---

## ¿Qué son los índices?

Los **índices** son como el **índice de un libro**. Si buscas "dragones" en un libro de 500 páginas, no lees página por página: vas al índice y saltas directo a la página 234.

En programación:
```python
indexes = [models.Index(fields=['event_type', 'created_at'])]
```

Esto le dice a la base de datos: "Cuando busquen eventos por tipo y fecha, no busques en toda la caja, ve directo a donde están guardados".

---

## Ejercicio práctico

1. Abre el panel de admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
2. Crea una `DataSource` llamada "Tienda Online"
3. Crea un `Event` asociado a esa fuente:
   - `event_type`: "compra"
   - `payload`: `{"producto": "camisa", "precio": 25}`
4. Guarda y observa cómo se conectan

---

## ¿Qué sigue?

Ahora que entiendes las piezas, puedes empezar a:
- Crear endpoints para recibir datos
- Hacer gráficos con D3.js
- Exportar reportes

En los siguientes capítulos aprenderás a construir la API y el frontend.

---

## Resumen del capítulo C4

✅ Entendimos qué son los modelos (instrucciones LEGO)  
✅ Vimos los 4 modelos de InsightBoard  
✅ Entendimos las relaciones entre modelos  
✅ Aprendimos qué es JSONField  
✅ Descubrimos para qué sirven los índices  
✅ Creamos datos de prueba en el panel de admin  

**¡Ahora eres un arquitecto de datos en miniatura!** 🏗️
