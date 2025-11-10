# 📧 Configuración de Email - Sistema de Recuperación de Contraseña

Este documento muestra todas las configuraciones y código relacionado con el envío de emails en el sistema.

---

## 📋 Tabla de Contenidos
1. [Configuración en Settings](#configuración-en-settings)
2. [Vista de Recuperación de Contraseña](#vista-de-recuperación-de-contraseña)
3. [Template HTML del Email](#template-html-del-email)
4. [Modo Desarrollo vs Producción](#modo-desarrollo-vs-producción)
5. [Instalación de Dependencias](#instalación-de-dependencias)

---

## 1. Configuración en Settings

**Archivo:** `LiliProject/settings.py`

```python
# Resend Email Configuration
RESEND_API_KEY = 're_U7GLhZyZ_9GCv9DF3aVgDepLzuA9NNjyS'
RESEND_FROM_EMAIL = 'onboarding@resend.dev'
RESEND_TEST_EMAIL = 'alvaro.elo@alumnos.ucn.cl'  # Email verificado en Resend para pruebas
COMPANY_NAME = 'Dulcería Lilis'
```

### Variables:
- **RESEND_API_KEY**: API Key de Resend para autenticación
- **RESEND_FROM_EMAIL**: Email remitente (requiere dominio verificado en producción)
- **RESEND_TEST_EMAIL**: Email de prueba para desarrollo (solo emails a este destino en modo test)
- **COMPANY_NAME**: Nombre de la empresa usado en los emails

---

## 2. Vista de Recuperación de Contraseña

**Archivo:** `autenticacion/views.py`

### Importaciones necesarias:
```python
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
import resend
import traceback
```

### Función completa:
```python
def password_reset_request(request):
    """Vista para solicitar recuperación de contraseña"""
    
    if request.method == 'POST':
        email = request.POST.get('email')
        reset_link = None
        email_sent = False
        
        try:
            # Buscar usuario por email
            user = User.objects.get(email=email)
            
            # Generar token de recuperación
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir el link de recuperación
            reset_link = request.build_absolute_uri(
                f'/password-reset-confirm/{uid}/{token}/'
            )
            
            # Enviar email con Resend
            try:
                import resend
                from django.conf import settings
                
                resend.api_key = settings.RESEND_API_KEY
                
                # Nombre completo del usuario o username
                user_name = user.get_full_name() or user.username
                
                # HTML del email (ver sección siguiente)
                html_content = f"""[HTML CONTENT]"""
                
                # En modo de prueba, enviar a email verificado
                # En producción con dominio verificado, enviar al email del usuario
                destination_email = settings.RESEND_TEST_EMAIL if hasattr(settings, 'RESEND_TEST_EMAIL') else email
                
                # Enviar email
                r = resend.Emails.send({
                    "from": settings.RESEND_FROM_EMAIL,
                    "to": destination_email,
                    "subject": f"🔐 Recuperación de Contraseña - {settings.COMPANY_NAME}",
                    "html": html_content
                })
                
                email_sent = True
                
                # Mensaje informativo en desarrollo
                if destination_email != email:
                    print(f"[DESARROLLO] Email de recuperación para {email} enviado a {destination_email}")
                
            except Exception as email_error:
                # Si falla el envío de email, registrar el error
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error al enviar email: {email_error}")
                print(f"Detalle completo: {error_detail}")
                email_sent = False
            
        except User.DoesNotExist:
            # Por seguridad, no revelar que el email no existe
            pass
        except Exception as e:
            messages.error(request, 'Error al procesar la solicitud. Intenta nuevamente.')
            return render(request, 'password_reset.html')
        
        # Siempre mostrar un mensaje genérico por seguridad
        if reset_link:
            if email_sent:
                # Email enviado exitosamente
                from django.conf import settings
                if hasattr(settings, 'RESEND_TEST_EMAIL') and email != settings.RESEND_TEST_EMAIL:
                    # Modo de desarrollo - informar que se envió al email de prueba
                    messages.success(request, f'✅ Correo enviado exitosamente a {settings.RESEND_TEST_EMAIL} (modo prueba)')
                    messages.info(request, f'ℹ️ En producción se enviaría a: {email}')
                else:
                    messages.success(request, f'Se ha enviado un correo a {email} con las instrucciones para restablecer tu contraseña.')
            else:
                # Falló el envío - mostrar el link (solo en desarrollo)
                messages.warning(request, 'El correo no pudo ser enviado. Usa el siguiente enlace:')
                return render(request, 'password_reset.html', {
                    'reset_link': reset_link,
                    'email': email
                })
        else:
            # Usuario no existe - mensaje genérico sin revelar
            messages.success(request, 'Si el correo está registrado, recibirás las instrucciones para restablecer tu contraseña.')
        
        return render(request, 'password_reset.html')
    
    return render(request, 'password_reset.html')
```

---

## 3. Template HTML del Email

El contenido HTML del email se genera dinámicamente en la vista:

```python
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #D20A11 0%, #8B0000 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; padding: 15px 30px; background: #D20A11; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍬 {settings.COMPANY_NAME}</h1>
            <p style="margin: 0;">Recuperación de Contraseña</p>
        </div>
        <div class="content">
            <h2>Hola, {user_name}!</h2>
            <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.</p>
            <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
            
            <div style="text-align: center;">
                <a href="{reset_link}" class="button">Restablecer Contraseña</a>
            </div>
            
            <p>O copia y pega este enlace en tu navegador:</p>
            <p style="background: white; padding: 10px; border-radius: 5px; word-break: break-all; font-size: 12px;">
                {reset_link}
            </p>
            
            <div class="warning">
                <strong>⚠️ Importante:</strong>
                <ul style="margin: 10px 0;">
                    <li>Este enlace es válido por <strong>24 horas</strong></li>
                    <li>Si no solicitaste este cambio, ignora este correo</li>
                    <li>Tu contraseña actual seguirá siendo válida</li>
                </ul>
            </div>
            
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                Si tienes problemas con el botón, copia y pega el enlace directamente en tu navegador.
            </p>
        </div>
        <div class="footer">
            <p>Este correo fue enviado desde {settings.COMPANY_NAME}</p>
            <p>© 2025 {settings.COMPANY_NAME}. Todos los derechos reservados.</p>
        </div>
    </div>
</body>
</html>
"""
```

### Variables dinámicas en el template:
- `{settings.COMPANY_NAME}`: Nombre de la empresa
- `{user_name}`: Nombre completo del usuario o username
- `{reset_link}`: URL completa para restablecer contraseña

---

## 4. Modo Desarrollo vs Producción

### 🔧 Modo Desarrollo (Actual)
```python
# En settings.py
RESEND_TEST_EMAIL = 'alvaro.elo@alumnos.ucn.cl'

# En views.py - Línea de envío
destination_email = settings.RESEND_TEST_EMAIL if hasattr(settings, 'RESEND_TEST_EMAIL') else email
```

**Comportamiento:**
- ✅ Todos los emails se envían a `alvaro.elo@alumnos.ucn.cl`
- ✅ Muestra mensaje indicando modo prueba
- ✅ Informa a qué email se enviaría en producción
- ✅ No requiere dominio verificado

### 🚀 Modo Producción

**Para activar modo producción:**

1. **Verificar un dominio en Resend:**
   - Ir a: https://resend.com/domains
   - Agregar tu dominio (ej: dulcerialilis.cl)
   - Configurar registros DNS (MX, SPF, DKIM)

2. **Actualizar `settings.py`:**
```python
# Cambiar el email remitente a tu dominio verificado
RESEND_FROM_EMAIL = 'noreply@dulcerialilis.cl'

# Comentar o eliminar RESEND_TEST_EMAIL para modo producción
# RESEND_TEST_EMAIL = 'alvaro.elo@alumnos.ucn.cl'
```

3. **El código automáticamente detecta el modo:**
```python
# Si RESEND_TEST_EMAIL existe → modo desarrollo
# Si NO existe → modo producción (envía al email real del usuario)
destination_email = settings.RESEND_TEST_EMAIL if hasattr(settings, 'RESEND_TEST_EMAIL') else email
```

---

## 5. Instalación de Dependencias

### Instalar Resend:
```bash
pip install resend
```

### Agregar a requirements.txt:
```txt
resend==2.0.0
```

---

## 📊 Flujo Completo del Sistema

```
1. Usuario solicita recuperación
   ↓
2. Sistema verifica email en BD
   ↓
3. Genera token único (válido 24h)
   ↓
4. Crea URL de recuperación
   ↓
5. Envía email con Resend
   ├─ Desarrollo: a alvaro.elo@alumnos.ucn.cl
   └─ Producción: al email del usuario
   ↓
6. Usuario recibe email
   ↓
7. Click en botón/link
   ↓
8. Valida token
   ↓
9. Permite cambiar contraseña
   ↓
10. Guarda nueva contraseña
```

---

## 🔒 Características de Seguridad

1. **Token de un solo uso**: Django genera tokens únicos e irrepetibles
2. **Válido 24 horas**: Después expira automáticamente
3. **No revela información**: Mensaje genérico si el email no existe
4. **Hash seguro**: Las contraseñas se almacenan con hash
5. **HTTPS recomendado**: Para proteger el token en tránsito

---

## 🐛 Debugging

### Ver errores en consola:
Los errores se imprimen con traceback completo:
```python
print(f"Error al enviar email: {email_error}")
print(f"Detalle completo: {error_detail}")
```

### Errores comunes:

1. **"You can only send testing emails to your own email"**
   - Causa: API key en modo prueba
   - Solución: Ya configurado con `RESEND_TEST_EMAIL`

2. **"Invalid API key"**
   - Causa: API key incorrecta o expirada
   - Solución: Verificar en https://resend.com/api-keys

3. **"Domain not verified"**
   - Causa: Intentando enviar desde dominio no verificado
   - Solución: Usar 'onboarding@resend.dev' o verificar dominio

---

## 📝 URLs Configuradas

**Archivo:** `LiliProject/urls.py`

```python
from autenticacion.views import (
    password_reset_request, 
    password_reset_confirm
)

urlpatterns = [
    # Recuperación de Contraseña
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
```

---

## ✅ Testing

### Probar en desarrollo:
1. Ir a: http://127.0.0.1:8000/password-reset/
2. Ingresar email de un usuario existente
3. El email llegará a: alvaro.elo@alumnos.ucn.cl
4. Verificar bandeja de entrada
5. Click en el link del email
6. Cambiar contraseña
7. Probar login con nueva contraseña

---

## 📞 Contacto y Soporte

- **Resend Dashboard**: https://resend.com/
- **Documentación Resend**: https://resend.com/docs
- **API Keys**: https://resend.com/api-keys
- **Dominios**: https://resend.com/domains

---

**Última actualización:** Noviembre 10, 2025  
**Versión del sistema:** Django 5.2.7  
**Versión de Resend:** 2.0.0
