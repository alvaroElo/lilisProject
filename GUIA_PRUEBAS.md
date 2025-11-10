# 🧪 Guía de Pruebas - Nuevas Funcionalidades

## 📋 Tabla de Contenidos
1. [Prueba de SweetAlert2](#prueba-de-sweetalert2)
2. [Prueba de Exportación Excel](#prueba-de-exportación-excel)
3. [Verificación de Estilos](#verificación-de-estilos)

---

## 🎨 Prueba de SweetAlert2

### Opción 1: Prueba Interactiva (Recomendado)
1. Abrir el archivo `test_sweetalert2.html` en un navegador web
2. Probar cada botón para ver las diferentes alertas
3. Verificar que los estilos y animaciones funcionen correctamente

### Opción 2: Prueba en la Aplicación
1. Iniciar el servidor Django:
   ```bash
   python manage.py runserver
   ```

2. Navegar a http://127.0.0.1:8000/usuarios/

3. **Probar eliminación de usuario:**
   - Click en botón rojo "Desactivar" de cualquier usuario
   - Verificar que aparezca el modal de SweetAlert2
   - Verificar elementos visuales:
     - ✅ Título: "¿Desactivar Usuario?"
     - ✅ Texto con nombre del usuario en negrita
     - ✅ Icono de advertencia (⚠️)
     - ✅ Botón rojo "Sí, desactivar" con icono
     - ✅ Botón gris "Cancelar" con icono
   
   - **Al confirmar:**
     - ✅ Aparece modal de carga "Desactivando..."
     - ✅ Spinner de carga animado
     - ✅ Al completar: modal de éxito verde
     - ✅ Timer de 2 segundos con barra de progreso
     - ✅ Página se recarga automáticamente

   - **Al cancelar:**
     - ✅ Modal se cierra sin hacer nada

### Verificación de Colores
- **Botón Confirmar**: Rojo (#dc3545)
- **Botón Cancelar**: Gris (#6c757d)
- **Éxito**: Verde (#198754)
- **Error**: Rojo (#dc3545)

---

## 📊 Prueba de Exportación Excel

### Paso 1: Preparar Datos de Prueba
1. Asegurarse de tener usuarios en la base de datos
2. Si es necesario, ejecutar:
   ```bash
   python scripts/crear_vendedores_test.py
   ```

### Paso 2: Prueba Básica
1. Navegar a http://127.0.0.1:8000/usuarios/
2. Click en botón "Excel" (verde con icono)
3. Verificar:
   - ✅ Aparece SweetAlert2 "Exportando..."
   - ✅ Archivo se descarga automáticamente
   - ✅ Aparece SweetAlert2 de éxito
   - ✅ Nombre del archivo: `usuarios_YYYYMMDD_HHMMSS.xlsx`

### Paso 3: Verificar Contenido del Excel
Abrir el archivo Excel descargado y verificar:

#### Encabezados:
- ✅ Fondo azul (#0066CC)
- ✅ Texto blanco
- ✅ Negrita
- ✅ Centrado horizontal y vertical
- ✅ Bordes en todas las celdas

#### Columnas (en orden):
1. Usuario
2. Nombre Completo
3. Email
4. Teléfono
5. Rol
6. Área/Unidad
7. Estado
8. Fecha Creación

#### Datos:
- ✅ Bordes en todas las celdas
- ✅ Alineación vertical centrada
- ✅ Ancho de columnas optimizado
- ✅ Estados traducidos: "Activo" / "Inactivo"
- ✅ Fechas en formato: DD/MM/YYYY HH:MM

### Paso 4: Prueba con Filtros
1. **Aplicar búsqueda**: Buscar un usuario específico
2. **Exportar**: Click en botón Excel
3. **Verificar**: Solo el usuario buscado aparece en el Excel

4. **Aplicar filtro de rol**: Seleccionar "Vendedor"
5. **Exportar**: Click en botón Excel
6. **Verificar**: Solo usuarios con rol "Vendedor" en el Excel

7. **Aplicar filtro de estado**: Seleccionar "Activo"
8. **Exportar**: Click en botón Excel
9. **Verificar**: Solo usuarios activos en el Excel

### Paso 5: Prueba con Ordenamiento
1. **Ordenar por nombre**: Click en encabezado "Nombre Completo"
2. **Exportar**: Click en botón Excel
3. **Verificar**: Datos en Excel están ordenados por nombre

4. **Cambiar orden**: Click nuevamente (descendente)
5. **Exportar**: Click en botón Excel
6. **Verificar**: Datos en Excel están en orden descendente

### Paso 6: Prueba Combinada
1. Aplicar búsqueda + filtro de rol + ordenamiento
2. Exportar
3. Verificar que el Excel respete todos los filtros y orden

---

## 🎨 Verificación de Estilos

### SweetAlert2
Verificar en el navegador (F12 > Network):
- ✅ sweetalert2.min.css se carga correctamente
- ✅ sweetalert2.min.js se carga correctamente

### Botones en la Tabla
- ✅ Hover sobre botones muestra transición suave
- ✅ Colores: Azul (Ver), Amarillo (Editar), Rojo (Desactivar)

### Headers Ordenables
- ✅ Cursor cambia a pointer al pasar sobre headers
- ✅ Background cambia al hacer hover
- ✅ Iconos de ordenamiento cambian según estado

---

## 🐛 Solución de Problemas

### SweetAlert2 no aparece
1. Verificar consola del navegador (F12)
2. Verificar que los CDN estén cargando:
   ```
   https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css
   https://cdn.jsdelivr.net/npm/sweetalert2@11
   ```
3. Limpiar caché del navegador (Ctrl + Shift + Del)

### Excel no descarga
1. Verificar que openpyxl está instalado:
   ```bash
   pip list | grep openpyxl
   ```
2. Verificar logs del servidor Django
3. Verificar permisos de descarga en el navegador
4. Verificar que la ruta esté registrada:
   ```bash
   python manage.py show_urls | grep exportar
   ```

### Archivo Excel vacío o con errores
1. Verificar que hay datos en la base de datos
2. Verificar logs del servidor para ver errores
3. Verificar que los filtros no están excluyendo todos los registros

### Formato del Excel incorrecto
1. Verificar versión de openpyxl:
   ```bash
   pip show openpyxl
   ```
2. Debe ser versión 3.1.5 o superior
3. Reinstalar si es necesario:
   ```bash
   pip install --upgrade openpyxl
   ```

---

## ✅ Checklist de Pruebas

### SweetAlert2 - Eliminación
- [ ] Modal de confirmación aparece correctamente
- [ ] Colores son correctos (rojo/gris)
- [ ] Iconos Font Awesome se muestran
- [ ] Al confirmar: loading → success → reload
- [ ] Al cancelar: modal se cierra
- [ ] Timer de 2 segundos funciona
- [ ] Progress bar se muestra

### SweetAlert2 - Formularios
- [ ] Loading al hacer clic en "Editar"
- [ ] Datos se cargan correctamente en el modal
- [ ] Validación de campos muestra errores en lista
- [ ] Loading al guardar/actualizar usuario
- [ ] Mensaje de éxito con timer al guardar
- [ ] Confirmación al cerrar modal con cambios
- [ ] Toast de éxito al cargar foto de perfil
- [ ] Error si foto > 2MB
- [ ] Error si archivo no es imagen
- [ ] Validación de email formato correcto
- [ ] Validación de password mínimo 8 caracteres

### Exportación Excel
- [ ] Archivo se descarga
- [ ] Nombre incluye timestamp
- [ ] Encabezados tienen formato (azul/blanco/negrita)
- [ ] 8 columnas presentes
- [ ] Datos correctos
- [ ] Bordes en todas las celdas
- [ ] Ancho de columnas optimizado
- [ ] Fechas en formato correcto
- [ ] Estados traducidos (Activo/Inactivo)

### Filtros y Ordenamiento
- [ ] Búsqueda respetada en exportación
- [ ] Filtro de rol respetado
- [ ] Filtro de estado respetado
- [ ] Ordenamiento respetado
- [ ] Combinación de filtros funciona

---

## 📞 Soporte

Si encuentras algún problema:
1. Revisar esta guía de pruebas
2. Verificar logs del servidor Django
3. Verificar consola del navegador (F12)
4. Revisar el archivo `FUNCIONALIDADES_USUARIOS.md`

---

*Última actualización: 10/11/2025*
