from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from autenticacion.models import Usuario


class RoleBasedAdminMiddleware(MiddlewareMixin):
    """
    Middleware para controlar el acceso al admin según el rol del usuario
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Solo aplicar a rutas del admin
        if not request.path.startswith('/admin/'):
            return None
            
        # Permitir acceso al login del admin
        if request.path in ['/admin/login/', '/admin/logout/']:
            return None
            
        # Si no está autenticado, dejamos que Django maneje el redirect
        if not request.user.is_authenticated:
            return None
            
        # Si es superusuario, permitir acceso completo
        if request.user.is_superuser:
            return None
            
        try:
            usuario_profile = request.user.usuario_profile
            rol = usuario_profile.rol.nombre
        except:
            # Si no tiene perfil o rol, denegar acceso
            return HttpResponseForbidden("No tienes permisos para acceder al admin")
            
        # Definir qué apps puede ver cada rol
        permisos_por_rol = {
            'VENDEDOR': ['productos', 'maestros'],  # Solo productos y maestros
            'BODEGUERO': ['inventario', 'maestros'],  # Solo inventario y maestros
            'FINANZAS': ['compras', 'maestros'],  # Solo compras y maestros
            'JEFE_VENTAS': ['productos', 'maestros', 'compras'],  # Productos, maestros y compras
        }
        
        apps_permitidas = permisos_por_rol.get(rol, [])
        
        # Verificar si está accediendo a una app permitida
        path_parts = request.path.strip('/').split('/')
        if len(path_parts) >= 2:
            app_name = path_parts[1]  # admin/app_name/model_name/
            
            # Permitir acceso al índice del admin
            if app_name == '' or app_name == 'admin':
                return None
                
            # Si la app no está en las permitidas, denegar acceso
            if app_name not in apps_permitidas:
                return HttpResponseForbidden(f"No tienes permisos para acceder a {app_name}")
        
        return None