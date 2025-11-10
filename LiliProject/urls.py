"""
URL configuration for LiliProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from autenticacion.views import (
    login_view, dashboard_view, logout_view,
    usuarios_list, usuario_create, usuario_edit, usuario_delete,
    password_reset_request, password_reset_confirm,
    exportar_usuarios_excel
)
from maestros.views import (
    proveedores_list, proveedor_create, proveedor_edit, proveedor_delete,
    exportar_proveedores_excel
)
from LiliProject.views import error_404, error_500

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Autenticación y Dashboard
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # Recuperación de Contraseña
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    
    # Gestión de Usuarios
    path('usuarios/', usuarios_list, name='usuarios_list'),
    path('usuarios/create/', usuario_create, name='usuario_create'),
    path('usuarios/<int:usuario_id>/edit/', usuario_edit, name='usuario_edit'),
    path('usuarios/<int:usuario_id>/delete/', usuario_delete, name='usuario_delete'),
    path('usuarios/exportar-excel/', exportar_usuarios_excel, name='exportar_usuarios_excel'),
    
    # Gestión de Proveedores
    path('proveedores/', proveedores_list, name='proveedores_list'),
    path('proveedores/create/', proveedor_create, name='proveedor_create'),
    path('proveedores/<int:proveedor_id>/edit/', proveedor_edit, name='proveedor_edit'),
    path('proveedores/<int:proveedor_id>/delete/', proveedor_delete, name='proveedor_delete'),
    path('proveedores/exportar-excel/', exportar_proveedores_excel, name='exportar_proveedores_excel'),
    
    # Rutas de prueba para páginas de error (SOLO PARA DESARROLLO)
    path('test-404/', error_404, name='test_404'),
    path('test-500/', error_500, name='test_500'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Agregar una ruta catch-all al final para páginas 404 personalizadas en DEBUG mode
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^.*$', error_404),
    ]

# Handlers de errores personalizados (funcionan cuando DEBUG=False)
handler404 = 'LiliProject.views.error_404'
handler500 = 'LiliProject.views.error_500'
