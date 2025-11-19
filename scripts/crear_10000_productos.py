"""
Script para crear 10,000 productos de prueba en la base de datos
Dulcería Lilis - Sistema de Gestión de Inventario
"""

import os
import sys
import django
from decimal import Decimal
from random import randint, choice, uniform
from django.utils import timezone

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SECRET_KEY', 'unsafe-dev-key')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from productos.models import Producto
from maestros.models import Categoria, Marca, UnidadMedida


def crear_datos_base():
    """Crear categorías, marcas y unidades de medida necesarias"""
    
    print("📦 Creando datos base (categorías, marcas, unidades)...")
    
    # Categorías para dulcería
    categorias = [
        ('Chocolates', 'Productos de chocolate y derivados'),
        ('Caramelos', 'Caramelos y gomitas'),
        ('Galletas', 'Galletas y obleas'),
        ('Chicles', 'Chicles y mentas'),
        ('Snacks Salados', 'Papas fritas, nachos, etc'),
        ('Bebidas', 'Bebidas y refrescos'),
        ('Dulces Regionales', 'Dulces típicos chilenos'),
        ('Bombones', 'Bombones finos y rellenos'),
        ('Confitería', 'Confites y pastillas'),
        ('Repostería', 'Insumos para repostería'),
    ]
    
    categorias_obj = []
    for nombre, descripcion in categorias:
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
        categorias_obj.append(cat)
        if created:
            print(f"  ✓ Categoría creada: {nombre}")
    
    # Marcas
    marcas_nombres = [
        'Nestlé', 'Costa', 'Ambrosoli', 'Arcor', 'Ferrero', 
        'Mondelez', 'Hershey\'s', 'Cadbury', 'Trident', 'Halls',
        'Lays', 'Doritos', 'Cheetos', 'Pringles', 'Coca-Cola',
        'Pepsi', 'Fanta', 'Sprite', 'Calaf', 'Sahne-Nuss',
        'Bon o Bon', 'Milka', 'Toblerone', 'Kit Kat', 'Snickers',
        'M&M\'s', 'Twix', 'Mars', 'Bounty', 'Milky Way',
        'Rolo', 'Smarties', 'Kinder', 'Raffaello', 'Ferrero Rocher',
        'Tofi', 'Super 8', 'Negrita', 'Triton', 'Mamut',
    ]
    
    marcas_obj = []
    for nombre in marcas_nombres:
        marca, created = Marca.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Marca {nombre}'}
        )
        marcas_obj.append(marca)
        if created:
            print(f"  ✓ Marca creada: {nombre}")
    
    # Unidades de medida
    unidades = [
        ('UND', 'Unidad', 'UNIDAD', Decimal('1')),
        ('KG', 'Kilogramo', 'PESO', Decimal('1')),
        ('GR', 'Gramo', 'PESO', Decimal('0.001')),
        ('L', 'Litro', 'VOLUMEN', Decimal('1')),
        ('ML', 'Mililitro', 'VOLUMEN', Decimal('0.001')),
        ('CAJA', 'Caja', 'UNIDAD', Decimal('1')),
        ('PAQUETE', 'Paquete', 'UNIDAD', Decimal('1')),
    ]
    
    unidades_obj = []
    for codigo, nombre, tipo, factor in unidades:
        uom, created = UnidadMedida.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'tipo': tipo,
                'factor_base': factor
            }
        )
        unidades_obj.append(uom)
        if created:
            print(f"  ✓ Unidad creada: {codigo}")
    
    return categorias_obj, marcas_obj, unidades_obj


def generar_nombre_producto(indice, categoria, marca):
    """Generar nombre de producto basado en categoría y marca"""
    
    # Prefijos según categoría
    prefijos = {
        'Chocolates': ['Chocolate', 'Barra', 'Tableta'],
        'Caramelos': ['Caramelo', 'Gomita', 'Dulce'],
        'Galletas': ['Galleta', 'Oblea', 'Wafer'],
        'Chicles': ['Chicle', 'Menta', 'Goma'],
        'Snacks Salados': ['Papas', 'Nachos', 'Snack'],
        'Bebidas': ['Bebida', 'Refresco', 'Jugo'],
        'Dulces Regionales': ['Dulce', 'Manjar', 'Chilenito'],
        'Bombones': ['Bombón', 'Trufa', 'Praline'],
        'Confitería': ['Confite', 'Pastilla', 'Mentita'],
        'Repostería': ['Insumo', 'Esencia', 'Colorante'],
    }
    
    # Sabores/variantes
    variantes = [
        'Clásico', 'Light', 'Sin Azúcar', 'Extra', 'Premium',
        'Menta', 'Frutilla', 'Limón', 'Naranja', 'Chocolate',
        'Vainilla', 'Coco', 'Leche', 'Amargo', 'Blanco',
        'Relleno', 'Crocante', 'Suave', 'Especial', 'Original'
    ]
    
    # Tamaños
    tamanos = ['Mini', 'Regular', 'Grande', 'Familiar', 'Individual', 'XL']
    
    prefijo = choice(prefijos.get(categoria.nombre, ['Producto']))
    variante = choice(variantes)
    tamano = choice(tamanos)
    
    return f"{marca.nombre} {prefijo} {variante} {tamano} {indice}"


