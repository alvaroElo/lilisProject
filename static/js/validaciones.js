/**
 * Sistema de Validaciones para Formularios
 * Dulcería Lilis - Sistema de Gestión
 * 
 * Funciones de validación reutilizables para todos los formularios del sistema
 */

// ============================================================================
// VALIDACIÓN DE RUT CHILENO
// ============================================================================

/**
 * Formatea un RUT chileno agregando puntos y guión
 * @param {string} rut - RUT sin formato
 * @returns {string} RUT formateado (ej: 12.345.678-9)
 */
function formatearRUT(rut) {
    // Eliminar todo excepto números y K
    rut = rut.replace(/[^0-9kK]/g, '').toUpperCase();
    
    if (rut.length < 2) return rut;
    
    // Separar número del dígito verificador
    let numero = rut.slice(0, -1);
    let dv = rut.slice(-1);
    
    // Agregar puntos cada 3 dígitos
    numero = numero.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    
    return `${numero}-${dv}`;
}

/**
 * Calcula el dígito verificador de un RUT
 * @param {string} rut - Número del RUT sin DV
 * @returns {string} Dígito verificador (0-9 o K)
 */
function calcularDVRUT(rut) {
    let suma = 0;
    let multiplo = 2;
    
    // Procesar de derecha a izquierda
    for (let i = rut.length - 1; i >= 0; i--) {
        suma += multiplo * parseInt(rut.charAt(i));
        multiplo = multiplo < 7 ? multiplo + 1 : 2;
    }
    
    let resto = suma % 11;
    let dv = 11 - resto;
    
    if (dv === 11) return '0';
    if (dv === 10) return 'K';
    return dv.toString();
}

/**
 * Valida si un RUT chileno es válido
 * @param {string} rut - RUT a validar
 * @returns {boolean} True si es válido
 */
function validarRUT(rut) {
    // Eliminar formato
    rut = rut.replace(/[^0-9kK]/g, '').toUpperCase();
    
    if (rut.length < 2) return false;
    
    // Separar número y DV
    let numero = rut.slice(0, -1);
    let dv = rut.slice(-1);
    
    // Validar que el número sea numérico
    if (!/^\d+$/.test(numero)) return false;
    
    // Calcular DV esperado
    let dvEsperado = calcularDVRUT(numero);
    
    return dv === dvEsperado;
}

