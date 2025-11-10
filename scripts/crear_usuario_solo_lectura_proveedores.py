"""
Script para crear un usuario con acceso de solo lectura a proveedores
Dulcería Lilis - Sistema de Gestión

Uso:
    python scripts/crear_usuario_solo_lectura_proveedores.py
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

from django.contrib.auth.models import User
from autenticacion.models import Usuario, Rol

def crear_usuario_solo_lectura():
    """Crea un usuario con permisos de solo lectura para proveedores"""
    
    print("="*70)
    print("CREACIÓN DE USUARIO CON ACCESO DE SOLO LECTURA A PROVEEDORES")
    print("="*70)
    
    # Datos del usuario
    username = "consultor_proveedores"
    email = "consultor.proveedores@dulcerialilis.com"
    first_name = "Consultor"
    last_name = "Proveedores"
    password = "consultor123"  # Contraseña por defecto
    
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"\n✗ El usuario '{username}' ya existe.")
            print(f"  Si deseas recrearlo, primero debes eliminarlo manualmente.\n")
            return
        
        # Obtener o crear el rol FINANZAS (usaremos este para permisos limitados)
        try:
            rol = Rol.objects.get(nombre='FINANZAS')
            print(f"\n✓ Rol 'FINANZAS' encontrado")
        except Rol.DoesNotExist:
            print("\n  Creando rol 'FINANZAS'...")
            rol = Rol.objects.create(
                nombre='FINANZAS',
                descripcion='Personal de Finanzas - Acceso limitado',
                permisos={
                    'proveedores': {
                        'ver': True,
                        'crear': False,
                        'editar': False,
                        'eliminar': False,
                        'exportar': True
                    },
                    'compras': {
                        'ver': True,
                        'crear': False,
                        'editar': False,
                        'eliminar': False
                    },
                    'reportes': {
                        'ver': True,
                        'exportar': True
                    }
                }
            )
            print(f"✓ Rol 'FINANZAS' creado con permisos limitados")
        
        # Si el rol ya existe pero no tiene permisos definidos, actualizarlos
        if not rol.permisos:
            rol.permisos = {
                'proveedores': {
                    'ver': True,
                    'crear': False,
                    'editar': False,
                    'eliminar': False,
                    'exportar': True
                },
                'compras': {
                    'ver': True,
                    'crear': False,
                    'editar': False,
                    'eliminar': False
                },
                'reportes': {
                    'ver': True,
                    'exportar': True
                }
            }
            rol.save()
            print(f"✓ Permisos del rol 'FINANZAS' actualizados")
        
        # Crear el User de Django
        print(f"\n  Creando usuario '{username}'...")
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        print(f"✓ Usuario Django creado")
        
        # Crear el perfil Usuario
        usuario = Usuario.objects.create(
            user=user,
            rol=rol,
            estado='ACTIVO',
            telefono='+56 9 1234 5678',
            area_unidad='Finanzas',
            observaciones='Usuario de solo lectura para módulo de proveedores. Puede ver y exportar, pero no crear, editar o eliminar.'
        )
        print(f"✓ Perfil de usuario creado")
        
        # Resumen
        print("\n" + "="*70)
        print("✓ USUARIO CREADO EXITOSAMENTE")
        print("="*70)
        print(f"\n📋 INFORMACIÓN DE ACCESO:")
        print(f"   Usuario:      {username}")
        print(f"   Correo:       {email}")
        print(f"   Contraseña:   {password}")
        print(f"   Rol:          {rol.get_nombre_display()}")
        print(f"   Estado:       {usuario.get_estado_display()}")
        print(f"   Área:         {usuario.area_unidad}")
        
        print(f"\n🔒 PERMISOS ASIGNADOS:")
        print(f"   ✓ Ver proveedores")
        print(f"   ✓ Exportar a Excel")
        print(f"   ✗ Crear proveedores")
        print(f"   ✗ Editar proveedores")
        print(f"   ✗ Eliminar/Bloquear proveedores")
        
        print(f"\n💡 NOTA:")
        print(f"   Este usuario solo puede visualizar información y exportar datos.")
        print(f"   No puede realizar cambios en el sistema.")
        print(f"   Los botones de acción estarán deshabilitados en la interfaz.")
        
        print("\n✓ Proceso completado!\n")
        
    except Exception as e:
        print(f"\n✗ Error al crear el usuario: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        crear_usuario_solo_lectura()
    except KeyboardInterrupt:
        print("\n\n⊘ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error fatal: {str(e)}")
