from django.contrib import admin
from .models import Categoria, Marca, UnidadMedida, Proveedor, Producto, ProductoProveedor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria_padre', 'activo', 'created_at']
    list_filter = ['activo', 'created_at', 'categoria_padre']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria_padre')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'factor_base', 'activo', 'created_at']
    list_filter = ['tipo', 'activo', 'created_at']
    search_fields = ['codigo', 'nombre']
    ordering = ['codigo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo')
        }),
        ('Conversión', {
            'fields': ('factor_base',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['rut_nif', 'razon_social', 'email', 'telefono', 'estado', 'condiciones_pago', 'created_at']
    list_filter = ['estado', 'condiciones_pago', 'pais', 'created_at']
    search_fields = ['rut_nif', 'razon_social', 'nombre_fantasia', 'email']
    ordering = ['razon_social']
    
    fieldsets = (
        ('Información Legal', {
            'fields': ('rut_nif', 'razon_social', 'nombre_fantasia')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'sitio_web')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad', 'pais')
        }),
        ('Condiciones Comerciales', {
            'fields': ('condiciones_pago', 'condiciones_pago_detalle', 'moneda')
        }),
        ('Contacto Principal', {
            'fields': ('contacto_principal_nombre', 'contacto_principal_email', 'contacto_principal_telefono'),
            'classes': ('collapse',)
        }),
        ('Estado y Observaciones', {
            'fields': ('estado', 'observaciones')
        }),
    )


class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    fields = ['proveedor', 'costo', 'lead_time_dias', 'min_lote', 'descuento_pct', 'preferente', 'activo']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'marca', 'precio_venta', 'stock_minimo', 'estado', 'created_at']
    list_filter = ['categoria', 'marca', 'estado', 'perishable', 'control_por_lote', 'control_por_serie', 'created_at']
    search_fields = ['sku', 'nombre', 'descripcion', 'ean_upc']
    ordering = ['sku']
    list_select_related = ['categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock']
    inlines = [ProductoProveedorInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo')
        }),
        ('Unidades de Medida', {
            'fields': ('uom_compra', 'uom_venta', 'uom_stock', 'factor_conversion')
        }),
        ('Costos y Precios', {
            'fields': ('costo_estandar', 'costo_promedio', 'precio_venta', 'impuesto_iva')
        }),
        ('Control de Stock', {
            'fields': ('stock_minimo', 'stock_maximo', 'punto_reorden')
        }),
        ('Control Especial', {
            'fields': ('perishable', 'control_por_lote', 'control_por_serie')
        }),
        ('Archivos', {
            'fields': ('imagen_url', 'ficha_tecnica_url'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    # Acción personalizada para activar productos
    def activar_productos(self, request, queryset):
        updated = queryset.update(estado='ACTIVO')
        self.message_user(request, f'{updated} productos activados correctamente.')
    activar_productos.short_description = "Activar productos seleccionados"
    
    # Acción personalizada para descontinuar productos
    def descontinuar_productos(self, request, queryset):
        updated = queryset.update(estado='DESCONTINUADO')
        self.message_user(request, f'{updated} productos descontinuados correctamente.')
    descontinuar_productos.short_description = "Descontinuar productos seleccionados"
    
    actions = ['activar_productos', 'descontinuar_productos']


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['producto', 'proveedor', 'costo', 'lead_time_dias', 'preferente', 'activo', 'created_at']
    list_filter = ['preferente', 'activo', 'created_at', 'proveedor']
    search_fields = ['producto__sku', 'producto__nombre', 'proveedor__razon_social']
    ordering = ['producto__sku', 'proveedor__razon_social']
    list_select_related = ['producto', 'proveedor']
