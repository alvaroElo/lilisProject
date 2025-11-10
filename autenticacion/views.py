from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from maestros.models import Producto
from inventario.models import AlertaStock, Bodega
from compras.models import OrdenCompra
from .models import Usuario, Rol


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
        'active_menu': 'dashboard',  # Para resaltar en el menú
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


@login_required(login_url='login')
def usuarios_list(request):
    """Vista de listado de usuarios con filtros y paginación"""
    
    # Obtener parámetros de búsqueda y filtros
    search = request.GET.get('search', '')
    rol_filter = request.GET.get('rol', '')
    estado_filter = request.GET.get('estado', '')
    per_page = request.GET.get('per_page', '10')
    
    # Query base
    usuarios = Usuario.objects.select_related('user', 'rol').all()
    
    # Aplicar filtros
    if search:
        usuarios = usuarios.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    if rol_filter:
        usuarios = usuarios.filter(rol__nombre=rol_filter)
    
    if estado_filter:
        usuarios = usuarios.filter(estado=estado_filter)
    
    # Ordenar por fecha de creación (más recientes primero)
    usuarios = usuarios.order_by('-created_at')
    
    # Estadísticas
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(estado='ACTIVO').count()
    usuarios_bloqueados = Usuario.objects.filter(estado='BLOQUEADO').count()
    usuarios_inactivos = Usuario.objects.filter(estado='INACTIVO').count()
    
    # Paginación
    try:
        per_page = int(per_page)
        if per_page not in [10, 20, 30]:
            per_page = 10
    except ValueError:
        per_page = 10
    
    paginator = Paginator(usuarios, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Obtener todos los roles para el filtro
    roles = Rol.objects.all()
    
    context = {
        'active_menu': 'usuarios',
        'page_obj': page_obj,
        'usuarios': page_obj.object_list,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'usuarios_bloqueados': usuarios_bloqueados,
        'usuarios_inactivos': usuarios_inactivos,
        'roles': roles,
        'search': search,
        'rol_filter': rol_filter,
        'estado_filter': estado_filter,
        'per_page': per_page,
    }
    
    return render(request, 'usuarios/usuarios_list.html', context)


@login_required(login_url='login')
def usuario_create(request):
    """Vista para crear un nuevo usuario (AJAX)"""
    
    if request.method == 'POST':
        try:
            # Datos del usuario Django
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            
            # Datos del perfil Usuario
            rol_id = request.POST.get('rol')
            telefono = request.POST.get('telefono', '')
            area_unidad = request.POST.get('area_unidad', '')
            estado = request.POST.get('estado', 'ACTIVO')
            
            # Validaciones básicas
            if not username or not email or not password or not rol_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos obligatorios deben ser completados.'
                }, status=400)
            
            # Verificar si el username ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': f'El nombre de usuario "{username}" ya está en uso.'
                }, status=400)
            
            # Verificar si el email ya existe
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': f'El email "{email}" ya está registrado.'
                }, status=400)
            
            # Crear usuario Django
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # Crear perfil Usuario
            rol = Rol.objects.get(id=rol_id)
            usuario = Usuario.objects.create(
                user=user,
                rol=rol,
                telefono=telefono,
                area_unidad=area_unidad,
                estado=estado
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {username} creado exitosamente.',
                'redirect': '/usuarios/'
            })
            
        except Rol.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El rol seleccionado no existe.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al crear usuario: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


@login_required(login_url='login')
def usuario_edit(request, usuario_id):
    """Vista para editar un usuario (AJAX)"""
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del User de Django
            usuario.user.first_name = request.POST.get('first_name', '')
            usuario.user.last_name = request.POST.get('last_name', '')
            usuario.user.email = request.POST.get('email', '')
            
            # Actualizar contraseña solo si se proporciona
            new_password = request.POST.get('password', '')
            if new_password:
                usuario.user.set_password(new_password)
            
            usuario.user.save()
            
            # Actualizar datos del perfil Usuario
            rol_id = request.POST.get('rol')
            if rol_id:
                usuario.rol = Rol.objects.get(id=rol_id)
            
            usuario.telefono = request.POST.get('telefono', '')
            usuario.area_unidad = request.POST.get('area_unidad', '')
            usuario.estado = request.POST.get('estado', 'ACTIVO')
            usuario.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {usuario.user.username} actualizado exitosamente.',
                'redirect': '/usuarios/'
            })
            
        except Rol.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'El rol seleccionado no existe.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al actualizar usuario: {str(e)}'
            }, status=500)
    
    # GET - Devolver datos del usuario en JSON
    return JsonResponse({
        'id': usuario.id,
        'username': usuario.user.username,
        'email': usuario.user.email,
        'first_name': usuario.user.first_name,
        'last_name': usuario.user.last_name,
        'rol_id': usuario.rol.id,
        'telefono': usuario.telefono or '',
        'area_unidad': usuario.area_unidad or '',
        'estado': usuario.estado,
    })


@login_required(login_url='login')
def usuario_delete(request, usuario_id):
    """Vista para desactivar un usuario (soft delete)"""
    
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuario, id=usuario_id)
            
            # No permitir eliminar el propio usuario
            if usuario.user == request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'No puedes desactivar tu propio usuario.'
                }, status=400)
            
            # Desactivar usuario (soft delete)
            usuario.estado = 'INACTIVO'
            usuario.user.is_active = False
            usuario.save()
            usuario.user.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {usuario.user.username} desactivado exitosamente.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al desactivar usuario: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)
