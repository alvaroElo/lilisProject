# 🚀 Instrucciones para Ver los Templates

## ✅ Archivos Creados

Se han creado:
1. ✅ `LiliProject/test_views.py` - Vistas de prueba para todos los templates
2. ✅ `LiliProject/urls.py` - URLs actualizadas con todas las rutas

## 🎯 Cómo Ver los Templates

### Paso 1: Asegúrate de tener datos en la BD

Si ya ejecutaste `cargar_datos.py` antes, ¡perfecto! Si no, hazlo ahora:

```bash
python cargar_datos.py
```

Esto cargará:
- 5 usuarios (admin, vendedor1, bodeguero1, finanzas1, jefe_ventas)
- 10 productos
- 4 proveedores
- 8 categorías
- 10 marcas
- 3 bodegas
- Y más...

### Paso 2: Ejecuta el Servidor

```bash
python manage.py runserver
```

### Paso 3: Accede a los Templates

Abre tu navegador y visita las siguientes URLs:

#### 🔐 Autenticación (Sin Login Requerido)
- **Login**: http://127.0.0.1:8000/login/
- **Recuperar Contraseña**: http://127.0.0.1:8000/password-reset/
- **Nueva Contraseña**: http://127.0.0.1:8000/password-reset-confirm/

⚠️ **Nota**: Las páginas de login NO requieren autenticación, puedes verlas directamente.

#### 🏠 Dashboard y Módulos (Requieren Login)

Primero inicia sesión con:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

O cualquier otro usuario del sistema:
- `vendedor1` / `vendedor123`
- `bodeguero1` / `bodega123`
- `finanzas1` / `finanzas123`
- `jefe_ventas` / `jefe123`

Luego puedes visitar:

**Dashboard:**
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/dashboard/

**Usuarios:**
- Lista: http://127.0.0.1:8000/usuarios/
- Crear: http://127.0.0.1:8000/usuarios/crear/
- Editar: http://127.0.0.1:8000/usuarios/1/editar/

**Productos:**
- Lista: http://127.0.0.1:8000/productos/
- Crear: http://127.0.0.1:8000/productos/crear/
- Editar: http://127.0.0.1:8000/productos/1/editar/

**Proveedores:**
- Lista: http://127.0.0.1:8000/proveedores/

**Inventario:**
- Principal: http://127.0.0.1:8000/inventario/
  - Tab Movimientos
  - Tab Stock Actual
  - Tab Lotes
  - Tab Alertas

## 🎨 Lo Que Verás

### ✅ Funcionando:
- ✅ **Diseño completo** con colores de la empresa
- ✅ **Header** con logo placeholder, usuario y logout
- ✅ **Navegación** con menú funcional
- ✅ **Footer** corporativo
- ✅ **Listas** con datos reales de la BD
- ✅ **Filtros** (estructura visual, backend parcial)
- ✅ **Formularios** con todos los campos
- ✅ **Badges** de estado (Activo, Inactivo, etc.)
- ✅ **Tabs** en inventario (navegación JavaScript)
- ✅ **Responsive** design

### ⚠️ Aún No Funciona (Backend Pendiente):
- ⚠️ Crear/Editar usuarios (formularios no guardan)
- ⚠️ Crear/Editar productos (formularios no guardan)
- ⚠️ Filtros de búsqueda (algunos sí, otros no)
- ⚠️ Paginación
- ⚠️ Exportar a Excel
- ⚠️ Botones de eliminar
- ⚠️ Recuperación real de contraseña

## 📊 Datos de Prueba

Los templates mostrarán datos reales de tu base de datos:

| Modelo | Registros | Descripción |
|--------|-----------|-------------|
| Usuarios | 5 | admin, vendedor1, bodeguero1, finanzas1, jefe_ventas |
| Productos | 10 | Chocolates, dulces, galletas, chicles |
| Proveedores | 4 | Distribuidoras activas |
| Categorías | 8 | Dulces, Chocolates, Galletas, etc. |
| Marcas | 10 | Nestlé, Ferrero, Haribo, etc. |
| Bodegas | 3 | Principal, Refrigerada, Cuarentena |

## 🔧 Troubleshooting

### Error: "Template does not exist"
```bash
# Verifica que settings.py tenga:
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    }
]
```

### Error: "Static files not loading"
```bash
# Verifica que settings.py tenga:
STATICFILES_DIRS = [BASE_DIR / 'static']

# Y ejecuta:
python manage.py collectstatic --noinput
```

### Error: "Page not found (404)"
Asegúrate de que las URLs coincidan con las que están en `LiliProject/urls.py`

### No veo los logos
Los logos son placeholders SVG temporales. Para usar logos reales:
1. Coloca tus archivos PNG en `static/img/`
2. Nómbralos:
   - `Logo-lilis-header.png`
   - `Logo-lilis-footer.png`
   - `Logo-lilis.png`

### No puedo iniciar sesión
Los templates de login solo son visuales. Para login real:
1. Ve al admin de Django: http://127.0.0.1:8000/admin/
2. Inicia sesión con `admin` / `admin123`
3. Regresa a http://127.0.0.1:8000/

## 🎯 Próximos Pasos

Una vez que hayas visto los templates:

### 1. Implementar Autenticación Real
```python
# En autenticacion/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'login.html')
```

### 2. Implementar Formularios de Guardado
```python
# En maestros/views.py
from django.shortcuts import render, redirect
from .models import Producto

def producto_create(request):
    if request.method == 'POST':
        # Procesar formulario
        producto = Producto.objects.create(
            sku=request.POST.get('sku'),
            nombre=request.POST.get('nombre'),
            # ... más campos
        )
        return redirect('productos_list')
    
    # GET: mostrar formulario
    context = {
        'categorias': Categoria.objects.filter(activo=True),
        'marcas': Marca.objects.filter(activo=True),
    }
    return render(request, 'producto_form.html', context)
```

### 3. Implementar Filtros Completos
```python
def productos_list(request):
    productos = Producto.objects.all()
    
    # Filtro por búsqueda
    search = request.GET.get('search')
    if search:
        productos = productos.filter(
            Q(sku__icontains=search) | 
            Q(nombre__icontains=search)
        )
    
    # Filtro por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    
    context = {'productos': productos}
    return render(request, 'productos_list.html', context)
```

## 📞 Ayuda

Si tienes problemas:
1. Revisa que el servidor esté corriendo
2. Verifica que tengas datos en la BD (`cargar_datos.py`)
3. Comprueba que el usuario tenga permisos
4. Revisa la consola del navegador (F12) para errores JavaScript
5. Revisa la terminal de Python para errores Django

## 🎉 ¡Disfruta los Templates!

Todo el diseño visual está listo. Solo falta conectar la lógica de negocio.

**Creado**: Octubre 2025  
**Versión**: 1.0  
**Estado**: ✅ Templates visuales funcionando
