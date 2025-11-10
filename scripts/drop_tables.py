#!/usr/bin/env python
"""
Script para eliminar todas las tablas de MySQL y hacer reset completo
"""
import os
import sys
import django

# Agregar el directorio raíz del proyecto al PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from django.db import connection

def main():
    print('ELIMINANDO TODAS LAS TABLAS DE MYSQL...')
    print('=' * 50)
    
    cursor = connection.cursor()
    
    # Desactivar verificación de claves foráneas
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    print('Verificacion de claves foraneas desactivada')
    
    # Obtener todas las tablas
    cursor.execute('SHOW TABLES')
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f'Encontradas {len(tables)} tablas para eliminar')
    
    # Eliminar todas las tablas
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS `{table}`')
        print(f'Tabla {table} eliminada')
    
    # Reactivar verificación de claves foráneas
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
    
    print(f'{len(tables)} tablas eliminadas exitosamente!')
    print('Base de datos limpia para migracion fresca')

if __name__ == '__main__':
    main()