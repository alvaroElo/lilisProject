"""
Script para crear 100 proveedores de prueba
Dulcería Lilis - Sistema de Gestión

Uso:
    python scripts/crear_proveedores_test.py
"""

import os
import sys
import django
from random import choice, randint

# Agregar el directorio raíz del proyecto al PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from maestros.models import Proveedor

# Datos de prueba para generar proveedores variados
RAZONES_SOCIALES = [
    "Distribuidora", "Comercial", "Importadora", "Exportadora", "Mayorista",
    "Industrias", "Productos", "Suministros", "Alimentos", "Confitería"
]

NOMBRES_FANTASIA = [
    "Dulces del Valle", "Golosinas Premium", "Sabor Latino", "Delicias Andinas",
    "Candy World", "Sweet Paradise", "Chocolates Finos", "Tentaciones",
    "La Esquina Dulce", "Sabores del Sur"
]

CIUDADES = [
    "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta",
    "Temuco", "Rancagua", "Talca", "Arica", "Iquique", "Puerto Montt",
    "Coquimbo", "Osorno", "Valdivia", "Punta Arenas"
]

CONDICIONES_PAGO = ['CONTADO', '30_DIAS', '60_DIAS', '90_DIAS', 'OTRO']

def crear_proveedores_test():
    """Crea 100 proveedores de prueba"""
    
    print("="*60)
    print("CREACIÓN DE PROVEEDORES DE PRUEBA")
    print("="*60)
    
    print("\nIniciando creación de proveedores...\n")
    
    proveedores_creados = 0
    proveedores_existentes = 0
    errores = 0
    
    for i in range(1, 101):
        try:
            # Generar datos del proveedor
            rut_base = 70000000 + (i * 1000)
            rut_nif = f"{rut_base:,}".replace(",", ".") + "-K"
            
            razon_social_tipo = choice(RAZONES_SOCIALES)
            razon_social = f"{razon_social_tipo} Test {i} S.A."
            nombre_fantasia = f"{choice(NOMBRES_FANTASIA)} {i}"
            
            email = f"proveedor{i}@test.com"
            telefono = f"+569 {randint(1000, 9999)} {randint(1000, 9999)}"
            sitio_web = f"https://www.proveedor{i}.cl"
            
            direccion = f"Av. Principal {randint(100, 9999)}, Oficina {randint(100, 999)}"
            ciudad = choice(CIUDADES)
            pais = "Chile"
            
            condiciones_pago = choice(CONDICIONES_PAGO)
            condiciones_pago_detalle = "Transferencia bancaria" if condiciones_pago == 'OTRO' else ""
            moneda = "CLP"
            
            # Contacto principal
            contacto_nombre = f"Juan Pérez {i}"
            contacto_telefono = f"+569 {randint(1000, 9999)} {randint(1000, 9999)}"
            contacto_email = f"contacto{i}@proveedor{i}.cl"
            
            # Estado aleatorio (90% activos, 10% bloqueados)
            estado = 'ACTIVO' if randint(1, 10) <= 9 else 'BLOQUEADO'
            
            observaciones = f"Proveedor de prueba número {i} - Generado automáticamente"
            
            # Verificar si el RUT ya existe
            if Proveedor.objects.filter(rut_nif=rut_nif).exists():
                print(f"⊘ Proveedor {i}/100: RUT {rut_nif} ya existe")
                proveedores_existentes += 1
                continue
            
            # Crear el proveedor
            proveedor = Proveedor.objects.create(
                rut_nif=rut_nif,
                razon_social=razon_social,
                nombre_fantasia=nombre_fantasia,
                email=email,
                telefono=telefono,
                sitio_web=sitio_web,
                direccion=direccion,
                ciudad=ciudad,
                pais=pais,
                condiciones_pago=condiciones_pago,
                condiciones_pago_detalle=condiciones_pago_detalle,
                moneda=moneda,
                contacto_principal_nombre=contacto_nombre,
                contacto_principal_telefono=contacto_telefono,
                contacto_principal_email=contacto_email,
                estado=estado,
                observaciones=observaciones
            )
            
            print(f"✓ Proveedor {i}/100: {razon_social} ({rut_nif}) creado - Estado: {estado}")
            proveedores_creados += 1
            
        except Exception as e:
            print(f"✗ Error al crear proveedor {i}: {str(e)}")
            errores += 1
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE CREACIÓN")
    print("="*60)
    print(f"✓ Proveedores creados:    {proveedores_creados}")
    print(f"⊘ Proveedores existentes: {proveedores_existentes}")
    print(f"✗ Errores:                {errores}")
    print(f"  Total procesados:       {proveedores_creados + proveedores_existentes + errores}/100")
    print("="*60)
    
    if proveedores_creados > 0:
        # Contar por estado
        total_activos = Proveedor.objects.filter(estado='ACTIVO').count()
        total_bloqueados = Proveedor.objects.filter(estado='BLOQUEADO').count()
        
        print("\n📊 ESTADÍSTICAS:")
        print(f"   Total proveedores:  {Proveedor.objects.count()}")
        print(f"   Activos:            {total_activos}")
        print(f"   Bloqueados:         {total_bloqueados}")
        
        # Contar por condiciones de pago
        print(f"\n💰 CONDICIONES DE PAGO:")
        for condicion, label in Proveedor.CONDICIONES_PAGO_CHOICES:
            count = Proveedor.objects.filter(condiciones_pago=condicion).count()
            print(f"   {label}: {count}")
    
    print("\n✓ Proceso completado!\n")

if __name__ == '__main__':
    try:
        crear_proveedores_test()
    except KeyboardInterrupt:
        print("\n\n⊘ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error fatal: {str(e)}")
