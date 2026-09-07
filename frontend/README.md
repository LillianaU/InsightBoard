# Frontend - InsightBoard

Interfaz web con Bootstrap para visualizar datos, registrar eventos y generar reportes.

## Páginas

| Archivo | Descripción |
|---------|-------------|
| `index.html` | Dashboard con estadísticas y gráficos |
| `events.html` | Formulario para registrar eventos y lista de eventos |
| `reports.html` | Crear reportes personalizados y ver reportes guardados |

## Estructura

```
frontend/
├── index.html
├── events.html
├── reports.html
├── css/
│   └── style.css
├── js/
│   └── app.js
├── images/
└── README.md
```

## Tecnologías

- **Bootstrap 5.3.2** - Framework CSS
- **Bootstrap Icons 1.11.1** - Iconos
- **Chart.js 4.4.1** - Gráficos
- **Vanilla JavaScript** - Lógica del frontend

## Cómo usarlo

Abre los archivos HTML directamente en tu navegador:

```bash
# Opción 1: Abrir directamente
start frontend/index.html

# Opción 2: Servir con Python
cd frontend
python -m http.server 8080
# Luego ve a http://localhost:8080
```

**Nota:** Para que funcione completamente, el backend debe estar corriendo en `http://127.0.0.1:8000`.

## Próximamente

- Integración completa con JWT (login)
- Exportación a PDF
- Filtros avanzados
- Modo oscuro
