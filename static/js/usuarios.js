/* ===================================
   MÓDULO DE USUARIOS - JAVASCRIPT
   Funcionalidad para gestión de usuarios
   =================================== */

let editMode = false;
let currentUsuarioId = null;
let formChanged = false;

// Validar formulario antes de enviar
function validateForm(formData, isEdit = false) {
    const errors = [];
    
    // Validar username
    const username = formData.get('username');
    if (!username || username.trim().length < 3) {
        errors.push('El nombre de usuario debe tener al menos 3 caracteres');
    }
    
    // Validar password (solo en creación o si se proporciona en edición)
    const password = formData.get('password');
    if (!isEdit && (!password || password.length < 8)) {
        errors.push('La contraseña debe tener al menos 8 caracteres');
    } else if (isEdit && password && password.length > 0 && password.length < 8) {
        errors.push('La contraseña debe tener al menos 8 caracteres');
    }
    
    // Validar email
    const email = formData.get('email');
    if (!email || !email.includes('@')) {
        errors.push('El email no es válido');
    }
    
    // Validar nombres
    const firstName = formData.get('first_name');
    if (!firstName || firstName.trim().length < 2) {
        errors.push('El nombre debe tener al menos 2 caracteres');
    }
    
    const lastName = formData.get('last_name');
    if (!lastName || lastName.trim().length < 2) {
        errors.push('El apellido debe tener al menos 2 caracteres');
    }
    
    // Validar rol
    const rol = formData.get('rol');
    if (!rol) {
        errors.push('Debe seleccionar un rol');
    }
    
    return errors;
}

// Abrir modal para crear
function openCreateModal() {
    editMode = false;
    document.getElementById('modalTitle').textContent = 'Agregar Nuevo Usuario';
    document.getElementById('btnSaveText').textContent = 'Guardar Usuario';
    document.getElementById('usuarioForm').reset();
    document.getElementById('usuarioId').value = '';
    
    // Habilitar todos los campos
    const formElements = document.querySelectorAll('#usuarioForm input, #usuarioForm select, #usuarioForm textarea');
    formElements.forEach(element => {
        element.readOnly = false;
        if (element.tagName === 'SELECT') {
            element.disabled = false;
        }
    });
    
    document.getElementById('username').readOnly = false;
    document.getElementById('password').required = true;
    document.getElementById('passwordRequired').style.display = 'inline';
    document.getElementById('passwordHelp').textContent = 'Mínimo 8 caracteres';
    
    // Mostrar botones de Guardar y Cancelar, ocultar Cerrar
    document.getElementById('btnGuardar').style.display = 'inline-block';
    document.getElementById('btnCancelar').style.display = 'inline-block';
    document.getElementById('btnCerrar').style.display = 'none';
    
    // Limpiar preview de foto
    document.getElementById('fotoPreview').style.display = 'none';
}

