/* ===================================
   MÓDULO DE PROVEEDORES - JAVASCRIPT
   Funcionalidad para gestión de proveedores
   =================================== */

let editMode = false;
let currentProveedorId = null;
let formChanged = false;

// Validar formulario antes de enviar
function validateForm(formData, isEdit = false) {
    const errors = [];
    
    // Validar RUT/NIF
    const rut_nif = formData.get('rut_nif');
    if (!rut_nif || rut_nif.trim().length < 3) {
        errors.push('El RUT/NIF debe tener al menos 3 caracteres');
    }
    
    // Validar razón social
    const razon_social = formData.get('razon_social');
    if (!razon_social || razon_social.trim().length < 3) {
        errors.push('La razón social debe tener al menos 3 caracteres');
    }
    
    // Validar email
    const email = formData.get('email');
    if (!email || !email.includes('@')) {
        errors.push('El email no es válido');
    }
    
    // Validar condiciones de pago
    const condiciones_pago = formData.get('condiciones_pago');
    if (!condiciones_pago) {
        errors.push('Debe seleccionar las condiciones de pago');
    }
    
    return errors;
}

// Abrir modal para crear
function openCreateModal() {
    // Verificar permisos
    if (typeof PERMISOS !== 'undefined' && !PERMISOS.crear) {
        Swal.fire({
            icon: 'error',
            title: 'Acceso Denegado',
            text: 'No tienes permisos para crear proveedores',
            confirmButtonColor: '#D20A11'
        });
        return;
    }
    
    editMode = false;
    document.getElementById('modalTitle').textContent = 'Agregar Nuevo Proveedor';
    document.getElementById('btnSaveText').textContent = 'Guardar Proveedor';
    document.getElementById('proveedorForm').reset();
    document.getElementById('proveedorId').value = '';
    
    // Habilitar todos los campos
    const formElements = document.querySelectorAll('#proveedorForm input, #proveedorForm select, #proveedorForm textarea');
    formElements.forEach(element => {
        element.readOnly = false;
        if (element.tagName === 'SELECT') {
            element.disabled = false;
        }
    });
    document.getElementById('rut_nif').readOnly = false;
    
    // Mostrar botones de Guardar y Cancelar, ocultar Cerrar
    document.getElementById('btnGuardar').style.display = 'inline-block';
    document.getElementById('btnCancelar').style.display = 'inline-block';
    document.getElementById('btnCerrar').style.display = 'none';
    
    // Mostrar/ocultar campo detalle condiciones
    toggleCondicionesDetalle();
}

// Mostrar/ocultar campo de detalle de condiciones de pago
function toggleCondicionesDetalle() {
    const condicionesPago = document.getElementById('condiciones_pago').value;
    const detalleGroup = document.getElementById('condicionesDetalleGroup');
    
    if (condicionesPago === 'OTRO') {
        detalleGroup.style.display = 'block';
        document.getElementById('condiciones_pago_detalle').required = true;
    } else {
        detalleGroup.style.display = 'none';
        document.getElementById('condiciones_pago_detalle').required = false;
        document.getElementById('condiciones_pago_detalle').value = '';
    }
}

