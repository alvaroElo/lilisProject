// ===========================================
// MÓDULO DE PRODUCTOS - Dulcería Lilis
// ===========================================

// Variables globales
let currentProductoId = null;
let isEditMode = false;

// Inicialización al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeTooltips();
});

// Inicializar event listeners
function initializeEventListeners() {
    // Botones de acción en la tabla
    document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', handleAction);
    });
    
    // Cambio de registros por página
    const perPageSelect = document.querySelector('select[onchange*="changePerPage"]');
    if (perPageSelect) {
        perPageSelect.removeAttribute('onchange');
        perPageSelect.addEventListener('change', function() {
            changePerPage(this.value);
        });
    }
}

// Inicializar tooltips de Bootstrap
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Manejar acciones de botones
function handleAction(event) {
    const button = event.currentTarget;
    const action = button.dataset.action;
    const id = button.dataset.id;
    
    switch(action) {
        case 'view':
            viewProducto(id);
            break;
        case 'edit':
            editProducto(id);
            break;
        case 'delete':
            deleteProducto(id, button.dataset.sku);
            break;
    }
}

// Abrir modal para crear producto
function openCreateModal() {
    isEditMode = false;
    currentProductoId = null;
    
    document.getElementById('modalTitle').textContent = 'Agregar Nuevo Producto';
    document.getElementById('productoForm').reset();
    document.getElementById('productoId').value = '';
    
    // Mostrar/ocultar campos
    document.getElementById('passwordRequired').style.display = 'inline';
    document.getElementById('passwordHelp').textContent = 'Mínimo 8 caracteres';
    
    // Habilitar todos los campos
    enableAllFields();
    
    // Mostrar/ocultar botones
    document.getElementById('btnGuardar').style.display = 'inline-block';
    document.getElementById('btnCerrar').style.display = 'none';
    document.getElementById('btnCancelar').style.display = 'inline-block';
    
    // Limpiar campos derivados (solo lectura)
    document.querySelectorAll('[readonly]').forEach(field => {
        if (!field.id.includes('stock_actual') && !field.id.includes('costo_promedio')) {
            field.removeAttribute('readonly');
        }
    });
}

// Ver detalles del producto
function viewProducto(id) {
    showLoading();
    
    fetch(`/productos/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            isEditMode = false;
            currentProductoId = id;
            
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-eye me-2"></i>Detalles del Producto';
            
            // Llenar formulario con datos
            fillFormWithData(data);
            
            // Deshabilitar todos los campos (modo solo lectura)
            disableAllFields();
            
            // Mostrar/ocultar botones
            document.getElementById('btnGuardar').style.display = 'none';
            document.getElementById('btnCancelar').style.display = 'none';
            document.getElementById('btnCerrar').style.display = 'inline-block';
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('modalProducto'));
            modal.show();
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showAlert('Error al cargar los datos del producto', 'error');
        });
}

// Editar producto
function editProducto(id) {
    showLoading();
    
    fetch(`/productos/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            isEditMode = true;
            currentProductoId = id;
            
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit me-2"></i>Editar Producto';
            document.getElementById('productoId').value = id;
            
            // Llenar formulario con datos
            fillFormWithData(data);
            
            // Habilitar campos editables
            enableAllFields();
            
            // Campos de solo lectura
            document.getElementById('stock_actual').setAttribute('readonly', 'readonly');
            document.getElementById('costo_promedio').setAttribute('readonly', 'readonly');
            
            // Mostrar/ocultar botones
            document.getElementById('btnGuardar').style.display = 'inline-block';
            document.getElementById('btnCerrar').style.display = 'none';
            document.getElementById('btnCancelar').style.display = 'inline-block';
            document.getElementById('btnSaveText').textContent = 'Actualizar Producto';
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('modalProducto'));
            modal.show();
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showAlert('Error al cargar los datos del producto', 'error');
        });
}

// Llenar formulario con datos
function fillFormWithData(data) {
    document.getElementById('sku').value = data.sku || '';
    document.getElementById('ean_upc').value = data.ean_upc || '';
    document.getElementById('nombre').value = data.nombre || '';
    document.getElementById('descripcion').value = data.descripcion || '';
    document.getElementById('categoria').value = data.categoria || '';
    document.getElementById('marca').value = data.marca || '';
    document.getElementById('modelo').value = data.modelo || '';
    document.getElementById('uom_compra').value = data.uom_compra || '';
    document.getElementById('uom_venta').value = data.uom_venta || '';
    document.getElementById('factor_conversion').value = data.factor_conversion || '1';
    document.getElementById('costo_estandar').value = data.costo_estandar || '';
    document.getElementById('costo_promedio').value = data.costo_promedio || '';
    document.getElementById('precio_venta').value = data.precio_venta || '';
    document.getElementById('impuesto_iva').value = data.impuesto_iva || '19';
    document.getElementById('stock_actual').value = data.stock_actual || '0';
    document.getElementById('stock_minimo').value = data.stock_minimo || '0';
    document.getElementById('stock_maximo').value = data.stock_maximo || '';
    document.getElementById('punto_reorden').value = data.punto_reorden || '';
    document.getElementById('perecible').checked = data.perecible || false;
    document.getElementById('control_por_lote').checked = data.control_por_lote || false;
    document.getElementById('control_por_serie').checked = data.control_por_serie || false;
    document.getElementById('imagen_url').value = data.imagen_url || '';
    document.getElementById('ficha_tecnica_url').value = data.ficha_tecnica_url || '';
    document.getElementById('estado').value = data.estado || 'ACTIVO';
}

