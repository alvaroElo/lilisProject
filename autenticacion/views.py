from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from maestros.models import Producto
from inventario.models import AlertaStock, Bodega
from compras.models import OrdenCompra


def login_view(request):
    """Vista de login"""
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Bienvenido {user.get_full_name() or user.username}!')
            
            # Redirigir a la página solicitada o al dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):
    """Vista del dashboard principal"""
    
    # Obtener estadísticas
    context = {
        'productos_count': Producto.objects.filter(estado='ACTIVO').count(),
        'alertas_count': AlertaStock.objects.filter(estado='ACTIVA').count(),
        'ordenes_count': OrdenCompra.objects.filter(estado__in=['BORRADOR', 'ENVIADA', 'CONFIRMADA']).count(),
        'bodegas_count': Bodega.objects.filter(activo=True).count(),
        'notification_count': AlertaStock.objects.filter(estado='ACTIVA').count(),
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def logout_view(request):
    """Vista de logout"""
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
