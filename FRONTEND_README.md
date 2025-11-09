# 🎨 Frontend - Dulcería Lilis

## ✅ Implementación Completada

Se ha creado el frontend completo del sistema con las siguientes características:

### 📁 Estructura Creada

```
static/
├── css/
│   ├── base.css         # Estilos base y variables CSS empresariales
│   ├── login.css        # Estilos página de login
│   └── dashboard.css    # Estilos dashboard con sidebar
├── js/
│   ├── base.js          # Utilidades JavaScript globales
│   ├── login.js         # Validación formulario login
│   └── dashboard.js     # Interacciones sidebar, dropdowns
└── img/
    └── (coloca aquí el logo de la empresa)

templates/
├── base.html            # Template base con includes CSS/JS
├── login.html           # Página de inicio de sesión
└── dashboard.html       # Dashboard con sidebar y header
```

### 🎨 Sistema de Diseño

**Colores Empresariales Implementados:**
- **Rojo Principal (#D20A11)**: Header, botones primarios
- **Dorado (#c4a75b)**: Navegación, elementos secundarios
- **Café Oscuro (#230E00)**: Footer
- **Estados**: Verde (éxito), Rojo (error), Amarillo (advertencia)

### 🚀 Cómo Ejecutar

#### 1. Configurar Ejecución de Scripts (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Activar Entorno Virtual
```powershell
.\venv\Scripts\Activate.ps1
```

#### 3. Ejecutar Migraciones (si no lo has hecho)
```powershell
python manage.py migrate
```

#### 4. Cargar Datos de Prueba (si no lo has hecho)
```powershell
python cargar_datos.py
```

#### 5. Iniciar Servidor
```powershell
python manage.py runserver
```

#### 6. Acceder al Sistema
- **URL Login**: http://127.0.0.1:8000/
- **URL Dashboard**: http://127.0.0.1:8000/dashboard/
- **URL Admin Django**: http://127.0.0.1:8000/admin/

### 👤 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| vendedor1 | vendedor123 | Vendedor |
| bodeguero1 | bodega123 | Bodeguero |
| finanzas1 | finanzas123 | Finanzas |
| jefe_ventas | jefe123 | Jefe de Ventas |

### ✨ Funcionalidades Implementadas

#### Página de Login
- ✅ Diseño responsive
- ✅ Validación de formularios en cliente y servidor
- ✅ Mensajes de error/éxito con Django messages
- ✅ Opción "Recordarme"
- ✅ Redirección automática si ya está autenticado

#### Dashboard
- ✅ Sidebar colapsable con navegación
- ✅ Header con título de página
- ✅ Dropdown de notificaciones con contador
- ✅ Dropdown de usuario con avatar e info
- ✅ Cards con estadísticas (productos, alertas, órdenes, bodegas)
- ✅ Enlaces directos al admin de Django para cada módulo
- ✅ Cerrar sesión funcional

#### Características Técnicas
- ✅ CSS completamente separado (no inline)
- ✅ JavaScript modular y documentado
- ✅ Sistema de variables CSS para mantenibilidad
- ✅ Responsive design (móvil, tablet, desktop)
- ✅ Iconos Font Awesome integrados
- ✅ Animaciones suaves y transiciones
- ✅ Sistema de alertas y notificaciones

### 🎯 Navegación del Sistema

**Desde el Sidebar:**

**Gestión:**
- Productos → `/admin/maestros/producto/`
- Categorías → `/admin/maestros/categoria/`
- Marcas → `/admin/maestros/marca/`
- Proveedores → `/admin/maestros/proveedor/`

**Inventario:**
- Stock Actual → `/admin/inventario/stockactual/`
- Movimientos → `/admin/inventario/movimientoinventario/`
- Bodegas → `/admin/inventario/bodega/`
- Alertas → `/admin/inventario/alertastock/`

**Compras:**
- Órdenes de Compra → `/admin/compras/ordencompra/`

**Sistema:**
- Usuarios → `/admin/autenticacion/usuario/`
- Configuración → `/admin/`

### 📝 Próximos Pasos (Recomendados)

1. **Agregar Logo:**
   - Coloca el logo de la empresa en `static/img/logo.png`
   - Formato recomendado: PNG transparente, 200x200px

2. **Personalizar Notificaciones:**
   - Las notificaciones actuales son estáticas
   - Se pueden hacer dinámicas conectando con el modelo `AlertaStock`

3. **Crear Vistas Personalizadas:**
   - Actualmente el sidebar enlaza al admin de Django
   - Puedes crear vistas custom para cada módulo

4. **Implementar API REST:**
   - Instalar Django REST Framework
   - Crear endpoints para operaciones AJAX
   - Mejorar la experiencia sin recargar página

5. **Agregar Más Páginas:**
   - Listados personalizados de productos
   - Dashboard con gráficos (Chart.js)
   - Reportes y estadísticas avanzadas

### 🐛 Solución de Problemas

**Los estilos no se cargan:**
```powershell
python manage.py collectstatic
```

**Error 404 en archivos estáticos:**
- Verifica que `DEBUG = True` en `.env`
- Asegúrate que `STATIC_URL` esté configurado en `settings.py`

**No aparecen las notificaciones:**
- Las notificaciones son de ejemplo estático
- Conectar con base de datos para notificaciones reales

### 📚 Documentación de Referencia

- **Guía de Frontend**: `GUIA_FRONTEND.md`
- **Instalación**: `INSTALACION.md`
- **Reset Database**: `RESET_DATABASE.md`

---

**Desarrollado para Dulcería Lilis**
*Sistema de Gestión de Inventario - Frontend v1.0*
