from django.db import models
from django.utils import timezone
from decimal import Decimal
from maestros.models import Categoria, Marca, UnidadMedida


class Producto(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('DESCONTINUADO', 'Descontinuado'),
    ]
    
    # Identificación
    sku = models.CharField(max_length=50, unique=True, help_text='Código SKU único')
    ean_upc = models.CharField(max_length=20, null=True, blank=True, 
                              help_text='Código de barras EAN/UPC (opcional, único si se usa)')
    nombre = models.CharField(max_length=255, help_text='Nombre del producto')
    descripcion = models.TextField(null=True, blank=True, help_text='Descripción detallada')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, 
                                 help_text='Categoría del producto')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True,
                             help_text='Marca del producto (opcional)')
    modelo = models.CharField(max_length=100, null=True, blank=True, 
                             help_text='Modelo del producto (opcional)')
    
    # Unidades y precios
    uom_compra = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                 related_name='productos_compra',
                                 help_text='Unidad de medida para compra')
    uom_venta = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, 
                                related_name='productos_venta',
                                help_text='Unidad de medida para venta')
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('1'), 
                                          help_text='Factor conversión de compra a venta (default 1)')
    costo_estandar = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True,
                                        help_text='Costo estándar del producto (opcional)')
    costo_promedio = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, 
                                       help_text='Costo promedio (solo lectura, calculado automáticamente)')
    precio_venta = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True,
                                      help_text='Precio de venta (opcional)')
    impuesto_iva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('19'), 
                                     help_text='Porcentaje IVA (ej: 19 para 19%)')
    
    # Stock y control
    stock_actual = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'),
                                      help_text='Stock actual (calculado automáticamente)')
    stock_minimo = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'),
                                      help_text='Stock mínimo (default 0)')
    stock_maximo = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True,
                                      help_text='Stock máximo (opcional)')
    punto_reorden = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True,
                                       help_text='Punto de reorden (opcional, si no se usa el mínimo)')
    
    # Control especial
    perecible = models.BooleanField(default=False, help_text='Producto perecedero')
    control_por_lote = models.BooleanField(default=False, help_text='Requiere control por lote')
    control_por_serie = models.BooleanField(default=False, help_text='Requiere control por número de serie')
    
    # Relaciones y soporte
    imagen_url = models.URLField(max_length=500, null=True, blank=True, 
                                help_text='URL de la imagen del producto (opcional)')
    ficha_tecnica_url = models.URLField(max_length=500, null=True, blank=True,
                                       help_text='URL de la ficha técnica PDF (opcional)')
    
    # Derivados (solo lectura, calculados automáticamente)
    alerta_bajo_stock = models.BooleanField(default=False, editable=False,
                                           help_text='Se activa cuando stock_actual < stock_minimo')
    alerta_por_vencer = models.BooleanField(default=False, editable=False,
                                           help_text='Se activa cuando hay lotes próximos a vencer')
    
    # Metadatos
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['categoria']),
            models.Index(fields=['estado']),
            models.Index(fields=['alerta_bajo_stock']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sku} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        # Actualizar alerta de bajo stock
        if self.stock_actual < self.stock_minimo:
            self.alerta_bajo_stock = True
        else:
            self.alerta_bajo_stock = False
        super().save(*args, **kwargs)
    
    @property
    def margen_utilidad(self):
        """Calcula el margen de utilidad porcentual"""
        if self.precio_venta and self.costo_promedio and self.costo_promedio > 0:
            return ((self.precio_venta - self.costo_promedio) / self.costo_promedio) * 100
        return None
    
    @property
    def requiere_reorden(self):
        """Indica si el producto requiere reorden"""
        punto = self.punto_reorden if self.punto_reorden else self.stock_minimo
        return self.stock_actual <= punto
