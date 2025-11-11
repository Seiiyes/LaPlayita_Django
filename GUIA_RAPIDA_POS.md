# ⚡ GUÍA RÁPIDA - APP POS

## Iniciar el Servidor

```bash
cd la_playita_project
python manage.py runserver
```

## Acceder a la Aplicación

**POS Principal:**
```
http://localhost:8000/pos/
```

**Admin de Django:**
```
http://localhost:8000/admin/
```

---

## Flujo de Uso del POS

### 1. **Buscar Productos**
- Escribir en el campo "Buscar producto..."
- Presionar Enter o click en el botón "Buscar"
- Los productos se filtran en tiempo real

### 2. **Agregar al Carrito**
- Click en el botón "Agregar" del producto
- Se abre un modal para seleccionar:
  - Lote específico (con fecha de vencimiento)
  - Cantidad deseada
- Click en "Agregar al Carrito"

### 3. **Ver Carrito**
- En el lado derecho está el carrito
- Muestra:
  - Productos agregados
  - Cantidades
  - Precio unitario
  - Subtotal
  - Impuestos (19%)
  - **Total a pagar**

### 4. **Modificar Carrito**
- **Cambiar cantidad**: Editar el número en la fila
- **Remover producto**: Click en el icono de papelera
- **Vaciar carrito**: Click en "Vaciar Carrito"

### 5. **Procesar Venta**
- Click en botón "Procesar Venta"
- Se abre modal con campos:
  - Cliente (opcional)
  - Método de pago (requiero)
  - Canal de venta (requerido)
- Click en "Confirmar Venta"
- Se redirige al recibo de venta

### 6. **Ver Recibo**
- Información completa de la venta
- Tabla de productos
- Resumen con impuestos
- Botones para:
  - Nueva venta
  - Ver historial
  - Imprimir

---

## Acceder al Admin

### Login
- Usuario: (debe ser superusuario o staff)
- Contraseña: (tu contraseña)

### Opciones en Admin

**Sección POS:**
- ✓ Ventas
  - Ver todas las ventas
  - Filtrar por fecha, usuario, método de pago
  - Ver detalles inline
  
- ✓ Pedidos
  - Crear nuevos pedidos
  - Cambiar estados (acciones en lote)
  - Ver detalles de productos

---

## Métodos de Pago Disponibles

1. **Efectivo**
2. **Tarjeta Débito**
3. **Tarjeta Crédito**
4. **Transferencia**
5. **Cheque**

## Canales de Venta Disponibles

1. **Mostrador**
2. **Teléfono**
3. **Online**
4. **Delivery**

---

## Cálculos Automáticos

✅ El sistema calcula automáticamente:
- Subtotal = Precio × Cantidad
- Impuestos = Subtotal × 19%
- Total = Subtotal + Impuestos

✅ El sistema actualiza automáticamente:
- Stock del producto
- Cantidad disponible del lote
- Costo promedio del producto

---

## Atajos Útiles

| Acción | Método |
|--------|--------|
| Buscar | `Enter` en campo de búsqueda |
| Agregar | Click o `Enter` en producto |
| Modificar cantidad | Editar número y `Enter` |
| Remover | Click en icono papelera |
| Procesar venta | Click en botón verde |
| Vaciar carrito | Click en botón rojo |

---

## Solución de Problemas Comunes

### ❓ El carrito se vacía al recargar
- Los datos están en localStorage, revisa consola (F12)
- Verifica que el navegador permita localStorage

### ❓ No puedo procesar una venta
- Asegúrate de tener items en el carrito
- Selecciona método de pago y canal
- Verifica autenticación

### ❓ El stock no actualiza
- Los cambios se guardan en la BD
- Recarga la página para ver cambios

### ❓ No veo productos
- Verifica que existan productos con stock > 0
- Prueba buscando por nombre

---

## Estructura de la URL

```
/pos/                           → Vista principal
/pos/api/buscar-productos/      → API de búsqueda
/pos/api/producto/<id>/         → API de detalles
/pos/api/procesar-venta/        → API de venta
/pos/venta/<id>/                → Ver venta
/pos/ventas/                    → Historial
```

---

## Datos de Ejemplo

Para probar, puedes crear:

### Productos
- Nombre: "Coca Cola 2L"
- Precio: $5.99
- Stock: 50
- Categoría: Bebidas

### Clientes
- Nombre: "Juan"
- Apellido: "Pérez"
- Email: "juan@example.com"
- Teléfono: "1234567890"

---

## Notas Importantes

⚠️ **La aplicación requiere:**
- Estar autenticado como usuario
- Tener rol de Vendedor o Administrador
- MySQL ejecutándose
- Base de datos "laplayita" disponible

⚠️ **Las ventas:**
- Se guardan inmediatamente en la BD
- No se pueden deshacer desde el POS
- Se pueden editar desde el admin

⚠️ **El stock:**
- Se actualiza automáticamente al vender
- Si falta stock, la venta falla
- Se valida antes de procesar

---

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Versión:** 1.0  
**Última actualización:** 10 de Noviembre de 2025
