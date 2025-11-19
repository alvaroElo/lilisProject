"""
Script para crear 10,001 movimientos de inventario de prueba
Dulcería Lilis - Sistema de Gestión

⚠️ IMPORTANTE: 
- Ejecutar DESPUÉS del script crear_10000_productos.py
- Solo crea movimientos de tipo INGRESO, AJUSTE y DEVOLUCIÓN
- Evita SALIDA para no generar stocks negativos

Uso:
    python scripts/crear_10001_movimientos.py
"""

import os
import sys
import django
from decimal import Decimal
from random import randint, choice, uniform
from datetime import datetime, timedelta
from django.utils import timezone

# Agregar el directorio raíz del proyecto al PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from inventario.models import MovimientoInventario, Bodega
from productos.models import Producto
from maestros.models import Proveedor, UnidadMedida
from autenticacion.models import Usuario


def crear_datos_base():
    """Crear o verificar datos base necesarios"""
    
    print("📦 Verificando datos base...\n")
    
    # Verificar productos
    total_productos = Producto.objects.count()
    if total_productos < 100:
        print(f"⚠️  ADVERTENCIA: Solo hay {total_productos} productos en la base de datos")
        print("   Se recomienda ejecutar primero: python scripts/crear_10000_productos.py")
        respuesta = input("\n¿Desea continuar de todas formas? (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Operación cancelada")
            sys.exit(0)
    else:
        print(f"✓ Productos disponibles: {total_productos:,}")
    
    # Crear bodegas si no existen
    bodegas_data = [
        ('BOD-01', 'Bodega Principal', 'Av. Principal 1234', 'PRINCIPAL'),
        ('BOD-02', 'Bodega Sucursal Norte', 'Calle Norte 567', 'SUCURSAL'),
        ('BOD-03', 'Bodega Sucursal Sur', 'Calle Sur 890', 'SUCURSAL'),
        ('BOD-04', 'Bodega Centro', 'Calle Centro 123', 'SUCURSAL'),
        ('BOD-TRANS', 'Bodega Tránsito', 'En movimiento', 'TRANSITO'),
    ]
    
    bodegas = []
    for codigo, nombre, direccion, tipo in bodegas_data:
        bodega, created = Bodega.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'direccion': direccion,
                'tipo': tipo
            }
        )
        bodegas.append(bodega)
        if created:
            print(f"  ✓ Bodega creada: {codigo} - {nombre}")
    
    # Verificar proveedores
    proveedores = list(Proveedor.objects.filter(estado='ACTIVO')[:50])
    if len(proveedores) < 5:
        print(f"\n⚠️  ADVERTENCIA: Solo hay {len(proveedores)} proveedores activos")
        print("   Se recomienda tener al menos 50 proveedores")
        print("   Ejecutar: python scripts/crear_proveedores_test.py")
    else:
        print(f"✓ Proveedores disponibles: {len(proveedores)}")
    
    # Obtener usuario para los movimientos
    usuarios = list(Usuario.objects.all()[:10])
    if not usuarios:
        print("\n❌ ERROR: No hay usuarios en el sistema")
        print("   Debe crear al menos un usuario antes de ejecutar este script")
        sys.exit(1)
    
    print(f"✓ Usuarios disponibles: {len(usuarios)}")
    
    # Verificar unidades de medida
    unidades = list(UnidadMedida.objects.filter(activo=True))
    if not unidades:
        print("\n❌ ERROR: No hay unidades de medida en el sistema")
        sys.exit(1)
    
    print(f"✓ Unidades de medida: {len(unidades)}")
    
    return bodegas, proveedores, usuarios, unidades


def generar_fecha_aleatoria(dias_atras=365):
    """Generar fecha aleatoria dentro del rango especificado"""
    hoy = timezone.now()
    dias_random = randint(0, dias_atras)
    fecha = hoy - timedelta(days=dias_random)
    
    # Agregar horas aleatorias
    horas = randint(8, 18)  # Entre 8 AM y 6 PM
    minutos = randint(0, 59)
    
    return fecha.replace(hour=horas, minute=minutos, second=0, microsecond=0)


def generar_motivo_ajuste():
    """Generar motivos de ajuste aleatorios"""
    motivos = [
        "Ajuste por inventario físico",
        "Corrección de stock por conteo",
        "Ajuste por diferencia en sistema",
        "Actualización por auditoría",
        "Corrección de error de ingreso",
        "Ajuste por productos dañados",
        "Ajuste por merma",
        "Corrección de stock inicial",
        "Ajuste por reclasificación",
        "Ajuste por cambio de ubicación",
    ]
    return choice(motivos)


