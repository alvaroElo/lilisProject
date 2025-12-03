/* ===================================
   MÓDULO DE MOVIMIENTOS - JAVASCRIPT
   Gestión de movimientos de inventario con wizard de 3 pasos
   =================================== */

// Variables globales
let currentStep = 1;
const totalSteps = 3;
let isEditMode = false;
let productos = [];
let bodegas = [];
let proveedores = [];
let unidades = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    init();
});

function init() {
    setupEventListeners();
    setupWizardNavigation();
    setupRealTimeSearch();
}

// Configurar listeners de eventos
function setupEventListeners() {
    // Botones de acción en la tabla
    document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.action;
            const id = this.dataset.id;
            
            if (action === 'view') {
                viewMovimiento(id);
            } else if (action === 'edit') {
                editMovimiento(id);
            } else if (action === 'delete') {
                const tipo = this.dataset.tipo;
                deleteMovimiento(id, tipo);
            }
        });
    });
    
    // Cambios en el tipo de movimiento
    document.getElementById('tipoMovimiento').addEventListener('change', function() {
        updateFieldsVisibility();
    });
    
    // Cambios en switches de control avanzado
    document.getElementById('manejoPorLotes').addEventListener('change', toggleLoteField);
    document.getElementById('manejoPorSeries').addEventListener('change', toggleSerieField);
    document.getElementById('perecible').addEventListener('change', toggleVencimientoField);
    
    // Calcular costo total automáticamente
    document.getElementById('cantidad').addEventListener('input', calculateTotal);
    document.getElementById('costoUnitario').addEventListener('input', calculateTotal);
    
    // Resetear form al cerrar modal
    const modalElement = document.getElementById('modalMovimiento');
    modalElement.addEventListener('hidden.bs.modal', function() {
        resetForm();
        // Asegurar que se limpie el backdrop
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
    });
}

// Configurar navegación del wizard
function setupWizardNavigation() {
    document.getElementById('btnNext').addEventListener('click', nextStep);
    document.getElementById('btnPrev').addEventListener('click', prevStep);
    document.getElementById('btnSave').addEventListener('click', saveMovimiento);
}

// Búsqueda en tiempo real (ahora manejado en el template)
function setupRealTimeSearch() {
    // La búsqueda en tiempo real ahora se maneja directamente en el template
    // para mantener el foco y posición del cursor
}

// Abrir modal para crear movimiento
async function openCreateModal() {
    isEditMode = false;
    currentStep = 1;
    resetForm();
    
    // Cambiar título
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle me-2"></i>Registrar Movimiento';
    
    // Cargar datos para el formulario
    await loadFormData();
    
    // Establecer fecha actual
    const now = new Date();
    const dateString = now.toISOString().slice(0, 16);
    document.getElementById('fechaMovimiento').value = dateString;
    
    // Mostrar paso 1
    showStep(1);
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('modalMovimiento'));
    modal.show();
}

