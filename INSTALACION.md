# 🚀 Instalación Rápida - Sistema Dulcería Lilis

## Requisitos
- Python 3.8+
- MySQL 8.0+
- Git

## ⚠️ Problema Común en Windows (VS Code)
Si al activar el entorno virtual obtienes un error de PowerShell:
```powershell
# Solución rápida - Ejecutar en terminal como administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Comandos de Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/alvaroElo/lilisProject.git
cd LiliProject

# 2. Entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows VS Code PowerShell
# venv\Scripts\activate.bat        # Windows CMD
# source venv/bin/activate         # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar MySQL
mysql -u root -p
```
```sql
CREATE DATABASE dulceria_lilis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lili_user'@'localhost' IDENTIFIED BY 'lili_password123';
GRANT ALL PRIVILEGES ON dulceria_lilis.* TO 'lili_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# 5. Variables de entorno
copy .env.example .env         # Windows
# cp .env.production.example .env
# cp .env.example .env         # Mac/Linux
# Editar .env con tu configuración MySQL

# 6. Migrar base de datos
python manage.py makemigrations
python manage.py migrate

# 7. Cargar datos de ejemplo
python scripts/cargar_datos.py
python scripts/crear_proveedores_test.py
python scripts/crear_vendedores_test.py
python scripts/crear_usuario_solo_lectura_proveedores.py
python scripts/crear_usuario_editor.py
python scripts/migrar_permisos_roles.py

# 8. Ejecutar servidor
python manage.py runserver
```

## Acceso al Sistema
- **URL**: http://127.0.0.1:8000/admin/
- **Usuario**: `admin` / `admin123`

## Usuarios de Prueba
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| vendedor1 | vendedor123 | Vendedor |
| bodeguero1 | bodega123 | Bodeguero |
| finanzas1 | finanzas123 | Finanzas |
| jefe_ventas | jefe123 | Jefe Ventas |

## Comandos Útiles

```bash
# Reiniciar base de datos completa
python scripts/drop_tables.py
python manage.py makemigrations
python manage.py migrate
python scripts/cargar_datos.py

# Crear superusuario
python manage.py createsuperuser

# Si hay problemas con makemigrations
python manage.py makemigrations autenticacion
python manage.py makemigrations maestros
python manage.py makemigrations inventario
python manage.py makemigrations compras
```

## ⚠️ Solución de Problemas

**Error en makemigrations:**
```bash
# Si falla makemigrations, ejecutar por aplicación:
python manage.py makemigrations autenticacion
python manage.py makemigrations maestros  
python manage.py makemigrations inventario
python manage.py makemigrations compras
python manage.py migrate
```