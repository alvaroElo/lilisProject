/**
 * DULCERÍA LILIS - LOGIN JS
 * Validación de formulario de login
 */

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Limpiar errores previos
            clearErrors();
            
            // Validar campos
            let isValid = true;
            
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (!username.value.trim()) {
                showFieldError(username, 'El nombre de usuario es requerido');
                isValid = false;
            }
            
            if (!password.value) {
                showFieldError(password, 'La contraseña es requerida');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                return false;
            }
            
            // Mostrar loading en botón
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-small"></span> Iniciando sesión...';
            
            // Si hay validación AJAX, descomentar:
            // e.preventDefault();
            // performLogin(username.value, password.value, submitBtn, originalText);
        });
        
        // Limpiar error al escribir
        const inputs = loginForm.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    }
});

/**
 * Mostrar error en campo específico
 */
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    // Crear mensaje de error si no existe
    let errorDiv = field.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    errorDiv.textContent = message;
}

/**
 * Limpiar error de campo específico
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
        errorDiv.remove();
    }
}

/**
 * Limpiar todos los errores
 */
function clearErrors() {
    const invalidFields = document.querySelectorAll('.is-invalid');
    invalidFields.forEach(field => {
        clearFieldError(field);
    });
}

/**
 * Login con AJAX (opcional - descomentar si se usa)
 */
/*
function performLogin(username, password, submitBtn, originalText) {
    fetch('/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect || '/dashboard/';
        } else {
            showLoginError(data.message || 'Credenciales incorrectas');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    })
    .catch(error => {
        showLoginError('Error de conexión. Intente nuevamente.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}
*/

/**
 * Mostrar error general de login
 */
function showLoginError(message) {
    const loginBody = document.querySelector('.login-body');
    
    // Remover alerta anterior si existe
    const oldAlert = loginBody.querySelector('.alert');
    if (oldAlert) {
        oldAlert.remove();
    }
    
    // Crear nueva alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.innerHTML = `
        <strong>Error:</strong> ${message}
    `;
    
    // Insertar al inicio del login-body
    loginBody.insertBefore(alertDiv, loginBody.firstChild);
    
    // Auto-hide después de 5 segundos
    setTimeout(() => {
        alertDiv.style.transition = 'opacity 0.3s';
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

/**
 * Obtener cookie CSRF (para AJAX)
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
