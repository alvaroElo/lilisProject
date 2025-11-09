# 📚 Sistema de Plantillas - Dulcería Lilis

## 🎯 Estructura Simple (2 niveles)

```
base.html
  ↓
dashboard_base.html (Sidebar + Header)
  ↓
[cualquier módulo].html (Solo contenido)
```

---

## 📁 Plantillas Disponibles

### 1. `base.html`
- HTML básico
- Bootstrap 5 + CSS empresarial
- Font Awesome
- **NO usar directamente**

### 2. `dashboard_base.html`
- Extiende de `base.html`
- Sidebar con menú completo
- Header con notificaciones y perfil
- **NO usar directamente**

### 3. Tu módulo (ejemplo: `dashboard.html`)
- Extiende de `dashboard_base.html`
- Solo escribe tu contenido
- **Este es el que usas**

---

## 🚀 Crear un Nuevo Módulo

### 1. Crea el archivo HTML:

```django
{% extends 'dashboard_base.html' %}
{% load static %}

{% block title %}Mi Módulo - Dulcería Lilis{% endblock %}
{% block page_title %}Mi Módulo{% endblock %}

{% block content %}
<!-- Tu contenido aquí -->
<div class="card">
    <div class="card-body">
        <h2>Hola Mundo</h2>
    </div>
</div>
{% endblock %}
```

### 2. Crea la vista en Django:

```python
@login_required
def mi_modulo_view(request):
    return render(request, 'mi_modulo.html', {
        'active_menu': 'mi_modulo',  # Resalta en el menú
    })
```

### 3. Agrega la URL:

```python
path('mi-modulo/', mi_modulo_view, name='mi_modulo'),
```

---

## ✅ Ejemplos Incluidos

- **`dashboard.html`** - Dashboard principal
- **`productos_list.html`** - Lista con tabla y filtros
- **`productos_form.html`** - Formulario completo

---

## 🎨 Bootstrap 5 Disponible

### Grid
```html
<div class="row g-4">
    <div class="col-12 col-md-6 col-lg-4">
        Contenido
    </div>
</div>
```

### Cards
```html
<div class="card border-0 shadow-sm">
    <div class="card-header bg-gradient-primary text-white">
        Título
    </div>
    <div class="card-body">
        Contenido
    </div>
</div>
```

### Botones
```html
<button class="btn btn-primary">Primario</button>
<button class="btn btn-secondary">Secundario</button>
```

### Tablas
```html
<table class="table table-hover">
    <thead class="bg-gradient-primary text-white">
        <tr><th>Columna</th></tr>
    </thead>
    <tbody>
        <tr><td>Dato</td></tr>
    </tbody>
</table>
```

---

**Eso es todo!** 🎉 Simple y funcional.
