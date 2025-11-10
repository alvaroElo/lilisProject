# 📁 Scripts de Utilidad - Dulcería Lilis

Esta carpeta contiene scripts de utilidad para administración y mantenimiento del sistema.

---

## 📜 Scripts Disponibles

### 1. `cargar_datos.py`
**Propósito:** Cargar datos iniciales o de prueba en la base de datos

**Uso:**
```bash
python scripts/cargar_datos.py
```

**Descripción:**
- Carga datos de productos, categorías, marcas, etc.
- Útil para inicializar la BD o entornos de desarrollo

---

### 2. `drop_tables.py`
**Propósito:** Eliminar todas las tablas de la base de datos

**⚠️ PELIGRO:** Este script elimina TODOS los datos

**Uso:**
```bash
python scripts/drop_tables.py
```

**Descripción:**
- Elimina todas las tablas del sistema
- Usar solo para resetear la BD en desarrollo
- **NO usar en producción**

---

### 3. `crear_vendedores_test.py`
**Propósito:** Crear 100 usuarios vendedores de prueba

**Uso:**
```bash
python scripts/crear_vendedores_test.py
```

**Descripción:**
- Crea 100 usuarios: vendedorTest1 hasta vendedorTest100
- Email: vendedorTest[N]@dulcerialilis.com
- Contraseña: vendedor123
- Rol: VENDEDOR
- Estado: ACTIVO

**Credenciales:**
- **Usuario:** vendedorTest1 a vendedorTest100
- **Contraseña:** vendedor123

---

## 🚀 Cómo Crear un Nuevo Script

1. Crea un nuevo archivo `.py` en esta carpeta
2. Agrega la configuración de Django al inicio:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

# Aquí importas tus modelos
from autenticacion.models import Usuario

# Tu código aquí
```

3. Documéntalo en este README

---

## 📋 Buenas Prácticas

✅ **Siempre incluir:**
- Mensajes informativos de lo que está haciendo
- Confirmación antes de acciones destructivas
- Manejo de errores con try/except
- Resumen final de resultados

✅ **Nomenclatura:**
- Usar nombres descriptivos en español
- Formato: `accion_objetivo.py`
- Ejemplos: `crear_usuarios_test.py`, `limpiar_stock_antiguo.py`

❌ **Evitar:**
- Operaciones destructivas sin confirmación
- Scripts sin documentación
- Hard-coded de datos sensibles

---

## 📁 Estructura Recomendada

```
scripts/
├── README.md                      # Este archivo
├── cargar_datos.py               # Carga inicial de datos
├── drop_tables.py                # Limpieza de BD
├── crear_vendedores_test.py      # Usuarios de prueba
├── [futuro] backup_database.py   # Respaldo de BD
├── [futuro] generar_reportes.py  # Reportes automáticos
└── [futuro] migracion_datos.py   # Migración de datos
```

---

**Última actualización:** Noviembre 2025  
**Proyecto:** Dulcería Lilis - Sistema de Gestión
