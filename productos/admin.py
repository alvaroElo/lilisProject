from django.contrib import admin
from .models import Producto
from maestros.models import ProductoProveedor


class ProductoProveedorInline(admin.TabularInline):
    model = ProductoProveedor
    extra = 1
    fields = ['proveedor', 'costo', 'lead_time_dias', 'min_lote', 'descuento_pct', 'preferente', 'activo']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'marca', 'stock_actual', 'stock_minimo', 'alerta_bajo_stock', 'estado']
    list_filter = ['estado', 'categoria', 'marca', 'alerta_bajo_stock', 'perecible']
    search_fields = ['sku', 'nombre', 'descripcion', 'ean_upc']
    readonly_fields = ['stock_actual', 'costo_promedio', 'alerta_bajo_stock', 'alerta_por_vencer', 'created_at', 'updated_at']
    inlines = [ProductoProveedorInline]
    
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo')
        }),
        ('Unidades y Precios', {
            'fields': ('uom_compra', 'uom_venta', 'factor_conversion', 'costo_estandar', 'costo_promedio', 'precio_venta', 'impuesto_iva')
        }),
        ('Stock y Control', {
            'fields': ('stock_actual', 'stock_minimo', 'stock_maximo', 'punto_reorden', 'alerta_bajo_stock')
        }),
        ('Control Especial', {
            'fields': ('perecible', 'control_por_lote', 'control_por_serie', 'alerta_por_vencer')
        }),
        ('Recursos', {
            'fields': ('imagen_url', 'ficha_tecnica_url')
        }),
        ('Estado y Fechas', {
            'fields': ('estado', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['activar_productos', 'descontinuar_productos']
    
    def activar_productos(self, request, queryset):
        updated = queryset.update(estado='ACTIVO')
        self.message_user(request, f'{updated} productos activados correctamente.')
    activar_productos.short_description = "Activar productos seleccionados"
    
    def descontinuar_productos(self, request, queryset):
        updated = queryset.update(estado='DESCONTINUADO')
        self.message_user(request, f'{updated} productos descontinuados correctamente.')
    descontinuar_productos.short_description = "Descontinuar productos seleccionados"