// Ver detalles del movimiento
async function viewMovimiento(id) {
    try {
        showLoading();
        
        const response = await fetch(`/movimientos/${id}/edit/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            // Mostrar detalles en un alert de SweetAlert
            const mov = data.movimiento;
            
            let htmlContent = `
                <div class="text-start">
                    <table class="table table-sm table-bordered">
                        <tr><th>Fecha:</th><td>${mov.fecha_movimiento}</td></tr>
                        <tr><th>Tipo:</th><td><strong>${mov.tipo_movimiento}</strong></td></tr>
                        <tr><th>Producto:</th><td>${mov.producto_sku} - ${mov.producto_nombre}</td></tr>
                        <tr><th>Cantidad:</th><td><strong>${mov.cantidad}</strong></td></tr>
                        ${mov.bodega_origen_id ? `<tr><th>Bodega Origen:</th><td>${mov.bodega_origen_id}</td></tr>` : ''}
                        ${mov.bodega_destino_id ? `<tr><th>Bodega Destino:</th><td>${mov.bodega_destino_id}</td></tr>` : ''}
                        ${mov.proveedor_id ? `<tr><th>Proveedor:</th><td>${mov.proveedor_id}</td></tr>` : ''}
                        ${mov.lote_codigo ? `<tr><th>Lote:</th><td>${mov.lote_codigo}</td></tr>` : ''}
                        ${mov.serie ? `<tr><th>Serie:</th><td>${mov.serie}</td></tr>` : ''}
                        ${mov.costo_unitario ? `<tr><th>Costo Unitario:</th><td>$${mov.costo_unitario}</td></tr>` : ''}
                        ${mov.costo_total ? `<tr><th>Costo Total:</th><td><strong>$${mov.costo_total}</strong></td></tr>` : ''}
                        ${mov.documento_referencia ? `<tr><th>Doc. Referencia:</th><td>${mov.documento_referencia}</td></tr>` : ''}
                        ${mov.motivo_ajuste ? `<tr><th>Motivo:</th><td>${mov.motivo_ajuste}</td></tr>` : ''}
                        ${mov.observaciones ? `<tr><th>Observaciones:</th><td>${mov.observaciones}</td></tr>` : ''}
                        <tr><th>Estado:</th><td><span class="badge bg-${mov.estado === 'CONFIRMADO' ? 'success' : mov.estado === 'PENDIENTE' ? 'warning' : 'danger'}">${mov.estado}</span></td></tr>
                    </table>
                </div>
            `;
            
            Swal.fire({
                title: 'Detalles del Movimiento',
                html: htmlContent,
                icon: 'info',
                width: 600,
                confirmButtonColor: '#0d6efd',
                confirmButtonText: 'Cerrar'
            });
        } else {
            showAlert(data.message, 'error');
        }
    } catch (error) {
        hideLoading();
        showAlert('Error al cargar los detalles del movimiento', 'error');
        console.error(error);
    }
}

// Editar movimiento
async function editMovimiento(id) {
    try {
        showLoading();
        
        isEditMode = true;
        currentStep = 1;
        
        // Cargar datos del formulario primero
        await loadFormData();
        
        // Luego cargar datos del movimiento
        const response = await fetch(`/movimientos/${id}/edit/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            const mov = data.movimiento;
            
            // Llenar formulario
            document.getElementById('movimientoId').value = mov.id;
            document.getElementById('fechaMovimiento').value = mov.fecha_movimiento;
            document.getElementById('tipoMovimiento').value = mov.tipo_movimiento;
            document.getElementById('producto').value = mov.producto_id;
            document.getElementById('cantidad').value = mov.cantidad;
            document.getElementById('unidadMedida').value = mov.unidad_medida_id;
            
            if (mov.proveedor_id) {
                document.getElementById('proveedor').value = mov.proveedor_id;
            }
            if (mov.bodega_origen_id) {
                document.getElementById('bodegaOrigen').value = mov.bodega_origen_id;
            }
            if (mov.bodega_destino_id) {
                document.getElementById('bodegaDestino').value = mov.bodega_destino_id;
            }
            if (mov.costo_unitario) {
                document.getElementById('costoUnitario').value = mov.costo_unitario;
            }
            if (mov.costo_total) {
                document.getElementById('costoTotal').value = mov.costo_total;
            }
            
            // Step 2 - Control avanzado
            if (mov.lote_id) {
                document.getElementById('manejoPorLotes').checked = true;
                toggleLoteField();
                document.getElementById('lote').value = mov.lote_codigo;
            }
            if (mov.serie) {
                document.getElementById('manejoPorSeries').checked = true;
                toggleSerieField();
                document.getElementById('serie').value = mov.serie;
            }
            
            // Step 3 - Referencias
            if (mov.documento_referencia) {
                document.getElementById('documentoReferencia').value = mov.documento_referencia;
            }
            if (mov.motivo_ajuste) {
                document.getElementById('motivoAjuste').value = mov.motivo_ajuste;
            }
            if (mov.observaciones) {
                document.getElementById('observaciones').value = mov.observaciones;
            }
            if (mov.estado) {
                document.getElementById('estadoMovimiento').value = mov.estado;
            }
            
            // Actualizar visibilidad de campos según tipo
            updateFieldsVisibility();
            
            // Cambiar título
            document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit me-2"></i>Editar Movimiento';
            
            // Mostrar paso 1
            showStep(1);
            
            // Abrir modal
            const modal = new bootstrap.Modal(document.getElementById('modalMovimiento'));
            modal.show();
        } else {
            showAlert(data.message, 'error');
        }
    } catch (error) {
        hideLoading();
        showAlert('Error al cargar el movimiento', 'error');
        console.error(error);
    }
}

