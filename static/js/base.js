/**
 * DULCERÍA LILIS - BASE JS
 * Funciones globales y utilidades
 */

// Detectar modo oscuro (opcional para futuro)
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// Funciones de utilidad globales
window.LiliUtils = {
    
    /**
     * Formatear número como moneda CLP
     */
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        }).format(amount);
    },
    
    /**
     * Formatear fecha
     */
    formatDate: function(date, format = 'short') {
        const options = format === 'short' 
            ? { year: 'numeric', month: '2-digit', day: '2-digit' }
            : { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        
        return new Intl.DateTimeFormat('es-CL', options).format(new Date(date));
    },
    
    /**
     * Obtener CSRF Token para requests AJAX
     */
    getCsrfToken: function() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    },
    
    /**
     * Hacer request AJAX
     */
    request: async function(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            return await response.json();
        } catch (error) {
            console.error('Request error:', error);
            throw error;
        }
    },
    
    /**
     * Debounce para optimizar eventos
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Log de carga
console.log('%c🍬 Dulcería Lilis - Sistema de Gestión', 'color: #D20A11; font-size: 16px; font-weight: bold;');
console.log('%cSistema cargado correctamente', 'color: #c4a75b;');
