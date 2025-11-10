from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Rol(models.Model):
    ROLES_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Vendedor'),
        ('BODEGUERO', 'Bodeguero'),
        ('FINANZAS', 'Finanzas'),
        ('JEFE_VENTAS', 'Jefe de Ventas'),
    ]
    
    nombre = models.CharField(max_length=50, unique=True, choices=ROLES_CHOICES)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    permisos = models.JSONField(null=True, blank=True, help_text='JSON con permisos del rol')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return f"{self.get_nombre_display()}"


class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
        ('INACTIVO', 'Inactivo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_profile')
    telefono = models.CharField(max_length=30, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True, help_text='Foto de perfil del usuario')
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    area_unidad = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.user.username} ({self.get_estado_display()})"

    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()


class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expira_en = models.DateTimeField()
    usado = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Token de Reseteo de Contraseña'
        verbose_name_plural = 'Tokens de Reseteo de Contraseña'
        indexes = [
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"Token para {self.usuario.user.username}"


class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token_sesion = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    ultimo_actividad = models.DateTimeField()
    expira_en = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'sesiones'
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        indexes = [
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"Sesión de {self.usuario.user.username}"