// Eliminar (anular) movimiento
function deleteMovimiento(id, tipo) {
    Swal.fire({
        title: '¿Anular Movimiento?',
        html: `¿Estás seguro de que deseas anular este movimiento de tipo <strong>${tipo}</strong>?<br><br>
               <span class="text-danger">Esta acción no se puede deshacer.</span>`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, anular',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                showLoading();
                
                const response = await fetch(`/movimientos/${id}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    Swal.fire({
                        title: '¡Anulado!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonColor: '#28a745',
                        timer: 2000,
                        timerProgressBar: true
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    showAlert(data.message, 'error');
                }
            } catch (error) {
                hideLoading();
                showAlert('Error al anular el movimiento', 'error');
                console.error(error);
            }
        }
    });
}

// Cargar datos para el formulario
async function loadFormData() {
    try {
        showLoading();
        
        const response = await fetch('/movimientos/create/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            unidades = data.unidades;
            
            // Solo poblar el select de unidad de medida (los demás usan autocomplete)
            populateSelect('unidadMedida', unidades, 'id', item => `${item.codigo} - ${item.nombre}`);
        } else {
            showAlert('Error al cargar datos del formulario', 'error');
        }
    } catch (error) {
        hideLoading();
        showAlert('Error al cargar datos del formulario', 'error');
        console.error(error);
    }
}

// Poblar un select
function populateSelect(selectId, data, valueKey, textFunction) {
    const select = document.getElementById(selectId);
    const currentValue = select.value;
    
    // Limpiar opciones excepto la primera
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    // Agregar nuevas opciones
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item[valueKey];
        option.textContent = textFunction(item);
        select.appendChild(option);
    });
    
    // Restaurar valor si existía
    if (currentValue) {
        select.value = currentValue;
    }
}

// Actualizar visibilidad de campos según tipo de movimiento
function updateFieldsVisibility() {
    const tipo = document.getElementById('tipoMovimiento').value;
    const proveedorGroup = document.getElementById('proveedorGroup');
    const bodegaOrigenGroup = document.getElementById('bodegaOrigenGroup');
    const bodegaDestinoGroup = document.getElementById('bodegaDestinoGroup');
    const proveedorId = document.getElementById('proveedorId');
    const bodegaOrigenId = document.getElementById('bodegaOrigenId');
    const bodegaDestinoId = document.getElementById('bodegaDestinoId');
    
    // Reset required
    proveedorId.required = false;
    bodegaOrigenId.required = false;
    bodegaDestinoId.required = false;
    
    // Ocultar todos
    proveedorGroup.style.display = 'none';
    bodegaOrigenGroup.style.display = 'none';
    bodegaDestinoGroup.style.display = 'none';
    
    // Mostrar según tipo
    switch(tipo) {
        case 'INGRESO':
            proveedorGroup.style.display = 'block';
            bodegaDestinoGroup.style.display = 'block';
            proveedorId.required = true;
            bodegaDestinoId.required = true;
            break;
        case 'SALIDA':
            bodegaOrigenGroup.style.display = 'block';
            bodegaOrigenId.required = true;
            break;
        case 'AJUSTE':
            bodegaOrigenGroup.style.display = 'block';
            bodegaOrigenId.required = true;
            break;
        case 'DEVOLUCION':
            proveedorGroup.style.display = 'block';
            bodegaOrigenGroup.style.display = 'block';
            proveedorId.required = true;
            bodegaOrigenId.required = true;
            break;
        case 'TRANSFERENCIA':
            bodegaOrigenGroup.style.display = 'block';
            bodegaDestinoGroup.style.display = 'block';
            bodegaOrigenId.required = true;
            bodegaDestinoId.required = true;
            break;
    }
}

// Toggle campo de lote
function toggleLoteField() {
    const checked = document.getElementById('manejoPorLotes').checked;
    const loteGroup = document.getElementById('loteGroup');
    const label = document.getElementById('lotesLabel');
    
    loteGroup.style.display = checked ? 'block' : 'none';
    label.textContent = checked ? '1 (sí)' : '0 (no)';
}

// Toggle campo de serie
function toggleSerieField() {
    const checked = document.getElementById('manejoPorSeries').checked;
    const serieGroup = document.getElementById('serieGroup');
    const label = document.getElementById('seriesLabel');
    
    serieGroup.style.display = checked ? 'block' : 'none';
    label.textContent = checked ? '1 (sí)' : '0 (no)';
}

// Toggle campo de vencimiento
function toggleVencimientoField() {
    const checked = document.getElementById('perecible').checked;
    const vencimientoGroup = document.getElementById('fechaVencimientoGroup');
    const label = document.getElementById('perecibleLabel');
    
    vencimientoGroup.style.display = checked ? 'block' : 'none';
    label.textContent = checked ? '1 (sí)' : '0 (no)';
}

// Calcular costo total
function calculateTotal() {
    const cantidad = parseFloat(document.getElementById('cantidad').value) || 0;
    const costoUnitario = parseFloat(document.getElementById('costoUnitario').value) || 0;
    const costoTotal = cantidad * costoUnitario;
    
    document.getElementById('costoTotal').value = costoTotal.toFixed(2);
}

// Navegación del wizard
function nextStep() {
    if (validateCurrentStep()) {
        if (currentStep < totalSteps) {
            currentStep++;
            showStep(currentStep);
        }
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

function showStep(step) {
    // Ocultar todos los pasos
    document.querySelectorAll('.wizard-content').forEach(content => {
        content.style.display = 'none';
    });
    
    // Mostrar paso actual
    document.querySelector(`.wizard-content[data-step="${step}"]`).style.display = 'block';
    
    // Actualizar indicadores de paso
    document.querySelectorAll('.wizard-step').forEach((stepEl, index) => {
        stepEl.classList.remove('active', 'completed');
        if (index + 1 < step) {
            stepEl.classList.add('completed');
        } else if (index + 1 === step) {
            stepEl.classList.add('active');
        }
    });
    
    // Actualizar botones
    document.getElementById('btnPrev').style.display = step === 1 ? 'none' : 'inline-block';
    document.getElementById('btnNext').style.display = step === totalSteps ? 'none' : 'inline-block';
    document.getElementById('btnSave').style.display = step === totalSteps ? 'inline-block' : 'none';
}

// Validar paso actual
function validateCurrentStep() {
    if (currentStep === 1) {
        // Validar campos obligatorios del paso 1
        const fecha = document.getElementById('fechaMovimiento').value;
        const tipo = document.getElementById('tipoMovimiento').value;
        const producto = document.getElementById('productoId').value;
        const cantidad = document.getElementById('cantidad').value;
        const unidad = document.getElementById('unidadMedida').value;
        
        if (!fecha || !tipo || !producto || !cantidad || !unidad) {
            showAlert('Por favor completa todos los campos obligatorios', 'warning');
            return false;
        }
        
        // Validar campos según tipo
        const proveedor = document.getElementById('proveedorId').value;
        const bodegaOrigen = document.getElementById('bodegaOrigenId').value;
        const bodegaDestino = document.getElementById('bodegaDestinoId').value;
        
        if ((tipo === 'INGRESO' || tipo === 'DEVOLUCION') && !proveedor) {
            showAlert('Proveedor es obligatorio para este tipo de movimiento', 'warning');
            return false;
        }
        
        if ((tipo === 'SALIDA' || tipo === 'AJUSTE' || tipo === 'TRANSFERENCIA' || tipo === 'DEVOLUCION') && !bodegaOrigen) {
            showAlert('Bodega origen es obligatoria para este tipo de movimiento', 'warning');
            return false;
        }
        
        if ((tipo === 'INGRESO' || tipo === 'TRANSFERENCIA') && !bodegaDestino) {
            showAlert('Bodega destino es obligatoria para este tipo de movimiento', 'warning');
            return false;
        }
    }
    
    return true;
}

// Guardar movimiento
async function saveMovimiento() {
    if (!validateCurrentStep()) {
        return;
    }
    
    try {
        showLoading();
        
        // Recopilar datos del formulario
        const formData = {
            tipo_movimiento: document.getElementById('tipoMovimiento').value,
            fecha_movimiento: document.getElementById('fechaMovimiento').value,
            producto_id: document.getElementById('productoId').value,
            cantidad: document.getElementById('cantidad').value,
            unidad_medida_id: document.getElementById('unidadMedida').value,
            proveedor_id: document.getElementById('proveedorId').value || null,
            bodega_origen_id: document.getElementById('bodegaOrigenId').value || null,
            bodega_destino_id: document.getElementById('bodegaDestinoId').value || null,
            costo_unitario: document.getElementById('costoUnitario').value || null,
            costo_total: document.getElementById('costoTotal').value || null,
            lote_id: document.getElementById('manejoPorLotes').checked ? document.getElementById('lote').value : null,
            serie: document.getElementById('manejoPorSeries').checked ? document.getElementById('serie').value : null,
            documento_referencia: document.getElementById('documentoReferencia').value,
            motivo_ajuste: document.getElementById('motivoAjuste').value,
            observaciones: document.getElementById('observaciones').value,
            estado: document.getElementById('estadoMovimiento').value || 'PENDIENTE'
        };
        
        let url, method;
        if (isEditMode) {
            const id = document.getElementById('movimientoId').value;
            url = `/movimientos/${id}/edit/`;
            method = 'POST';
        } else {
            url = '/movimientos/create/';
            method = 'POST';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            Swal.fire({
                title: '¡Éxito!',
                text: data.message,
                icon: 'success',
                confirmButtonColor: '#28a745',
                timer: 2000,
                timerProgressBar: true
            }).then(() => {
                // Cerrar modal
                bootstrap.Modal.getInstance(document.getElementById('modalMovimiento')).hide();
                // Recargar página
                location.reload();
            });
        } else {
            showAlert(data.message, 'error');
        }
    } catch (error) {
        hideLoading();
        showAlert('Error al guardar el movimiento', 'error');
        console.error(error);
    }
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
    
    const exportUrl = `/movimientos/exportar-excel/${params ? '?' + params : ''}`;
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

// Resetear formulario
function resetForm() {
    document.getElementById('formMovimiento').reset();
    document.getElementById('movimientoId').value = '';
    currentStep = 1;
    isEditMode = false;
    
    // Resetear autocompletados
    document.getElementById('productoId').value = '';
    document.getElementById('productoSearch').value = '';
    document.getElementById('proveedorId').value = '';
    document.getElementById('proveedorSearch').value = '';
    document.getElementById('bodegaOrigenId').value = '';
    document.getElementById('bodegaOrigenSearch').value = '';
    document.getElementById('bodegaDestinoId').value = '';
    document.getElementById('bodegaDestinoSearch').value = '';
    
    selectedProducto = null;
    selectedProveedor = null;
    selectedBodegaOrigen = null;
    selectedBodegaDestino = null;
    
    // Resetear switches
    document.getElementById('manejoPorLotes').checked = false;
    document.getElementById('manejoPorSeries').checked = false;
    document.getElementById('perecible').checked = false;
    
    toggleLoteField();
    toggleSerieField();
    toggleVencimientoField();
    
    // Ocultar campos opcionales
    document.getElementById('proveedorGroup').style.display = 'none';
    document.getElementById('bodegaOrigenGroup').style.display = 'none';
    document.getElementById('bodegaDestinoGroup').style.display = 'none';
    
    showStep(1);
}

// Mostrar loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="loading-spinner"></div>';
    document.body.appendChild(overlay);
}

// Ocultar loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Mostrar alerta
function showAlert(message, type = 'info') {
    const icons = {
        success: 'success',
        error: 'error',
        warning: 'warning',
        info: 'info'
    };
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#0d6efd'
    };
    
    Swal.fire({
        icon: icons[type] || 'info',
        title: message,
        confirmButtonColor: colors[type] || '#0d6efd',
        timer: 3000,
        timerProgressBar: true
    });
}

// Obtener cookie (para CSRF token)
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

/* ===================================
   AUTOCOMPLETADO DE BODEGAS CON AJAX
   =================================== */

let bodegaSearchTimeout = null;
let selectedBodega = null;
let currentBodegaIndex = -1;

// Inicializar autocompletado de bodegas
function initBodegaAutocomplete() {
    const bodegaSearch = document.getElementById('bodegaSearch');
    const bodegaId = document.getElementById('bodegaId');
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    
    if (!bodegaSearch || !bodegaId || !bodegaDropdown) return;
    
    // Si hay una bodega seleccionada, mostrar botón de limpiar
    if (bodegaId.value && bodegaSearch.value) {
        showClearBodegaButton();
    }
    
    // Evento input - búsqueda en tiempo real
    bodegaSearch.addEventListener('input', function() {
        const query = this.value.trim();
        
        // Limpiar timeout anterior
        if (bodegaSearchTimeout) {
            clearTimeout(bodegaSearchTimeout);
        }
        
        // Si el campo está vacío, ocultar dropdown
        if (query === '') {
            bodegaDropdown.style.display = 'none';
            bodegaSearch.classList.remove('active');
            return;
        }
        
        // Mostrar loading
        showBodegaLoading();
        
        // Buscar después de 300ms
        bodegaSearchTimeout = setTimeout(() => {
            searchBodegas(query);
        }, 300);
    });
    
    // Evento focus - mostrar todas las bodegas si está vacío
    bodegaSearch.addEventListener('focus', function() {
        const query = this.value.trim();
        
        if (query === '') {
            // Si está vacío, cargar todas las bodegas
            showBodegaLoading();
            searchBodegas('');
        } else if (bodegaDropdown.innerHTML !== '') {
            // Si hay texto y resultados previos, mostrar dropdown
            bodegaDropdown.style.display = 'block';
            bodegaSearch.classList.add('active');
        }
    });
    
    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!bodegaSearch.contains(e.target) && !bodegaDropdown.contains(e.target)) {
            bodegaDropdown.style.display = 'none';
            bodegaSearch.classList.remove('active');
        }
    });
    
    // Navegación con teclado
    bodegaSearch.addEventListener('keydown', function(e) {
        const items = bodegaDropdown.querySelectorAll('.autocomplete-item');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentBodegaIndex = Math.min(currentBodegaIndex + 1, items.length - 1);
            updateActiveBodegaItem(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentBodegaIndex = Math.max(currentBodegaIndex - 1, 0);
            updateActiveBodegaItem(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (currentBodegaIndex >= 0 && items[currentBodegaIndex]) {
                items[currentBodegaIndex].click();
            }
        } else if (e.key === 'Escape') {
            bodegaDropdown.style.display = 'none';
            bodegaSearch.classList.remove('active');
        }
    });
}

// Buscar bodegas con AJAX
function searchBodegas(query) {
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    const bodegaSearch = document.getElementById('bodegaSearch');
    
    const url = `/movimientos/bodegas/buscar/?q=${encodeURIComponent(query)}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayBodegaResults(data.results);
            } else {
                showBodegaError('Error al buscar bodegas');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showBodegaError('Error de conexión');
        });
}

// Mostrar resultados de búsqueda
function displayBodegaResults(results) {
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    const bodegaSearch = document.getElementById('bodegaSearch');
    
    currentBodegaIndex = -1;
    
    if (results.length === 0) {
        bodegaDropdown.innerHTML = '<div class="autocomplete-no-results">No se encontraron bodegas</div>';
    } else {
        let html = '';
        results.forEach((bodega, index) => {
            html += `
                <div class="autocomplete-item" data-index="${index}" data-id="${bodega.id}" data-codigo="${bodega.codigo}" data-nombre="${bodega.nombre}">
                    <div class="autocomplete-item-code">
                        <i class="fas fa-warehouse me-2"></i>${bodega.codigo}
                    </div>
                    <div class="autocomplete-item-name">${bodega.nombre}</div>
                </div>
            `;
        });
        bodegaDropdown.innerHTML = html;
        
        // Agregar eventos click a los items
        bodegaDropdown.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', function() {
                selectBodega({
                    id: this.dataset.id,
                    codigo: this.dataset.codigo,
                    nombre: this.dataset.nombre
                });
            });
        });
    }
    
    bodegaDropdown.style.display = 'block';
    bodegaSearch.classList.add('active');
}

