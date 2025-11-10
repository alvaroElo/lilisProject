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
    usuarios_list, usuario_create, usuario_edit, usuario_delete
)

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Autenticación y Dashboard
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # Gestión de Usuarios
    path('usuarios/', usuarios_list, name='usuarios_list'),
    path('usuarios/create/', usuario_create, name='usuario_create'),
    path('usuarios/<int:usuario_id>/edit/', usuario_edit, name='usuario_edit'),
    path('usuarios/<int:usuario_id>/delete/', usuario_delete, name='usuario_delete'),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
