#!/usr/bin/env python
"""Script para limpiar la tabla django_migrations"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from django.db import connection

def clean_migrations_table():
    """Limpia la tabla django_migrations"""
    print("Limpiando tabla django_migrations...")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        try:
            # Verificar si la tabla existe
            cursor.execute("SHOW TABLES LIKE 'django_migrations'")
            if cursor.fetchone():
                # Limpiar la tabla
                cursor.execute("DELETE FROM django_migrations")
                print("✓ Tabla django_migrations limpiada exitosamente")
            else:
                print("✓ Tabla django_migrations no existe (esto es normal en reset completo)")
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    if clean_migrations_table():
        print("\n✓ Proceso completado. Ahora puedes ejecutar 'python manage.py makemigrations'")
    else:
        print("\n✗ Hubo errores durante el proceso")
        sys.exit(1)
