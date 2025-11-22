from rest_framework import serializers
from maestros.models import Categoria, Marca


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activo']


class MarcaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Marca"""
    
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion', 'activo']