// Seleccionar una bodega
function selectBodega(bodega) {
    const bodegaSearch = document.getElementById('bodegaSearch');
    const bodegaId = document.getElementById('bodegaId');
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    
    selectedBodega = bodega;
    bodegaId.value = bodega.id;
    bodegaSearch.value = `${bodega.codigo} - ${bodega.nombre}`;
    
    bodegaDropdown.style.display = 'none';
    bodegaSearch.classList.remove('active');
    
    // Mostrar botón de limpiar
    showClearBodegaButton();
    
    // Enviar formulario automáticamente para aplicar el filtro
    document.getElementById('filterForm').submit();
}

// Limpiar selección de bodega
function clearBodegaSelection() {
    const bodegaSearch = document.getElementById('bodegaSearch');
    const bodegaId = document.getElementById('bodegaId');
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    
    selectedBodega = null;
    bodegaId.value = '';
    bodegaSearch.value = '';
    
    bodegaDropdown.style.display = 'none';
    bodegaSearch.classList.remove('active');
    
    // Ocultar botón de limpiar
    hideClearBodegaButton();
    
    // Enviar formulario para quitar el filtro
    document.getElementById('filterForm').submit();
}

// Mostrar loading en dropdown
function showBodegaLoading() {
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    const bodegaSearch = document.getElementById('bodegaSearch');
    
    bodegaDropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
    bodegaDropdown.style.display = 'block';
    bodegaSearch.classList.add('active');
}

