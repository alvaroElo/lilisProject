#!/usr/bin/env python
"""
Script para verificar que los templates están listos para visualizar
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiliProject.settings')
django.setup()

from pathlib import Path
from django.conf import settings

def check_file_exists(file_path, description):
    """Verifica si un archivo existe"""
    if file_path.exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO EXISTE")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 VERIFICACIÓN DE TEMPLATES Y ARCHIVOS")
    print("="*60 + "\n")
    
    BASE_DIR = settings.BASE_DIR
    all_ok = True
    
    # Verificar estructura de carpetas
    print("📁 Verificando estructura de carpetas...\n")
    
    folders = [
        (BASE_DIR / 'templates', "Carpeta templates"),
        (BASE_DIR / 'static', "Carpeta static"),
        (BASE_DIR / 'static' / 'css', "Carpeta static/css"),
        (BASE_DIR / 'static' / 'js', "Carpeta static/js"),
        (BASE_DIR / 'static' / 'img', "Carpeta static/img"),
    ]
    
    for folder, desc in folders:
        if not check_file_exists(folder, desc):
            all_ok = False
    
    # Verificar templates HTML
    print("\n📄 Verificando templates HTML...\n")
    
    templates = [
        'base.html',
        'login.html',
        'password_reset.html',
        'password_reset_confirm.html',
        'dashboard.html',
        'usuarios_list.html',
        'usuario_form.html',
        'productos_list.html',
        'producto_form.html',
        'proveedores_list.html',
        'inventario_list.html',
    ]
    
    for template in templates:
        template_path = BASE_DIR / 'templates' / template
        if not check_file_exists(template_path, f"Template {template}"):
            all_ok = False
    
    # Verificar archivos estáticos
    print("\n🎨 Verificando archivos estáticos...\n")
    
    static_files = [
        ('static/css/styles.css', "CSS principal"),
        ('static/js/main.js', "JavaScript principal"),
    ]
    
    for file_path, desc in static_files:
        full_path = BASE_DIR / file_path
        if not check_file_exists(full_path, desc):
            all_ok = False
    
    # Verificar archivos de configuración
    print("\n⚙️ Verificando archivos de configuración...\n")
    
    config_files = [
        ('LiliProject/test_views.py', "Vistas de prueba"),
        ('LiliProject/urls.py', "URLs"),
        ('LiliProject/settings.py', "Settings"),
    ]
    
    for file_path, desc in config_files:
        full_path = BASE_DIR / file_path
        if not check_file_exists(full_path, desc):
            all_ok = False
    
    # Verificar configuración de Django
    print("\n🔧 Verificando configuración Django...\n")
    
    templates_dirs = settings.TEMPLATES[0].get('DIRS', [])
    if BASE_DIR / 'templates' in templates_dirs:
        print(f"✅ TEMPLATES DIRS configurado correctamente")
    else:
        print(f"❌ TEMPLATES DIRS no está configurado")
        all_ok = False
    
    if hasattr(settings, 'STATICFILES_DIRS'):
        print(f"✅ STATICFILES_DIRS configurado: {settings.STATICFILES_DIRS}")
    else:
        print(f"❌ STATICFILES_DIRS no está configurado")
        all_ok = False
    
    # Verificar datos en BD
    print("\n💾 Verificando datos en la base de datos...\n")
    
    try:
        from maestros.models import Producto, Categoria, Proveedor
        from autenticacion.models import Usuario
        from inventario.models import Bodega
        
        productos_count = Producto.objects.count()
        categorias_count = Categoria.objects.count()
        proveedores_count = Proveedor.objects.count()
        usuarios_count = Usuario.objects.count()
        bodegas_count = Bodega.objects.count()
        
        print(f"✅ Productos: {productos_count}")
        print(f"✅ Categorías: {categorias_count}")
        print(f"✅ Proveedores: {proveedores_count}")
        print(f"✅ Usuarios: {usuarios_count}")
        print(f"✅ Bodegas: {bodegas_count}")
        
        if productos_count == 0:
            print("\n⚠️  No hay productos. Ejecuta: python cargar_datos.py")
    except Exception as e:
        print(f"❌ Error al verificar BD: {e}")
        print("⚠️  Ejecuta: python cargar_datos.py")
    
    # Resumen final
    print("\n" + "="*60)
    if all_ok:
        print("✅ TODO LISTO! Puedes ejecutar:")
        print("   python manage.py runserver")
        print("\nY visitar:")
        print("   - Login: http://127.0.0.1:8000/login/")
        print("   - Dashboard: http://127.0.0.1:8000/dashboard/")
        print("   - Productos: http://127.0.0.1:8000/productos/")
        print("\nUsuario de prueba:")
        print("   admin / admin123")
    else:
        print("❌ Hay problemas. Revisa los errores arriba.")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
