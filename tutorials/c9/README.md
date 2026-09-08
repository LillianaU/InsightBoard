# C9 - Publicar en Render

> **Tiempo estimado:** 30 minutos
> **Dificultad:** ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a publicar InsightBoard en **Render** para que cualquier persona pueda acceder desde internet.

### Al final de este capitulo tendras:
- InsightBoard funcionando en la nube
- Base de datos PostgreSQL en Render
- Superusuario creado para trabajar
- URL publica para compartir

---

## ¿Que es Render?

Render es una plataforma de hosting para aplicaciones web. Es como un arrendatario que cuida tu servidor 24/7.

| Caracteristica | Descripcion |
|---------------|-------------|
| **Gratis** | Tier gratuito para empezar |
| **Automatico** | Detecta tu codigo y despliega solo |
| **PostgreSQL** | Base de datos gestionada |
| **HTTPS** | Certificado SSL incluido |
| **GitHub** | Se actualiza cuando subes codigo |

---

## Paso 1: Subir el codigo a GitHub

Si aun no has subido tu codigo:

1. Ve a **https://github.com** y crea una cuenta (si no tienes)
2. Crea un repositorio nuevo llamado `InsightBoard`
3. En tu terminal:

```bash
cd C:\Users\LILLYU\Documents\GitHub\InsightBoard
git init
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/TU-USUARIO/InsightBoard.git
git push -u origin main
```

---

## Paso 2: Crear cuenta en Render

1. Ve a **https://render.com**
2. Haz clic en **"Get Started for Free"**
3. Registrate con tu cuenta de GitHub
4. Autoriza a Render a acceder a tus repositorios

---

## Paso 3: Crear base de datos PostgreSQL

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configura:
   - **Name:** `insightboard-db`
   - **Database:** `insightboard`
   - **User:** `postgres`
   - **Plan:** Free
4. Haz clic en **"Create Database"**
5. Espera a que el estado diga **"Available"** (~1-2 minutos)

---

## Paso 4: Crear el servicio web

1. En el dashboard, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name:** `InsightBoard`
   - **Region:** Oregon (US West) o la mas cercana
   - **Runtime:** Docker
   - **Plan:** Free
5. En **"Dockerfile Path"** deja `./Dockerfile`
6. Haz clic en **"Create Web Service"**

---

## Paso 5: Configurar variables de entorno

1. Ve a tu servicio web creado
2. Haz clic en **"Environment"**
3. Agrega estas variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (copiala de tu PostgreSQL - paso 6) |
| `DJANGO_SECRET_KEY` | `insightboard-secret-key-2026-segura` |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `insightboard.onrender.com` |

---

## Paso 6: Copiar DATABASE_URL

1. Ve a tu servicio **PostgreSQL** (insightboard-db)
2. Haz clic en **"Info"**
3. Copia **"Internal Database URL"** o **"External Database URL"**
4. Pegalo como value de `DATABASE_URL` en tu servicio web

La URL se ve asi:
```
postgresql://postgres:abc123@insightboard-db.render.com:5432/insightboard
```

---

## Paso 7: Redesplegar

1. Ve a la pestaña **"Events"**
2. Haz clic en **"Manual Deploy" > "Clear build cache & deploy"**
3. Espera a que termine (~3-5 minutos)

---

## Paso 8: Crear superusuario

Una vez que el deploy termine, necesitas crear un superusuario para trabajar.

### Opcion 1: Usar la consola de Render

1. Ve a tu servicio web
2. Haz clic en **"Shell"** (menu izquierdo)
3. Ejecuta:

```bash
uv run python manage.py createsuperuser
```

4. Ingresa:
   - Email: `admin@insightboard.com`
   - Username: `admin`
   - Contrasena: `admin123`

### Opcion 2: Usar el endpoint de registro (desde tu PC)

Si no puedes acceder al Shell, ejecuta este comando en **tu terminal local**:

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "https://insightboard.onrender.com/api/auth/register/" -Method Post -ContentType "application/json" -Body '{"email":"admin@insightboard.com","username":"admin","password":"admin123"}'
```

**Mac/Linux:**
```bash
curl -X POST https://insightboard.onrender.com/api/auth/register/ -H "Content-Type: application/json" -d '{"email":"admin@insightboard.com","username":"admin","password":"admin123"}'
```

Si ves la respuesta con el email y username, el usuario se creo correctamente.

---

## Paso 9: Verificar que funciona

Abre el navegador en:

| URL | Que veras |
|-----|-----------|
| https://insightboard.onrender.com/ | Login |
| https://insightboard.onrender.com/index.html | Dashboard |
| https://insightboard.onrender.com/api/docs/ | Documentacion Swagger |
| https://insightboard.onrender.com/admin/ | Panel de administracion |

### Prueba completa

1. Ve a https://insightboard.onrender.com/
2. Ingresa con `admin@insightboard.com` / `admin123`
3. Debes ver el dashboard
4. Ve a Eventos y crea un evento de prueba
5. Ve a Reportes y genera un reporte

---

## Paso 10: Configurar auto-deploy

Para que Render se actualice automaticamente cuando subas codigo:

1. Ve a **"Settings"** de tu servicio web
2. En **"Build" > "Auto Deploy"** selecciona **"On Commit"**
3. Ahora cada vez que hagas `git push`, Render redesplegara

---

## Variables de entorno completas

| Key | Value | Descripcion |
|-----|-------|-------------|
| `DATABASE_URL` | `postgresql://...` | URL de PostgreSQL |
| `DJANGO_SECRET_KEY` | `tu-clave-secreta` | Clave de seguridad |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | Modo produccion |
| `DEBUG` | `False` | Sin errores detallados |
| `ALLOWED_HOSTS` | `insightboard.onrender.com` | Dominio permitido |
| `CORS_ALLOWED_ORIGINS` | `https://insightboard.onrender.com` | CORS permitido |

---

## Solucion de problemas

### "Application failed to respond"
- Verifica que `DATABASE_URL` esta configurado
- Revisa los logs en la pestaña "Logs"

### "Password validation failed"
- La contrasena debe tener 8+ caracteres
- Usa una contrasena fuerte para el superusuario

### "Page not found (404)"
- Accede a `/login.html` o `/index.html`
- La raiz `/` redirige al login

### "No se puede conectar a la base de datos"
- Verifica que PostgreSQL esta en estado "Available"
- Verifica que `DATABASE_URL` es correcta

---

## Resumen del paso

| Paso | Que hicimos | Verificacion |
|------|------------|-------------|
| 1 | Subir codigo a GitHub | Repositorio visible |
| 2 | Crear cuenta en Render | Dashboard accesible |
| 3 | Crear PostgreSQL | Estado "Available" |
| 4 | Crear Web Service | Servicio creado |
| 5 | Configurar variables | Todas las variables puestas |
| 6 | Copiar DATABASE_URL | URL correcta |
| 7 | Redesplegar | Deploy exitoso |
| 8 | Crear superusuario | Puedes hacer login |
| 9 | Verificar | Dashboard funciona |
| 10 | Auto-deploy | Se actualiza con git push |

---

**Felicidades, InsightBoard esta en la nube!**
