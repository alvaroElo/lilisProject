from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Movimientos de Inventario
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
    path('movimientos/create/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:movimiento_id>/edit/', views.movimiento_edit, name='movimiento_edit'),
    path('movimientos/<int:movimiento_id>/delete/', views.movimiento_delete, name='movimiento_delete'),
    path('movimientos/exportar-excel/', views.exportar_movimientos_excel, name='exportar_movimientos_excel'),
]
