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
Remove-Item "autenticacion\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "maestros\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "inventario\migrations\0001_initial.py" -ErrorAction SilentlyContinue; Remove-Item "compras\migrations\0001_initial.py" -ErrorAction SilentlyContinue
```

### 4. Generar nuevas migraciones
```powershell
venv\Scripts\python.exe manage.py makemigrations
```

### 5. Aplicar migraciones
```powershell
venv\Scripts\python.exe manage.py migrate
```

### 6. Cargar datos de ejemplo
```powershell
venv\Scripts\python.exe scripts\cargar_datos.py
```

### 7. Iniciar servidor
```powershell
venv\Scripts\python.exe manage.py runserver
```

## Usuarios disponibles después del reset:
- `admin` / `admin123` (Administrador)
- `vendedor1` / `vendedor123` (Vendedor)
- `bodeguero1` / `bodega123` (Bodeguero)
- `finanzas1` / `finanzas123` (Finanzas)
- `jefe_ventas` / `jefe123` (Jefe Ventas)