def crear_productos_masivos(cantidad=10000):
    """Crear productos de forma masiva"""
    
    print(f"\n🎯 Iniciando creación de {cantidad:,} productos...\n")
    
    # Obtener datos base
    categorias, marcas, unidades = crear_datos_base()
    
    # Verificar que tenemos unidades necesarias
    und_unidad = next((u for u in unidades if u.codigo == 'UND'), unidades[0])
    und_gramo = next((u for u in unidades if u.codigo == 'GR'), und_unidad)
    
    # Lista para bulk create
    productos = []
    skus_existentes = set(Producto.objects.values_list('sku', flat=True))
    
    print("🏭 Generando productos...")
    
    # Contador de SKU para evitar duplicados
    sku_counter = 1000000
    
    for i in range(1, cantidad + 1):
        # Seleccionar categoría y marca aleatoria
        categoria = choice(categorias)
        marca = choice(marcas)
        
        # Generar SKU único
        while True:
            sku = f"PRD{sku_counter:08d}"
            if sku not in skus_existentes:
                skus_existentes.add(sku)
                break
            sku_counter += 1
        
        sku_counter += 1
        
        # Generar código de barras (EAN-13 simulado)
        ean = f"773{randint(1000000000, 9999999999)}" if randint(0, 100) > 30 else None
        
        # Generar nombre
        nombre = generar_nombre_producto(i, categoria, marca)
        
        # Precios aleatorios
        costo = Decimal(str(round(uniform(100, 5000), 2)))
        precio_venta = costo * Decimal(str(round(uniform(1.2, 2.5), 2)))  # Margen 20-150%
        
        # Stock aleatorio
        stock_actual = Decimal(str(randint(0, 500)))
        stock_minimo = Decimal(str(randint(5, 50)))
        stock_maximo = stock_minimo * Decimal(str(randint(3, 10)))
        
        # Determinar si es perecible (30% probabilidad)
        perecible = categoria.nombre in ['Chocolates', 'Galletas', 'Repostería'] and randint(0, 100) < 30
        
        # Crear producto
        producto = Producto(
            sku=sku,
            ean_upc=ean,
            nombre=nombre,
            descripcion=f"Descripción del producto {nombre}",
            categoria=categoria,
            marca=marca if randint(0, 100) > 10 else None,  # 90% con marca
            modelo=f"MOD-{randint(100, 999)}" if randint(0, 100) > 50 else None,
            uom_compra=und_gramo if categoria.nombre in ['Chocolates', 'Galletas'] else und_unidad,
            uom_venta=und_unidad,
            factor_conversion=Decimal('1'),
            costo_estandar=costo,
            costo_promedio=costo * Decimal(str(round(uniform(0.95, 1.05), 2))),
            precio_venta=precio_venta,
            impuesto_iva=Decimal('19'),
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            punto_reorden=stock_minimo * Decimal('1.5'),
            perecible=perecible,
            control_por_lote=perecible,
            control_por_serie=False,
            estado=choice(['ACTIVO', 'ACTIVO', 'ACTIVO', 'INACTIVO']),  # 75% activos
            alerta_bajo_stock=stock_actual < stock_minimo,
        )
        
        productos.append(producto)
        
        # Mostrar progreso cada 500 productos
        if i % 500 == 0:
            print(f"  📊 Progreso: {i:,} / {cantidad:,} productos generados ({(i/cantidad)*100:.1f}%)")
    
    print(f"\n💾 Guardando {len(productos):,} productos en la base de datos...")
    print("⏳ Esto puede tomar varios minutos...")
    
    # Bulk create en lotes de 1000 para evitar problemas de memoria
    batch_size = 1000
    total_creados = 0
    
    for i in range(0, len(productos), batch_size):
        batch = productos[i:i + batch_size]
        Producto.objects.bulk_create(batch, batch_size=batch_size)
        total_creados += len(batch)
        print(f"  ✓ Lote guardado: {total_creados:,} / {len(productos):,} productos")
    
    print(f"\n✅ ¡Proceso completado!")
    print(f"✨ Se crearon {total_creados:,} productos exitosamente")
    
    # Estadísticas finales
    print("\n📈 Estadísticas:")
    print(f"  • Total productos: {Producto.objects.count():,}")
    print(f"  • Productos activos: {Producto.objects.filter(estado='ACTIVO').count():,}")
    print(f"  • Productos con alerta: {Producto.objects.filter(alerta_bajo_stock=True).count():,}")
    print(f"  • Productos perecibles: {Producto.objects.filter(perecible=True).count():,}")
    
    # Por categoría
    print("\n📦 Productos por categoría:")
    for cat in categorias:
        count = Producto.objects.filter(categoria=cat).count()
        print(f"  • {cat.nombre}: {count:,}")


def main():
    """Función principal"""
    print("=" * 70)
    print("🍬 DULCERÍA LILIS - GENERADOR DE PRODUCTOS MASIVOS")
    print("=" * 70)
    print()
    
    try:
        respuesta = input("⚠️  ¿Desea crear 10,000 productos de prueba? (s/n): ")
        
        if respuesta.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        cantidad = input("\n📝 ¿Cuántos productos desea crear? (por defecto 10000): ").strip()
        cantidad = int(cantidad) if cantidad else 10000
        
        if cantidad <= 0:
            print("❌ La cantidad debe ser mayor a 0")
            return
        
        if cantidad > 100000:
            confirmar = input(f"⚠️  Creará {cantidad:,} productos. Esto puede tomar mucho tiempo. ¿Continuar? (s/n): ")
            if confirmar.lower() != 's':
                print("❌ Operación cancelada")
                return
        
        crear_productos_masivos(cantidad)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