// Mostrar error en dropdown
function showBodegaError(message) {
    const bodegaDropdown = document.getElementById('bodegaDropdown');
    bodegaDropdown.innerHTML = `<div class="autocomplete-no-results text-danger"><i class="fas fa-exclamation-circle me-2"></i>${message}</div>`;
}

// Actualizar item activo en navegación por teclado
function updateActiveBodegaItem(items) {
    items.forEach((item, index) => {
        if (index === currentBodegaIndex) {
            item.classList.add('active');
            item.scrollIntoView({ block: 'nearest' });
        } else {
            item.classList.remove('active');
        }
    });
}

// Mostrar botón de limpiar
function showClearBodegaButton() {
    let btn = document.querySelector('.btn-clear-bodega');
    if (!btn) {
        btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'btn-clear-bodega';
        btn.title = 'Limpiar selección';
        btn.onclick = clearBodegaSelection;
        btn.innerHTML = '<i class="fas fa-times"></i>';
        document.getElementById('bodegaSearch').parentElement.appendChild(btn);
    }
    btn.style.display = 'block';
}

// Ocultar botón de limpiar
function hideClearBodegaButton() {
    const btn = document.querySelector('.btn-clear-bodega');
    if (btn) {
        btn.style.display = 'none';
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initBodegaAutocomplete();
        initModalAutocompletes();
    });
} else {
    initBodegaAutocomplete();
    initModalAutocompletes();
}

