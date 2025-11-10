/* ===================================
   MÓDULO DE USUARIOS - JAVASCRIPT
   Funcionalidad para gestión de usuarios
   =================================== */

let editMode = false;
let currentUsuarioId = null;

// Abrir modal para crear
function openCreateModal() {
    editMode = false;
    document.getElementById('modalTitle').textContent = 'Agregar Nuevo Usuario';
    document.getElementById('btnSaveText').textContent = 'Guardar Usuario';
    document.getElementById('usuarioForm').reset();
    document.getElementById('usuarioId').value = '';
    document.getElementById('username').readOnly = false;
    document.getElementById('password').required = true;
    document.getElementById('passwordRequired').style.display = 'inline';
    document.getElementById('passwordHelp').textContent = 'Mínimo 8 caracteres';
}

// Editar usuario
function editUsuario(id) {
    editMode = true;
    currentUsuarioId = id;
    
    fetch(`/usuarios/${id}/edit/`)
        .then(response => response.json())
        .then(data => {
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
            
            const modal = new bootstrap.Modal(document.getElementById('modalUsuario'));
            modal.show();
        })
        .catch(error => {
            alert('Error al cargar los datos del usuario');
            console.error(error);
        });
}

// Ver detalles
function viewUsuario(id) {
    editUsuario(id);
}

// Guardar usuario (crear o actualizar)
function saveUsuario() {
    const form = document.getElementById('usuarioForm');
    const formData = new FormData(form);
    
    let url = editMode ? `/usuarios/${currentUsuarioId}/edit/` : '/usuarios/create/';
    
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
            alert(data.message);
            window.location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        alert('Error al guardar el usuario');
        console.error(error);
    });
}

// Desactivar usuario
function deleteUsuario(id, username) {
    if (confirm(`¿Está seguro de desactivar al usuario "${username}"?`)) {
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
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert('Error al desactivar el usuario');
            console.error(error);
        });
    }
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
    alert('Exportando a Excel... (función pendiente de implementación)');
    // Aquí se puede implementar la exportación real usando una librería o endpoint backend
}

// Exportar a PDF
function exportarPDF() {
    alert('Exportando a PDF... (función pendiente de implementación)');
    // Aquí se puede implementar la exportación real
}

// Event delegation para botones de acción
document.addEventListener('DOMContentLoaded', function() {
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
    
    // Vista previa de foto de perfil
    const fotoInput = document.getElementById('foto_perfil');
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño (2MB)
                if (file.size > 2 * 1024 * 1024) {
                    alert('El archivo es demasiado grande. Máximo 2MB.');
                    e.target.value = '';
                    return;
                }
                
                // Validar tipo
                if (!file.type.startsWith('image/')) {
                    alert('Por favor selecciona un archivo de imagen válido.');
                    e.target.value = '';
                    return;
                }
                
                // Mostrar vista previa
                const reader = new FileReader();
                reader.onload = function(event) {
                    document.getElementById('fotoPreviewImg').src = event.target.result;
                    document.getElementById('fotoPreview').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
