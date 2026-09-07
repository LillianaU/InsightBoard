# C7 - Autenticacion JWT

> **Tiempo estimado:** 25 minutos  
> **Dificultad:** ⭐ ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a entender como funciona la **autenticacion JWT** en InsightBoard: como los usuarios inician sesion, como se protegen las rutas, y como el frontend maneja los tokens.

---

## ¿Que es JWT?

**JWT** (JSON Web Token) es como un **pase de entrada** temporal.

```
CUANDO INICIAS SESION:
─────────────────────────────────────────────
1. Envias: email + contrasena
2. El servidor verifica que son correctos
3. El servidor te da un "pase" (token)
4. Guardas el pase en tu navegador
─────────────────────────────────────────────

CUANDO QUIERES ACCEDER A ALGO PROTEGIDO:
─────────────────────────────────────────────
1. Muestras tu pase (token en el header)
2. El servidor verifica que no ha expirado
3. Si es valido, te deja pasar
4. Si no, te pide que inicies sesion de nuevo
─────────────────────────────────────────────
```

---

## Estructura de un JWT

Un token JWT se ve asi:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImFkbWluQGluc2lnaHRib2FyZC5jb20iLCJleHAiOjE2OTQwMDAwMDB9.firma_secreta
```

Tiene 3 partes separadas por puntos:
1. **Header** - Tipo de algoritmo
2. **Payload** - Datos del usuario (email, ID, fecha de expiracion)
3. **Firma** - Verificacion de seguridad

---

## Como funciona en InsightBoard

```
┌──────────┐     POST /api/auth/login/      ┌──────────┐
│ Frontend │  ─────────────────────────────>  │ Backend  │
│          │     {email, password}            │          │
│          │                                  │ Verifica │
│          │  <─────────────────────────────  │ usuario  │
│          │     {access: "token...",         │          │
│          │      user: {...}}                │          │
└──────────┘                                  └──────────┘
     │
     │ Guarda token en localStorage
     ▼
┌──────────┐   GET /api/events/list/         ┌──────────┐
│ Frontend │  ─────────────────────────────>  │ Backend  │
│          │   Authorization: Bearer token    │          │
│          │                                  │ Verifica │
│          │  <─────────────────────────────  │ token    │
│          │     [ eventos... ]               │          │
└──────────┘                                  └──────────┘
```

---

## Paso 1: Configurar SimpleJWT

En `config/settings/base.py` ya tenemos configurado:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

| Token | Duracion | Para que sirve |
|-------|---------|----------------|
| Access | 4 horas | Acceder a endpoints protegidos |
| Refresh | 7 dias | Obtener un access token nuevo sin hacer login de nuevo |

---

## Paso 2: Probar el login

### 2.1 Registrar un usuario nuevo

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d "{\"email\": \"test@test.com\", \"username\": \"testuser\", \"password\": \"test1234\"}"
```

**Resultado esperado:**

```json
{
    "id": 2,
    "email": "test@test.com",
    "username": "testuser",
    "first_name": "",
    "last_name": ""
}
```

### 2.2 Hacer login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"test@test.com\", \"password\": \"test1234\"}"
```

**Resultado esperado:**

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": 2,
        "email": "test@test.com",
        "username": "testuser"
    }
}
```

**Copia el valor de `"access"`** - es tu token.

---

## Paso 3: Probar endpoints protegidos

### 3.1 Endpoint sin token (debe fallar)

```bash
curl http://127.0.0.1:8000/api/auth/me/
```

**Resultado:** `{"detail":"Authentication credentials were not provided."}`

### 3.2 Endpoint con token (debe funcionar)

Reemplaza `TU_TOKEN` con el token que copiaste:

```bash
curl -H "Authorization: Bearer TU_TOKEN" http://127.0.0.1:8000/api/auth/me/
```

**Resultado esperado:**

```json
{
    "id": 2,
    "email": "test@test.com",
    "username": "testuser",
    "first_name": "",
    "last_name": ""
}
```

---

## Paso 4: Entender como el frontend maneja JWT

### 4.1 Guardar el token (login.html)

Cuando el usuario hace login, el frontend:

```javascript
// 1. Enviar credenciales al backend
const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});

// 2. Obtener el token
const data = await response.json();

// 3. Guardar en localStorage
localStorage.setItem('token', data.access);
localStorage.setItem('user', JSON.stringify(data.user));

// 4. Redirigir al dashboard
window.location.href = 'index.html';
```

### 4.2 Usar el token (en cada peticion)

