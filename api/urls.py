from django.urls import path, include
from rest_framework import routers
from .views import CategoriaViewSet, MarcaViewSet

# Router para las APIs
router = routers.DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]