/* ===================================
   AUTOCOMPLETADOS DEL MODAL
   =================================== */

function initModalAutocompletes() {
    initProductoAutocomplete();
    initProveedorAutocomplete();
    initBodegaOrigenAutocomplete();
    initBodegaDestinoAutocomplete();
}

// ===== PRODUCTO AUTOCOMPLETE =====
let productoSearchTimeout = null;
let selectedProducto = null;

function initProductoAutocomplete() {
    const search = document.getElementById('productoSearch');
    const dropdown = document.getElementById('productoDropdown');
    
    if (!search || !dropdown) return;
    
    search.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (productoSearchTimeout) clearTimeout(productoSearchTimeout);
        
        if (query === '') {
            dropdown.style.display = 'none';
            search.classList.remove('active');
            return;
        }
        
        dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
        dropdown.style.display = 'block';
        search.classList.add('active');
        
        productoSearchTimeout = setTimeout(() => searchProductos(query), 300);
    });
    
    search.addEventListener('focus', function() {
        if (this.value.trim() === '') {
            dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
            dropdown.style.display = 'block';
            search.classList.add('active');
            searchProductos('');
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!search.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
            search.classList.remove('active');
        }
    });
}

function searchProductos(query) {
    fetch(`/movimientos/productos/buscar/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayProductoResults(data.results);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('productoDropdown').innerHTML = '<div class="autocomplete-no-results text-danger">Error de conexión</div>';
        });
}

function displayProductoResults(results) {
    const dropdown = document.getElementById('productoDropdown');
    
    if (results.length === 0) {
        dropdown.innerHTML = '<div class="autocomplete-no-results">No se encontraron productos</div>';
    } else {
        let html = '';
        results.forEach(producto => {
            html += `
                <div class="autocomplete-item" data-id="${producto.id}" data-sku="${producto.sku}" data-nombre="${producto.nombre}">
                    <div class="autocomplete-item-code">
                        <i class="fas fa-box me-2"></i>${producto.sku}
                    </div>
                    <div class="autocomplete-item-name">${producto.nombre}</div>
                </div>
            `;
        });
        dropdown.innerHTML = html;
        
        dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', function() {
                selectProducto({
                    id: this.dataset.id,
                    sku: this.dataset.sku,
                    nombre: this.dataset.nombre
                });
            });
        });
    }
    
    dropdown.style.display = 'block';
}

function selectProducto(producto) {
    selectedProducto = producto;
    document.getElementById('productoId').value = producto.id;
    document.getElementById('productoSearch').value = `${producto.sku} - ${producto.nombre}`;
    document.getElementById('productoDropdown').style.display = 'none';
    document.getElementById('productoSearch').classList.remove('active');
}

// ===== PROVEEDOR AUTOCOMPLETE =====
let proveedorSearchTimeout = null;
let selectedProveedor = null;

function initProveedorAutocomplete() {
    const search = document.getElementById('proveedorSearch');
    const dropdown = document.getElementById('proveedorDropdown');
    
    if (!search || !dropdown) return;
    
    search.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (proveedorSearchTimeout) clearTimeout(proveedorSearchTimeout);
        
        if (query === '') {
            dropdown.style.display = 'none';
            search.classList.remove('active');
            return;
        }
        
        dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
        dropdown.style.display = 'block';
        search.classList.add('active');
        
        proveedorSearchTimeout = setTimeout(() => searchProveedores(query), 300);
    });
    
    search.addEventListener('focus', function() {
        if (this.value.trim() === '') {
            dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
            dropdown.style.display = 'block';
            search.classList.add('active');
            searchProveedores('');
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!search.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
            search.classList.remove('active');
        }
    });
}

function searchProveedores(query) {
    fetch(`/movimientos/proveedores/buscar/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayProveedorResults(data.results);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('proveedorDropdown').innerHTML = '<div class="autocomplete-no-results text-danger">Error de conexión</div>';
        });
}

