"""
Vistas personalizadas para manejo de errores
"""
from django.shortcuts import render


def error_404(request, exception=None):
    """
    Vista personalizada para error 404 - Página no encontrada
    """
    return render(request, '404.html', status=404)


def error_500(request):
    """
    Vista personalizada para error 500 - Error del servidor
    """
    return render(request, '500.html', status=500)
