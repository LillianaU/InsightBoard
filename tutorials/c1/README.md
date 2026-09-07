# C1 - Instalar herramientas

> **Tiempo estimado:** 20 minutos  
> **Dificultad:** ⭐ ⭐

---

## ¿Que vamos a hacer?

Vamos a instalar en tu computadora las 4 herramientas que necesitamos para programar:

| Herramienta | Para que sirve | Analogia |
|------------|---------------|----------|
| **Python** | Lenguaje de programacion | El idioma de la computadora |
| **VS Code** | Editor de codigo | El cuaderno donde escribimos |
| **Git** | Control de versiones | El boton de guardar |
| **uv** | Gestor de paquetes | El instalador automatico |

---

## Paso 1: Instalar Python

1. Abre tu navegador ve a **https://www.python.org/downloads/**
2. Haz clic en el boton azul que dice **"Download Python 3.12.x"**
3. Ejecuta el archivo que se descargo
4. **MUY IMPORTANTE:** Marca la casilla **"Add Python to PATH"** (abajo en el instalador)
5. Haz clic en **"Install Now"**
6. Espera a que termine y haz clic en **"Close"**

### Verificar que funciono

Abre la **Terminal de Windows**:
- Presiona `Windows + R`
- Escribe `cmd`
- Presiona `Enter`

Escribe este comando y presiona Enter:

```bash
python --version
```

**Resultado esperado:** Debes ver algo como `Python 3.12.x`

> Si ves el numero de version, Python esta instalado correctamente. Si ves un error, vuelve a instalar y asegurate de marcar "Add to PATH".

---

## Paso 2: Instalar Visual Studio Code

1. Ve a **https://code.visualstudio.com/**
2. Haz clic en **"Download for Windows"**
3. Ejecuta el instalador
4. Sigue haciendo clic en "Siguiente" hasta terminar (deja las opciones por defecto)
5. Abre VS Code

### Verificar que funciono

Abre VS Code. Debes ver una pantalla como esta:

```
┌─────────────────────────────────────┐
│  Visual Studio Code                 │
│                                     │
│  [Boton azul: "Open Folder"]        │
│  [Archivos recientes]               │
└─────────────────────────────────────┘

Si ves esto, VS Code esta listo.
```

---

## Paso 3: Instalar Git

1. Ve a **https://git-scm.com/downloads/win**
2. Haz clic en la version para Windows
3. Ejecuta el instalador
4. Deja **TODAS** las opciones como vienen por defecto (siguiente, siguiente, siguiente...)
5. Haz clic en "Install" y espera

### Verificar que funciono

En la terminal escribe:

```bash
git --version
```

**Resultado esperado:** `git version 2.x.x`

---

## Paso 4: Instalar uv

`uv` es un instalador rapido de paquetes de Python. Reemplaza a `pip` y es mucho mas veloz.

En la terminal de Windows escribe:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Espera a que termine. Cuando veas el mensaje de exito, **cierra la terminal y vuelve a abrirla**.

### Verificar que funciono

Abre una **nueva** terminal y escribe:

```bash
uv --version
```

**Resultado esperado:** `uv 0.x.x` (cualquier numero de version sirve)

---

## Paso 5: Abrir el proyecto en VS Code

1. Abre **VS Code**
2. Ve a **File > Open Folder** (Archivo > Abrir carpeta)
3. Navega hasta la carpeta `InsightBoard`
4. Haz clic en **"Select Folder"**

Debes ver la estructura del proyecto en el panel izquierdo:

```
InsightBoard/
├── config/
├── apps/
├── frontend/
├── tutorials/
├── docker-compose.yml
├── manage.py
└── ...
```

---

## Paso 6: Probar la terminal

Practica con estos comandos basicos. Escribe cada uno y presiona Enter:

```bash
# Ver en que carpeta estas
cd

# Listar archivos
dir

# Ver la version de Python
python --version

# Ver la version de uv
uv --version
```

Si todos funcionan, ¡estas listo!

---

## Solucion de problemas

### "python no se reconoce como comando"
- Vuelve a instalar Python
- Marca **"Add Python to PATH"** en el instalador
- Cierra y vuelve a abrir la terminal

### "git no se reconoce como comando"
- Vuelve a instalar Git
- Cierra y vuelve a abrir la terminal

### "uv no se reconoce como comando"
- Cierra la terminal y vuelve a abrirla
- Si no funciona, ejecuta el instalador de uv de nuevo

---

## Resumen del paso

| Herramienta | Comando para verificar | Resultado esperado |
|------------|----------------------|-------------------|
| Python | `python --version` | `Python 3.12.x` |
| VS Code | Abrir la aplicacion | Se abre la ventana |
| Git | `git --version` | `git version 2.x.x` |
| uv | `uv --version` | `uv 0.x.x` |

---

**¿Todo funciono? Sigue con el [Capitulo 2: Docker y base de datos](../c2/README.md)**
