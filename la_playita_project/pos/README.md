# 📦 APP POS - Punto de Venta

## Descripción

App completa de **Punto de Venta (POS)** para el sistema La Playita. Incluye gestión de ventas en tiempo real con carrito de compras, búsqueda de productos, selección de lotes y procesamiento de pagos.

## ✨ Características

### 🎯 Funcionalidades Principales

1. **Interfaz POS Completa**
   - Vista principal con grid de productos
   - Carrito de compras en tiempo real
   - Búsqueda y filtrado de productos
   - Selección de lotes para cada producto

2. **Procesamiento de Ventas**
   - Creación de ventas con detalles
   - Cálculo automático de subtotales e impuestos (19%)
   - Múltiples métodos de pago
   - Canales de venta configurables
   - Actualización automática de stock

3. **Gestión de Lotes**
   - Selección de lote específico para cada producto
   - Control de fecha de caducidad
   - Disponibilidad en tiempo real

4. **Historial y Reportes**
   - Listado completo de ventas con filtros
   - Detalle de cada venta
   - Búsqueda por fecha, método de pago y usuario
   - Impresión de recibos

5. **Admin Mejorado**
   - Registro completo de modelos en Django Admin
   - Inlines para detalles
   - Filtros y búsquedas avanzadas
   - Acciones en lote para cambio de estados (pedidos)

## 📁 Estructura de Archivos

```
pos/
├── migrations/
├── static/
│   └── pos/
│       └── js/
│           └── carrito.js          # Lógica del carrito (JavaScript)
├── templates/
│   └── pos/
│       ├── pos_main.html           # Vista principal POS
│       ├── venta_detalle.html      # Detalle de una venta
│       └── listar_ventas.html      # Listado de ventas
├── admin.py                         # Configuración del admin
├── apps.py                          # Configuración de la app
├── forms.py                         # Formularios
├── models.py                        # Modelos de datos
├── tests.py                         # Tests unitarios
├── urls.py                          # Rutas
├── views.py                         # Vistas y APIs
└── README.md                        # Esta documentación
```

## 🗄️ Modelos de Datos

### Venta
- **Campos**:
  - `fecha_venta`: Fecha y hora de la venta
  - `metodo_pago`: Método de pago utilizado
  - `canal_venta`: Canal por el que se realizó
  - `cliente`: Referencia al cliente (opcional)
  - `usuario`: Vendedor que realizó la venta
  - `total_venta`: Total de la venta

### VentaDetalle
- **Campos**:
  - `venta`: Referencia a la venta
  - `producto`: Producto vendido
  - `lote`: Lote específico
  - `cantidad`: Cantidad vendida
  - `subtotal`: Subtotal del item

### Pedido
- **Estados**:
  - Pendiente
  - En Preparación
  - Listo para Entrega
  - Completado
  - Cancelado
- **Campos principales**: cliente, usuario, fechas, estado, total

### PedidoDetalle
- Detalles de cada producto en un pedido
- Incluye cantidad y precio unitario capturado

## 🔗 Rutas (URLs)

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/pos/` | GET | Vista principal del POS |
| `/pos/api/buscar-productos/` | GET | Buscar productos por nombre |
| `/pos/api/producto/<id>/` | GET | Obtener detalles de un producto |
| `/pos/api/procesar-venta/` | POST | Procesar una venta |
| `/pos/venta/<id>/` | GET | Ver detalle de una venta |
| `/pos/ventas/` | GET | Listar todas las ventas |

## 🎨 Frontend - JavaScript

### Clase CarritoPOS

Archivo: `static/pos/js/carrito.js`

#### Métodos Principales:

```javascript
// Inicialización
new CarritoPOS()

// Operaciones del carrito
agregarAlCarrito(productoId, nombre, precio, cantidad, loteId)
removerDelCarrito(index)
actualizarCantidadCarrito(index, nuevaCantidad)
vaciarCarrito()

// Búsqueda
buscarProductos()
cargarTodosLosProductos()

// Procesamiento
mostrarFormularioPago()
confirmarVenta()

// Utilidades
formatearMoneda(valor)
escaparHTML(texto)
mostrarNotificacion(mensaje, tipo)
```

#### Características:

- **localStorage**: Guarda el carrito en el navegador
- **AJAX**: Comunicación con el servidor sin recargar
- **Bootstrap Modals**: Modales para seleccionar lotes y pago
- **Validaciones**: Verificación de stock y datos requeridos

## 📝 Formularios

### VentaForm
Formulario para crear una venta (cliente, método de pago, canal)

### ProductoSearchForm
Formulario para búsqueda de productos

### CarritoItemForm
Formulario para agregar items al carrito

### PedidoForm
Formulario para crear pedidos

### PedidoDetalleForm
Formulario para detalles de pedidos

## 🧪 Tests

Cobertura completa de tests unitarios:

```bash
# Ejecutar todos los tests
python manage.py test pos

