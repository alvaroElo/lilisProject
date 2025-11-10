"""
Script para migrar permisos de roles al nuevo formato
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from autenticacion.models import Rol

def migrar_permisos():
    """
    Migrar roles con formato antiguo al nuevo formato de permisos
    """
    
    print('='*60)
    print('MIGRACIÓN DE PERMISOS DE ROLES')
    print('='*60)
    
    # Rol ADMIN - Acceso total a todo
    admin_rol = Rol.objects.get(nombre='ADMIN')
    admin_rol.permisos = {
        'usuarios': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'exportar': True},
        'proveedores': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'exportar': True},
        'productos': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'compras': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
        'inventario': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
    }
    admin_rol.save()
    print(f'✅ Rol ADMIN actualizado')
    
    # Rol VENDEDOR - Solo lectura de productos e inventario
    vendedor_rol = Rol.objects.get(nombre='VENDEDOR')
    vendedor_rol.permisos = {
        'usuarios': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'proveedores': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'productos': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
        'compras': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False},
        'inventario': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    }
    vendedor_rol.save()
    print(f'✅ Rol VENDEDOR actualizado')
    
    # Rol BODEGUERO - Inventario completo, productos lectura
    bodeguero_rol = Rol.objects.get(nombre='BODEGUERO')
    bodeguero_rol.permisos = {
        'usuarios': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'proveedores': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'productos': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
        'compras': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
        'inventario': {'ver': True, 'crear': True, 'editar': True, 'eliminar': False},
    }
    bodeguero_rol.save()
    print(f'✅ Rol BODEGUERO actualizado')
    
    # Rol JEFE_VENTAS - Ver productos e inventario, gestionar productos
    jefe_ventas_rol = Rol.objects.get(nombre='JEFE_VENTAS')
    jefe_ventas_rol.permisos = {
        'usuarios': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'proveedores': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': True},
        'productos': {'ver': True, 'crear': True, 'editar': True, 'eliminar': False},
        'compras': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
        'inventario': {'ver': True, 'crear': False, 'editar': False, 'eliminar': False},
    }
    jefe_ventas_rol.save()
    print(f'✅ Rol JEFE_VENTAS actualizado')
    
    print('\n' + '='*60)
    print('MIGRACIÓN COMPLETADA')
    print('='*60)
    print('Todos los roles han sido actualizados al nuevo formato:')
    print('  - usuarios: {ver, crear, editar, eliminar, exportar}')
    print('  - proveedores: {ver, crear, editar, eliminar, exportar}')
    print('  - productos: {ver, crear, editar, eliminar}')
    print('  - compras: {ver, crear, editar, eliminar}')
    print('  - inventario: {ver, crear, editar, eliminar}')
    print('='*60)

if __name__ == '__main__':
    migrar_permisos()
