from django.contrib import admin
from django.utils import timezone
from .models import Bodega, Lote, MovimientoInventario, StockActual, AlertaStock


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'activo', 'created_at']
    list_filter = ['tipo', 'activo', 'created_at']
    search_fields = ['codigo', 'nombre', 'direccion']
    ordering = ['codigo']


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['codigo_lote', 'producto', 'fecha_vencimiento', 'cantidad_disponible', 
                   'cantidad_reservada', 'bodega', 'estado', 'created_at']
    list_filter = ['estado', 'fecha_vencimiento', 'bodega', 'created_at', 'producto__categoria']
    search_fields = ['codigo_lote', 'producto__sku', 'producto__nombre']
    ordering = ['-created_at']
    list_select_related = ['producto', 'bodega', 'proveedor']
    
    fieldsets = (
        ('Información del Lote', {
            'fields': ('codigo_lote', 'producto', 'bodega', 'proveedor')
        }),
        ('Fechas', {
            'fields': ('fecha_produccion', 'fecha_vencimiento')
        }),
        ('Cantidades', {
            'fields': ('cantidad_inicial', 'cantidad_disponible', 'cantidad_reservada')
        }),
        ('Costos', {
            'fields': ('costo_unitario',)
        }),
        ('Estado', {
            'fields': ('estado', 'motivo_bloqueo')
        }),
    )


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['tipo_movimiento', 'fecha_movimiento', 'producto', 'cantidad', 
                   'bodega_origen', 'bodega_destino', 'estado', 'usuario']
    list_filter = ['tipo_movimiento', 'estado', 'fecha_movimiento', 'documento_padre_tipo', 
                  'bodega_origen', 'bodega_destino']
    search_fields = ['producto__sku', 'producto__nombre', 'documento_referencia', 
                    'usuario__user__username']
    ordering = ['-fecha_movimiento']
    list_select_related = ['producto', 'bodega_origen', 'bodega_destino', 'usuario', 'usuario__user', 'lote']
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('tipo_movimiento', 'fecha_movimiento', 'producto', 'cantidad', 'unidad_medida')
        }),
        ('Bodegas', {
            'fields': ('bodega_origen', 'bodega_destino')
        }),
        ('Proveedor y Costos', {
            'fields': ('proveedor', 'costo_unitario', 'costo_total')
        }),
        ('Control de Lote/Serie', {
            'fields': ('lote', 'serie'),
            'classes': ('collapse',)
        }),
        ('Documento de Origen', {
            'fields': ('documento_padre_tipo', 'documento_padre_id', 'documento_referencia')
        }),
        ('Observaciones y Justificación', {
            'fields': ('motivo_ajuste', 'observaciones')
        }),
        ('Estado y Usuarios', {
            'fields': ('estado', 'usuario', 'fecha_confirmacion', 'usuario_confirmacion')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StockActual)
class StockActualAdmin(admin.ModelAdmin):
    list_display = ['producto', 'bodega', 'cantidad_disponible', 'cantidad_reservada', 
                   'cantidad_transito', 'ultimo_ingreso', 'ultima_salida']
    list_filter = ['bodega', 'producto__categoria', 'updated_at']
    search_fields = ['producto__sku', 'producto__nombre', 'bodega__codigo', 'bodega__nombre']
    ordering = ['producto__sku', 'bodega__codigo']
    list_select_related = ['producto', 'bodega']
    
    readonly_fields = ['updated_at']


@admin.register(AlertaStock)
class AlertaStockAdmin(admin.ModelAdmin):
    list_display = ['tipo_alerta', 'producto', 'bodega', 'cantidad_actual', 'prioridad', 
                   'estado', 'fecha_generacion']
    list_filter = ['tipo_alerta', 'prioridad', 'estado', 'fecha_generacion', 'bodega']
    search_fields = ['producto__sku', 'producto__nombre']
    ordering = ['-fecha_generacion', 'prioridad']
    list_select_related = ['producto', 'bodega', 'lote', 'resuelto_por_usuario']
    
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('tipo_alerta', 'producto', 'bodega', 'lote')
        }),
        ('Cantidades y Límites', {
            'fields': ('cantidad_actual', 'cantidad_limite')
        }),
        ('Vencimiento', {
            'fields': ('fecha_vencimiento', 'dias_vencimiento'),
            'classes': ('collapse',)
        }),
        ('Prioridad y Estado', {
            'fields': ('prioridad', 'estado', 'fecha_generacion')
        }),
        ('Resolución', {
            'fields': ('fecha_resolucion', 'resuelto_por_usuario', 'motivo_resolucion'),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    # Acción personalizada para resolver alertas
    def resolver_alertas(self, request, queryset):
        updated = queryset.update(estado='RESUELTA', fecha_resolucion=timezone.now())
        self.message_user(request, f'{updated} alertas resueltas correctamente.')
    resolver_alertas.short_description = "Resolver alertas seleccionadas"
    
    actions = ['resolver_alertas']
