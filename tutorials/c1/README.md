# C1 - ¡Bienvenido a tu taller de creación digital!

> **Edad recomendada:** 11 años en adelante  
> **Tiempo estimado:** 20 minutos  
> **Dificultad:** ⭐ ⭐

---

## ¿Qué vamos a construir?

Imagina que tienes una **caja mágica** donde puedes guardar información de todo lo que pasa en tu vida:
- Cuántos goles metiste jugando fútbol
- Cuántos libros leíste en un mes
- Cuántas veces comiste pizza en una semana

Con **InsightBoard**, esa caja mágica se convierte en gráficos, números y colores que te cuentan historias.

---

## ¿Qué necesitamos antes de empezar?

### 1. Una computadora con Windows
Vamos a usar:
- **Terminal** (una pantalla negra donde escribimos comandos)
- **Visual Studio Code** (nuestro taller de trabajo)
- **Git** (para guardar nuestros avances)

### 2. Instalar Python
Python es como el **lenguaje secreto** que entiende tu computadora para hacer cosas increíbles.

1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga la versión que diga **"Download Python 3.12"**
3. **IMPORTANTE:** Cuando se abra el instalador, marca la casilla que dice **"Add Python to PATH"** (esto es como darle a Python una llave para entrar a tu computadora)
4. Clic en **"Install Now"**
5. Espera a que termine y clic en **"Close"**

### 3. Instalar Visual Studio Code
Es como el **cuaderno de dibujo** de los programadores.

1. Ve a [code.visualstudio.com](https://code.visualstudio.com/)
2. Descarga la versión para Windows
3. Instala normalmente (siguiente, siguiente, siguiente...)
4. Abre VS Code

### 4. Instalar Git
Git es como el **botón de guardar** de un videojuego, pero para código.

1. Ve a [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
2. Descarga e instala
3. Deja todas las opciones como vienen por defecto

---

## ¿Qué es `uv`?

`uv` es una **herramienta mágica** que hace el trabajo pesado por nosotros:
- Instala programas rápido como un rayo ⚡
- Crea carpetas organizadas
- Se asegura de que todos los programas funcionen juntos sin pelear

### Instalar `uv`

Abre la **Terminal** de Windows (presiona `Windows + R`, escribe `cmd` y presiona Enter) y escribe:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Esto descarga e instala `uv` automáticamente. Cuando termine, cierra la terminal y vuelve a abrirla.

Para verificar que funcionó, escribe:

```bash
uv --version
```

Si ves algo como `uv 0.8.15`, ¡felicidades! 🎉

---

## Abriendo nuestro proyecto en VS Code

1. Abre VS Code
2. Ve a **File > Open Folder**
3. Busca la carpeta `InsightBoard` que está en `C:\Users\LILLYU\Documents\GitHub\InsightBoard`
4. Clic en **"Select Folder"**

Ahora deberías ver todos los archivos del proyecto en el panel izquierdo de VS Code.

---

## ¿Cómo funciona una terminal?

La terminal es como hablarle a tu computadora en **comandos secretos**. Aquí los más importantes:

| Comando | ¿Qué hace? | Analogía |
|---------|-----------|----------|
| `cd carpeta` | Entra a una carpeta | Como abrir una puerta |
| `dir` o `ls` | Muestra qué hay dentro | Como encender la luz |
| `uv run comando` | Ejecuta un comando | Como presionar play |
| `cls` | Limpia la pantalla | Como borrar el pizarrón |

**Tip:** Si te equivocas, no pasa nada. Puedes volver a escribir el comando.

---

## Tu primera prueba: crear una carpeta

Vamos a practicar creando una carpeta de prueba:

```bash
mkdir mi_carpeta_prueba
dir
```

Si ves `mi_carpeta_prueba` en la lista, ¡lo hiciste bien! 🎉

---

## ¿Qué sigue?

En el siguiente capítulo vamos a entender cómo organizar la información de InsightBoard usando **modelos de base de datos** como si fueran piezas de LEGO.

> **Ejercicio para casa:** Dibuja en un papel cómo organizarías tu colección de videojuegos, libros o juguetes. ¿Por categorías? ¿Por fecha? ¿Por color?

---

## Resumen del capítulo C1

✅ Instalamos Python  
✅ Instalamos VS Code  
✅ Instalamos Git  
✅ Instalamos `uv`  
✅ Aprendimos comandos básicos de terminal  
✅ Abrimos el proyecto en VS Code  

**¡Estás listo para el siguiente nivel!** 🚀
