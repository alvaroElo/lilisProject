from django.urls import path, include
from rest_framework import routers
from .views import CategoriaViewSet, MarcaViewSet
from rest_framework.authtoken.views import obtain_auth_token   # importa la vista para obtener el token

# Router para las APIs
router = routers.DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_login'),  # Endpoint para obtener el token
]