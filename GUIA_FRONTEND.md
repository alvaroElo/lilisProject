# Guía de Frontend - Dulcería Lilis

## Objetivo
Este documento proporciona instrucciones detalladas para desarrollar interfaces de usuario consistentes con el sistema de diseño de Dulcería Lilis. Está diseñado para ser interpretado por asistentes de IA.

---

## 1. Paleta de Colores

### Variables CSS Principales
```css
--color-header: #D20A11          /* Rojo principal para encabezados */
--color-footer: #230E00          /* Café oscuro para footer */
--color-submenu: #c4a75b         /* Dorado para navegación y acentos */
--color-text-focus: #1b1919      /* Negro para texto importante */
--color-text: #4e4e4e            /* Gris para texto normal */
--color-text2: #c4a75b           /* Dorado para texto alternativo */
```

### Colores de Estado
```css
--color-success: #28a745         /* Verde para éxito */
--color-danger: #dc3545          /* Rojo para errores/peligro */
--color-warning: #ffc107         /* Amarillo para advertencias */
--color-info: #17a2b8            /* Azul para información */
```

### Uso de Colores
- **Rojo (#D20A11)**: Header, botones primarios, bordes activos
- **Dorado (#c4a75b)**: Navegación, botones secundarios, badges de rol
- **Café (#230E00)**: Footer únicamente
- **Verde (#28a745)**: Confirmaciones, validaciones correctas, badges de "activo"
- **Rojo (#dc3545)**: Errores, validaciones fallidas, botones de eliminar

---


## 12. Reglas de Oro

1. **Consistencia**: Usar siempre las mismas clases para elementos similares
2. **Semántica**: Los colores tienen significado (rojo=peligro, verde=éxito, etc.)
3. **Espaciado**: Usar clases utilitarias, no CSS inline
4. **Validación**: Todos los formularios deben validarse
5. **Accesibilidad**: Labels asociados a inputs, alt en imágenes
6. **Performance**: Cargar CSS antes de contenido, JS al final del body

