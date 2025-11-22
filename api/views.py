from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from maestros.models import Categoria, Marca
from .serializers import CategoriaSerializer, MarcaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Categoria.
    
    Endpoints:
    - GET /api/categorias/ - Lista todas las categorías
    - POST /api/categorias/ - Crea una nueva categoría
    - GET /api/categorias/<id>/ - Obtiene una categoría específica
    - PUT /api/categorias/<id>/ - Actualiza una categoría
    - DELETE /api/categorias/<id>/ - Elimina una categoría
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class MarcaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Marca.
    
    Endpoints:
    - GET /api/marcas/ - Lista todas las marcas
    - POST /api/marcas/ - Crea una nueva marca
    - GET /api/marcas/<id>/ - Obtiene una marca específica
    - PUT /api/marcas/<id>/ - Actualiza una marca
    - DELETE /api/marcas/<id>/ - Elimina una marca
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
