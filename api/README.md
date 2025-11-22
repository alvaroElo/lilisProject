# API REST - Dulcería Lilis

API CRUD completa usando Django REST Framework.

## Modelos Expuestos

### 1. Categoria
### 2. Marca

## Endpoints Disponibles

### Categorías

| Método | URL | Acción |
|--------|-----|--------|
| GET | `/api/categorias/` | Lista todas las categorías |
| POST | `/api/categorias/` | Crea una nueva categoría |
| GET | `/api/categorias/<id>/` | Ver una categoría específica |
| PUT | `/api/categorias/<id>/` | Actualizar una categoría |
| DELETE | `/api/categorias/<id>/` | Eliminar una categoría |

### Marcas

| Método | URL | Acción |
|--------|-----|--------|
| GET | `/api/marcas/` | Lista todas las marcas |
| POST | `/api/marcas/` | Crea una nueva marca |
| GET | `/api/marcas/<id>/` | Ver una marca específica |
| PUT | `/api/marcas/<id>/` | Actualizar una marca |
| DELETE | `/api/marcas/<id>/` | Eliminar una marca |

## Estructura de Datos

### Categoria
```json
{
    "id": 1,
    "nombre": "Dulces",
    "descripcion": "Productos dulces variados",
    "activo": true
}
```

### Marca
```json
{
    "id": 1,
    "nombre": "Ambrosoli",
    "descripcion": "Marca chilena de dulces",
    "activo": true
}
```

## Autenticación

Todos los endpoints requieren autenticación. El usuario debe estar logueado en el sistema.

## Pruebas

### Con navegador
Visita: `http://localhost:8000/api/` para ver la interfaz navegable de DRF.

### Con curl o Postman
Ejemplos:

```bash
# GET - Listar categorías
curl -X GET http://localhost:8000/api/categorias/ -u usuario:contraseña

# POST - Crear categoría
curl -X POST http://localhost:8000/api/categorias/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Chocolates", "descripcion": "Productos de chocolate", "activo": true}' \
  -u usuario:contraseña

# PUT - Actualizar categoría
curl -X PUT http://localhost:8000/api/categorias/1/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Chocolates Premium", "descripcion": "Chocolates de alta calidad", "activo": true}' \
  -u usuario:contraseña

# DELETE - Eliminar categoría
curl -X DELETE http://localhost:8000/api/categorias/1/ -u usuario:contraseña
```
