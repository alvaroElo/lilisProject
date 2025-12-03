from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Movimientos de Inventario
    path('', views.movimientos_list, name='movimientos_list'),
    path('create/', views.movimiento_create, name='movimiento_create'),
    path('<int:movimiento_id>/edit/', views.movimiento_edit, name='movimiento_edit'),
    path('<int:movimiento_id>/delete/', views.movimiento_delete, name='movimiento_delete'),
    path('exportar-excel/', views.exportar_movimientos_excel, name='exportar_movimientos_excel'),
    
    # AJAX endpoints
    path('bodegas/buscar/', views.buscar_bodegas, name='buscar_bodegas'),
]
