# Sistema de Gestión Dulcería Lilis

Sistema de gestión de inventario desarrollado en Django para Dulcería Lilis, que incluye manejo de productos, proveedores, inventario y órdenes de compra.

## ⚡ Inicio Rápido

```bash
# 1. Clonar repositorio y navegar
git clone https://github.com/alvaroElo/lilisProject.git
cd LiliProject

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env  # Windows
# cp .env.example .env    # Mac/Linux
# Editar .env con tu configuración MySQL

# 5. Configurar MySQL y migrar
python manage.py migrate

# 6. Cargar datos de ejemplo
python cargar_datos.py

# 7. Ejecutar servidor
python manage.py runserver
```

## 📖 Documentación Completa

👉 **[Ver Guía de Instalación Paso a Paso](INSTALACION.md)**

## 🚀 Acceso al Sistema

- **URL**: http://127.0.0.1:8000/admin/
- **Usuario Admin**: `admin` / `admin123`

## 👥 Usuarios de Prueba

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| admin | admin123 | Administrador | Acceso completo |
| vendedor1 | vendedor123 | Vendedor | Ventas e inventario |
| bodeguero1 | bodega123 | Bodeguero | Gestión inventario |
| finanzas1 | finanzas123 | Finanzas | Compras y reportes |
| jefe_ventas | jefe123 | Jefe Ventas | Supervisión ventas |

## Características Principales

### 🔐 Sistema de Autenticación y Roles
- **Administrador**: Acceso completo al sistema
- **Vendedor**: Acceso a productos y maestros
- **Bodeguero**: Acceso a inventario y maestros
- **Finanzas**: Acceso a compras y maestros
- **Jefe de Ventas**: Acceso a productos, maestros y compras

### 📦 Módulos del Sistema

#### **Autenticación**
- Gestión de usuarios y roles
- Control de acceso basado en permisos
- Sesiones y tokens de recuperación

#### **Maestros**
- Productos con códigos SKU/EAN
- Categorías jerárquicas
- Marcas y proveedores
- Unidades de medida
- Relaciones productos-proveedores

#### **Inventario**
- Control de stock por bodega
- Movimientos de inventario
- Control por lotes y series
- Alertas de stock (bajo, sobre, vencimiento)
- Trazabilidad completa

#### **Compras**
- Órdenes de compra
- Seguimiento de recepciones
- Control de autorizaciones

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MySQL/MariaDB (opcional, se puede usar SQLite)
- Git

### Pasos de Instalación

1. **Clonar el repositorio** (si aplica)
```bash
git clone <repository-url>
cd LiliProject
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install django python-dotenv mysqlclient
```

5. **Configurar variables de entorno**
Editar archivo `.env`:
```env
DJANGO_SECRET_KEY=supersecret
DJANGO_DEBUG=True

# Para MySQL
DB_ENGINE=mysql
DB_NAME=dulceria_lilis
DB_USER=lili_user
DB_PASSWORD=lili_password123
DB_HOST=localhost
DB_PORT=3306

# Para SQLite (más simple para pruebas)
# DB_ENGINE=sqlite
# DB_NAME=db.sqlite3
```

6. **Configurar base de datos MySQL** (opcional)
```sql
CREATE DATABASE dulceria_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lili_user'@'localhost' IDENTIFIED BY 'lili_password123';
GRANT ALL PRIVILEGES ON dulceria_lilis.* TO 'lili_user'@'localhost';
FLUSH PRIVILEGES;
```

6. **Ejecutar migraciones**
```bash
python manage.py migrate
```

7. **Cargar datos de ejemplo** (recomendado)
```bash
python cargar_datos.py
```

Este script crea automáticamente:
- **Admin**: usuario: `admin`, contraseña: `admin123`
- **Vendedor**: usuario: `vendedor1`, contraseña: `vendedor123`
- Categorías, marcas, unidades de medida
- Proveedor y bodega de ejemplo
- Productos de muestra

8. **Iniciar servidor**
```bash
python manage.py runserver
```

## 🎯 Uso del Sistema

