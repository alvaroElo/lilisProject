"""
Context processors para el proyecto
"""

def permisos_usuario(request):
    """
    Context processor que agrega los permisos del usuario al contexto global
    """
    # Valores por defecto: sin acceso a nada
    permisos = {
        'usuarios': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'proveedores': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False, 'exportar': False},
        'productos': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False},
        'compras': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False},
        'inventario': {'ver': False, 'crear': False, 'editar': False, 'eliminar': False},
    }
    
    if request.user.is_authenticated:
        # Superusuarios tienen acceso total
        if request.user.is_superuser:
            permisos = {
                'usuarios': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'exportar': True},
                'proveedores': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True, 'exportar': True},
                'productos': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
                'compras': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
                'inventario': {'ver': True, 'crear': True, 'editar': True, 'eliminar': True},
            }
        # Usuarios con rol y permisos definidos
        elif hasattr(request.user, 'usuario_profile'):
            usuario = request.user.usuario_profile
            if usuario.rol and usuario.rol.permisos:
                # Sobrescribir solo los módulos que tienen permisos definidos
                for modulo, permisos_modulo in usuario.rol.permisos.items():
                    if modulo in permisos:
                        permisos[modulo].update(permisos_modulo)
    
    return {'permisos_modulos': permisos}