/**
 * Aplica validación de RUT a un campo input
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionRUT(input) {
    // Formatear mientras escribe
    input.addEventListener('input', function() {
        let cursorPos = this.selectionStart;
        let valueBefore = this.value;
        
        this.value = formatearRUT(this.value);
        
        // Ajustar posición del cursor
        if (this.value.length > valueBefore.length) {
            cursorPos++;
        }
        this.setSelectionRange(cursorPos, cursorPos);
    });
    
    // Validar al perder foco
    input.addEventListener('blur', function() {
        if (this.value && !validarRUT(this.value)) {
            this.classList.add('is-invalid');
            mostrarError(this, 'RUT inválido');
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE EMAIL
// ============================================================================

/**
 * Valida formato de correo electrónico
 * @param {string} email - Email a validar
 * @returns {boolean} True si es válido
 */
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Aplica validación de email a un campo input
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionEmail(input) {
    input.addEventListener('blur', function() {
        if (this.value && !validarEmail(this.value)) {
            this.classList.add('is-invalid');
            mostrarError(this, 'Email inválido');
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE TELÉFONO
// ============================================================================

/**
 * Formatea número de teléfono chileno
 * @param {string} telefono - Teléfono sin formato
 * @returns {string} Teléfono formateado
 */
function formatearTelefono(telefono) {
    // Eliminar todo excepto números y +
    telefono = telefono.replace(/[^0-9+]/g, '');
    
    // Si empieza con 569, agregar +
    if (telefono.startsWith('569') && telefono.length > 3) {
        return `+${telefono}`;
    }
    
    return telefono;
}

/**
 * Valida formato de teléfono chileno
 * @param {string} telefono - Teléfono a validar
 * @returns {boolean} True si es válido
 */
function validarTelefono(telefono) {
    // Celular: +56 9 XXXX XXXX (11 dígitos con código)
    // Fijo: +56 X XXXX XXXX (10-11 dígitos)
    telefono = telefono.replace(/[^0-9]/g, '');
    
    return telefono.length >= 9 && telefono.length <= 11;
}

/**
 * Aplica validación de teléfono a un campo input
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionTelefono(input) {
    input.addEventListener('input', function() {
        this.value = formatearTelefono(this.value);
    });
    
    input.addEventListener('blur', function() {
        if (this.value && !validarTelefono(this.value)) {
            this.classList.add('is-invalid');
            mostrarError(this, 'Teléfono inválido (mínimo 9 dígitos)');
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE NÚMEROS
// ============================================================================

/**
 * Valida que un valor sea numérico y esté en rango
 * @param {string} valor - Valor a validar
 * @param {number} min - Valor mínimo (opcional)
 * @param {number} max - Valor máximo (opcional)
 * @returns {boolean} True si es válido
 */
function validarNumero(valor, min = null, max = null) {
    const numero = parseFloat(valor);
    
    if (isNaN(numero)) return false;
    if (min !== null && numero < min) return false;
    if (max !== null && numero > max) return false;
    
    return true;
}

/**
 * Aplica validación numérica a un campo input
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionNumero(input) {
    const min = input.getAttribute('min') ? parseFloat(input.getAttribute('min')) : null;
    const max = input.getAttribute('max') ? parseFloat(input.getAttribute('max')) : null;
    
    input.addEventListener('input', function() {
        // Solo permitir números y punto decimal
        this.value = this.value.replace(/[^0-9.]/g, '');
        
        // Evitar múltiples puntos decimales
        const parts = this.value.split('.');
        if (parts.length > 2) {
            this.value = parts[0] + '.' + parts.slice(1).join('');
        }
    });
    
    input.addEventListener('blur', function() {
        if (this.value && !validarNumero(this.value, min, max)) {
            this.classList.add('is-invalid');
            let mensaje = 'Número inválido';
            if (min !== null && max !== null) {
                mensaje = `Debe estar entre ${min} y ${max}`;
            } else if (min !== null) {
                mensaje = `Debe ser mayor o igual a ${min}`;
            } else if (max !== null) {
                mensaje = `Debe ser menor o igual a ${max}`;
            }
            mostrarError(this, mensaje);
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE TEXTO
// ============================================================================

/**
 * Valida longitud de texto
 * @param {string} texto - Texto a validar
 * @param {number} minLength - Longitud mínima (opcional)
 * @param {number} maxLength - Longitud máxima (opcional)
 * @returns {boolean} True si es válido
 */
function validarTexto(texto, minLength = null, maxLength = null) {
    if (minLength !== null && texto.length < minLength) return false;
    if (maxLength !== null && texto.length > maxLength) return false;
    return true;
}

/**
 * Aplica validación de texto a un campo input
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionTexto(input) {
    const minLength = input.getAttribute('minlength') ? parseInt(input.getAttribute('minlength')) : null;
    const maxLength = input.getAttribute('maxlength') ? parseInt(input.getAttribute('maxlength')) : null;
    
    input.addEventListener('blur', function() {
        if (this.value && !validarTexto(this.value, minLength, maxLength)) {
            this.classList.add('is-invalid');
            let mensaje = 'Texto inválido';
            if (minLength !== null) {
                mensaje = `Debe tener al menos ${minLength} caracteres`;
            }
            mostrarError(this, mensaje);
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE CAMPOS REQUERIDOS
// ============================================================================

/**
 * Valida que un campo requerido no esté vacío
 * @param {HTMLInputElement} input - Campo de entrada
 * @returns {boolean} True si es válido
 */
function validarRequerido(input) {
    if (input.type === 'checkbox' || input.type === 'radio') {
        return input.checked;
    }
    return input.value.trim() !== '';
}

/**
 * Aplica validación de campo requerido
 * @param {HTMLInputElement} input - Campo de entrada
 */
function aplicarValidacionRequerido(input) {
    input.addEventListener('blur', function() {
        if (this.hasAttribute('required') && !validarRequerido(this)) {
            this.classList.add('is-invalid');
            mostrarError(this, 'Este campo es obligatorio');
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// VALIDACIÓN DE FECHAS
// ============================================================================

/**
 * Valida que una fecha esté en formato válido
 * @param {string} fecha - Fecha en formato YYYY-MM-DD
 * @returns {boolean} True si es válida
 */
function validarFecha(fecha) {
    if (!fecha) return false;
    const date = new Date(fecha);
    return date instanceof Date && !isNaN(date);
}

/**
 * Aplica validación de fecha a un campo input
 * @param {HTMLInputElement} input - Campo de entrada tipo date
 */
function aplicarValidacionFecha(input) {
    input.addEventListener('blur', function() {
        if (this.value && !validarFecha(this.value)) {
            this.classList.add('is-invalid');
            mostrarError(this, 'Fecha inválida');
        } else {
            this.classList.remove('is-invalid');
            ocultarError(this);
        }
    });
}

// ============================================================================
// FUNCIONES DE UI PARA MOSTRAR ERRORES
// ============================================================================

/**
 * Muestra mensaje de error bajo un campo
 * @param {HTMLInputElement} input - Campo con error
 * @param {string} mensaje - Mensaje de error
 */
function mostrarError(input, mensaje) {
    // Buscar si ya existe un mensaje de error
    let errorDiv = input.parentElement.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        input.parentElement.appendChild(errorDiv);
    }
    
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
}

/**
 * Oculta mensaje de error de un campo
 * @param {HTMLInputElement} input - Campo sin error
 */
function ocultarError(input) {
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// ============================================================================
// INICIALIZACIÓN AUTOMÁTICA
// ============================================================================

/**
 * Inicializa validaciones en todos los campos del formulario
 * @param {HTMLFormElement} formulario - Formulario a validar (opcional)
 */
function inicializarValidaciones(formulario = document) {
    // Validación de RUT
    formulario.querySelectorAll('input[data-tipo="rut"]').forEach(input => {
        aplicarValidacionRUT(input);
    });
    
    // Validación de Email
    formulario.querySelectorAll('input[type="email"], input[data-tipo="email"]').forEach(input => {
        aplicarValidacionEmail(input);
    });
    
    // Validación de Teléfono
    formulario.querySelectorAll('input[data-tipo="telefono"]').forEach(input => {
        aplicarValidacionTelefono(input);
    });
    
    // Validación de Números
    formulario.querySelectorAll('input[type="number"], input[data-tipo="numero"]').forEach(input => {
        aplicarValidacionNumero(input);
    });
    
    // Validación de Texto
    formulario.querySelectorAll('input[type="text"], textarea').forEach(input => {
        if (!input.hasAttribute('data-tipo')) {
            aplicarValidacionTexto(input);
        }
    });
    
    // Validación de Fechas
    formulario.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(input => {
        aplicarValidacionFecha(input);
    });
    
    // Validación de Campos Requeridos
    formulario.querySelectorAll('input[required], select[required], textarea[required]').forEach(input => {
        aplicarValidacionRequerido(input);
    });
}

/**
 * Valida todo el formulario antes de enviar
 * @param {HTMLFormElement} formulario - Formulario a validar
 * @returns {boolean} True si todo es válido
 */
function validarFormulario(formulario) {
    let esValido = true;
    
    // Validar todos los campos requeridos
    formulario.querySelectorAll('[required]').forEach(input => {
        if (!validarRequerido(input)) {
            input.classList.add('is-invalid');
            mostrarError(input, 'Este campo es obligatorio');
            esValido = false;
        }
    });
    
    // Validar RUTs
    formulario.querySelectorAll('input[data-tipo="rut"]').forEach(input => {
        if (input.value && !validarRUT(input.value)) {
            input.classList.add('is-invalid');
            mostrarError(input, 'RUT inválido');
            esValido = false;
        }
    });
    
    // Validar Emails
    formulario.querySelectorAll('input[type="email"], input[data-tipo="email"]').forEach(input => {
        if (input.value && !validarEmail(input.value)) {
            input.classList.add('is-invalid');
            mostrarError(input, 'Email inválido');
            esValido = false;
        }
    });
    
    // Validar Teléfonos
    formulario.querySelectorAll('input[data-tipo="telefono"]').forEach(input => {
        if (input.value && !validarTelefono(input.value)) {
            input.classList.add('is-invalid');
            mostrarError(input, 'Teléfono inválido');
            esValido = false;
        }
    });
    
    // Validar Números
    formulario.querySelectorAll('input[type="number"], input[data-tipo="numero"]').forEach(input => {
        const min = input.getAttribute('min') ? parseFloat(input.getAttribute('min')) : null;
        const max = input.getAttribute('max') ? parseFloat(input.getAttribute('max')) : null;
        
        if (input.value && !validarNumero(input.value, min, max)) {
            input.classList.add('is-invalid');
            mostrarError(input, 'Número inválido');
            esValido = false;
        }
    });
    
    if (!esValido) {
        // Scroll al primer error
        const primerError = formulario.querySelector('.is-invalid');
        if (primerError) {
            primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    return esValido;
}

// ============================================================================
// AUTO-INICIALIZACIÓN AL CARGAR LA PÁGINA
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar validaciones en todos los formularios
    inicializarValidaciones();
    
    // Interceptar submit de formularios
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validarFormulario(this)) {
                e.preventDefault();
                
                // Mostrar alerta
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger alert-dismissible fade show';
                alert.innerHTML = `
                    <i class="fas fa-exclamation-triangle"></i>
                    Por favor corrige los errores en el formulario antes de continuar.
                    <button type="button" class="btn-close" onclick="this.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                
                this.insertBefore(alert, this.firstChild);
                
                // Auto-remover después de 5 segundos
                setTimeout(() => alert.remove(), 5000);
            }
        });
    });
});

// Exportar funciones para uso global
window.validaciones = {
    formatearRUT,
    validarRUT,
    validarEmail,
    validarTelefono,
    validarNumero,
    validarTexto,
    validarRequerido,
    validarFecha,
    validarFormulario,
    inicializarValidaciones,
    mostrarError,
    ocultarError
};
