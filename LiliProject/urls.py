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
from django.contrib.auth import views as auth_views
from . import test_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ============================================
    # RUTAS DE PRUEBA PARA TEMPLATES
    # ============================================
    
    # Autenticación
    path('login/', test_views.test_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', test_views.test_password_reset, name='password_reset'),
    path('password-reset-confirm/', test_views.test_password_reset_confirm, name='password_reset_confirm'),
    
    # Dashboard
    path('', test_views.test_dashboard, name='dashboard'),
    path('dashboard/', test_views.test_dashboard, name='dashboard'),
    
    # Demo de Validaciones
    path('demo/validaciones/', test_views.test_validaciones_demo, name='validaciones_demo'),
    path('demo/estilos-alertas/', test_views.test_estilos_alertas_demo, name='estilos_alertas_demo'),
    
    # Usuarios
    path('usuarios/', test_views.test_usuarios_list, name='usuarios_list'),
    path('usuarios/crear/', test_views.test_usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/', test_views.test_usuario_edit, name='usuario_detail'),
    path('usuarios/<int:pk>/editar/', test_views.test_usuario_edit, name='usuario_edit'),
    
    # Productos
    path('productos/', test_views.test_productos_list, name='productos_list'),
    path('productos/crear/', test_views.test_producto_create, name='productos_create'),
    path('productos/<int:pk>/', test_views.test_producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', test_views.test_producto_edit, name='producto_edit'),
    
    # Proveedores
    path('proveedores/', test_views.test_proveedores_list, name='proveedores_list'),
    path('proveedores/crear/', test_views.test_proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/', test_views.test_proveedor_detail, name='proveedor_detail'),
    path('proveedores/<int:pk>/editar/', test_views.test_proveedor_edit, name='proveedor_edit'),
    
    # Inventario
    path('inventario/', test_views.test_inventario_list, name='inventario_list'),
    path('inventario/movimiento/crear/', test_views.test_movimiento_create, name='movimiento_create'),
    path('inventario/movimiento/<int:pk>/', test_views.test_movimiento_detail, name='movimiento_detail'),
    path('inventario/stock/', test_views.test_stock_list, name='stock_list'),
    
    # Orden de Compra (placeholder)
    path('compras/orden/crear/', test_views.test_orden_compra_create, name='orden_compra_create'),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