// Editar usuario
function editUsuario(id) {
    editMode = true;
    currentUsuarioId = id;
    
    // Mostrar loading
    Swal.fire({
        title: 'Cargando...',
        html: 'Obteniendo datos del usuario',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    fetch(`/usuarios/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            // Cerrar loading
            Swal.close();
            
            document.getElementById('modalTitle').textContent = 'Editar Usuario';
            document.getElementById('btnSaveText').textContent = 'Actualizar Usuario';
            
            document.getElementById('usuarioId').value = data.id;
            document.getElementById('username').value = data.username;
            document.getElementById('username').readOnly = true;
            document.getElementById('first_name').value = data.first_name;
            document.getElementById('last_name').value = data.last_name;
            document.getElementById('email').value = data.email;
            document.getElementById('telefono').value = data.telefono;
            document.getElementById('rol').value = data.rol_id;
            document.getElementById('area_unidad').value = data.area_unidad;
            document.getElementById('estado').value = data.estado;
            
            // Mostrar foto de perfil actual si existe
            if (data.foto_perfil_url) {
                document.getElementById('fotoPreviewImg').src = data.foto_perfil_url;
                document.getElementById('fotoPreview').style.display = 'block';
            } else {
                document.getElementById('fotoPreview').style.display = 'none';
            }
            
            document.getElementById('password').required = false;
            document.getElementById('password').value = '';
            document.getElementById('passwordRequired').style.display = 'none';
            document.getElementById('passwordHelp').textContent = 'Dejar en blanco para mantener la actual';
            
            // Habilitar todos los campos excepto username
            const formElements = document.querySelectorAll('#usuarioForm input, #usuarioForm select, #usuarioForm textarea');
            formElements.forEach(element => {
                element.readOnly = false;
                if (element.tagName === 'SELECT') {
                    element.disabled = false;
                }
            });
            document.getElementById('username').readOnly = true; // Username no se puede editar
            
            // Mostrar botones de Guardar y Cancelar, ocultar Cerrar
            document.getElementById('btnGuardar').style.display = 'inline-block';
            document.getElementById('btnCancelar').style.display = 'inline-block';
            document.getElementById('btnCerrar').style.display = 'none';
            
            const modal = new bootstrap.Modal(document.getElementById('modalUsuario'));
            modal.show();
        })
        .catch(error => {
            Swal.fire({
                title: 'Error',
                text: 'Error al cargar los datos del usuario',
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
            console.error(error);
        });
}

// Ver detalles (solo lectura)
function viewUsuario(id) {
    editMode = false;
    currentUsuarioId = id;
    
    // Mostrar loading
    Swal.fire({
        title: 'Cargando...',
        html: 'Obteniendo datos del usuario',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    fetch(`/usuarios/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
            Swal.close();
            
            document.getElementById('modalTitle').textContent = 'Detalle del Usuario';
            
            document.getElementById('usuarioId').value = data.id;
            document.getElementById('username').value = data.username;
            document.getElementById('first_name').value = data.first_name;
            document.getElementById('last_name').value = data.last_name;
            document.getElementById('email').value = data.email;
            document.getElementById('telefono').value = data.telefono;
            document.getElementById('rol').value = data.rol_id;
            document.getElementById('area_unidad').value = data.area_unidad;
            document.getElementById('estado').value = data.estado;
            
            // Mostrar foto de perfil actual si existe
            if (data.foto_perfil_url) {
                document.getElementById('fotoPreviewImg').src = data.foto_perfil_url;
                document.getElementById('fotoPreview').style.display = 'block';
            } else {
                document.getElementById('fotoPreview').style.display = 'none';
            }
            
            document.getElementById('password').required = false;
            document.getElementById('password').value = '';
            document.getElementById('passwordRequired').style.display = 'none';
            
            // MODO SOLO LECTURA: Deshabilitar todos los campos
            const formElements = document.querySelectorAll('#usuarioForm input, #usuarioForm select, #usuarioForm textarea');
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
            
            const modal = new bootstrap.Modal(document.getElementById('modalUsuario'));
            modal.show();
        })
        .catch(error => {
            Swal.fire({
                title: 'Error',
                text: 'Error al cargar los datos del usuario',
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
            console.error(error);
        });
}

// Guardar usuario (crear o actualizar)
function saveUsuario() {
    const form = document.getElementById('usuarioForm');
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
    
    let url = editMode ? `/usuarios/${currentUsuarioId}/edit/` : '/usuarios/create/';
    let action = editMode ? 'Actualizando' : 'Guardando';
    
    // Mostrar loading
    Swal.fire({
        title: `${action}...`,
        html: '<i class="fas fa-user-edit fa-2x mb-3"></i><br>Por favor espere',
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
            // Resetear flag de cambios antes de cerrar
            formChanged = false;
            
            Swal.fire({
                title: '¡Éxito!',
                text: data.message,
                icon: 'success',
                confirmButtonColor: '#198754',
                timer: 2000,
                timerProgressBar: true
            }).then(() => {
                // Cerrar modal y recargar
                const modal = bootstrap.Modal.getInstance(document.getElementById('modalUsuario'));
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
            text: 'Error al guardar el usuario',
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
        console.error(error);
    });
}

// Desactivar usuario
function deleteUsuario(id, username) {
    Swal.fire({
        title: '¿Desactivar Usuario?',
        html: `¿Está seguro de desactivar al usuario <strong>"${username}"</strong>?<br><br>El usuario no podrá acceder al sistema.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '<i class="fas fa-user-slash me-2"></i>Sí, desactivar',
        cancelButtonText: '<i class="fas fa-times me-2"></i>Cancelar',
        reverseButtons: true,
        focusCancel: true
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar loading
            Swal.fire({
                title: 'Desactivando...',
                html: 'Por favor espere',
                allowOutsideClick: false,
                allowEscapeKey: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });
            
            fetch(`/usuarios/${id}/delete/`, {
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
                        title: '¡Desactivado!',
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
                    text: 'Error al desactivar el usuario',
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
    // Obtener parámetros actuales de la URL (filtros, búsqueda, orden)
    const url = new URL(window.location.href);
    const params = url.searchParams.toString();
    
    // Mostrar mensaje de exportación
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
    
    // Construir URL de exportación con los mismos filtros
    const exportUrl = `/usuarios/exportar-excel/${params ? '?' + params : ''}`;
    
    // Descargar archivo
    window.location.href = exportUrl;
    
    // Cerrar mensaje después de un momento
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

// Exportar a PDF
function exportarPDF() {
    alert('Exportando a PDF... (función pendiente de implementación)');
    // Aquí se puede implementar la exportación real
}

// Función para ordenar tabla
function sortTable(field) {
    const url = new URL(window.location.href);
    const currentSort = url.searchParams.get('sort');
    const currentOrder = url.searchParams.get('order') || 'desc';
    
    // Si es el mismo campo, alternar orden
    if (currentSort === field) {
        url.searchParams.set('order', currentOrder === 'asc' ? 'desc' : 'asc');
    } else {
        // Si es campo nuevo, ordenar ascendente
        url.searchParams.set('sort', field);
        url.searchParams.set('order', 'asc');
    }
    
    // Resetear a página 1 al ordenar
    url.searchParams.set('page', 1);
    
    window.location.href = url.toString();
}

// Event delegation para botones de acción
document.addEventListener('DOMContentLoaded', function() {
    // Detectar cambios en el formulario
    const form = document.getElementById('usuarioForm');
    if (form) {
        form.addEventListener('input', function() {
            formChanged = true;
        });
        
        form.addEventListener('change', function() {
            formChanged = true;
        });
    }
    
    // Al abrir modal, resetear flag
    const modalElement = document.getElementById('modalUsuario');
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
    
    // Delegar eventos a los botones de acción
    document.body.addEventListener('click', function(e) {
        const button = e.target.closest('.btn-action-solid');
        if (!button) return;
        
        const action = button.dataset.action;
        const id = button.dataset.id;
        const username = button.dataset.username;
        
        switch(action) {
            case 'view':
                viewUsuario(id);
                break;
            case 'edit':
                editUsuario(id);
                break;
            case 'delete':
                deleteUsuario(id, username);
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
                // Marcar columna activa
                th.classList.add('active');
                
                // Actualizar icono según orden
                icon.classList.remove('fa-sort');
                if (currentOrder === 'asc') {
                    icon.classList.add('fa-sort-up');
                } else {
                    icon.classList.add('fa-sort-down');
                }
            } else {
                // Columnas no activas
                th.classList.remove('active');
            }
        });
    }
    
    // Vista previa de foto de perfil
    const fotoInput = document.getElementById('foto_perfil');
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño (2MB)
                if (file.size > 2 * 1024 * 1024) {
                    Swal.fire({
                        title: 'Archivo muy grande',
                        html: 'El archivo es demasiado grande.<br>Tamaño máximo: <strong>2MB</strong>',
                        icon: 'warning',
                        confirmButtonColor: '#ffc107'
                    });
                    e.target.value = '';
                    return;
                }
                
                // Validar tipo
                if (!file.type.startsWith('image/')) {
                    Swal.fire({
                        title: 'Formato no válido',
                        html: 'Por favor selecciona un archivo de imagen válido.<br>Formatos aceptados: <strong>JPG, PNG, GIF</strong>',
                        icon: 'warning',
                        confirmButtonColor: '#ffc107'
                    });
                    e.target.value = '';
                    return;
                }
                
                // Mostrar vista previa
                const reader = new FileReader();
                reader.onload = function(event) {
                    document.getElementById('fotoPreviewImg').src = event.target.result;
                    document.getElementById('fotoPreview').style.display = 'block';
                    
                    // Mostrar notificación de éxito
                    Swal.fire({
                        toast: true,
                        position: 'top-end',
                        icon: 'success',
                        title: 'Imagen cargada',
                        showConfirmButton: false,
                        timer: 2000,
                        timerProgressBar: true
                    });
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