def generar_documento_referencia(tipo_movimiento):
    """Generar número de documento de referencia"""
    if tipo_movimiento == 'INGRESO':
        prefijo = 'FC'  # Factura
    elif tipo_movimiento == 'DEVOLUCION':
        prefijo = 'DEV'  # Devolución
    elif tipo_movimiento == 'AJUSTE':
        prefijo = 'AJ'  # Ajuste
    else:
        prefijo = 'DOC'
    
    numero = randint(1000, 99999)
    return f"{prefijo}-{numero}"


def crear_movimientos_masivos(cantidad=10001):
    """Crear movimientos de inventario de forma masiva"""
    
    print(f"\n🎯 Iniciando creación de {cantidad:,} movimientos...\n")
    
    # Obtener datos base
    bodegas, proveedores, usuarios, unidades = crear_datos_base()
    
    # Obtener productos activos
    productos = list(Producto.objects.filter(estado='ACTIVO'))
    if not productos:
        print("❌ ERROR: No hay productos activos")
        return
    
    print(f"\n🏭 Generando {cantidad:,} movimientos...")
    print("⏳ Esto puede tomar varios minutos...\n")
    
    # Tipos de movimiento permitidos (sin SALIDA)
    tipos_movimiento = [
        'INGRESO',      # 60% - Ingresos de mercadería
        'INGRESO',
        'INGRESO',
        'INGRESO',
        'INGRESO',
        'INGRESO',
        'AJUSTE',       # 30% - Ajustes de inventario
        'AJUSTE',
        'AJUSTE',
        'DEVOLUCION',   # 10% - Devoluciones
    ]
    
    # Lista para bulk create
    movimientos = []
    
    # Estadísticas
    stats = {
        'INGRESO': 0,
        'AJUSTE': 0,
        'DEVOLUCION': 0,
    }
    
    for i in range(1, cantidad + 1):
        # Seleccionar datos aleatorios
        tipo_movimiento = choice(tipos_movimiento)
        producto = choice(productos)
        usuario = choice(usuarios)
        unidad_medida = producto.uom_compra
        bodega_destino = choice(bodegas[:-1])  # Excluir bodega de tránsito
        
        # Cantidad aleatoria
        cantidad_mov = Decimal(str(randint(1, 200)))
        
        # Costo unitario con variación
        if producto.costo_estandar:
            costo_base = float(producto.costo_estandar)
            variacion = uniform(0.9, 1.1)  # ±10%
            costo_unitario = Decimal(str(round(costo_base * variacion, 2)))
        else:
            costo_unitario = Decimal(str(round(uniform(100, 5000), 2)))
        
        costo_total = cantidad_mov * costo_unitario
        
        # Fecha aleatoria (último año)
        fecha_movimiento = generar_fecha_aleatoria(dias_atras=365)
        
        # Estado (90% confirmados, 10% pendientes)
        estado = 'CONFIRMADO' if randint(1, 10) <= 9 else 'PENDIENTE'
        fecha_confirmacion = fecha_movimiento + timedelta(hours=randint(1, 24)) if estado == 'CONFIRMADO' else None
        usuario_confirmacion = usuario if estado == 'CONFIRMADO' else None
        
        # Campos específicos según tipo de movimiento
        proveedor = None
        bodega_origen = None
        documento_padre_tipo = None
        motivo_ajuste = None
        observaciones = None
        
        if tipo_movimiento == 'INGRESO':
            proveedor = choice(proveedores) if proveedores else None
            documento_padre_tipo = 'ORDEN_COMPRA'
            observaciones = f"Ingreso de mercadería - Proveedor: {proveedor.razon_social if proveedor else 'N/A'}"
            
        elif tipo_movimiento == 'AJUSTE':
            bodega_origen = bodega_destino
            documento_padre_tipo = 'AJUSTE_MANUAL'
            motivo_ajuste = generar_motivo_ajuste()
            observaciones = f"Ajuste de inventario - {motivo_ajuste}"
            
        elif tipo_movimiento == 'DEVOLUCION':
            proveedor = choice(proveedores) if proveedores else None
            bodega_origen = bodega_destino
            documento_padre_tipo = 'DEVOLUCION_PROVEEDOR'
            motivo_ajuste = "Devolución de productos al proveedor"
            observaciones = f"Devolución - Proveedor: {proveedor.razon_social if proveedor else 'N/A'}"
        
        # Documento de referencia
        documento_referencia = generar_documento_referencia(tipo_movimiento)
        
        # Crear movimiento
        movimiento = MovimientoInventario(
            tipo_movimiento=tipo_movimiento,
            fecha_movimiento=fecha_movimiento,
            producto=producto,
            proveedor=proveedor,
            bodega_origen=bodega_origen,
            bodega_destino=bodega_destino,
            cantidad=cantidad_mov,
            unidad_medida=unidad_medida,
            costo_unitario=costo_unitario,
            costo_total=costo_total,
            documento_padre_tipo=documento_padre_tipo,
            documento_referencia=documento_referencia,
            motivo_ajuste=motivo_ajuste,
            usuario=usuario,
            observaciones=observaciones,
            estado=estado,
            fecha_confirmacion=fecha_confirmacion,
            usuario_confirmacion=usuario_confirmacion,
        )
        
        movimientos.append(movimiento)
        stats[tipo_movimiento] += 1
        
        # Mostrar progreso cada 500 movimientos
        if i % 500 == 0:
            print(f"  📊 Progreso: {i:,} / {cantidad:,} movimientos generados ({(i/cantidad)*100:.1f}%)")
    
    print(f"\n💾 Guardando {len(movimientos):,} movimientos en la base de datos...")
    print("⏳ Esto puede tomar varios minutos...\n")
    
    # Bulk create en lotes de 1000
    batch_size = 1000
    total_creados = 0
    
    for i in range(0, len(movimientos), batch_size):
        batch = movimientos[i:i + batch_size]
        MovimientoInventario.objects.bulk_create(batch, batch_size=batch_size)
        total_creados += len(batch)
        print(f"  ✓ Lote guardado: {total_creados:,} / {len(movimientos):,} movimientos")
    
    print(f"\n✅ ¡Proceso completado!")
    print(f"✨ Se crearon {total_creados:,} movimientos exitosamente\n")
    
    # Estadísticas finales
    print("=" * 70)
    print("📈 ESTADÍSTICAS DE MOVIMIENTOS")
    print("=" * 70)
    print(f"📦 Total movimientos:        {MovimientoInventario.objects.count():,}")
    print(f"✅ Movimientos confirmados:  {MovimientoInventario.objects.filter(estado='CONFIRMADO').count():,}")
    print(f"⏳ Movimientos pendientes:   {MovimientoInventario.objects.filter(estado='PENDIENTE').count():,}")
    
    print(f"\n📊 Por tipo de movimiento:")
    for tipo, _ in MovimientoInventario.TIPO_MOVIMIENTO_CHOICES:
        count = MovimientoInventario.objects.filter(tipo_movimiento=tipo).count()
        if count > 0:
            porcentaje = (count / total_creados) * 100
            print(f"  • {tipo.ljust(15)}: {count:>6,} ({porcentaje:>5.1f}%)")
    
    print(f"\n📅 Por rango de fechas:")
    hoy = timezone.now()
    ultima_semana = MovimientoInventario.objects.filter(
        fecha_movimiento__gte=hoy - timedelta(days=7)
    ).count()
    ultimo_mes = MovimientoInventario.objects.filter(
        fecha_movimiento__gte=hoy - timedelta(days=30)
    ).count()
    ultimo_trimestre = MovimientoInventario.objects.filter(
        fecha_movimiento__gte=hoy - timedelta(days=90)
    ).count()
    
    print(f"  • Última semana:     {ultima_semana:,}")
    print(f"  • Último mes:        {ultimo_mes:,}")
    print(f"  • Último trimestre:  {ultimo_trimestre:,}")
    
    print(f"\n🏢 Por bodega destino:")
    for bodega in bodegas[:-1]:  # Excluir tránsito
        count = MovimientoInventario.objects.filter(bodega_destino=bodega).count()
        if count > 0:
            print(f"  • {bodega.nombre.ljust(25)}: {count:,}")
    
    print("\n" + "=" * 70)
    
    # Nota sobre actualización de stocks
    print("\n⚠️  NOTA IMPORTANTE:")
    print("   Los movimientos fueron creados pero los stocks de productos")
    print("   no se actualizaron automáticamente.")
    print("   Para actualizar stocks, ejecutar desde el panel de administración")
    print("   o implementar la lógica de actualización de stocks.")
    print()


def main():
    """Función principal"""
    print("=" * 70)
    print("📦 DULCERÍA LILIS - GENERADOR DE MOVIMIENTOS DE INVENTARIO")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Ejecutar DESPUÉS de crear_10000_productos.py")
    print("   - Solo crea movimientos de INGRESO, AJUSTE y DEVOLUCIÓN")
    print("   - NO crea movimientos de SALIDA (evita stocks negativos)")
    print()
    
    try:
        respuesta = input("¿Desea crear 10,001 movimientos de prueba? (s/n): ")
        
        if respuesta.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        cantidad = input("\n📝 ¿Cuántos movimientos desea crear? (por defecto 10001): ").strip()
        cantidad = int(cantidad) if cantidad else 10001
        
        if cantidad <= 0:
            print("❌ La cantidad debe ser mayor a 0")
            return
        
        if cantidad > 50000:
            confirmar = input(f"⚠️  Creará {cantidad:,} movimientos. Esto puede tomar mucho tiempo. ¿Continuar? (s/n): ")
            if confirmar.lower() != 's':
                print("❌ Operación cancelada")
                return
        
        crear_movimientos_masivos(cantidad)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