```javascript
// Obtener token del localStorage
const token = localStorage.getItem('token');

// Incluirlo en el header Authorization
const response = await fetch('http://127.0.0.1:8000/api/metrics/summary/', {
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    }
});
```

### 4.3 Cerrar sesion

```javascript
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
```

---

## Paso 5: Proteger paginas del frontend

Cada pagina que requiere login debe verificar que el usuario esta autenticado:

```javascript
// Al cargar la pagina
document.addEventListener('DOMContentLoaded', () => {
    if (!AUTH.isAuthenticated()) {
        window.location.href = 'login.html';
    }
    AUTH.updateNavbar();
});
```

---

## Paso 6: Manejar token expirado

Cuando el token expira, el backend devuelve `401 Unauthorized`. El frontend debe:

```javascript
async apiGet(endpoint) {
    const response = await fetch(`${this.API_URL}${endpoint}`, {
        headers: this.getHeaders()
    });

    if (response.status === 401) {
        // Token expirado o invalido
        this.logout();  // Borrar token
        window.location.href = 'login.html';  // Redirigir a login
        return;
    }

    return response.json();
}
```

---

## Paso 7: Probar el flujo completo

1. Abre http://localhost:8080/login.html
2. Ingresa `admin@insightboard.com` / `admin123`
3. Debes ser redirigido al dashboard
4. Verifica que ves el email del usuario en la barra de navegacion
5. Haz clic en "Salir"
6. Debes ser redirigido al login

---

## Diagrama de flujo completo

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACION                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. LOGIN                                                    │
│     ┌─────────┐  POST /api/auth/login/  ┌─────────┐        │
│     │ Browser │ ──────────────────────> │ Django  │        │
│     │         │  {email, password}      │         │        │
│     │         │ <────────────────────── │         │        │
│     │         │  {access, user}         │         │        │
│     └─────────┘                         └─────────┘        │
│          │                                                     │
│          │ 2. Guardar token                                   │
│          ▼                                                     │
│     localStorage.setItem('token', access)                     │
│          │                                                     │
│          │ 3. Peticion autenticada                            │
│          ▼                                                     │
│     ┌─────────┐  GET /api/events/list/  ┌─────────┐        │
│     │ Browser │ ──────────────────────> │ Django  │        │
│     │         │  Authorization: Bearer  │         │        │
│     │         │ <────────────────────── │         │        │
│     │         │  [events...]            │         │        │
│     └─────────┘                         └─────────┘        │
│                                                              │
│  4. TOKEN EXPIRA (401)                                       │
│     ┌─────────┐  GET /api/events/list/  ┌─────────┐        │
│     │ Browser │ ──────────────────────> │ Django  │        │
│     │         │  Authorization: Bearer  │         │        │
│     │         │ <────────────────────── │         │        │
│     │         │  401 Unauthorized       │         │        │
│     └─────────┘                         └─────────┘        │
│          │                                                     │
│          │ 5. Redirigir a login                                │
│          ▼                                                     │
│     window.location.href = 'login.html'                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Seguridad

### Buenas practicas

1. **Nunca guardes tokens en cookies** - Usa `localStorage` o `sessionStorage`
2. **Cierra sesion automaticamente** cuando el token expire
3. **No envies contrasenas en texto plano** - Siempre usa HTTPS en produccion
4. **Cierra sesion** cuando el usuario no este activo

### Que protege JWT

| Endpoint | Requiere JWT | Que pasa si no lo tienes |
|----------|-------------|-------------------------|
| `/api/auth/register/` | No | Cualquiera puede registrarse |
| `/api/auth/login/` | No | Cualquiera puede hacer login |
| `/api/auth/me/` | Si | Error 401 |
| `/api/events/list/` | Si | Error 401 |
| `/api/events/ingest/` | No | Cualquiera puede enviar eventos |
| `/api/metrics/summary/` | Si | Error 401 |
| `/api/reports/` | Si | Error 401 |

---

## Resumen del paso

| Paso | Que aprendimos | Verificacion |
|------|---------------|-------------|
| 1 | Configuracion JWT | `SIMPLE_JWT` en settings |
| 2 | Login con curl | Obtienes un token |
| 3 | Token en headers | Puedes acceder a endpoints protegidos |
| 4 | Frontend + JWT | `auth.js` maneja tokens |
| 5 | Proteger paginas | `requireAuth()` redirige a login |
| 6 | Token expirado | Se redirige automaticamente |
| 7 | Flujo completo | Login -> Dashboard -> Logout |

---

**¿La autenticacion funciona? Sigue con el [Capitulo 8: Probar y deploy](../c8/README.md)**
