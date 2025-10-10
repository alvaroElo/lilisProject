from django.contrib import admin
from .models import OrdenCompra, OrdenCompraDetalle


class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 1
    fields = ['producto', 'cantidad_solicitada', 'cantidad_recibida', 'precio_unitario', 
             'descuento_pct', 'unidad_medida', 'observaciones']
    readonly_fields = ['subtotal']


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'proveedor', 'fecha_orden', 'fecha_entrega_esperada', 
                   'estado', 'total', 'usuario_creacion', 'created_at']
    list_filter = ['estado', 'fecha_orden', 'fecha_entrega_esperada', 'proveedor', 'created_at']
    search_fields = ['numero_orden', 'proveedor__razon_social', 'proveedor__rut_nif']
    ordering = ['-fecha_orden']
    list_select_related = ['proveedor', 'usuario_creacion', 'usuario_creacion__user', 'usuario_autorizacion']
    inlines = [OrdenCompraDetalleInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_orden', 'proveedor', 'fecha_orden', 'fecha_entrega_esperada')
        }),
        ('Estado y Moneda', {
            'fields': ('estado', 'moneda')
        }),
        ('Totales', {
            'fields': ('subtotal', 'impuestos', 'total'),
            'classes': ('collapse',)
        }),
        ('Usuarios', {
            'fields': ('usuario_creacion', 'usuario_autorizacion', 'fecha_autorizacion')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def save_formset(self, request, form, formset, change):
        """Sobrescribir para recalcular totales después de guardar detalles"""
        super().save_formset(request, form, formset, change)
        if formset.model == OrdenCompraDetalle:
            form.instance.calcular_totales()
    
    # Acción personalizada para enviar órdenes
    def enviar_ordenes(self, request, queryset):
        updated = queryset.filter(estado='BORRADOR').update(estado='ENVIADA')
        self.message_user(request, f'{updated} órdenes enviadas correctamente.')
    enviar_ordenes.short_description = "Enviar órdenes seleccionadas (solo borradores)"
    
    # Acción personalizada para confirmar órdenes
    def confirmar_ordenes(self, request, queryset):
        updated = queryset.filter(estado='ENVIADA').update(estado='CONFIRMADA')
        self.message_user(request, f'{updated} órdenes confirmadas correctamente.')
    confirmar_ordenes.short_description = "Confirmar órdenes seleccionadas (solo enviadas)"
    
    # Acción personalizada para cancelar órdenes
    def cancelar_ordenes(self, request, queryset):
        updated = queryset.exclude(estado__in=['RECIBIDA_COMPLETA', 'CANCELADA']).update(estado='CANCELADA')
        self.message_user(request, f'{updated} órdenes canceladas correctamente.')
    cancelar_ordenes.short_description = "Cancelar órdenes seleccionadas"
    
    actions = ['enviar_ordenes', 'confirmar_ordenes', 'cancelar_ordenes']


@admin.register(OrdenCompraDetalle)
class OrdenCompraDetalleAdmin(admin.ModelAdmin):
    list_display = ['orden_compra', 'producto', 'cantidad_solicitada', 'cantidad_recibida', 
                   'precio_unitario', 'subtotal', 'porcentaje_recibido']
    list_filter = ['orden_compra__estado', 'orden_compra__proveedor', 'producto__categoria']
    search_fields = ['orden_compra__numero_orden', 'producto__sku', 'producto__nombre']
    ordering = ['-orden_compra__fecha_orden', 'producto__sku']
    list_select_related = ['orden_compra', 'producto', 'unidad_medida']
    
    fieldsets = (
        ('Orden y Producto', {
            'fields': ('orden_compra', 'producto', 'unidad_medida')
        }),
        ('Cantidades', {
            'fields': ('cantidad_solicitada', 'cantidad_recibida')
        }),
        ('Precios', {
            'fields': ('precio_unitario', 'descuento_pct', 'subtotal')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['subtotal']
    
    def porcentaje_recibido(self, obj):
        return f"{obj.porcentaje_recibido:.1f}%"
    porcentaje_recibido.short_description = "% Recibido"
