// ============================
// Main JavaScript File
// Sistema Dulcería Lilis
// ============================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema Dulcería Lilis cargado');
    
    // Inicializar tooltips
    initTooltips();
    
    // Inicializar confirmaciones
    initConfirmations();
    
    // Inicializar filtros
    initFilters();
});

// ============================
// Tooltips
// ============================
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.dataset.tooltip;
            showTooltip(this, tooltipText);
        });
    });
}

function showTooltip(element, text) {
    // Implementación futura de tooltips
    element.title = text;
}

// ============================
// Confirmaciones
// ============================
function initConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Está seguro de que desea eliminar este elemento?')) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// ============================
// Filtros
// ============================
function initFilters() {
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        const clearButton = document.createElement('button');
        clearButton.type = 'button';
        clearButton.className = 'btn btn-secondary';
        clearButton.innerHTML = '<i class="fas fa-times"></i> Limpiar';
        clearButton.addEventListener('click', function() {
            form.reset();
            form.submit();
        });
        
        const formRow = form.querySelector('.form-row');
        if (formRow) {
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';
            const label = document.createElement('label');
            label.className = 'form-label';
            label.innerHTML = '&nbsp;';
            formGroup.appendChild(label);
            formGroup.appendChild(clearButton);
            formRow.appendChild(formGroup);
        }
    });
}

// ============================
// Utilidades de Formato
// ============================
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(new Date(date));
}

function formatDateTime(date) {
    return new Intl.DateTimeFormat('es-CL', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// ============================
// Notificaciones
// ============================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ============================
// Validaciones de Formularios
// ============================
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            markFieldAsInvalid(field, 'Este campo es requerido');
            isValid = false;
        } else {
            markFieldAsValid(field);
        }
    });
    
    return isValid;
}

function markFieldAsInvalid(field, message) {
    field.classList.add('error');
    
    // Remover mensaje de error anterior
    const existingError = field.parentElement.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar nuevo mensaje
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    field.parentElement.appendChild(errorElement);
}

function markFieldAsValid(field) {
    field.classList.remove('error');
    const errorElement = field.parentElement.querySelector('.form-error');
    if (errorElement) {
        errorElement.remove();
    }
}

// ============================
// AJAX Helpers
// ============================
async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        showNotification('Error al cargar los datos', 'error');
        throw error;
    }
}

async function postData(url, data, options = {}) {
    return fetchData(url, {
        method: 'POST',
        body: JSON.stringify(data),
        ...options
    });
}

// ============================
// Exportar funciones globales
// ============================
window.LiliSystem = {
    formatCurrency,
    formatDate,
    formatDateTime,
    showNotification,
    validateForm,
    fetchData,
    postData
};
