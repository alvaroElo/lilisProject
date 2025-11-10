# Configuración de Base de Datos RDS en AWS

Esta guía te ayudará a configurar la base de datos MySQL en Amazon RDS para el proyecto Dulcería Lilis.

## 📋 Requisitos Previos

- Instancia RDS MySQL creada en AWS
- Acceso a la consola de AWS
- Cliente MySQL instalado en tu servidor o local
- Credenciales de administrador de RDS

## 🔐 1. Conexión Inicial a RDS

### Conectar como usuario administrador:

```bash
mysql \
  --ssl \
  --ssl-ca=/etc/ssl/certs/aws-rds/rds-combined-ca-bundle.pem \
  --ssl-verify-server-cert \
  -h dulceria-lilis.chf1shttozye.us-east-1.rds.amazonaws.com \
  -u admin \
  -p
```

**Nota:** Reemplaza el host con el endpoint de tu instancia RDS.

## 🗄️ 2. Crear Base de Datos y Usuario

Una vez conectado al servidor MySQL, ejecuta los siguientes comandos:

### Crear la base de datos:

```sql
CREATE DATABASE dulceria_lilis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Crear el usuario de la aplicación:

```sql
CREATE USER 'lilis_user'@'%' IDENTIFIED BY 'L1l1s_S3cur3_P4ssw0rd!';
```

### Requerir conexión SSL (seguridad):

```sql
ALTER USER 'lilis_user'@'%' REQUIRE SSL;
```

### Otorgar permisos completos sobre la base de datos:

```sql
GRANT ALL PRIVILEGES ON dulceria_lilis_db.* TO 'lilis_user'@'%';
```

### Aplicar los cambios:

```sql
FLUSH PRIVILEGES;
```

### Salir de MySQL:

```sql
EXIT;
```

## ✅ 3. Verificar la Creación

Reconecta usando el nuevo usuario para verificar:

```bash
mysql \
  --ssl \
  --ssl-ca=/etc/ssl/certs/aws-rds/rds-combined-ca-bundle.pem \
  --ssl-verify-server-cert \
  -h dulceria-lilis.chf1shttozye.us-east-1.rds.amazonaws.com \
  -u lilis_user \
  -p dulceria_lilis_db
```

Dentro de MySQL, verifica que puedes acceder:

```sql
SHOW DATABASES;
USE dulceria_lilis_db;
SHOW TABLES;
```

## 🔧 4. Configurar Variables de Entorno

Actualiza tu archivo `.env` con las nuevas credenciales:

```env
# Database Configuration
DB_ENGINE=mysql
DB_NAME=dulceria_lilis_db
DB_USER=lilis_user
DB_PASSWORD=L1l1s_S3cur3_P4ssw0rd!
DB_HOST=dulceria-lilis.chf1shttozye.us-east-1.rds.amazonaws.com
DB_PORT=3306
```

## 🚀 5. Ejecutar Migraciones de Django

Desde tu proyecto Django:

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## 🛡️ 6. Configuración de Security Groups en AWS

### Para que tu EC2 pueda conectarse a RDS:

1. Ve a **AWS Console → RDS → Databases → dulceria-lilis**
2. En la sección **Connectivity & Security**, anota el **Security Group**
3. Ve a **EC2 → Security Groups**
4. Selecciona el Security Group de RDS
5. En **Inbound Rules**, agrega:
   - **Type:** MySQL/Aurora
   - **Protocol:** TCP
   - **Port Range:** 3306
   - **Source:** Security Group de tu instancia EC2 (o su IP privada)

## 📝 Script Completo de Configuración

Para ejecutar todo de una vez, puedes crear un archivo SQL:

```bash
# Crear archivo de configuración
cat > setup_rds.sql << 'EOF'
CREATE DATABASE IF NOT EXISTS dulceria_lilis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'lilis_user'@'%' IDENTIFIED BY 'L1l1s_S3cur3_P4ssw0rd!';
ALTER USER 'lilis_user'@'%' REQUIRE SSL;
GRANT ALL PRIVILEGES ON dulceria_lilis_db.* TO 'lilis_user'@'%';
FLUSH PRIVILEGES;
SELECT User, Host, ssl_type FROM mysql.user WHERE User = 'lilis_user';
SHOW DATABASES;
EOF

# Ejecutar el script
mysql \
  --ssl \
  --ssl-ca=/etc/ssl/certs/aws-rds/rds-combined-ca-bundle.pem \
  --ssl-verify-server-cert \
  -h dulceria-lilis.chf1shttozye.us-east-1.rds.amazonaws.com \
  -u admin \
  -p < setup_rds.sql
```

## 🔍 Troubleshooting

### Error: "Can't connect to server (115)"

**Causa:** Problema de Security Group o red.

**Solución:**
- Verifica que el Security Group de RDS permite conexiones desde tu EC2
- Verifica que ambos están en la misma VPC
- Prueba conectividad: `telnet tu-rds-endpoint 3306`

### Error: "Access denied for user"

**Causa:** Credenciales incorrectas o permisos insuficientes.

**Solución:**
- Verifica el usuario y contraseña
- Asegúrate de que el usuario tenga permisos sobre la base de datos
- Ejecuta `FLUSH PRIVILEGES;`

### Error: "SSL connection error"

**Causa:** Certificado SSL no encontrado o inválido.

**Solución:**
```bash
# Descargar certificado de AWS RDS
sudo mkdir -p /etc/ssl/certs/aws-rds
cd /etc/ssl/certs/aws-rds
sudo wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
sudo mv global-bundle.pem rds-combined-ca-bundle.pem
```

## 📚 Recursos Adicionales

- [Documentación oficial de Amazon RDS](https://docs.aws.amazon.com/rds/)
- [Mejores prácticas de seguridad en RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.Security.html)
- [Configuración SSL para MySQL en RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)

## ⚠️ Notas de Seguridad

1. **NUNCA** uses credenciales de administrador (`admin`) en tu aplicación
2. **SIEMPRE** usa SSL para conexiones a RDS
3. **CAMBIA** la contraseña de ejemplo por una segura
4. **LIMITA** el acceso a RDS solo a IPs/Security Groups necesarios
5. **HABILITA** los backups automáticos en RDS
6. **MONITOREA** los logs de conexión en CloudWatch

---

**Proyecto:** Dulcería Lilis  
**Base de Datos:** MySQL 8.0 en Amazon RDS  
**Última actualización:** Noviembre 2025