// Habilitar todos los campos
function enableAllFields() {
    document.querySelectorAll('#productoForm input, #productoForm select, #productoForm textarea').forEach(field => {
        field.removeAttribute('disabled');
        field.removeAttribute('readonly');
    });
    
    // Mantener campos de solo lectura
    document.getElementById('stock_actual').setAttribute('readonly', 'readonly');
    document.getElementById('costo_promedio').setAttribute('readonly', 'readonly');
}

// Deshabilitar todos los campos
function disableAllFields() {
    document.querySelectorAll('#productoForm input, #productoForm select, #productoForm textarea').forEach(field => {
        field.setAttribute('disabled', 'disabled');
    });
}

// Guardar producto (crear o actualizar)
function saveProducto() {
    if (!validateForm()) {
        return;
    }
    
    const form = document.getElementById('productoForm');
    const formData = new FormData(form);
    
    // Agregar token CSRF
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    let url = '/productos/create/';
    if (isEditMode && currentProductoId) {
        url = `/productos/${currentProductoId}/edit/`;
    }
    
    showLoading();
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            showAlert(data.message, 'success');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalProducto'));
            modal.hide();
            
            // Recargar página después de un breve delay
            setTimeout(() => {
                window.location.href = data.redirect || '/productos/';
            }, 1500);
        } else {
            showAlert(data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showAlert('Error al guardar el producto', 'error');
    });
}

// Validar formulario
function validateForm() {
    const requiredFields = [
        { id: 'sku', name: 'SKU' },
        { id: 'nombre', name: 'Nombre' },
        { id: 'categoria', name: 'Categoría' },
        { id: 'uom_compra', name: 'Unidad de Compra' },
        { id: 'uom_venta', name: 'Unidad de Venta' }
    ];
    
    for (let field of requiredFields) {
        const element = document.getElementById(field.id);
        if (!element.value.trim()) {
            showAlert(`El campo ${field.name} es obligatorio`, 'warning');
            element.focus();
            return false;
        }
    }
    
    // Validar que factor_conversion sea mayor a 0
    const factorConversion = parseFloat(document.getElementById('factor_conversion').value);
    if (isNaN(factorConversion) || factorConversion <= 0) {
        showAlert('El Factor de Conversión debe ser mayor a 0', 'warning');
        document.getElementById('factor_conversion').focus();
        return false;
    }
    
    // Validar que IVA esté entre 0 y 100
    const iva = parseFloat(document.getElementById('impuesto_iva').value);
    if (isNaN(iva) || iva < 0 || iva > 100) {
        showAlert('El IVA debe estar entre 0 y 100', 'warning');
        document.getElementById('impuesto_iva').focus();
        return false;
    }
    
    return true;
}

// Eliminar (desactivar) producto
function deleteProducto(id, sku) {
    Swal.fire({
        title: '¿Desactivar Producto?',
        html: `¿Estás seguro de desactivar el producto <strong>${sku}</strong>?<br><small class="text-muted">El producto quedará como INACTIVO</small>`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '<i class="fas fa-check me-2"></i>Sí, desactivar',
        cancelButtonText: '<i class="fas fa-times me-2"></i>Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            showLoading();
            
            fetch(`/productos/${id}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    showAlert(data.message, 'success');
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    showAlert(data.message, 'error');
                }
            })
            .catch(error => {
                hideLoading();
                console.error('Error:', error);
                showAlert('Error al desactivar el producto', 'error');
            });
        }
    });
}

// Exportar a Excel
function exportarExcel() {
    // Verificar permisos
    if (typeof PERMISOS !== 'undefined' && !PERMISOS.exportar) {
        Swal.fire({
            icon: 'error',
            title: 'Acceso Denegado',
            text: 'No tienes permisos para exportar datos',
            confirmButtonColor: '#D20A11'
        });
        return;
    }
    
    const url = new URL(window.location.href);
    const params = url.searchParams.toString();
    
    Swal.fire({
        title: 'Exportando...',
        html: 'Generando archivo Excel<br>Por favor espere',
        icon: 'info',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    const exportUrl = `/productos/exportar-excel/${params ? '?' + params : ''}`;
    window.location.href = exportUrl;
    
    setTimeout(() => {
        Swal.fire({
            title: '¡Exportado!',
            text: 'El archivo Excel se ha descargado correctamente',
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });
    }, 2000);
}

// Exportar a PDF
function exportarPDF() {
    if (!PERMISOS.exportar) {
        showAlert('No tienes permisos para exportar productos', 'warning');
        return;
    }
    
    showAlert('Funcionalidad de exportar a PDF en desarrollo', 'info');
}

// Cambiar cantidad de registros por página
function changePerPage(value) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('per_page', value);
    urlParams.set('page', '1'); // Volver a la primera página
    window.location.href = '/productos/?' + urlParams.toString();
}

// Mostrar loading overlay
function showLoading() {
    let overlay = document.querySelector('.loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="spinner-border text-light" role="status"><span class="visually-hidden">Cargando...</span></div>';
        document.body.appendChild(overlay);
    }
    overlay.classList.add('active');
}

// Ocultar loading overlay
function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Mostrar alertas con SweetAlert2
function showAlert(message, type) {
    const icons = {
        success: 'success',
        error: 'error',
        warning: 'warning',
        info: 'info'
    };
    
    const titles = {
        success: '¡Éxito!',
        error: 'Error',
        warning: 'Advertencia',
        info: 'Información'
    };
    
    Swal.fire({
        title: titles[type] || 'Notificación',
        text: message,
        icon: icons[type] || 'info',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#D20A11',
        timer: 3000,
        timerProgressBar: true
    });
}

// Limpiar formulario al cerrar modal
document.getElementById('modalProducto')?.addEventListener('hidden.bs.modal', function () {
    document.getElementById('productoForm').reset();
    currentProductoId = null;
    isEditMode = false;
    document.getElementById('btnSaveText').textContent = 'Guardar Producto';
});
