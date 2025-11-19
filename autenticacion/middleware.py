from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from autenticacion.models import Usuario


class NoCacheAfterLogoutMiddleware(MiddlewareMixin):
    """
    Middleware para prevenir el acceso a páginas cacheadas después del logout
    mediante el botón 'Atrás' del navegador
    """
    
    def process_response(self, request, response):
        # Aplicar headers de no-cache a todas las páginas protegidas
        if request.user.is_authenticated:
            # Prevenir cualquier tipo de caché en el navegador
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response


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
            
        # Verificar que tenga perfil de usuario
        try:
            usuario_profile = request.user.usuario_profile
            rol = usuario_profile.rol.nombre
        except:
            # Si no tiene perfil, solo permitir logout
            if request.path != '/admin/logout/':
                return HttpResponseForbidden("No tienes un perfil de usuario configurado")
            return None
            
        # Permitir acceso al índice del admin para usuarios con staff
        if request.path == '/admin/' and request.user.is_staff:
            return None
            
        # Para rutas específicas de modelos, Django manejará los permisos
        # Este middleware solo bloquea accesos no autorizados básicos
        return None