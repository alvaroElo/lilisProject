"""
Script para crear un usuario con permisos de ver y editar en proveedores y usuarios
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from django.contrib.auth.models import User
from autenticacion.models import Usuario, Rol

def crear_usuario_editor():
    """
    Crea un usuario con permisos de ver y editar en proveedores y usuarios
    """
    
    # Verificar si el usuario ya existe
    username = 'editor_general'
    if User.objects.filter(username=username).exists():
        print(f'⚠️  El usuario "{username}" ya existe')
        user = User.objects.get(username=username)
        usuario = user.usuario_profile
    else:
        # Crear usuario de Django
        user = User.objects.create_user(
            username=username,
            email='editor@dulcerialilis.cl',
            password='editor123',
            first_name='Editor',
            last_name='General'
        )
        print(f'✅ Usuario Django creado: {username}')
    
    # Crear o actualizar rol EDITOR con permisos específicos
    rol, created = Rol.objects.get_or_create(
        nombre='EDITOR',
        defaults={
            'descripcion': 'Rol con permisos de visualización y edición',
            'permisos': {
                'proveedores': {
                    'ver': True,
                    'crear': False,
                    'editar': True,
                    'eliminar': True,
                    'exportar': True
                },
                'usuarios': {
                    'ver': True,
                    'crear': False,
                    'editar': True,
                    'eliminar': True,
                    'exportar': True
                },
                'productos': {
                    'ver': False,
                    'crear': False,
                    'editar': False,
                    'eliminar': False
                },
                'compras': {
                    'ver': False,
                    'crear': False,
                    'editar': False,
                    'eliminar': False
                },
                'inventario': {
                    'ver': False,
                    'crear': False,
                    'editar': False,
                    'eliminar': False
                }
            }
        }
    )
    
    if not created:
        # Actualizar permisos si el rol ya existía
        rol.permisos = {
            'proveedores': {
                'ver': True,
                'crear': False,
                'editar': True,
                'eliminar': True,
                'exportar': True
            },
            'usuarios': {
                'ver': True,
                'crear': False,
                'editar': True,
                'eliminar': True,
                'exportar': True
            },
            'productos': {
                'ver': False,
                'crear': False,
                'editar': False,
                'eliminar': False
            },
            'compras': {
                'ver': False,
                'crear': False,
                'editar': False,
                'eliminar': False
            },
            'inventario': {
                'ver': False,
                'crear': False,
                'editar': False,
                'eliminar': False
            }
        }
        rol.save()
        print(f'🔄 Rol actualizado: {rol.nombre}')
    else:
        print(f'✅ Rol creado: {rol.nombre}')
    
    # Crear o actualizar perfil de usuario
    if not hasattr(user, 'usuario_profile'):
        usuario = Usuario.objects.create(
            user=user,
            rol=rol,
            telefono='+56 9 8765 4321',
            area_unidad='Administración',
            estado='ACTIVO'
        )
        print(f'✅ Perfil de usuario creado')
    else:
        usuario = user.usuario_profile
        usuario.rol = rol
        usuario.estado = 'ACTIVO'
        usuario.save()
        print(f'🔄 Perfil de usuario actualizado')
    
    print('\n' + '='*60)
    print('USUARIO CREADO EXITOSAMENTE')
    print('='*60)
    print(f'Username:  {username}')
    print(f'Password:  editor123')
    print(f'Email:     editor@dulcerialilis.cl')
    print(f'Rol:       {rol.nombre}')
    print('\nPERMISOS ASIGNADOS:')
    print('─' * 60)
    print('📋 PROVEEDORES:')
    print('   ✓ Ver: Sí')
    print('   ✓ Crear: No')
    print('   ✓ Editar: Sí')
    print('   ✓ Eliminar: Sí')
    print('   ✓ Exportar: Sí')
    print('\n👥 USUARIOS:')
    print('   ✓ Ver: Sí')
    print('   ✓ Crear: No')
    print('   ✓ Editar: Sí')
    print('   ✓ Eliminar: Sí')
    print('   ✓ Exportar: Sí')
    print('\n❌ PRODUCTOS: Sin acceso')
    print('❌ COMPRAS: Sin acceso')
    print('❌ INVENTARIO: Sin acceso')
    print('='*60)
    print('⚠️  IMPORTANTE: Recuerda cerrar sesión y volver a iniciar')
    print('   para que los permisos se apliquen correctamente.')
    print('='*60)

if __name__ == '__main__':
    crear_usuario_editor()