function displayProveedorResults(results) {
    const dropdown = document.getElementById('proveedorDropdown');
    
    if (results.length === 0) {
        dropdown.innerHTML = '<div class="autocomplete-no-results">No se encontraron proveedores</div>';
    } else {
        let html = '';
        results.forEach(proveedor => {
            html += `
                <div class="autocomplete-item" data-id="${proveedor.id}" data-rut="${proveedor.rut}" data-razon="${proveedor.razon_social}">
                    <div class="autocomplete-item-code">
                        <i class="fas fa-truck me-2"></i>${proveedor.rut}
                    </div>
                    <div class="autocomplete-item-name">${proveedor.razon_social}</div>
                </div>
            `;
        });
        dropdown.innerHTML = html;
        
        dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', function() {
                selectProveedor({
                    id: this.dataset.id,
                    rut: this.dataset.rut,
                    razon_social: this.dataset.razon
                });
            });
        });
    }
    
    dropdown.style.display = 'block';
}

function selectProveedor(proveedor) {
    selectedProveedor = proveedor;
    document.getElementById('proveedorId').value = proveedor.id;
    document.getElementById('proveedorSearch').value = `${proveedor.rut} - ${proveedor.razon_social}`;
    document.getElementById('proveedorDropdown').style.display = 'none';
    document.getElementById('proveedorSearch').classList.remove('active');
}

