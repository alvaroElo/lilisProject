from django.db import models
from django.utils import timezone
from decimal import Decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    categoria_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                                      help_text='Para subcategorías')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'marcas'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    TIPO_CHOICES = [
        ('PESO', 'Peso'),
        ('VOLUMEN', 'Volumen'),
        ('LONGITUD', 'Longitud'),
        ('UNIDAD', 'Unidad'),
        ('TIEMPO', 'Tiempo'),
    ]
    
    codigo = models.CharField(max_length=10, unique=True, help_text='Código único de la unidad (ej: KG, L, UND)')
    nombre = models.CharField(max_length=50, help_text='Nombre completo de la unidad')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    factor_base = models.DecimalField(max_digits=18, decimal_places=6, default=Decimal('1'), 
                                    help_text='Factor de conversión a unidad base del tipo')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'unidades_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['tipo']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Proveedor(models.Model):
    CONDICIONES_PAGO_CHOICES = [
        ('CONTADO', 'Contado'),
        ('30_DIAS', '30 días'),
        ('60_DIAS', '60 días'),
        ('90_DIAS', '90 días'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]
    
    rut_nif = models.CharField(max_length=20, unique=True, help_text='RUT o NIF único')
    razon_social = models.CharField(max_length=255)
    nombre_fantasia = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=128, null=True, blank=True)
    pais = models.CharField(max_length=64, default='Chile')
    condiciones_pago = models.CharField(max_length=20, choices=CONDICIONES_PAGO_CHOICES)
    condiciones_pago_detalle = models.CharField(max_length=255, null=True, blank=True, 
                                              help_text='Detalle si es OTRO')
    moneda = models.CharField(max_length=8, default='CLP', help_text='Código ISO moneda')
    contacto_principal_nombre = models.CharField(max_length=120, null=True, blank=True)
    contacto_principal_email = models.EmailField(null=True, blank=True)
    contacto_principal_telefono = models.CharField(max_length=30, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        indexes = [
            models.Index(fields=['rut_nif']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.razon_social} ({self.rut_nif})"


class ProductoProveedor(models.Model):
    # Importación diferida para evitar dependencias circulares
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=18, decimal_places=6, 
                              help_text='Costo del producto con este proveedor')
    lead_time_dias = models.IntegerField(default=7, help_text='Tiempo de entrega en días')
    min_lote = models.DecimalField(max_digits=18, decimal_places=6, default=Decimal('1'), 
                                 help_text='Cantidad mínima de compra')
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, 
                                      help_text='Porcentaje de descuento')
    preferente = models.BooleanField(default=False, help_text='Proveedor preferente')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos_proveedores'
        verbose_name = 'Producto-Proveedor'
        verbose_name_plural = 'Productos-Proveedores'
        unique_together = ['producto', 'proveedor']
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['proveedor']),
            models.Index(fields=['preferente']),
        ]

    def __str__(self):
        return f"{self.producto.sku} - {self.proveedor.razon_social}"
