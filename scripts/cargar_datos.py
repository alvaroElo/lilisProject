#!/usr/bin/env python
"""
Script para cargar datos de ejemplo completos en MySQL
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
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from autenticacion.models import Rol, Usuario
from maestros.models import Categoria, Marca, UnidadMedida, Proveedor, Producto
from inventario.models import Bodega
from decimal import Decimal


def asignar_permisos_por_rol():
    """Asignar permisos de Django basados en roles"""
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    
    # Limpiar grupos existentes y crear nuevos
    Group.objects.filter(name__in=['Vendedores', 'Bodegueros', 'Finanzas', 'Jefe_Ventas']).delete()
    
    grupo_vendedor = Group.objects.create(name='Vendedores')
    grupo_bodeguero = Group.objects.create(name='Bodegueros')
    grupo_finanzas = Group.objects.create(name='Finanzas')
    grupo_jefe_ventas = Group.objects.create(name='Jefe_Ventas')
    
    # Obtener content types de maestros
    from maestros.models import Producto, Categoria, Marca, UnidadMedida, Proveedor
    
    # Obtener content types de inventario y compras
    try:
        from inventario.models import StockActual, MovimientoInventario, Bodega, AlertaStock
        from compras.models import OrdenCompra, OrdenCompraDetalle
    except:
        pass
    
    # === PERMISOS PARA VENDEDOR ===
    permisos_vendedor_codenames = [
        # Maestros - lectura y gestión de productos para testing
        'view_producto', 'add_producto', 'change_producto', 'delete_producto',
        'view_categoria', 'view_marca', 'view_unidadmedida',
        # Inventario - solo consulta
        'view_stockactual', 'view_bodega'
    ]
    
    for codename in permisos_vendedor_codenames:
        try:
            permiso = Permission.objects.get(codename=codename)
            grupo_vendedor.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"  Permiso {codename} no encontrado")
    
    # === PERMISOS PARA BODEGUERO ===
    permisos_bodeguero_codenames = [
        # Maestros - lectura
        'view_producto', 'view_categoria', 'view_marca', 'view_unidadmedida',
        # Inventario - completo
        'view_stockactual', 'add_stockactual', 'change_stockactual',
        'view_movimientoinventario', 'add_movimientoinventario', 'change_movimientoinventario',
        'view_bodega', 'change_bodega',
        'view_alertastock', 'change_alertastock'
    ]
    
    for codename in permisos_bodeguero_codenames:
        try:
            permiso = Permission.objects.get(codename=codename)
            grupo_bodeguero.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"  Permiso {codename} no encontrado")
    
    # === PERMISOS PARA FINANZAS ===
    permisos_finanzas_codenames = [
        # Maestros - productos y proveedores
        'view_producto', 'view_categoria', 'view_marca', 'view_unidadmedida',
        'view_proveedor', 'add_proveedor', 'change_proveedor',
        # Compras - completo
        'view_ordencompra', 'add_ordencompra', 'change_ordencompra',
        'view_ordencompradetalle', 'add_ordencompradetalle', 'change_ordencompradetalle',
        # Inventario - solo lectura
        'view_stockactual'
    ]
    
    for codename in permisos_finanzas_codenames:
        try:
            permiso = Permission.objects.get(codename=codename)
            grupo_finanzas.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"  Permiso {codename} no encontrado")
    
    # === PERMISOS PARA JEFE VENTAS ===
    permisos_jefe_ventas_codenames = [
        # Maestros - productos completos
        'view_producto', 'add_producto', 'change_producto',
        'view_categoria', 'view_marca', 'view_unidadmedida',
        # Inventario - lectura y reportes
        'view_stockactual', 'view_movimientoinventario', 'view_bodega',
        # Compras - lectura
        'view_ordencompra', 'view_ordencompradetalle'
    ]
    
    for codename in permisos_jefe_ventas_codenames:
        try:
            permiso = Permission.objects.get(codename=codename)
            grupo_jefe_ventas.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"  Permiso {codename} no encontrado")
    
    print("✓ Permisos por rol configurados")

def main():
    print('🔄 CARGANDO DATOS COMPLETOS DE EJEMPLO EN MYSQL...')
    
    # ====== CREAR ROLES COMPLETOS ======
    roles_data = [
        {
            'nombre': 'ADMIN',
            'descripcion': 'Administrador del sistema con acceso completo',
            'permisos': {
                'usuarios': ['crear', 'leer', 'actualizar', 'eliminar'],
                'productos': ['crear', 'leer', 'actualizar', 'eliminar'],
                'inventario': ['crear', 'leer', 'actualizar', 'eliminar'],
                'compras': ['crear', 'leer', 'actualizar', 'eliminar'],
                'reportes': ['generar', 'exportar'],
                'configuracion': ['modificar']
            }
        },
        {
            'nombre': 'VENDEDOR',
            'descripcion': 'Vendedor con acceso a ventas e inventario básico',
            'permisos': {
                'productos': ['leer'],
                'inventario': ['leer', 'consultar_stock'],
                'ventas': ['crear', 'leer'],
                'clientes': ['crear', 'leer', 'actualizar']
            }
        },
        {
            'nombre': 'BODEGUERO',
            'descripcion': 'Encargado de bodega con acceso a inventario',
            'permisos': {
                'productos': ['leer'],
                'inventario': ['crear', 'leer', 'actualizar'],
                'movimientos': ['crear', 'leer'],
                'recepcion': ['crear', 'aprobar'],
                'stock': ['ajustar', 'contar']
            }
        },
        {
            'nombre': 'FINANZAS',
            'descripcion': 'Personal de finanzas con acceso a compras y reportes',
            'permisos': {
                'compras': ['crear', 'leer', 'actualizar', 'aprobar'],
                'proveedores': ['crear', 'leer', 'actualizar'],
                'pagos': ['crear', 'leer', 'aprobar'],
                'reportes': ['generar', 'exportar'],
                'costos': ['revisar', 'actualizar']
            }
        },
        {
            'nombre': 'JEFE_VENTAS',
            'descripcion': 'Jefe de ventas con supervisión del equipo',
            'permisos': {
                'productos': ['leer', 'actualizar_precios'],
                'inventario': ['leer'],
                'ventas': ['crear', 'leer', 'supervisar'],
                'vendedores': ['supervisar', 'asignar'],
                'reportes': ['generar', 'exportar'],
                'metas': ['establecer', 'revisar']
            }
        }
    ]
    
    for rol_data in roles_data:
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            defaults={
                'descripcion': rol_data['descripcion'],
                'permisos': rol_data['permisos']
            }
        )
        if created:
            print(f"✓ Rol {rol_data['nombre']}: creado")
    
    # ====== CONFIGURAR PERMISOS POR ROL ======
    asignar_permisos_por_rol()
    
    # ====== CREAR SUPERUSUARIO ======
    # Crear superusuario admin
    try:
        user_admin = User.objects.get(username='admin')
        print('✓ Usuario admin ya existe')
    except User.DoesNotExist:
        user_admin = User.objects.create_superuser(
            username='admin',
            email='admin@dulcerialilis.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema'
        )
        print('✓ Superusuario admin creado')
        
        rol_admin = Rol.objects.get(nombre='ADMIN')
        usuario_admin = Usuario.objects.create(
            user=user_admin,
            telefono='3001234567',
            rol=rol_admin,
            estado='ACTIVO',
            area_unidad='Administración',
            observaciones='Usuario administrador principal'
        )
        print('✓ Perfil admin creado')
    
    # Crear usuarios adicionales
    usuarios_adicionales = [
        {
            'username': 'vendedor1',
            'email': 'vendedor1@dulcerialilis.com',
            'password': 'vendedor123',
            'first_name': 'Ana',
            'last_name': 'García',
            'telefono': '3102345678',
            'rol': 'VENDEDOR',
            'area_unidad': 'Ventas',
            'observaciones': 'Usuario vendedor de mostrador'
        },
        {
            'username': 'bodeguero1',
            'email': 'bodeguero1@dulcerialilis.com',
            'password': 'bodega123',
            'first_name': 'Carlos',
            'last_name': 'Martínez',
            'telefono': '3113456789',
            'rol': 'BODEGUERO',
            'area_unidad': 'Bodega',
            'observaciones': 'Encargado de inventario y recepción'
        },
        {
            'username': 'finanzas1',
            'email': 'finanzas1@dulcerialilis.com',
            'password': 'finanzas123',
            'first_name': 'María',
            'last_name': 'López',
            'telefono': '3124567890',
            'rol': 'FINANZAS',
            'area_unidad': 'Contabilidad',
            'observaciones': 'Responsable de cuentas por pagar y cobrar'
        },
        {
            'username': 'jefe_ventas',
            'email': 'jefeventas@dulcerialilis.com',
            'password': 'jefe123',
            'first_name': 'Roberto',
            'last_name': 'Sánchez',
            'telefono': '3135678901',
            'rol': 'JEFE_VENTAS',
            'area_unidad': 'Gerencia Ventas',
            'observaciones': 'Supervisor del equipo de ventas'
        }
    ]
    
    for user_data in usuarios_adicionales:
        try:
            django_user = User.objects.get(username=user_data['username'])
            # Asegurar que el usuario tenga is_staff=True
            if not django_user.is_staff:
                django_user.is_staff = True
                django_user.save()
            
            # Asignar a grupo si no está ya asignado
            from django.contrib.auth.models import Group
            grupo_map = {
                'VENDEDOR': 'Vendedores',
                'BODEGUERO': 'Bodegueros', 
                'FINANZAS': 'Finanzas',
                'JEFE_VENTAS': 'Jefe_Ventas'
            }
            
            if user_data['rol'] in grupo_map:
                try:
                    grupo = Group.objects.get(name=grupo_map[user_data['rol']])
                    if not django_user.groups.filter(name=grupo.name).exists():
                        django_user.groups.add(grupo)
                except Group.DoesNotExist:
                    print(f"  Grupo {grupo_map[user_data['rol']]} no encontrado")
            
            print(f"✓ Usuario {user_data['username']} ya existe")
        except User.DoesNotExist:
            # Crear usuario Django
            django_user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=True
            )
            
            # Obtener el rol
            rol_obj = Rol.objects.get(nombre=user_data['rol'])
            
            # Crear perfil de usuario
            usuario_profile = Usuario.objects.create(
                user=django_user,
                telefono=user_data['telefono'],
                rol=rol_obj,
                estado='ACTIVO',
                area_unidad=user_data['area_unidad'],
                observaciones=user_data['observaciones']
            )
            
            # Asignar usuario a grupo correspondiente
            from django.contrib.auth.models import Group
            grupo_map = {
                'VENDEDOR': 'Vendedores',
                'BODEGUERO': 'Bodegueros', 
                'FINANZAS': 'Finanzas',
                'JEFE_VENTAS': 'Jefe_Ventas'
            }
            
            if user_data['rol'] in grupo_map:
                try:
                    grupo = Group.objects.get(name=grupo_map[user_data['rol']])
                    django_user.groups.add(grupo)
                except Group.DoesNotExist:
                    pass
            
            print(f"✓ Usuario {user_data['username']} creado")
    
    # ====== CREAR CATEGORÍAS ======
    categorias = [
        ('Dulces', 'Dulces tradicionales y modernos'),
        ('Chocolates', 'Chocolates y productos de cacao'),
        ('Galletas', 'Galletas dulces y saladas'),
        ('Caramelos', 'Caramelos duros y blandos'),
        ('Chicles', 'Chicles y gomas de mascar'),
        ('Helados', 'Helados y productos congelados'),
        ('Pasteles', 'Pasteles y productos de repostería'),
        ('Bebidas', 'Bebidas dulces y refrescos'),
    ]
    
    for nombre, descripcion in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
        if created:
            print(f"✓ Categoría {nombre}: creada")
    
    # ====== CREAR MARCAS ======
    marcas = [
        ('Nestlé', 'Multinacional suiza de alimentos'),
        ('Costa', 'Marca nacional de snacks'),
        ('Ferrero', 'Chocolates y dulces italianos'),
        ('Haribo', 'Gomitas y caramelos alemanes'),
        ('Mondelez', 'Snacks y chocolates'),
        ('Colombina', 'Dulces y confites colombianos'),
        ('Bon Bon Bum', 'Chupetes y caramelos'),
        ('Trident', 'Chicles y gomas de mascar'),
        ('Oreo', 'Galletas y productos relacionados'),
        ('Nucita', 'Chocolates y dulces nacionales'),
    ]
    
    for nombre, descripcion in marcas:
        marca, created = Marca.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
        if created:
            print(f"✓ Marca {nombre}: creada")
    
    # ====== CREAR UNIDADES DE MEDIDA ======
    unidades = [
        ('UND', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('GR', 'Gramo'),
        ('LB', 'Libra'),
        ('LT', 'Litro'),
        ('ML', 'Mililitro'),
        ('CJ', 'Caja'),
        ('PQ', 'Paquete'),
        ('BL', 'Bolsa'),
        ('DOC', 'Docena'),
    ]
    
    for codigo, nombre in unidades:
        unidad, created = UnidadMedida.objects.get_or_create(
            codigo=codigo,
            defaults={'nombre': nombre}
        )
        if created:
            print(f"✓ Unidad {codigo}: creada")
    
    # ====== CREAR PROVEEDORES ======
    proveedores_data = [
        {
            'razon_social': 'Distribuidora La Esperanza S.A.S',
            'rut_nif': '900123456-7',
            'telefono': '3001234567',
            'email': 'ventas@laesperanza.com',
            'direccion': 'Calle 45 # 12-34, Bogotá',
            'contacto_principal_nombre': 'María González',
            'condiciones_pago': '30_DIAS',
            'estado': 'ACTIVO'
        },
        {
            'razon_social': 'Dulces del Valle Ltda',
            'rut_nif': '800456789-3',
            'telefono': '3112345678',
            'email': 'pedidos@dulcesdelvalle.com',
            'direccion': 'Carrera 15 # 67-89, Cali',
            'contacto_principal_nombre': 'Carlos Pérez',
            'condiciones_pago': 'CONTADO',
            'estado': 'ACTIVO'
        },
        {
            'razon_social': 'Confitería Premium S.A',
            'rut_nif': '901234567-8',
            'telefono': '3203456789',
            'email': 'comercial@confiteriapremium.com',
            'direccion': 'Avenida 68 # 25-41, Medellín',
            'contacto_principal_nombre': 'Ana Rodríguez',
            'condiciones_pago': '30_DIAS',
            'estado': 'ACTIVO'
        },
        {
            'razon_social': 'Mayorista Dulce Hogar',
            'rut_nif': '890123456-2',
            'telefono': '3154567890',
            'email': 'info@dulcehogar.net',
            'direccion': 'Calle 72 # 11-28, Barranquilla',
            'contacto_principal_nombre': 'Luis Martínez',
            'condiciones_pago': '60_DIAS',
            'estado': 'ACTIVO'
        }
    ]
    
    for proveedor_data in proveedores_data:
        proveedor, created = Proveedor.objects.get_or_create(
            rut_nif=proveedor_data['rut_nif'],
            defaults=proveedor_data
        )
        if created:
            print(f"✓ Proveedor {proveedor_data['razon_social']}: creado")
    
    # ====== CREAR BODEGAS ======
    bodegas_data = [
        {
            'codigo': 'BOD-001',
            'nombre': 'Bodega Principal',
            'direccion': 'Primer piso - Área A',
            'tipo': 'PRINCIPAL',
            'activo': True
        },
        {
            'codigo': 'BOD-002',
            'nombre': 'Bodega Refrigerada',
            'direccion': 'Primer piso - Área B',
            'tipo': 'SUCURSAL',
            'activo': True
        },
        {
            'codigo': 'BOD-003',
            'nombre': 'Bodega de Cuarentena',
            'direccion': 'Segundo piso - Área C',
            'tipo': 'TRANSITO',
            'activo': True
        }
    ]
    
    for bodega_data in bodegas_data:
        bodega, created = Bodega.objects.get_or_create(
            codigo=bodega_data['codigo'],
            defaults=bodega_data
        )
        if created:
            print(f"✓ Bodega {bodega_data['nombre']}: creada")
    
    # ====== CREAR PRODUCTOS COMPLETOS ======
    # Obtener referencias
    nestle = Marca.objects.get(nombre='Nestlé')
    costa = Marca.objects.get(nombre='Costa')
    ferrero = Marca.objects.get(nombre='Ferrero')
    haribo = Marca.objects.get(nombre='Haribo')
    colombina = Marca.objects.get(nombre='Colombina')
    oreo = Marca.objects.get(nombre='Oreo')
    
    dulces_cat = Categoria.objects.get(nombre='Dulces')
    choc_cat = Categoria.objects.get(nombre='Chocolates')
    galletas_cat = Categoria.objects.get(nombre='Galletas')
    caramelos_cat = Categoria.objects.get(nombre='Caramelos')
    chicles_cat = Categoria.objects.get(nombre='Chicles')
    
    und_unidad = UnidadMedida.objects.get(codigo='UND')
    kg_unidad = UnidadMedida.objects.get(codigo='KG')
    gr_unidad = UnidadMedida.objects.get(codigo='GR')
    pq_unidad = UnidadMedida.objects.get(codigo='PQ')
    cj_unidad = UnidadMedida.objects.get(codigo='CJ')
    
    productos = [
        # Chocolates
        {
            'sku': 'CHOC-001',
            'nombre': 'Chocolate Nestlé 50g',
            'descripcion': 'Chocolate con leche de 50 gramos',
            'marca': nestle,
            'categoria': choc_cat,
            'uom_compra': und_unidad,
            'uom_venta': und_unidad,
            'uom_stock': und_unidad,
            'precio_venta': Decimal('2000.00'),
            'costo_estandar': Decimal('1500.00'),
            'stock_minimo': Decimal('50'),
            'stock_maximo': Decimal('500'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'CHOC-002',
            'nombre': 'Ferrero Rocher x12',
            'descripcion': 'Caja de 12 chocolates Ferrero Rocher',
            'marca': ferrero,
            'categoria': choc_cat,
            'uom_compra': cj_unidad,
            'uom_venta': cj_unidad,
            'uom_stock': cj_unidad,
            'precio_venta': Decimal('35000.00'),
            'costo_estandar': Decimal('25000.00'),
            'stock_minimo': Decimal('20'),
            'stock_maximo': Decimal('100'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'CHOC-003',
            'nombre': 'Nucita 250g',
            'descripcion': 'Chocolate en polvo Nucita 250 gramos',
            'marca': colombina,
            'categoria': choc_cat,
            'uom_compra': pq_unidad,
            'uom_venta': pq_unidad,
            'uom_stock': pq_unidad,
            'precio_venta': Decimal('6500.00'),
            'costo_estandar': Decimal('4500.00'),
            'stock_minimo': Decimal('30'),
            'stock_maximo': Decimal('200'),
            'estado': 'ACTIVO'
        },
        # Dulces y Caramelos
        {
            'sku': 'CAR-001',
            'nombre': 'Caramelos Costa 1kg',
            'descripcion': 'Caramelos surtidos por kilogramo',
            'marca': costa,
            'categoria': dulces_cat,
            'uom_compra': kg_unidad,
            'uom_venta': kg_unidad,
            'uom_stock': kg_unidad,
            'precio_venta': Decimal('12000.00'),
            'costo_estandar': Decimal('8000.00'),
            'stock_minimo': Decimal('10'),
            'stock_maximo': Decimal('100'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'GOM-001',
            'nombre': 'Gomitas Haribo 100g',
            'descripcion': 'Gomitas de frutas Haribo 100 gramos',
            'marca': haribo,
            'categoria': caramelos_cat,
            'uom_compra': pq_unidad,
            'uom_venta': pq_unidad,
            'uom_stock': pq_unidad,
            'precio_venta': Decimal('3500.00'),
            'costo_estandar': Decimal('2500.00'),
            'stock_minimo': Decimal('40'),
            'stock_maximo': Decimal('300'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'CHU-001',
            'nombre': 'Bon Bon Bum x24',
            'descripcion': 'Chupetes Bon Bon Bum caja por 24 unidades',
            'marca': colombina,
            'categoria': caramelos_cat,
            'uom_compra': cj_unidad,
            'uom_venta': cj_unidad,
            'uom_stock': cj_unidad,
            'precio_venta': Decimal('18000.00'),
            'costo_estandar': Decimal('12000.00'),
            'stock_minimo': Decimal('15'),
            'stock_maximo': Decimal('80'),
            'estado': 'ACTIVO'
        },
        # Galletas
        {
            'sku': 'GAL-001',
            'nombre': 'Galletas Oreo 154g',
            'descripcion': 'Galletas Oreo paquete de 154 gramos',
            'marca': oreo,
            'categoria': galletas_cat,
            'uom_compra': pq_unidad,
            'uom_venta': pq_unidad,
            'uom_stock': pq_unidad,
            'precio_venta': Decimal('4500.00'),
            'costo_estandar': Decimal('3200.00'),
            'stock_minimo': Decimal('25'),
            'stock_maximo': Decimal('150'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'GAL-002',
            'nombre': 'Festival Nestlé 432g',
            'descripcion': 'Galletas Festival surtidas 432 gramos',
            'marca': nestle,
            'categoria': galletas_cat,
            'uom_compra': pq_unidad,
            'uom_venta': pq_unidad,
            'uom_stock': pq_unidad,
            'precio_venta': Decimal('7800.00'),
            'costo_estandar': Decimal('5500.00'),
            'stock_minimo': Decimal('20'),
            'stock_maximo': Decimal('120'),
            'estado': 'ACTIVO'
        },
        # Chicles
        {
            'sku': 'CHI-001',
            'nombre': 'Trident Menta x10',
            'descripcion': 'Chicles Trident sabor menta paquete x10',
            'marca': colombina,
            'categoria': chicles_cat,
            'uom_compra': pq_unidad,
            'uom_venta': pq_unidad,
            'uom_stock': pq_unidad,
            'precio_venta': Decimal('2500.00'),
            'costo_estandar': Decimal('1800.00'),
            'stock_minimo': Decimal('60'),
            'stock_maximo': Decimal('400'),
            'estado': 'ACTIVO'
        },
        {
            'sku': 'CHI-002',
            'nombre': 'Chicles Globo Costa x50',
            'descripcion': 'Chicles globo surtidos caja por 50 unidades',
            'marca': costa,
            'categoria': chicles_cat,
            'uom_compra': cj_unidad,
            'uom_venta': cj_unidad,
            'uom_stock': cj_unidad,
            'precio_venta': Decimal('12500.00'),
            'costo_estandar': Decimal('8500.00'),
            'stock_minimo': Decimal('12'),
            'stock_maximo': Decimal('60'),
            'estado': 'ACTIVO'
        }
    ]
    
    for producto_data in productos:
        producto, created = Producto.objects.get_or_create(
            sku=producto_data['sku'],
            defaults=producto_data
        )
        if created:
            print(f"✓ Producto {producto_data['sku']}: creado")
    
    print('\n🎉 ¡SEMILLAS COMPLETAS CARGADAS EXITOSAMENTE!')
    print('=' * 60)
    print('✅ Base de datos: dulceria_lilis')
    print('✅ 5 roles creados')
    print('✅ 5 usuarios configurados')
    print('✅ 8 categorías de productos')
    print('✅ 10 marcas registradas')
    print('✅ 10 unidades de medida')
    print('✅ 4 proveedores activos')
    print('✅ 3 bodegas configuradas')
    print('✅ 10 productos completos')
    print('\n👥 USUARIOS DISPONIBLES:')
    print('   👤 admin / admin123 (Administrador)')
    print('   👤 vendedor1 / vendedor123 (Vendedor)')
    print('   👤 bodeguero1 / bodega123 (Bodeguero)')
    print('   👤 finanzas1 / finanzas123 (Finanzas)')
    print('   👤 jefe_ventas / jefe123 (Jefe Ventas)')
    print('\n🌐 Servidor disponible en: http://127.0.0.1:8000/admin/')

if __name__ == '__main__':
    main()