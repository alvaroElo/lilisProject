# 🎨 SweetAlert2 en Formularios de Usuario

## ✅ Mejoras Implementadas

### 1. **Loading al Cargar Datos para Edición**
Cuando se hace clic en "Editar" usuario:
```javascript
Swal.fire({
    title: 'Cargando...',
    html: 'Obteniendo datos del usuario',
    allowOutsideClick: false,
    didOpen: () => {
        Swal.showLoading();
    }
});
```
- ✅ Spinner de carga mientras se obtienen los datos
- ✅ Bloquea interacción durante la carga
- ✅ Se cierra automáticamente al cargar el modal

---

### 2. **Validación del Lado del Cliente con SweetAlert2**

#### Validaciones Implementadas:
- ✅ **Username**: Mínimo 3 caracteres
- ✅ **Password**: Mínimo 8 caracteres (requerido en creación, opcional en edición)
- ✅ **Email**: Formato válido con @
- ✅ **Nombre**: Mínimo 2 caracteres
- ✅ **Apellido**: Mínimo 2 caracteres
- ✅ **Rol**: Debe seleccionarse

#### Mensaje de Error:
```javascript
Swal.fire({
    title: 'Errores de Validación',
    html: '<ul style="text-align: left;">
            <li>Error 1</li>
            <li>Error 2</li>
          </ul>',
    icon: 'warning',
    confirmButtonColor: '#ffc107'
});
```

---

### 3. **Loading al Guardar/Actualizar**

```javascript
Swal.fire({
    title: 'Guardando...',
    html: '<i class="fas fa-user-edit fa-2x mb-3"></i><br>Por favor espere',
    allowOutsideClick: false,
    didOpen: () => {
        Swal.showLoading();
    }
});
```

- ✅ Icono animado de usuario
- ✅ Mensaje dinámico: "Guardando..." o "Actualizando..."
- ✅ Bloquea doble submit

---

### 4. **Mensaje de Éxito con Timer**

```javascript
Swal.fire({
    title: '¡Éxito!',
    text: 'Usuario guardado correctamente',
    icon: 'success',
    confirmButtonColor: '#198754',
    timer: 2000,
    timerProgressBar: true
}).then(() => {
    window.location.reload();
});
```

- ✅ Timer de 2 segundos
- ✅ Progress bar animado
- ✅ Recarga automática de página
- ✅ Modal se cierra antes de recargar

---

### 5. **Validación de Foto de Perfil**

#### Tamaño de Archivo:
```javascript
if (file.size > 2 * 1024 * 1024) {
    Swal.fire({
        title: 'Archivo muy grande',
        html: 'Tamaño máximo: <strong>2MB</strong>',
        icon: 'warning'
    });
}
```

#### Tipo de Archivo:
```javascript
if (!file.type.startsWith('image/')) {
    Swal.fire({
        title: 'Formato no válido',
        html: 'Formatos aceptados: <strong>JPG, PNG, GIF</strong>',
        icon: 'warning'
    });
}
```

#### Confirmación de Carga:
```javascript
Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: 'Imagen cargada',
    timer: 2000,
    timerProgressBar: true
});
```
- ✅ Notificación tipo "toast" en esquina superior derecha
- ✅ No bloquea la interacción
- ✅ Desaparece automáticamente

---

### 6. **Confirmación al Cerrar Modal con Cambios**

```javascript
Swal.fire({
    title: '¿Descartar cambios?',
    text: 'Tienes cambios sin guardar',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Sí, descartar',
    cancelButtonText: 'Seguir editando',
    reverseButtons: true
});
```

- ✅ Detecta automáticamente cambios en el formulario
- ✅ Pregunta antes de cerrar si hay cambios
- ✅ Permite continuar editando o descartar
- ✅ Se resetea al guardar exitosamente

---

### 7. **Manejo de Errores del Backend**

```javascript
Swal.fire({
    title: 'Error de Validación',
    html: data.message,
    icon: 'warning',
    confirmButtonColor: '#ffc107'
});
```

- ✅ Muestra mensajes de error del servidor
- ✅ Color amarillo para errores de validación
- ✅ Color rojo para errores del sistema

---

## 📋 Flujos Completos

### Flujo de Creación:
1. Usuario hace clic en "Agregar Usuario"
2. Modal se abre limpio
3. Usuario llena campos
4. **Si intenta cerrar**: Pregunta si descartar cambios
5. Usuario hace clic en "Guardar"
6. **Validación del lado del cliente**:
   - ❌ Si hay errores → Muestra lista de errores
   - ✅ Si pasa → Continúa
7. **Loading**: "Guardando..."
8. **Backend responde**:
   - ✅ Éxito → SweetAlert éxito → Recarga página
   - ❌ Error → SweetAlert error con mensaje

