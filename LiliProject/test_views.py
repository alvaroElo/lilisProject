"""
Vistas de prueba para visualizar los templates del frontend
Sin necesidad de backend completo
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from maestros.models import Producto, Categoria, Marca, Proveedor, UnidadMedida
from inventario.models import StockActual, MovimientoInventario, Bodega, Lote, AlertaStock
from autenticacion.models import Usuario, Rol
from django.utils import timezone
from datetime import timedelta


# ============================================
# VISTAS DE AUTENTICACIÓN
# ============================================

def test_login(request):
    """Vista de prueba para el login"""
    return render(request, 'login.html')


def test_password_reset(request):
    """Vista de prueba para recuperar contraseña"""
    return render(request, 'password_reset.html')


def test_password_reset_confirm(request):
    """Vista de prueba para confirmar nueva contraseña"""
    return render(request, 'password_reset_confirm.html')


@login_required
def test_validaciones_demo(request):
    """Vista de prueba para demostrar el sistema de validaciones"""
    return render(request, 'validaciones_demo.html')


@login_required
def test_estilos_alertas_demo(request):
    """Vista de prueba para demostrar los estilos mejorados de alertas"""
    return render(request, 'estilos_alertas_demo.html')


# ============================================
# DASHBOARD
# ============================================

@login_required
def test_dashboard(request):
    """Vista de prueba para el dashboard"""
    
    # Calcular estadísticas reales
    total_productos = Producto.objects.filter(estado='ACTIVO').count()
    total_stock = StockActual.objects.aggregate(
        total=Sum('cantidad_disponible')
    )['total'] or 0
    alertas_stock = AlertaStock.objects.filter(estado='ACTIVA').count()
    proveedores_activos = Proveedor.objects.filter(estado='ACTIVO').count()
    
    # Alertas recientes
    alertas_recientes = AlertaStock.objects.filter(
        estado='ACTIVA'
    ).select_related('producto', 'bodega').order_by('-fecha_generacion')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_stock': int(total_stock),
        'alertas_stock': alertas_stock,
        'proveedores_activos': proveedores_activos,
        'alertas_recientes': alertas_recientes,
    }
    return render(request, 'dashboard.html', context)


# ============================================
# USUARIOS
# ============================================

@login_required
def test_usuarios_list(request):
    """Vista de prueba para lista de usuarios"""
    
    usuarios = Usuario.objects.select_related('user', 'rol').all()
    
    # Aplicar filtros si existen
    search = request.GET.get('search')
    if search:
        usuarios = usuarios.filter(
            user__username__icontains=search
        ) | usuarios.filter(
            user__first_name__icontains=search
        ) | usuarios.filter(
            user__last_name__icontains=search
        )
    
    rol_filter = request.GET.get('rol')
    if rol_filter:
        usuarios = usuarios.filter(rol__nombre=rol_filter)
    
    estado_filter = request.GET.get('estado')
    if estado_filter:
        usuarios = usuarios.filter(estado=estado_filter)
    
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'usuarios_list.html', context)


@login_required
def test_usuario_create(request):
    """Vista de prueba para crear usuario"""
    
    roles = Rol.objects.all()
    
    context = {
        'roles': roles,
    }
    return render(request, 'usuario_form.html', context)


@login_required
def test_usuario_edit(request, pk):
    """Vista de prueba para editar usuario"""
    
    usuario = Usuario.objects.select_related('user', 'rol').get(pk=pk)
    roles = Rol.objects.all()
    
    context = {
        'usuario': usuario,
        'roles': roles,
    }
    return render(request, 'usuario_form.html', context)


# ============================================
# PRODUCTOS
# ============================================

@login_required
def test_productos_list(request):
    """Vista de prueba para lista de productos"""
    
    productos = Producto.objects.select_related(
        'categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock'
    ).all()
    
    # Aplicar filtros
    search = request.GET.get('search')
    if search:
        productos = productos.filter(
            sku__icontains=search
        ) | productos.filter(
            nombre__icontains=search
        )
    
    categoria_filter = request.GET.get('categoria')
    if categoria_filter:
        productos = productos.filter(categoria_id=categoria_filter)
    
    marca_filter = request.GET.get('marca')
    if marca_filter:
        productos = productos.filter(marca_id=marca_filter)
    
    estado_filter = request.GET.get('estado')
    if estado_filter:
        productos = productos.filter(estado=estado_filter)
    
    # Agregar stock actual a cada producto (simulado)
    for producto in productos:
        stock = StockActual.objects.filter(producto=producto).first()
        producto.stock_actual = stock.cantidad_disponible if stock else 0
        
        # Simular fecha de vencimiento si es perecedero
        if producto.perishable:
            producto.fecha_vencimiento = timezone.now().date() + timedelta(days=60)
            producto.dias_vencimiento = 60
    
    categorias = Categoria.objects.filter(activo=True)
    marcas = Marca.objects.filter(activo=True)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas,
    }
    return render(request, 'productos_list.html', context)


@login_required
def test_producto_create(request):
    """Vista de prueba para crear producto"""
    
    categorias = Categoria.objects.filter(activo=True)
    marcas = Marca.objects.filter(activo=True)
    unidades_medida = UnidadMedida.objects.filter(activo=True)
    
    context = {
        'categorias': categorias,
        'marcas': marcas,
        'unidades_medida': unidades_medida,
    }
    return render(request, 'producto_form.html', context)


@login_required
def test_producto_edit(request, pk):
    """Vista de prueba para editar producto"""
    
    producto = Producto.objects.select_related(
        'categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock'
    ).get(pk=pk)
    
    categorias = Categoria.objects.filter(activo=True)
    marcas = Marca.objects.filter(activo=True)
    unidades_medida = UnidadMedida.objects.filter(activo=True)
    
    context = {
        'producto': producto,
        'categorias': categorias,
        'marcas': marcas,
        'unidades_medida': unidades_medida,
    }
    return render(request, 'producto_form.html', context)


@login_required
def test_producto_detail(request, pk):
    """Vista de prueba para detalle de producto"""
    
    producto = Producto.objects.select_related(
        'categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock'
    ).get(pk=pk)
    
    context = {
        'producto': producto,
    }
    return render(request, 'producto_form.html', context)


# ============================================
# PROVEEDORES
# ============================================

@login_required
def test_proveedores_list(request):
    """Vista de prueba para lista de proveedores"""
    
    proveedores = Proveedor.objects.all()
    
    # Aplicar filtros
    search = request.GET.get('search')
    if search:
        proveedores = proveedores.filter(
            rut_nif__icontains=search
        ) | proveedores.filter(
            razon_social__icontains=search
        ) | proveedores.filter(
            email__icontains=search
        )
    
    estado_filter = request.GET.get('estado')
    if estado_filter:
        proveedores = proveedores.filter(estado=estado_filter)
    
    condiciones_filter = request.GET.get('condiciones_pago')
    if condiciones_filter:
        proveedores = proveedores.filter(condiciones_pago=condiciones_filter)
    
    context = {
        'proveedores': proveedores,
    }
    return render(request, 'proveedores_list.html', context)


@login_required
def test_proveedor_create(request):
    """Vista de prueba para crear proveedor"""
    context = {}
    return render(request, 'proveedor_form.html', context)


@login_required
def test_proveedor_edit(request, pk):
    """Vista de prueba para editar proveedor"""
    proveedor = Proveedor.objects.get(pk=pk)
    context = {'proveedor': proveedor}
    return render(request, 'proveedor_form.html', context)


@login_required
def test_proveedor_detail(request, pk):
    """Vista de prueba para detalle de proveedor"""
    proveedor = Proveedor.objects.get(pk=pk)
    context = {'proveedor': proveedor}
    return render(request, 'proveedor_form.html', context)


# ============================================
# INVENTARIO
# ============================================

@login_required
def test_inventario_list(request):
    """Vista de prueba para inventario con tabs"""
    
    # Tab Movimientos
    movimientos = MovimientoInventario.objects.select_related(
        'producto', 'proveedor', 'bodega_origen', 'bodega_destino', 
        'unidad_medida', 'usuario'
    ).order_by('-fecha_movimiento')[:20]
    
    # Tab Stock Actual
    stock_items = StockActual.objects.select_related(
        'producto', 'bodega'
    ).all()[:20]
    
    # Tab Lotes
    lotes = Lote.objects.select_related(
        'producto', 'bodega', 'proveedor'
    ).order_by('-created_at')[:20]
    
    # Tab Alertas
    alertas = AlertaStock.objects.select_related(
        'producto', 'bodega', 'lote'
    ).filter(estado='ACTIVA').order_by('-fecha_generacion')[:20]
    
    context = {
        'movimientos': movimientos,
        'stock_items': stock_items,
        'lotes': lotes,
        'alertas': alertas,
    }
    return render(request, 'inventario_list.html', context)


@login_required
def test_movimiento_create(request):
    """Vista de prueba para crear movimiento"""
    
    productos = Producto.objects.filter(estado='ACTIVO')
    proveedores = Proveedor.objects.filter(estado='ACTIVO')
    bodegas = Bodega.objects.filter(activo=True)
    unidades = UnidadMedida.objects.filter(activo=True)
    
    context = {
        'productos': productos,
        'proveedores': proveedores,
        'bodegas': bodegas,
        'unidades_medida': unidades,
        'now': timezone.now(),
    }
    return render(request, 'movimiento_form.html', context)


@login_required
def test_movimiento_detail(request, pk):
    """Vista de prueba para detalle de movimiento"""
    
    movimiento = MovimientoInventario.objects.select_related(
        'producto', 'proveedor', 'bodega_origen', 'bodega_destino',
        'unidad_medida', 'usuario', 'usuario_confirmacion'
    ).get(pk=pk)
    
    # También pasar los datos necesarios para el template
    productos = Producto.objects.filter(estado='ACTIVO')
    proveedores = Proveedor.objects.filter(estado='ACTIVO')
    bodegas = Bodega.objects.filter(activo=True)
    unidades = UnidadMedida.objects.filter(activo=True)
    
    context = {
        'movimiento': movimiento,
        'productos': productos,
        'proveedores': proveedores,
        'bodegas': bodegas,
        'unidades_medida': unidades,
    }
    return render(request, 'movimiento_form.html', context)


@login_required
def test_stock_list(request):
    """Vista de prueba para consultar stock"""
    
    stock_items = StockActual.objects.select_related(
        'producto', 'bodega'
    ).all()
    
    context = {
        'stock_items': stock_items,
    }
    return render(request, 'inventario_list.html', context)


# ============================================
# ORDEN DE COMPRA (PLACEHOLDER)
# ============================================

@login_required
def test_orden_compra_create(request):
    """Vista de prueba para crear orden de compra"""
    context = {}
    return render(request, 'dashboard.html', context)
