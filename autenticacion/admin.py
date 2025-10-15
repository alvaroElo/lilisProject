from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Rol, Usuario, PasswordResetToken, Sesion


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'created_at']
    list_filter = ['nombre', 'created_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Información Adicional del Usuario'


class UserAdmin(BaseUserAdmin):
    inlines = [UsuarioInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol', 'get_estado', 'is_active']
    list_filter = ['is_active', 'is_staff', 'usuario_profile__estado', 'usuario_profile__rol']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_select_related = ['usuario_profile', 'usuario_profile__rol']
    
    def get_rol(self, obj):
        try:
            return obj.usuario_profile.rol.get_nombre_display()
        except:
            return 'Sin rol'
    get_rol.short_description = 'Rol'
    get_rol.admin_order_field = 'usuario_profile__rol__nombre'
    
    def get_estado(self, obj):
        try:
            return obj.usuario_profile.get_estado_display()
        except:
            return 'Sin estado'
    get_estado.short_description = 'Estado'
    get_estado.admin_order_field = 'usuario_profile__estado'


# Desregistrar el UserAdmin original y registrar el nuevo
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'estado', 'telefono', 'area_unidad', 'ultimo_acceso', 'created_at']
    list_filter = ['estado', 'rol', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'telefono']
    ordering = ['user__username']
    list_select_related = ['user', 'rol']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'rol', 'estado')
        }),
        ('Contacto', {
            'fields': ('telefono', 'area_unidad')
        }),
        ('Información Adicional', {
            'fields': ('observaciones', 'ultimo_acceso'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'token', 'usado', 'expira_en', 'created_at']
    list_filter = ['usado', 'created_at', 'expira_en']
    search_fields = ['usuario__user__username', 'token']
    ordering = ['-created_at']
    readonly_fields = ['token', 'created_at']
    list_select_related = ['usuario', 'usuario__user']


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'token_sesion', 'ip_address', 'ultimo_actividad', 'expira_en', 'created_at']
    list_filter = ['created_at', 'ultimo_actividad', 'expira_en']
    search_fields = ['usuario__user__username', 'ip_address', 'token_sesion']
    ordering = ['-ultimo_actividad']
    readonly_fields = ['token_sesion', 'created_at']
    list_select_related = ['usuario', 'usuario__user']