// Editar proveedor
function editProveedor(id) {
    // Verificar permisos
    if (typeof PERMISOS !== 'undefined' && !PERMISOS.editar) {
        Swal.fire({
            icon: 'error',
            title: 'Acceso Denegado',
            text: 'No tienes permisos para editar proveedores',
            confirmButtonColor: '#D20A11'
        });
        return;
    }
    
    editMode = true;
    currentProveedorId = id;
    
    // Mostrar loading
    Swal.fire({
        title: 'Cargando...',
        html: 'Obteniendo datos del proveedor',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    fetch(`/proveedores/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            Swal.close();
            
            document.getElementById('modalTitle').textContent = 'Editar Proveedor';
            document.getElementById('btnSaveText').textContent = 'Actualizar Proveedor';
            
            document.getElementById('proveedorId').value = data.id;
            document.getElementById('rut_nif').value = data.rut_nif;
            document.getElementById('razon_social').value = data.razon_social;
            document.getElementById('nombre_fantasia').value = data.nombre_fantasia;
            document.getElementById('email').value = data.email;
            document.getElementById('telefono').value = data.telefono;
            document.getElementById('sitio_web').value = data.sitio_web;
            document.getElementById('direccion').value = data.direccion;
            document.getElementById('ciudad').value = data.ciudad;
            document.getElementById('pais').value = data.pais;
            document.getElementById('condiciones_pago').value = data.condiciones_pago;
            document.getElementById('condiciones_pago_detalle').value = data.condiciones_pago_detalle;
            document.getElementById('moneda').value = data.moneda;
            document.getElementById('contacto_principal_nombre').value = data.contacto_principal_nombre;
            document.getElementById('contacto_principal_email').value = data.contacto_principal_email;
            document.getElementById('contacto_principal_telefono').value = data.contacto_principal_telefono;
            document.getElementById('estado').value = data.estado;
            document.getElementById('observaciones').value = data.observaciones;
            
            // Habilitar todos los campos excepto RUT/NIF
            const formElements = document.querySelectorAll('#proveedorForm input, #proveedorForm select, #proveedorForm textarea');
            formElements.forEach(element => {
                element.readOnly = false;
                if (element.tagName === 'SELECT') {
                    element.disabled = false;
                }
            });
            document.getElementById('rut_nif').readOnly = true; // RUT/NIF no se puede editar
            
            // Mostrar botones de Guardar y Cancelar, ocultar Cerrar
            document.getElementById('btnGuardar').style.display = 'inline-block';
            document.getElementById('btnCancelar').style.display = 'inline-block';
            document.getElementById('btnCerrar').style.display = 'none';
            
            // Mostrar/ocultar campo detalle condiciones
            toggleCondicionesDetalle();
            
            const modal = new bootstrap.Modal(document.getElementById('modalProveedor'));
            modal.show();
        })
        .catch(error => {
            Swal.fire({
                title: 'Error',
                text: 'Error al cargar los datos del proveedor',
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
            console.error(error);
        });
}

// Ver detalles (solo lectura)
function viewProveedor(id) {
    editMode = false;
    currentProveedorId = id;
    
    // Mostrar loading
    Swal.fire({
        title: 'Cargando...',
        html: 'Obteniendo datos del proveedor',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    fetch(`/proveedores/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            Swal.close();
            
            document.getElementById('modalTitle').textContent = 'Detalle del Proveedor';
            
            // Llenar el formulario con los datos
            document.getElementById('proveedorId').value = data.id;
            document.getElementById('rut_nif').value = data.rut_nif;
            document.getElementById('razon_social').value = data.razon_social;
            document.getElementById('nombre_fantasia').value = data.nombre_fantasia;
            document.getElementById('email').value = data.email;
            document.getElementById('telefono').value = data.telefono;
            document.getElementById('sitio_web').value = data.sitio_web;
            document.getElementById('direccion').value = data.direccion;
            document.getElementById('ciudad').value = data.ciudad;
            document.getElementById('pais').value = data.pais;
            document.getElementById('condiciones_pago').value = data.condiciones_pago;
            document.getElementById('condiciones_pago_detalle').value = data.condiciones_pago_detalle;
            document.getElementById('moneda').value = data.moneda;
            document.getElementById('contacto_principal_nombre').value = data.contacto_principal_nombre;
            document.getElementById('contacto_principal_email').value = data.contacto_principal_email;
            document.getElementById('contacto_principal_telefono').value = data.contacto_principal_telefono;
            document.getElementById('estado').value = data.estado;
            document.getElementById('observaciones').value = data.observaciones;
            
            // Mostrar/ocultar campo detalle condiciones
            toggleCondicionesDetalle();
            
            // MODO SOLO LECTURA: Deshabilitar todos los campos
            const formElements = document.querySelectorAll('#proveedorForm input, #proveedorForm select, #proveedorForm textarea');
            formElements.forEach(element => {
                element.readOnly = true;
                if (element.tagName === 'SELECT') {
                    element.disabled = true;
                }
            });
            
            // Ocultar botones de Guardar y Cancelar, mostrar solo Cerrar
            document.getElementById('btnGuardar').style.display = 'none';
            document.getElementById('btnCancelar').style.display = 'none';
            document.getElementById('btnCerrar').style.display = 'inline-block';
            
            const modal = new bootstrap.Modal(document.getElementById('modalProveedor'));
            modal.show();
        })
        .catch(error => {
            Swal.fire({
                title: 'Error',
                text: 'Error al cargar los datos del proveedor',
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
            console.error(error);
        });
}

// Guardar proveedor (crear o actualizar)
function saveProveedor() {
    const form = document.getElementById('proveedorForm');
    const formData = new FormData(form);
    
    // Validar campos del lado del cliente
    const validationErrors = validateForm(formData, editMode);
    if (validationErrors.length > 0) {
        Swal.fire({
            title: 'Errores de Validación',
            html: '<ul style="text-align: left;">' + 
                  validationErrors.map(err => `<li>${err}</li>`).join('') + 
                  '</ul>',
            icon: 'warning',
            confirmButtonColor: '#ffc107'
        });
        return;
    }
    
    let url = editMode ? `/proveedores/${currentProveedorId}/edit/` : '/proveedores/create/';
    let action = editMode ? 'Actualizando' : 'Guardando';
    
    // Mostrar loading
    Swal.fire({
        title: `${action}...`,
        html: '<i class="fas fa-truck fa-2x mb-3"></i><br>Por favor espere',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            formChanged = false;
            
            Swal.fire({
                title: '¡Éxito!',
                text: data.message,
                icon: 'success',
                confirmButtonColor: '#198754',
                timer: 2000,
                timerProgressBar: true
            }).then(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('modalProveedor'));
                if (modal) modal.hide();
                window.location.reload();
            });
        } else {
            Swal.fire({
                title: 'Error de Validación',
                html: data.message,
                icon: 'warning',
                confirmButtonColor: '#ffc107'
            });
        }
    })
    .catch(error => {
        Swal.fire({
            title: 'Error',
            text: 'Error al guardar el proveedor',
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
        console.error(error);
    });
}

// Bloquear proveedor
function deleteProveedor(id, razon_social) {
    // Verificar permisos
    if (typeof PERMISOS !== 'undefined' && !PERMISOS.eliminar) {
        Swal.fire({
            icon: 'error',
            title: 'Acceso Denegado',
            text: 'No tienes permisos para bloquear proveedores',
            confirmButtonColor: '#D20A11'
        });
        return;
    }
    
    Swal.fire({
        title: '¿Bloquear Proveedor?',
        html: `¿Está seguro de bloquear al proveedor <strong>"${razon_social}"</strong>?<br><br>El proveedor no podrá ser usado en nuevas compras.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '<i class="fas fa-ban me-2"></i>Sí, bloquear',
        cancelButtonText: '<i class="fas fa-times me-2"></i>Cancelar',
        reverseButtons: true,
        focusCancel: true
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Bloqueando...',
                html: 'Por favor espere',
                allowOutsideClick: false,
                allowEscapeKey: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });
            
            fetch(`/proveedores/${id}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: '¡Bloqueado!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonColor: '#198754',
                        timer: 2000,
                        timerProgressBar: true
                    }).then(() => {
                        window.location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: data.message,
                        icon: 'error',
                        confirmButtonColor: '#dc3545'
                    });
                }
            })
            .catch(error => {
                Swal.fire({
                    title: 'Error',
                    text: 'Error al bloquear el proveedor',
                    icon: 'error',
                    confirmButtonColor: '#dc3545'
                });
                console.error(error);
            });
        }
    });
}