### Flujo de Edición:
1. Usuario hace clic en "Editar"
2. **Loading**: "Cargando..."
3. Datos se cargan en el modal
4. Usuario modifica campos
5. **Si intenta cerrar**: Pregunta si descartar cambios
6. Usuario hace clic en "Actualizar"
7. **Validación del lado del cliente**
8. **Loading**: "Actualizando..."
9. **Backend responde**:
   - ✅ Éxito → SweetAlert éxito → Recarga
   - ❌ Error → SweetAlert error

### Flujo de Foto de Perfil:
1. Usuario selecciona archivo
2. **Validación de tamaño**: Max 2MB
3. **Validación de tipo**: Solo imágenes
4. **Toast de éxito**: "Imagen cargada"
5. **Preview**: Muestra imagen seleccionada

---

## 🎨 Estilos y Colores

| Tipo | Color | Uso |
|------|-------|-----|
| Éxito | Verde (#198754) | Operaciones exitosas |
| Error | Rojo (#dc3545) | Errores del sistema |
| Warning | Amarillo (#ffc107) | Validaciones, advertencias |
| Info | Azul (#0d6efd) | Información general |
| Confirmación | Rojo + Gris | Acciones destructivas |

---

## 🔧 Funciones Agregadas

### `validateForm(formData, isEdit)`
Valida todos los campos del formulario antes de enviar.

**Parámetros:**
- `formData`: FormData object con los datos del formulario
- `isEdit`: Boolean indicando si es edición o creación

**Retorna:**
- Array de strings con mensajes de error
- Array vacío si no hay errores

**Validaciones:**
- Username mínimo 3 caracteres
- Password mínimo 8 caracteres
- Email formato válido
- Nombres mínimo 2 caracteres
- Rol seleccionado

---

## 📊 Comparación Antes/Después

### Antes (alert nativo):
```javascript
alert('Usuario guardado correctamente');
```
- ❌ Feo y genérico
- ❌ Sin iconos
- ❌ Sin estilos
- ❌ Bloquea toda la página
- ❌ No es responsive

### Después (SweetAlert2):
```javascript
Swal.fire({
    title: '¡Éxito!',
    text: 'Usuario guardado correctamente',
    icon: 'success',
    timer: 2000,
    timerProgressBar: true
});
```
- ✅ Elegante y profesional
- ✅ Con iconos animados
- ✅ Estilos corporativos
- ✅ Modal centrado
- ✅ Completamente responsive
- ✅ Timer automático
- ✅ Progress bar

---

## 🧪 Casos de Prueba

### Test 1: Crear Usuario Válido
1. Abrir modal de creación
2. Llenar todos los campos correctamente
3. Click en "Guardar"
4. **Esperado**: Loading → Éxito → Recarga

### Test 2: Crear Usuario Inválido
1. Abrir modal de creación
2. Dejar campos vacíos o con datos inválidos
3. Click en "Guardar"
4. **Esperado**: Lista de errores de validación

### Test 3: Editar Usuario
1. Click en "Editar" usuario
2. **Esperado**: Loading → Datos cargados
3. Modificar campos
4. Click en "Actualizar"
5. **Esperado**: Loading → Éxito → Recarga

### Test 4: Cerrar Modal con Cambios
1. Abrir modal (crear o editar)
2. Modificar cualquier campo
3. Click fuera del modal o botón X
4. **Esperado**: Pregunta si descartar cambios

### Test 5: Foto de Perfil Inválida
1. Intentar subir archivo > 2MB
2. **Esperado**: Error de tamaño
3. Intentar subir archivo no-imagen
4. **Esperado**: Error de formato

### Test 6: Foto de Perfil Válida
1. Subir imagen < 2MB
2. **Esperado**: Toast de éxito + Preview

---

## 📦 Archivos Modificados

- ✅ `static/js/usuarios.js` - Todas las mejoras implementadas
- ✅ `templates/base.html` - CDN de SweetAlert2 (ya estaba)

---

## 🎯 Beneficios

1. **UX Mejorada**: Feedback visual claro en cada acción
2. **Validación Temprana**: Evita requests innecesarios al servidor
3. **Prevención de Errores**: Confirma acciones destructivas
4. **Feedback Continuo**: Usuario siempre sabe qué está pasando
5. **Profesional**: Apariencia moderna y consistente
6. **Responsive**: Funciona en todos los dispositivos

---

## 🚀 Próximas Mejoras Sugeridas

1. **Validación en tiempo real**: Mostrar errores mientras el usuario escribe
2. **Confirmación de email**: Enviar código de verificación
3. **Fuerza de contraseña**: Indicador visual de seguridad
4. **Autoguardado**: Guardar borradores automáticamente
5. **Deshacer**: Opción de revertir cambios recientes

---

*Documento actualizado: 10/11/2025*
*Versión: 2.0.0*
