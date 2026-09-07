# C4 - Modelos de base de datos

> **Tiempo estimado:** 30 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

En este capitulo vamos a **entender** los 4 modelos que creamos en el capitulo anterior. No vamos a crear nada nuevo, solo a comprender como funciona por dentro.

---

## ¿Que es un modelo?

Un **modelo** es como la **instruccion de armado de LEGO**. Nos dice:
- Que piezas necesito
- Como se conectan entre si
- Que forma tiene cada pieza

En programacion, un modelo describe **como se guarda la informacion** en la base de datos.

---

## Nuestros 4 modelos

### 1. DataSource (Fuente de Datos)

```python
class DataSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Analogia:** Es como una **caja de almacenamiento con etiqueta**.

| Campo | Tipo | Ejemplo | Que guarda |
|-------|------|---------|-----------|
| `name` | CharField | "Tienda Online" | Nombre de la fuente |
| `description` | TextField | "Ventas del sitio web" | Descripcion opcional |
| `created_by` | ForeignKey -> User | admin@insightboard.com | Quien la creo |
| `created_at` | DateTimeField | 2026-09-06 14:30 | Cuando se creo |

---

### 2. Event (Evento)

```python
class Event(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
```

**Analogia:** Es como una **ficha individual** que registra algo que paso.

| Campo | Tipo | Ejemplo | Que guarda |
|-------|------|---------|-----------|
| `source` | ForeignKey -> DataSource | "Tienda Online" | De que fuente viene |
| `event_type` | CharField | "compra", "visita" | Tipo de evento |
| `payload` | JSONField | `{"producto": "camisa", "precio": 25}` | Datos extra flexibles |
| `created_at` | DateTimeField | 2026-09-06 14:30 | Cuando paso |
| `user` | ForeignKey -> User | admin@insightboard.com | Quien lo hizo (opcional) |

**¿Que es `payload`?** Es una **cajita magica** donde guardamos cualquier informacion extra. Puede ser un numero, texto, lista o diccionario.

Ejemplos de payload:

```json
{"producto": "camisa", "precio": 25, "talla": "M"}
{"pagina": "/checkout", "duracion_segundos": 45}
{"temperatura": 22.5, "ciudad": "CDMX"}
```

---

### 3. DailyMetric (Metrica Diaria)

```python
class DailyMetric(models.Model):
    date = models.DateField()
    event_type = models.CharField(max_length=50)
    count = models.BigIntegerField()
    unique_users = models.BigIntegerField()
```

**Analogia:** Es como un **reporte pre-armado** que dice "en este dia paso X".

| Campo | Tipo | Ejemplo | Que guarda |
|-------|------|---------|-----------|
| `date` | DateField | 2026-09-06 | Dia del reporte |
| `event_type` | CharField | "compra" | Tipo de evento |
| `count` | BigIntegerField | 42 | Cuantos eventos hubo |
| `unique_users` | BigIntegerField | 15 | Cuantos usuarios distintos |

**¿Por que existe?** Para que los graficos se vean rapido sin tener que contar todos los eventos de nuevo cada vez.

---

### 4. SavedReport (Reporte Guardado)

```python
class SavedReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_reports')
    name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Analogia:** Es como **guardar una partida en un videojuego**.

| Campo | Tipo | Ejemplo | Que guarda |
|-------|------|---------|-----------|
| `user` | ForeignKey -> User | admin@insightboard.com | Quien lo guardo |
| `name` | CharField | "Ventas semanales" | Nombre del reporte |
| `config` | JSONField | `{"tipo": "barras", "dias": 7}` | Configuracion del reporte |
| `created_at` | DateTimeField | 2026-09-06 | Cuando lo guardo |

---

## Como se conectan los modelos

```
DataSource (1) ────┐
                   ├─── Event (muchos)
User (1) ──────────┘
                   ├─── Event (muchos)
                   ├─── DataSource (muchos)
                   └─── SavedReport (muchos)

DailyMetric (independiente)
```

**Regla de oro:** Una `DataSource` puede tener **muchos** `Event`, pero un `Event` pertenece a **una sola** `DataSource`.

Esto se llama **relacion uno a muchos** (ForeignKey).

---

## Que es un JSONField

Imagina que tienes una **cajita magica** donde puedes guardar cualquier cosa:

- Un numero: `42`
- Un texto: `"camisa azul"`
- Una lista: `["rojo", "azul", "verde"`
- Un diccionario: `{"talla": "M", "color": "azul"}`

Esa cajita magica es el `JSONField`. Nos sirve para guardar datos flexibles sin crear campos nuevos cada vez.

---

## Que son los indices

Los **indices** son como el **indice de un libro**. Si buscas "dragones" en un libro de 500 paginas, no lees pagina por pagina: vas al indice y saltas directo a la pagina 234.

En el codigo:

```python
indexes = [models.Index(fields=['event_type', 'created_at'])]
```

Esto le dice a la base de datos: "Cuando busquen eventos por tipo y fecha, no busques en toda la caja, ve directo a donde estan guardados".

---

## Ejercicio practico

1. Abre el panel de admin: http://127.0.0.1:8000/admin/
2. Ingresa con `admin@insightboard.com` / `admin123`
3. Crea una `DataSource` llamada "Tienda Online"
4. Crea un `Event` asociado a esa fuente:
   - `event_type`: "compra"
   - `payload`: `{"producto": "camisa", "precio": 25}`
5. Guarda y observa como se conectan

### Verificacion

- ¿Puedes ver la DataSource en la lista? = Funciona
- ¿Puedes ver el Event asociado? = Funciona
- ¿El Event muestra la fuente correcta? = Funciona

---

## Resumen del paso

| Concepto | Que es | Ejemplo |
|----------|-------|---------|
| Modelo | Instruccion de armado | Como armar un LEGO |
| DataSource | Caja de datos | "Tienda Online" |
| Event | Ficha individual | "Usuario compro camisa" |
| DailyMetric | Reporte del dia | "Hoy 42 ventas" |
| SavedReport | Partida guardada | "Grafico de ventas" |
| ForeignKey | Relacion uno a muchos | 1 DataSource -> muchos Events |
| JSONField | Cajita magica | Guarda cualquier dato |
| Index | Indice de libro | Busqueda rapida |

---

**¿Entendiste los modelos? Sigue con el [Capitulo 5: API REST con DRF](../c5/README.md)**