// Cambiar registros por página
function changePerPage(value) {
    const url = new URL(window.location.href);
    url.searchParams.set('per_page', value);
    url.searchParams.set('page', 1);
    window.location.href = url.toString();
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
    
    const exportUrl = `/proveedores/exportar-excel/${params ? '?' + params : ''}`;
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
    }, 1500);
}

// Función para ordenar tabla
function sortTable(field) {
    const url = new URL(window.location.href);
    const currentSort = url.searchParams.get('sort');
    const currentOrder = url.searchParams.get('order') || 'desc';
    
    if (currentSort === field) {
        url.searchParams.set('order', currentOrder === 'asc' ? 'desc' : 'asc');
    } else {
        url.searchParams.set('sort', field);
        url.searchParams.set('order', 'asc');
    }
    
    url.searchParams.set('page', 1);
    window.location.href = url.toString();
}

// Event delegation
document.addEventListener('DOMContentLoaded', function() {
    // Detectar cambios en el formulario
    const form = document.getElementById('proveedorForm');
    if (form) {
        form.addEventListener('input', function() {
            formChanged = true;
        });
        
        form.addEventListener('change', function() {
            formChanged = true;
        });
    }
    
    // Al abrir modal, resetear flag
    const modalElement = document.getElementById('modalProveedor');
    if (modalElement) {
        modalElement.addEventListener('show.bs.modal', function() {
            formChanged = false;
        });
        
        // Confirmar antes de cerrar si hay cambios
        modalElement.addEventListener('hide.bs.modal', function(e) {
            if (formChanged) {
                e.preventDefault();
                Swal.fire({
                    title: '¿Descartar cambios?',
                    text: 'Tienes cambios sin guardar',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#dc3545',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: '<i class="fas fa-trash me-2"></i>Sí, descartar',
                    cancelButtonText: '<i class="fas fa-times me-2"></i>Seguir editando',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        formChanged = false;
                        const modal = bootstrap.Modal.getInstance(modalElement);
                        modal.hide();
                    }
                });
            }
        });
    }
    
    // Event listener para condiciones de pago
    const condicionesPagoSelect = document.getElementById('condiciones_pago');
    if (condicionesPagoSelect) {
        condicionesPagoSelect.addEventListener('change', toggleCondicionesDetalle);
    }
    
    // Delegar eventos a los botones de acción
    document.body.addEventListener('click', function(e) {
        const button = e.target.closest('.btn-action-solid');
        if (!button) return;
        
        const action = button.dataset.action;
        const id = button.dataset.id;
        const razon_social = button.dataset.razonsocial;
        
        switch(action) {
            case 'view':
                viewProveedor(id);
                break;
            case 'edit':
                editProveedor(id);
                break;
            case 'delete':
                deleteProveedor(id, razon_social);
                break;
        }
    });
    
    // Manejar click en headers ordenables
    document.querySelectorAll('.sortable').forEach(function(th) {
        th.addEventListener('click', function() {
            const field = this.dataset.sort;
            sortTable(field);
        });
    });
    
    // Actualizar iconos de ordenamiento según estado actual
    const urlParams = new URLSearchParams(window.location.search);
    const currentSort = urlParams.get('sort');
    const currentOrder = urlParams.get('order') || 'desc';
    
    if (currentSort) {
        document.querySelectorAll('.sortable').forEach(function(th) {
            const icon = th.querySelector('.sort-icon');
            if (th.dataset.sort === currentSort) {
                th.classList.add('active');
                icon.classList.remove('fa-sort');
                if (currentOrder === 'asc') {
                    icon.classList.add('fa-sort-up');
                } else {
                    icon.classList.add('fa-sort-down');
                }
            } else {
                th.classList.remove('active');
            }
        });
    }
});
