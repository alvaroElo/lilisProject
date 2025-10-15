# 🎨 Templates Frontend - Sistema Dulcería Lilis

## 📁 Estructura de Archivos

```
templates/
├── base.html                    # Template base con header, nav y footer
├── login.html                   # Módulo 1: Login
├── password_reset.html          # Módulo 2: Recuperar contraseña
├── password_reset_confirm.html  # Módulo 3: Nueva contraseña
├── dashboard.html               # Dashboard principal
├── usuarios_list.html           # Módulo 4: Lista de usuarios
├── usuario_form.html            # Módulo 4: Formulario usuario
├── productos_list.html          # Módulo 5: Lista de productos
├── producto_form.html           # Módulo 5: Formulario producto
├── proveedores_list.html        # Módulo 6: Lista de proveedores
└── inventario_list.html         # Módulo 7: Gestión inventario

static/
├── css/
│   └── styles.css              # Estilos principales
├── js/
│   └── main.js                 # JavaScript principal
└── img/
    ├── Logo-lilis-header.png   # Logo para header (PENDIENTE)
    ├── Logo-lilis-footer.png   # Logo para footer (PENDIENTE)
    └── Logo-lilis.png          # Logo principal (PENDIENTE)
```

## 🎨 Paleta de Colores

```css
--color-header: #D20A11        /* Rojo principal para header */
--color-footer: #230E00        /* Negro/marrón oscuro para footer */
--color-background: #ffffff    /* Fondo blanco */
--color-submenu: #c4a75b       /* Dorado para menú secundario */
--color-text-focus: #1b1919    /* Texto principal oscuro */
--color-text: #4e4e4e          /* Texto secundario gris */
--color-text2: #c4a75b         /* Texto dorado/destacado */
```

## 📋 Módulos Implementados

### ✅ Módulo 1: Login
- **Archivos**: `login.html`
- **Características**:
  - Diseño moderno con gradiente
  - Split screen (logo + formulario)
  - Campos: usuario/email, contraseña
  - Checkbox "Recordar sesión"
  - Link a recuperar contraseña

### ✅ Módulo 2: Recuperar Contraseña
- **Archivos**: `password_reset.html`
- **Características**:
  - Formulario centrado
  - Icono grande de llave
  - Campo de email
  - Link de regreso al login

### ✅ Módulo 3: Nueva Contraseña
- **Archivos**: `password_reset_confirm.html`
- **Características**:
  - Requisitos de seguridad visibles
  - Dos campos: nueva contraseña y confirmar
  - Validación visual

### ✅ Módulo 4: Usuarios (Maestro)
- **Archivos**: `usuarios_list.html`, `usuario_form.html`
- **Características**:
  - CRUD completo
  - Filtros: búsqueda, rol, estado
  - Tabla con información completa
  - Badges de estado y rol
  - Formulario con validación
  - Sección de permisos por rol

### ✅ Módulo 5: Productos (Maestro)
- **Archivos**: `productos_list.html`, `producto_form.html`
- **Características**:
  - Filtros: búsqueda, categoría, marca, estado
  - Tabla con SKU, nombre, precios, stock
  - Alertas visuales por stock bajo
  - Badge de vencimiento (mes/año)
  - Formulario con secciones:
    - Información básica
    - Precios y costos
    - Control de stock
    - Características especiales (perecedero, lote, serie)
  - Checkbox interactivo para fecha vencimiento

### ✅ Módulo 6: Proveedores (Maestro)
- **Archivos**: `proveedores_list.html`
- **Características**:
  - Filtros: búsqueda, estado, condiciones pago
  - Tabla con RUT, razón social, contacto
  - Badges de estado y condiciones de pago
  - Información de ciudad/país

### ✅ Módulo 7: Inventario Transaccional
- **Archivos**: `inventario_list.html`
- **Características**:
  - Sistema de tabs:
    1. **Movimientos**: Ingresos, salidas, ajustes, etc.
    2. **Stock Actual**: Por bodega y producto
    3. **Lotes**: Control de vencimientos
    4. **Alertas**: Bajo stock, vencimientos, etc.
  - Badges de tipo y estado
  - Alertas visuales por prioridad

### ✅ Dashboard
- **Archivos**: `dashboard.html`
- **Características**:
  - 4 tarjetas de estadísticas con iconos
  - Tabla de alertas recientes
  - Accesos rápidos (quick actions)
  - Cards interactivos con hover

## 🔧 Componentes Reutilizables

### Base Template (`base.html`)
- Header con logo, título, usuario y logout
- Navegación con menú responsive
- Footer con info de contacto
- Sistema de permisos integrado
- Estructura de contenido flexible

### CSS (`styles.css`)
- Variables CSS para colores
- Reset y estilos base
- Componentes:
  - Cards
  - Botones (primary, secondary, success, danger, warning, info)
  - Formularios (labels, inputs, selects, textareas)
  - Tablas
  - Badges
  - Navigation
  - Header/Footer
- Responsive design
- Utilidades (margins, display, align, gap)

### JavaScript (`main.js`)
- Inicialización de tooltips
- Confirmaciones de eliminación
- Filtros con botón limpiar
- Validación de formularios
- Sistema de notificaciones
- Helpers de formato (moneda, fechas)
- Funciones AJAX
- API global `window.LiliSystem`

## 📝 Notas de Implementación

### 🚧 Pendientes
1. **Imágenes de logos**: Los archivos `Logo-lilis-*.png` deben agregarse a `static/img/`
2. **URLs**: Las rutas en los templates usan `{% url %}` - deben configurarse en `urls.py`
3. **Context Data**: Las vistas deben pasar los datos necesarios (productos, usuarios, etc.)
4. **Permisos**: Sistema de permisos Django ya integrado en templates
5. **Paginación**: No implementada aún en las listas
6. **Exportación**: Botones de exportar sin funcionalidad backend

### ✅ Funcionalidades Visual
- Diseño responsive
- Paleta de colores aplicada
- Iconos FontAwesome
- Hover effects
- Badges de estado
- Filtros funcionales (estructura HTML)
- Tabs interactivos (JavaScript incluido)
- Validaciones de formulario básicas

## 🎯 Próximos Pasos

Para conectar estos templates al backend:

1. **Configurar URLs en `urls.py`**:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    # ... más rutas
]
```

2. **Crear Views en `views.py`**:
```python
from django.shortcuts import render
from .models import Usuario, Producto, etc

def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios_list.html', {'usuarios': usuarios})
```

3. **Configurar STATIC_URL y STATICFILES_DIRS en `settings.py`**:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

4. **Agregar las imágenes de logos** a `static/img/`

5. **Ejecutar collectstatic** (para producción):
```bash
python manage.py collectstatic
```

## 📱 Responsive
Los templates son responsive y se adaptan a:
- Desktop (> 1024px)
- Tablet (768px - 1024px)
- Mobile (< 768px)

## 🔐 Seguridad
- CSRF tokens incluidos en formularios
- Sistema de permisos Django integrado
- Logout seguro
- Validación de campos requeridos

---

**Versión**: 1.0  
**Fecha**: Octubre 2025  
**Estado**: ✅ Templates visuales completos - Pendiente integración backend
