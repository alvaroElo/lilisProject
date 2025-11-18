from django.contrib import admin
from .models import Categoria, Marca, UnidadMedida, Proveedor, ProductoProveedor
from productos.models import Producto


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


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['producto', 'proveedor', 'costo', 'lead_time_dias', 'preferente', 'activo', 'created_at']
    list_filter = ['preferente', 'activo', 'created_at', 'proveedor']
    search_fields = ['producto__sku', 'producto__nombre', 'proveedor__razon_social']
    ordering = ['producto__sku', 'proveedor__razon_social']
    list_select_related = ['producto', 'proveedor']
