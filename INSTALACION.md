# 🚀 Instalación Rápida - Sistema Dulcería Lilis

## Requisitos
- Python 3.8+
- MySQL 8.0+
- Git

## Comandos de Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/alvaroElo/lilisProject.git
cd LiliProject

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

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
# cp .env.example .env         # Mac/Linux
# Editar .env con tu configuración MySQL

# 6. Migrar base de datos
python manage.py makemigrations
python manage.py migrate

# 7. Cargar datos de ejemplo
python cargar_datos.py

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
python drop_tables.py
python manage.py makemigrations
python manage.py migrate
python cargar_datos.py

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