// ===== BODEGA ORIGEN AUTOCOMPLETE =====
let bodegaOrigenSearchTimeout = null;
let selectedBodegaOrigen = null;

function initBodegaOrigenAutocomplete() {
    const search = document.getElementById('bodegaOrigenSearch');
    const dropdown = document.getElementById('bodegaOrigenDropdown');
    
    if (!search || !dropdown) return;
    
    search.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (bodegaOrigenSearchTimeout) clearTimeout(bodegaOrigenSearchTimeout);
        
        if (query === '') {
            dropdown.style.display = 'none';
            search.classList.remove('active');
            return;
        }
        
        dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
        dropdown.style.display = 'block';
        search.classList.add('active');
        
        bodegaOrigenSearchTimeout = setTimeout(() => searchBodegasModal(query, 'Origen'), 300);
    });
    
    search.addEventListener('focus', function() {
        if (this.value.trim() === '') {
            dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
            dropdown.style.display = 'block';
            search.classList.add('active');
            searchBodegasModal('', 'Origen');
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!search.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
            search.classList.remove('active');
        }
    });
}

// ===== BODEGA DESTINO AUTOCOMPLETE =====
let bodegaDestinoSearchTimeout = null;
let selectedBodegaDestino = null;

function initBodegaDestinoAutocomplete() {
    const search = document.getElementById('bodegaDestinoSearch');
    const dropdown = document.getElementById('bodegaDestinoDropdown');
    
    if (!search || !dropdown) return;
    
    search.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (bodegaDestinoSearchTimeout) clearTimeout(bodegaDestinoSearchTimeout);
        
        if (query === '') {
            dropdown.style.display = 'none';
            search.classList.remove('active');
            return;
        }
        
        dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
        dropdown.style.display = 'block';
        search.classList.add('active');
        
        bodegaDestinoSearchTimeout = setTimeout(() => searchBodegasModal(query, 'Destino'), 300);
    });
    
    search.addEventListener('focus', function() {
        if (this.value.trim() === '') {
            dropdown.innerHTML = '<div class="autocomplete-loading"><i class="fas fa-spinner me-2"></i>Buscando...</div>';
            dropdown.style.display = 'block';
            search.classList.add('active');
            searchBodegasModal('', 'Destino');
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!search.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
            search.classList.remove('active');
        }
    });
}

// Función compartida para buscar bodegas
function searchBodegasModal(query, tipo) {
    fetch(`/movimientos/bodegas/buscar/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayBodegaModalResults(data.results, tipo);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const dropdown = document.getElementById(`bodega${tipo}Dropdown`);
            dropdown.innerHTML = '<div class="autocomplete-no-results text-danger">Error de conexión</div>';
        });
}

function displayBodegaModalResults(results, tipo) {
    const dropdown = document.getElementById(`bodega${tipo}Dropdown`);
    
    if (results.length === 0) {
        dropdown.innerHTML = '<div class="autocomplete-no-results">No se encontraron bodegas</div>';
    } else {
        let html = '';
        results.forEach(bodega => {
            html += `
                <div class="autocomplete-item" data-id="${bodega.id}" data-codigo="${bodega.codigo}" data-nombre="${bodega.nombre}">
                    <div class="autocomplete-item-code">
                        <i class="fas fa-warehouse me-2"></i>${bodega.codigo}
                    </div>
                    <div class="autocomplete-item-name">${bodega.nombre}</div>
                </div>
            `;
        });
        dropdown.innerHTML = html;
        
        dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('click', function() {
                selectBodegaModal({
                    id: this.dataset.id,
                    codigo: this.dataset.codigo,
                    nombre: this.dataset.nombre
                }, tipo);
            });
        });
    }
    
    dropdown.style.display = 'block';
}

function selectBodegaModal(bodega, tipo) {
    if (tipo === 'Origen') {
        selectedBodegaOrigen = bodega;
    } else {
        selectedBodegaDestino = bodega;
    }
    
    document.getElementById(`bodega${tipo}Id`).value = bodega.id;
    document.getElementById(`bodega${tipo}Search`).value = `${bodega.codigo} - ${bodega.nombre}`;
    document.getElementById(`bodega${tipo}Dropdown`).style.display = 'none';
    document.getElementById(`bodega${tipo}Search`).classList.remove('active');
}
