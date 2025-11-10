# 🔄 RESET DATABASE

Pasos para eliminar todas las tablas y migrar de nuevo:

## ⚠️ ADVERTENCIA
Este proceso eliminará TODOS los datos de la base de datos permanentemente.

## Pasos:

### 1. Detener el servidor Django
```
Ctrl+C (si está corriendo)
```

### 2. Eliminar todas las tablas
```powershell
venv\Scripts\python.exe scripts\drop_tables.py
```

### 3. Eliminar archivos de migración
```powershell
Remove-Item "autenticacion\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "autenticacion\migrations\0002_usuario_foto_perfil.py" -ErrorAction SilentlyContinue; Remove-Item "maestros\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "inventario\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "compras\migrations\0001_initial.py" -ErrorAction SilentlyContinue
```

### 4. Generar nuevas migraciones
```powershell
python manage.py makemigrations
```

### 5. Aplicar migraciones
```powershell
python manage.py migrate
```

### 6. Cargar datos de ejemplo
```powershell
python scripts\cargar_datos.py
```

### 7. Crear carpeta media para fotos de perfil
```powershell
New-Item -ItemType Directory -Path "media\usuarios\fotos" -Force
```

### 8. (Opcional) Crear 100 usuarios vendedores de prueba
```powershell
python scripts\crear_vendedores_test.py
```

### 9. Iniciar servidor
```powershell
python manage.py runserver
```

## Usuarios disponibles después del reset:

### Usuarios principales:
- `admin` / `admin123` (Administrador)
- `vendedor1` / `vendedor123` (Vendedor)
- `bodeguero1` / `bodega123` (Bodeguero)
- `finanzas1` / `finanzas123` (Finanzas)
- `jefe_ventas` / `jefe123` (Jefe Ventas)

### Usuarios de prueba (si ejecutaste el paso 8):
- `vendedorTest1` a `vendedorTest100` / `vendedor123` (Vendedores)
- Email: `vendedorTest[N]@dulcerialilis.com`
- Todos con estado **Activo** y rol **Vendedor**