### Acceso al Admin
1. Ir a: `http://127.0.0.1:8000/admin/`
2. Ingresar credenciales:
   - **Administrador**: `admin` / `admin123`
   - **Vendedor**: `vendedor1` / `vendedor123`

### Funcionalidades del Admin

#### **Como Administrador (admin/admin123)**
- Acceso completo a todos los módulos
- Gestión de usuarios y roles
- Configuración del sistema
- Todas las operaciones CRUD

#### **Como Vendedor (vendedor1/vendedor123)**
- Solo acceso a Productos y Maestros
- No puede ver Inventario, Compras o Autenticación
- Demostración del control de acceso basado en roles

### Características Destacadas del Admin

#### **List Display y Filtros**
- Todas las vistas incluyen columnas relevantes
- Filtros por fechas, estados, categorías
- Búsqueda por campos clave

#### **Inline Formsets**
- **Productos**: Gestión de proveedores inline
- **Órdenes de Compra**: Detalles inline

#### **Acciones Personalizadas**
- **Productos**: Activar/Descontinuar en lote
- **Órdenes**: Enviar/Confirmar/Cancelar
- **Alertas**: Resolver en lote

#### **Validaciones Personalizadas**
- Cálculo automático de totales en órdenes
- Control de stock en movimientos
- Validación de fechas de vencimiento

## 📊 Estructura de la Base de Datos

### Principales Entidades
- **usuarios, roles**: Sistema de autenticación
- **productos, categorias, marcas**: Catálogo de productos
- **proveedores**: Maestro de proveedores
- **bodegas, lotes, stock_actual**: Control de inventario
- **movimientos_inventario**: Trazabilidad
- **ordenes_compra**: Proceso de compras
- **alertas_stock**: Sistema de alertas

## 🔧 Personalización

### Agregar Nuevos Roles
1. Editar `autenticacion/models.py` → `Rol.ROLES_CHOICES`
2. Actualizar `autenticacion/middleware.py` → `permisos_por_rol`
3. Ejecutar migraciones si es necesario

### Configurar Nuevas Validaciones
- Editar métodos `clean()` en modelos
- Agregar validaciones en formularios del admin

### Personalizar Dashboard
- Editar archivos `admin.py` de cada aplicación
- Configurar `list_display`, `list_filter`, `search_fields`

## 📋 Lista de Verificación de Requisitos

### ✅ Conexión BD
- [x] Settings.py configurado con .env
- [x] Migraciones aplicadas sin error

### ✅ Usuarios y Roles
- [x] Superusuario: admin/admin123
- [x] Usuario limitado: vendedor1/vendedor123
- [x] Control de acceso por middleware

### ✅ Admin Básico (4 maestras + 2 operativas)
- [x] **Maestras**: Producto, Categoria, Marca, Proveedor
- [x] **Operativas**: OrdenCompra, MovimientoInventario
- [x] list_display configurado
- [x] search_fields configurado
- [x] list_filter configurado
- [x] ordering configurado
- [x] list_select_related configurado

### ✅ Admin Pro
- [x] **Inline**: ProductoProveedor en Producto
- [x] **Inline**: OrdenCompraDetalle en OrdenCompra
- [x] **Acción personalizada**: Activar/descontinuar productos
- [x] **Validación**: Cálculo automático de totales

### ✅ Seguridad
- [x] Middleware de control de acceso por rol
- [x] Vendedor solo ve productos/maestros
- [x] Admin ve todo el sistema

## 🐛 Troubleshooting

### Error de conexión MySQL
```bash
# Verificar que MySQL esté corriendo
# Verificar credenciales en .env
# Usar SQLite temporalmente cambiando DB_ENGINE=sqlite
```

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problemas de permisos
```bash
# Verificar que el usuario tenga perfil de Usuario creado
# Verificar que el rol esté asignado correctamente
```

## 📞 Soporte

Para problemas técnicos:
1. Verificar logs del servidor de desarrollo
2. Revisar configuración de .env
3. Validar que las migraciones estén aplicadas
4. Comprobar que los usuarios tengan perfiles asociados

---

**Desarrollado para Dulcería Lilis** 
*Sistema de Gestión de Inventario v1.0*