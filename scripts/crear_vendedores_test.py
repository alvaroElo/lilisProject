"""
Script para crear 100 usuarios vendedores de prueba (VERSIÓN OPTIMIZADA)
Dulcería Lilis - Sistema de Gestión

Uso:
    python scripts/crear_vendedores_test.py
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
from django.contrib.auth.hashers import make_password # Importante para bulk_create

def crear_vendedores_test():
    """Crea 100 usuarios vendedores de prueba usando bulk_create"""
    
    print("="*60)
    print("CREACIÓN DE USUARIOS VENDEDORES DE PRUEBA (MODO RÁPIDO)")
    print("="*60)
    
    # --- 1. OBTENER EL ROL (Solo 1 consulta) ---
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

    print("\nIniciando creación en lote...\n")

    usuarios_creados = 0
    usuarios_existentes = 0
    errores = 0

    # --- 2. VERIFICAR USUARIOS EXISTENTES (Solo 1 consulta) ---
    
    # Generamos todos los nombres de usuario que queremos crear
    usernames_a_crear = [f"vendedorTest{i}" for i in range(1, 101)]
    
    # Consultamos la BD UNA SOLA VEZ para ver cuáles ya existen
    existentes_qs = User.objects.filter(
        username__in=usernames_a_crear
    ).values_list('username', flat=True)
    
    # Usamos un 'set' para búsquedas súper rápidas en memoria
    usernames_existentes = set(existentes_qs)
    
    print(f"✓ Encontrados {len(usernames_existentes)} usuarios existentes en 1 consulta.")

    # --- 3. PREPARAR CREACIÓN EN LOTE (Todo en memoria) ---
    
    # Hasheamos la contraseña UNA VEZ, no 100 veces
    password_hasheada = make_password("vendedor123")
    
    lista_users_a_crear = []
    lista_usernames_nuevos = [] # Para el paso 4

    for i in range(1, 101):
        username = f"vendedorTest{i}"
        
        # Si el usuario ya existe (chequeo en memoria, rápido)
        if username in usernames_existentes:
            usuarios_existentes += 1
            continue
            
        # Preparamos el objeto User (todavía no se guarda)
        user = User(
            username=username,
            email=f"vendedorTest{i}@dulcerialilis.com",
            first_name="Vendedor",
            last_name=f"Test{i}",
            password=password_hasheada # Usamos la contraseña ya hasheada
        )
        lista_users_a_crear.append(user)
        lista_usernames_nuevos.append(username) # Guardamos el nombre
        
    # --- 4. CREAR USUARIOS (Solo 1 consulta INSERT) ---
    if lista_users_a_crear:
        try:
            # ¡Aquí ocurre la magia! Se crean todos los usuarios a la vez
            User.objects.bulk_create(lista_users_a_crear)
            print(f"✓ {len(lista_users_a_crear)} Users creados en 1 consulta.")
        except Exception as e:
            print(f"✗ Error fatal en bulk_create de User: {str(e)}")
            return # Salir si falla
    else:
        print("ℹ️ No hay usuarios nuevos para crear.")

    # --- 5. CREAR PERFILES (2 consultas: 1 SELECT, 1 INSERT) ---
    
    # Para crear los perfiles (Usuario), necesitamos los IDs de los Users
    # que acabamos de crear.
    
    # 1 SELECT para obtener un mapa de {username: id}
    users_creados_map = dict(
        User.objects.filter(
            username__in=lista_usernames_nuevos
        ).values_list('username', 'id')
    )
    
    lista_perfiles_a_crear = []
    for username in lista_usernames_nuevos:
        user_id = users_creados_map.get(username)
        if not user_id:
            print(f"✗ Error: No se encontró ID para {username} post-creación.")
            errores += 1
            continue
            
        # Preparamos el perfil, asignando el ID de usuario directamente
        perfil = Usuario(
            user_id=user_id,
            rol=rol_vendedor,
            estado='ACTIVO',
            telefono=None,
            area_unidad='Ventas'
        )
        lista_perfiles_a_crear.append(perfil)
        usuarios_creados += 1

    # 1 INSERT para crear todos los perfiles a la vez
    if lista_perfiles_a_crear:
        try:
            Usuario.objects.bulk_create(lista_perfiles_a_crear)
            print(f"✓ {len(lista_perfiles_a_crear)} Perfiles de Usuario creados en 1 consulta.")
        except Exception as e:
            print(f"✗ Error fatal en bulk_create de Usuario: {str(e)}")
            errores += len(lista_perfiles_a_crear) # Asumir que todos fallaron

    # --- 6. RESUMEN ---
    print("\n" + "="*60)
    print("RESUMEN DE CREACIÓN (MODO RÁPIDO)")
    print("="*60)
    print(f"✓ Usuarios creados:       {usuarios_creados}")
    print(f"⊘ Usuarios existentes:   {usuarios_existentes}")
    print(f"✗ Errores:                {errores}")
    print(f"  Total procesados:     {usuarios_creados + usuarios_existentes + errores}/100")
    print("="*60)
    
    if usuarios_creados > 0:
        print("\n📋 INFORMACIÓN DE ACCESO:")
        print(f"  Usuario: vendedorTest1 a vendedorTest100")
        print(f"  Correo:  vendedorTest[N]@dulcerialilis.com")
        print(f"  Contraseña: vendedor123")
        print(f"  Rol: Vendedor")
        print(f"  Estado: Activo")
    
    print("\n✓ Proceso completado!\n")

if __name__ == '__main__':
    try:
        crear_vendedores_test()
    except KeyboardInterrupt:
        print("\n\n⊘ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error fatal: {str(e)}")