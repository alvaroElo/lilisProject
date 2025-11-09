/**
 * DULCERÍA LILIS - DASHBOARD JS
 * Funcionalidad para sidebar, dropdowns y notificaciones
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // === SIDEBAR TOGGLE ===
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            if (window.innerWidth > 992) {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('expanded');
            } else {
                sidebar.classList.toggle('show');
            }
        });
    }
    
    // Cerrar sidebar en móvil al hacer clic en un enlace
    const sidebarLinks = document.querySelectorAll('.sidebar-menu-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('show');
            }
        });
    });
    
    // === USER DROPDOWN ===
    const userProfileButton = document.querySelector('.user-profile-button');
    const userDropdown = document.querySelector('.user-dropdown');
    
    if (userProfileButton && userDropdown) {
        userProfileButton.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
            // Cerrar notificaciones si está abierto
            if (notificationDropdown) {
                notificationDropdown.classList.remove('show');
            }
        });
    }
    
    // === NOTIFICATION DROPDOWN ===
    const notificationBell = document.querySelector('.notification-bell');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    
    if (notificationBell && notificationDropdown) {
        notificationBell.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationDropdown.classList.toggle('show');
            // Cerrar user dropdown si está abierto
            if (userDropdown) {
                userDropdown.classList.remove('show');
            }
        });
    }
    
    // === CERRAR DROPDOWNS AL HACER CLIC FUERA ===
    document.addEventListener('click', function(e) {
        if (userDropdown && !userDropdown.contains(e.target) && !userProfileButton.contains(e.target)) {
            userDropdown.classList.remove('show');
        }
        if (notificationDropdown && !notificationDropdown.contains(e.target) && !notificationBell.contains(e.target)) {
            notificationDropdown.classList.remove('show');
        }
    });
    
    // === MARCAR NOTIFICACIÓN COMO LEÍDA ===
    const notificationItems = document.querySelectorAll('.notification-item');
    notificationItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.remove('unread');
            updateNotificationCount();
        });
    });
    
    // === ACTUALIZAR CONTADOR DE NOTIFICACIONES ===
    function updateNotificationCount() {
        const unreadCount = document.querySelectorAll('.notification-item.unread').length;
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            if (unreadCount > 0) {
                badge.textContent = unreadCount;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }
    
    // === HIGHLIGHT MENÚ ACTIVO ===
    const currentPath = window.location.pathname;
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });
    
    // === RESPONSIVE SIDEBAR ===
    function handleResize() {
        if (window.innerWidth > 992) {
            sidebar.classList.remove('show');
        }
    }
    
    window.addEventListener('resize', handleResize);
    
    // === PREVENIR CIERRE DE DROPDOWN AL HACER CLIC DENTRO ===
    if (userDropdown) {
        userDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    if (notificationDropdown) {
        notificationDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Inicializar contador de notificaciones
    updateNotificationCount();
});

/**
 * FUNCIONES AUXILIARES
 */

// Mostrar alerta temporal
function showAlert(message, type = 'info', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '250px';
    alertDiv.style.animation = 'slideIn 0.3s ease-out';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(alertDiv);
        }, 300);
    }, duration);
}

// Confirmar acción
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}
