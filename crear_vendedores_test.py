"""
Script para crear 100 usuarios vendedores de prueba
Dulcería Lilis - Sistema de Gestión

Uso:
    python crear_vendedores_test.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from django.contrib.auth.models import User
from autenticacion.models import Usuario, Rol

def crear_vendedores_test():
    """Crea 100 usuarios vendedores de prueba"""
    
    print("="*60)
    print("CREACIÓN DE USUARIOS VENDEDORES DE PRUEBA")
    print("="*60)
    
    # Obtener o crear el rol de vendedor
    try:
        rol_vendedor = Rol.objects.get(nombre='VENDEDOR')
        print(f"✓ Rol 'VENDEDOR' encontrado: {rol_vendedor}")
    except Rol.DoesNotExist:
        print("✗ El rol 'VENDEDOR' no existe. Creándolo...")
        rol_vendedor = Rol.objects.create(
            nombre='VENDEDOR',
            descripcion='Vendedor de la tienda'
        )
        print(f"✓ Rol 'VENDEDOR' creado: {rol_vendedor}")
    
    print("\nIniciando creación de usuarios...\n")
    
    usuarios_creados = 0
    usuarios_existentes = 0
    errores = 0
    
    for i in range(1, 101):
        try:
            # Generar datos del usuario
            username = f"vendedorTest{i}"
            email = f"vendedorTest{i}@dulcerialilis.com"
            first_name = "Vendedor"
            last_name = f"Test{i}"
            password = "vendedor123"  # Contraseña por defecto
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                print(f"⊘ Usuario {i}/100: {username} ya existe")
                usuarios_existentes += 1
                continue
            
            # Crear el User de Django
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # Crear el perfil Usuario
            usuario = Usuario.objects.create(
                user=user,
                rol=rol_vendedor,
                estado='ACTIVO',
                telefono=None,
                area_unidad='Ventas'
            )
            
            print(f"✓ Usuario {i}/100: {username} creado exitosamente")
            usuarios_creados += 1
            
        except Exception as e:
            print(f"✗ Error al crear usuario {i}: {str(e)}")
            errores += 1
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE CREACIÓN")
    print("="*60)
    print(f"✓ Usuarios creados:      {usuarios_creados}")
    print(f"⊘ Usuarios existentes:   {usuarios_existentes}")
    print(f"✗ Errores:               {errores}")
    print(f"  Total procesados:      {usuarios_creados + usuarios_existentes + errores}/100")
    print("="*60)
    
    if usuarios_creados > 0:
        print("\n📋 INFORMACIÓN DE ACCESO:")
        print(f"   Usuario: vendedorTest1 a vendedorTest100")
        print(f"   Correo:  vendedorTest[N]@dulcerialilis.com")
        print(f"   Contraseña: vendedor123")
        print(f"   Rol: Vendedor")
        print(f"   Estado: Activo")
    
    print("\n✓ Proceso completado!\n")

if __name__ == '__main__':
    try:
        crear_vendedores_test()
    except KeyboardInterrupt:
        print("\n\n⊘ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error fatal: {str(e)}")
