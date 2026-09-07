# C6 - Frontend y dashboards

> **Tiempo estimado:** 35 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a entender y configurar el **frontend** de InsightBoard: las paginas web que el usuario ve.

### Al final de este capitulo tendras:
- Un dashboard con graficos interactivos
- Un formulario para registrar eventos
- Un generador de reportes personalizados
- Graficos de lineas, barras y pasteles

---

## ¿Que es el frontend?

El **frontend** es lo que el usuario **ve** en el navegador. Mientras que el backend (Django) es el cerebro, el frontend es la **cara**.

```
FRONTEND (lo que ves)              BACKEND (lo que piensa)
┌─────────────────────┐           ┌─────────────────────┐
│   Dashboard         │           │   API REST          │
│   - Graficos        │ ───────>  │   - Endpoints       │
│   - Numeros         │  <──────  │   - Logica          │
│   - Tablas          │  JSON     │   - Base de datos   │
└─────────────────────┘           └─────────────────────┘
```

---

## Las 4 paginas del frontend

| Pagina | Archivo | Que hace |
|--------|---------|----------|
| Dashboard | `frontend/index.html` | Muestra estadisticas y graficos |
| Eventos | `frontend/events.html` | Formulario para crear eventos |
| Reportes | `frontend/reports.html` | Crear reportes personalizados |
| Login | `frontend/login.html` | Iniciar sesion |

---

## Tecnologias del frontend

| Tecnologia | Para que sirve |
|-----------|----------------|
| **Bootstrap 5** | Disenio responsive (se ve bien en celular y PC) |
| **Chart.js** | Dibujar graficos (lineas, barras, pasteles) |
| **JavaScript vanilla** | Logica del lado del cliente |
| **fetch API** | Hablar con el backend (hacer peticiones HTTP) |

---

## Paso 1: Entender la estructura del frontend

```
frontend/
├── index.html          # Dashboard principal
├── events.html         # Registro de eventos
├── reports.html        # Reportes personalizados
├── login.html          # Pagina de login
├── css/
│   └── style.css       # Estilos personalizados
└── js/
    ├── app.js          # Funciones utilitarias
    └── auth.js         # Manejo de autenticacion JWT
```

---

## Paso 2: Entender auth.js

El archivo `frontend/js/auth.js` maneja toda la autenticacion:

```javascript
const AUTH = {
    API_URL: 'http://127.0.0.1:8000/api',

    // Obtener token guardado
    getToken() {
        return localStorage.getItem('token');
    },

    // Obtener info del usuario
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    // Verificar si esta logueado
    isAuthenticated() {
        return !!this.getToken();
    },

    // Headers con token para peticiones autenticadas
    getHeaders() {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    // Hacer peticion GET
    async apiGet(endpoint) {
        const response = await fetch(`${this.API_URL}${endpoint}`, {
            headers: this.getHeaders()
        });
        if (!response.ok) {
            if (response.status === 401) {
                this.logout();
                window.location.href = 'login.html';
            }
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    },

    // Hacer peticion POST
    async apiPost(endpoint, data) {
        const response = await fetch(`${this.API_URL}${endpoint}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            if (response.status === 401) {
                this.logout();
                window.location.href = 'login.html';
            }
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || error.message || `HTTP ${response.status}`);
        }
        return response.json();
    },

    // Cerrar sesion
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    // Redirigir si no esta logueado
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = 'login.html';
        }
    }
};
```

### Flujo de autenticacion

```
1. Usuario ingresa email/contrasena en login.html
         │
2. frontend envia POST a /api/auth/login/
         │
3. Backend devuelve { access: "token...", user: {...} }
         │
4. frontend guarda token en localStorage
         │
5. Todas las peticiones incluyen Authorization: Bearer token
         │
6. Si token expira (401), se cierra sesion y redirige a login
```

---

## Paso 3: Entender app.js

El archivo `frontend/js/app.js` tiene funciones utiles:

```javascript
function formatDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString('es-ES');
}

function formatNumber(num) {
    return new Intl.NumberFormat('es-ES').format(num);
}
```

---

## Paso 4: Entender el Dashboard (index.html)

El dashboard muestra:
1. **Tarjetas de resumen** - Total de eventos, fuentes activas, usuarios activos
2. **Grafico de lineas** - Eventos por dia
3. **Grafico de pasteles** - Eventos por tipo
4. **Tabla de eventos recientes** - Ultimos eventos registrados

### Como funciona el grafico de lineas

```javascript
// 1. Pide datos al backend
const data = await AUTH.apiGet('/metrics/timeseries/?days=30');