# Tests específicos
python manage.py test pos.tests.VentaModelTests
python manage.py test pos.tests.POSViewTests
```

### Casos de Test Incluidos:

1. **Modelos**:
   - Creación de ventas con y sin cliente
   - Detalles de venta
   - Estados de pedidos
   - Cálculo automático de subtotales

2. **Vistas**:
   - Autenticación requerida
   - Búsqueda de productos
   - Procesamiento de ventas
   - Validaciones de stock
   - Listado de ventas

## 🔐 Seguridad

- ✅ **Autenticación**: Todas las vistas requieren login
- ✅ **Autorización**: Solo vendedores y administradores
- ✅ **CSRF Protection**: Tokens CSRF en formularios
- ✅ **Transacciones**: Operaciones atómicas en ventas
- ✅ **Validaciones**: Verificación de stock antes de vender

## ⚙️ Configuración Requerida

### En `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'pos.apps.PosConfig',
]
```

### En `urls.py` principal:

```python
urlpatterns = [
    # ...
    path('pos/', include('pos.urls')),
]
```

## 🚀 Uso

### 1. Acceder al POS

```
http://localhost:8000/pos/
```

### 2. Buscar Productos

- Escribir en el campo de búsqueda
- Presionar Enter o click en "Buscar"

### 3. Agregar al Carrito

- Click en botón "Agregar" del producto
- Seleccionar lote en el modal
- Ingresar cantidad
- Confirmar

### 4. Procesar Venta

- Click en "Procesar Venta"
- Seleccionar cliente (opcional)
- Elegir método de pago
- Elegir canal de venta
- Confirmar

### 5. Ver Historial

- Link "Ver Historial de Ventas"
- Filtrar por fecha, método de pago, etc.

## 📊 Métodos de Pago Soportados

- Efectivo
- Tarjeta Débito
- Tarjeta Crédito
- Transferencia
- Cheque

## 🏪 Canales de Venta Soportados

- Mostrador
- Teléfono
- Online
- Delivery

## 🔧 Instalación y Configuración Inicial

```bash
# Crear las tablas
python manage.py migrate pos

# Crear un superusuario (si no existe)
python manage.py createsuperuser

# Ejecutar el servidor
python manage.py runserver
```

## 📱 API REST

### GET `/pos/api/buscar-productos/`

**Parámetros**:
- `q`: Término de búsqueda
- `categoria`: ID de categoría (opcional)

**Respuesta**:
```json
{
    "productos": [
        {
            "id": 1,
            "nombre": "Producto",
            "precio": "10.00",
            "stock": 50,
            "categoria": "Bebidas"
        }
    ]
}
```

### GET `/pos/api/producto/<id>/`

**Respuesta**:
```json
{
    "id": 1,
    "nombre": "Producto",
    "precio": "10.00",
    "stock": 50,
    "categoria": "Bebidas",
    "lotes": [
        {
            "id": 1,
            "numero_lote": "LOT-001",
            "cantidad": 50,
            "fecha_caducidad": "2025-12-31"
        }
    ]
}
```

### POST `/pos/api/procesar-venta/`

**Body**:
```json
{
    "cliente_id": 1,
    "metodo_pago": "efectivo",
    "canal_venta": "mostrador",
    "items": [
        {
            "producto_id": 1,
            "lote_id": 1,
            "cantidad": 5
        }
    ]
}
```

**Respuesta (éxito)**:
```json
{
    "success": true,
    "venta_id": 123,
    "total": "50.00",
    "mensaje": "Venta #123 completada"
}
```

## 🐛 Troubleshooting

### El carrito no persiste después de recargar

- Verificar que el navegador permita localStorage
- Revisar la consola del navegador para errores

### Error de CSRF al procesar venta

- Asegurar que el token CSRF está en el HTML
- Verificar `X-CSRFToken` en headers AJAX

### Stock no actualiza

- Verificar que los lotes tienen `cantidad_disponible`
- Revisar logs de la app para errores de transacción

## 📈 Mejoras Futuras

- [ ] Descuentos y promociones
- [ ] Impresión de facturas automática
- [ ] Integración con sistemas de pago
- [ ] Reportes avanzados de ventas
- [ ] Sincronización con inventario en tiempo real
- [ ] Devoluciones y cambios
- [ ] Control de caja diaria

## 📞 Soporte

Para reportar bugs o sugerencias, contactar al equipo de desarrollo.

---

**Versión**: 1.0  
**Última Actualización**: Noviembre 2024  
**Estado**: ✅ Funcional
