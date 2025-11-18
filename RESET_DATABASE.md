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
python scripts/drop_tables.py
```

### 3. Eliminar archivos de migración

#### Windows PowerShell:
```powershell
Get-ChildItem -Path "autenticacion\migrations","maestros\migrations","productos\migrations","inventario\migrations","compras\migrations" -Filter "*.py" -Exclude "__init__.py" | Remove-Item -Force
```

#### Linux/Mac:
```bash
find autenticacion maestros productos inventario compras -path "*/migrations/*.py" -not -name "__init__.py" -delete
```

#### Verificar que solo queden archivos __init__.py:
```powershell
Get-ChildItem -Path "autenticacion\migrations","maestros\migrations","productos\migrations","inventario\migrations","compras\migrations" -Filter "*.py" | Select-Object Name,DirectoryName
```



### 4. Generar nuevas migraciones
```powershell
python manage.py makemigrations
```

### 5. Aplicar migraciones
```powershell
python manage.py migrate
```
#### revisa la bd pas ADMIN.aws
mysql  --ssl  --ssl-ca=/etc/ssl/certs/aws-rds/rds-combined-ca-bundle.pem  --ssl-verify-server-cert  -h dulceria-lilis.chf1shttozye.us-east-1.rds.amazonaws.com  -u admin -p
###
USE dulceria_lilis_db;
###
SHOW TABLES;


# 1. Recarga systemd para que lea el archivo .service modificado
sudo systemctl daemon-reload

# 2. Reinicia Gunicorn (para que use el nuevo comando)
sudo systemctl restart lilisProject

# 3. Reinicia Nginx (para asegurar la conexión)
sudo systemctl restart nginx

### 6. Cargar datos de ejemplo
```powershell
python scripts\cargar_datos.py

python scripts/cargar_datos.py
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