// 2. Extrae fechas y cantidades
const labels = data.map(d => d.day);
const counts = data.map(d => d.count);

// 3. Dibuja el grafico con Chart.js
new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Eventos',
            data: counts,
            borderColor: '#0d6efd'
        }]
    }
});
```

---

## Paso 5: Entender Events (events.html)

La pagina de eventos tiene 2 partes:

1. **Formulario** - Para crear eventos nuevos
2. **Tabla** - Muestra los eventos recientes

### Como se crea un evento

```javascript
async function createEvent() {
    const source = document.getElementById('source').value;
    const eventType = document.getElementById('eventType').value;
    const payload = JSON.parse(document.getElementById('payload').value);

    await AUTH.apiPost('/events/ingest/', {
        source: source,
        event_type: eventType,
        payload: payload
    });

    // Recargar la tabla
    loadEvents();
}
```

---

## Paso 6: Entender Reports (reports.html)

La pagina de reportes permite:
1. **Crear reportes** - Elegir tipo de grafico, metrica, dimension
2. **Ver preview** - Grafico en tiempo real
3. **Guardar reportes** - Para verlos despues
4. **Exportar CSV** - Descargar datos

### Como se genera un reporte

```javascript
async function generateReport() {
    const metric = document.getElementById('metric').value;
    const dimension = document.getElementById('dimension').value;
    const days = document.getElementById('days').value;

    // Pedir datos al backend
    const data = await AUTH.apiGet(`/metrics/${metric}/?dimension=${dimension}&days=${days}`);

    // Dibujar grafico
    drawChart(data);
}
```

---

## Paso 7: Iniciar el servidor del frontend

Para ver el frontend necesitas un servidor web. Abre una **nueva terminal** y ejecuta:

```bash
cd frontend
python -m http.server 8080
```

Abre el navegador en: **http://localhost:8080**

---

## Paso 8: Probar cada pagina

### Login
1. Ve a http://localhost:8080/login.html
2. Ingresa `admin@insightboard.com` / `admin123`
3. Debes ser redirigido al dashboard

### Dashboard
1. Ve a http://localhost:8080
2. Debes ver tarjetas con estadisticas
3. Debes ver graficos (aunque esten vacios si no hay datos)

### Eventos
1. Ve a http://localhost:8080/events.html
2. Crea un evento:
   - Source: "tienda"
   - Event Type: "compra"
   - Payload: `{"producto": "camisa", "precio": 25}`
3. Haz clic en "Registrar Evento"
4. El evento debe aparecer en la tabla

### Reportes
1. Ve a http://localhost:8080/reports.html
2. Selecciona una metrica y dimension
3. Haz clic en "Generar"
4. Debes ver un grafico

---

## Paso 9: Entender el CSS

El archivo `frontend/css/style.css` personaliza la apariencia:

```css
/* Tarjetas de resumen */
.stat-card {
    border-left: 4px solid #0d6efd;
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
}

/* Graficos */
.chart-container {
    position: relative;
    height: 300px;
}
```

---

## Solucion de problemas

### "No puedo acceder a http://localhost:8080"
- Asegurate de que el servidor esta corriendo: `python -m http.server 8080`
- Verifica que estas en la carpeta `frontend`

### "Error de conexion en el login"
- Asegurate de que el backend esta corriendo: `docker-compose ps`
- Verifica que el backend esta en http://127.0.0.1:8000

### "No veo graficos"
- Asegurate de que Chart.js esta cargado (revisa la consola del navegador)
- Verifica que hay datos en la base de datos

### "CORS error"
- Verifica que `CORS_ALLOW_ALL_ORIGINS = True` en settings

---

## Resumen del paso

| Paso | Que hicimos | Verificacion |
|------|------------|-------------|
| 1-3 | Entender frontend | Sabes que hace cada archivo |
| 4 | Dashboard | Ves tarjetas y graficos |
| 5 | Events | Puedes crear eventos |
| 6 | Reports | Puedes generar reportes |
| 7 | Servidor frontend | http://localhost:8080 funciona |
| 8 | Probar todo | Cada pagina funciona |

---

**¿El frontend funciona? Sigue con el [Capitulo 7: Autenticacion JWT](../c7/README.md)**
