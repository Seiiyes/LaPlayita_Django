/**
 * Sistema de Carrito de Compras para el POS
 * Gestiona la lógica del carrito, búsqueda de productos y cálculos
 */

class CarritoPOS {
    constructor() {
        this.carrito = [];
        this.impuesto = 0.19; // 19%
        this.inicializar();
    }

    inicializar() {
        this.cargarCarritoDelLocalStorage();
        this.configurarEventos();
        this.actualizarVistaCarrito();
    }

    configurarEventos() {
        // Búsqueda de productos
        const botonBusqueda = document.getElementById('product-search-button');
        const inputBusqueda = document.getElementById('product-search-input');

        if (botonBusqueda) {
            botonBusqueda.addEventListener('click', () => this.buscarProductos());
        }

        if (inputBusqueda) {
            inputBusqueda.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.buscarProductos();
                }
            });
        }

        // Botón de procesar venta
        const botonProcesar = document.querySelector('button.btn-success');
        if (botonProcesar && botonProcesar.textContent.includes('Procesar')) {
            botonProcesar.addEventListener('click', () => this.mostrarFormularioPago());
        }

        // Botón de cancelar venta
        const botonCancelar = document.querySelector('button.btn-outline-danger');
        if (botonCancelar && botonCancelar.textContent.includes('Cancelar')) {
            botonCancelar.addEventListener('click', () => this.vaciarCarrito());
        }
    }

    async buscarProductos() {
        const inputBusqueda = document.getElementById('product-search-input');
        const query = inputBusqueda.value.trim();

        if (!query) {
            this.cargarTodosLosProductos();
            return;
        }

        try {
            const response = await fetch(`/pos/api/buscar-productos/?q=${encodeURIComponent(query)}`);
            const datos = await response.json();

            if (datos.productos) {
                this.mostrarProductos(datos.productos);
            }
        } catch (error) {
            console.error('Error al buscar productos:', error);
            alert('Error al buscar productos');
        }
    }

    async cargarTodosLosProductos() {
        try {
            const inputBusqueda = document.getElementById('product-search-input');
            inputBusqueda.value = '';

            // Recargar la página para obtener todos los productos
            location.reload();
        } catch (error) {
            console.error('Error al cargar productos:', error);
        }
    }

    mostrarProductos(productos) {
        const contenedorProductos = document.getElementById('product-list');
        contenedorProductos.innerHTML = '';

        if (productos.length === 0) {
            contenedorProductos.innerHTML = '<p class="col-12 text-center text-muted">No se encontraron productos</p>';
            return;
        }

        productos.forEach(producto => {
            const colDiv = document.createElement('div');
            colDiv.className = 'col';

            const cartaHTML = `
                <div class="card h-100 product-card">
                    <div class="card-body">
                        <h5 class="card-title">${this.escaparHTML(producto.nombre)}</h5>
                        <p class="card-text text-muted">${this.escaparHTML(producto.categoria)}</p>
                        ${producto.descripcion ? `<p class="card-text small">${this.escaparHTML(producto.descripcion)}</p>` : ''}
                        <p class="card-text fw-bold">$${this.formatearMoneda(producto.precio)}</p>
                        <p class="card-text small">
                            <span class="badge bg-info">Stock: ${producto.stock}</span>
                        </p>
                        <button class="btn btn-sm btn-primary agregar-producto-btn" data-producto-id="${producto.id}" data-nombre="${this.escaparHTML(producto.nombre)}" data-precio="${producto.precio}">
                            <i class="bi bi-plus-circle me-1"></i>Agregar
                        </button>
                    </div>
                </div>
            `;

            colDiv.innerHTML = cartaHTML;
            contenedorProductos.appendChild(colDiv);

            // Agregar evento al botón de agregar
            const btnAgregar = colDiv.querySelector('.agregar-producto-btn');
            btnAgregar.addEventListener('click', () => this.abrirModalProducto(producto.id));
        });
    }

    async abrirModalProducto(productoId) {
        try {
            const response = await fetch(`/pos/api/producto/${productoId}/`);
            const producto = await response.json();

            if (producto.error) {
                alert('Error: ' + producto.error);
                return;
            }

            this.mostrarModalSeleccionarLote(producto);
        } catch (error) {
            console.error('Error al obtener producto:', error);
            alert('Error al obtener detalles del producto');
        }
    }

    mostrarModalSeleccionarLote(producto) {
        // Crear modal para seleccionar lote y cantidad
        let contenidoLotes = '';

        if (producto.lotes.length === 0) {
            contenidoLotes = '<p class="text-danger">No hay lotes disponibles</p>';
        } else {
            contenidoLotes = `
                <div class="mb-3">
                    <label for="lote-select" class="form-label">Seleccione Lote:</label>
                    <select id="lote-select" class="form-control">
                        ${producto.lotes.map(lote => `
                            <option value="${lote.id}" data-cantidad="${lote.cantidad}">
                                ${this.escaparHTML(lote.numero_lote)} - Vence: ${new Date(lote.fecha_caducidad).toLocaleDateString()} (${lote.cantidad} disponibles)
                            </option>
                        `).join('')}
                    </select>
                </div>
            `;
        }

        const html = `
            <div class="modal fade" id="modalProducto" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${this.escaparHTML(producto.nombre)}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>Precio:</strong> $${this.formatearMoneda(producto.precio)}</p>
                            <p><strong>Stock Total:</strong> ${producto.stock}</p>
                            <p><strong>Categoría:</strong> ${this.escaparHTML(producto.categoria)}</p>
                            ${producto.descripcion ? `<p><strong>Descripción:</strong> ${this.escaparHTML(producto.descripcion)}</p>` : ''}
                            
                            <hr>
                            
                            ${contenidoLotes}
                            
                            <div class="mb-3">
                                <label for="cantidad-input" class="form-label">Cantidad:</label>
                                <input type="number" id="cantidad-input" class="form-control" value="1" min="1" max="${producto.stock}">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-primary" id="btn-agregar-carrito">Agregar al Carrito</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remover modal anterior si existe
        const modalAnterior = document.getElementById('modalProducto');
        if (modalAnterior) {
            modalAnterior.remove();
        }

        // Agregar nuevo modal
        document.body.insertAdjacentHTML('beforeend', html);

        const modal = new bootstrap.Modal(document.getElementById('modalProducto'));

        // Configurar evento del botón agregar
        document.getElementById('btn-agregar-carrito').addEventListener('click', () => {
            const loteSelect = document.getElementById('lote-select');
            const cantidadInput = document.getElementById('cantidad-input');

            if (!loteSelect || loteSelect.options.length === 0) {
                alert('No hay lotes disponibles');
                return;
            }

            const loteId = parseInt(loteSelect.value);
            const cantidad = parseInt(cantidadInput.value);
            const cantidadDisponible = parseInt(loteSelect.selectedOptions[0].dataset.cantidad);

            if (cantidad <= 0 || cantidad > cantidadDisponible) {
                alert(`Ingrese una cantidad válida (máximo ${cantidadDisponible})`);
                return;
            }

            this.agregarAlCarrito(producto.id, producto.nombre, producto.precio, cantidad, loteId);
            modal.hide();
        });

        modal.show();
    }

    agregarAlCarrito(productoId, nombre, precio, cantidad, loteId) {
        // Verificar si el producto ya está en el carrito con el mismo lote
        const itemExistente = this.carrito.find(item => item.producto_id === productoId && item.lote_id === loteId);

        if (itemExistente) {
            itemExistente.cantidad += cantidad;
        } else {
            this.carrito.push({
                producto_id: productoId,
                nombre: nombre,
                precio: parseFloat(precio),
                cantidad: cantidad,
                lote_id: loteId
            });
        }

        this.guardarCarritoEnLocalStorage();
        this.actualizarVistaCarrito();
        this.mostrarNotificacion(`${nombre} agregado al carrito`);
    }

    removerDelCarrito(index) {
        this.carrito.splice(index, 1);
        this.guardarCarritoEnLocalStorage();
        this.actualizarVistaCarrito();
    }

    actualizarCantidadCarrito(index, nuevaCantidad) {
        nuevaCantidad = parseInt(nuevaCantidad);

        if (nuevaCantidad <= 0) {
            this.removerDelCarrito(index);
            return;
        }

        this.carrito[index].cantidad = nuevaCantidad;
        this.guardarCarritoEnLocalStorage();
        this.actualizarVistaCarrito();
    }

    actualizarVistaCarrito() {
        const contenedorItems = document.getElementById('cart-items');
        const subtotalSpan = document.getElementById('cart-subtotal');
        const impuestoSpan = document.getElementById('cart-tax');
        const totalSpan = document.getElementById('cart-total');

        contenedorItems.innerHTML = '';

        if (this.carrito.length === 0) {
            contenedorItems.innerHTML = '<tr><td colspan="4" class="text-center text-muted">El carrito está vacío</td></tr>';
            subtotalSpan.textContent = '$0.00';
            impuestoSpan.textContent = '$0.00';
            totalSpan.textContent = '$0.00';
            return;
        }

        let subtotal = 0;

        this.carrito.forEach((item, index) => {
            const subtotalItem = item.precio * item.cantidad;
            subtotal += subtotalItem;

            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>
                    <div>
                        <strong>${this.escaparHTML(item.nombre)}</strong>
                        <br>
                        <small class="text-muted">Lote ID: ${item.lote_id}</small>
                    </div>
                </td>
                <td class="text-end">
                    <input type="number" class="form-control form-control-sm" style="width: 70px;" value="${item.cantidad}" min="1" data-index="${index}">
                </td>
                <td class="text-end">
                    $${this.formatearMoneda(item.precio)} x ${item.cantidad} = <br>
                    <strong>$${this.formatearMoneda(subtotalItem)}</strong>
                </td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-danger eliminar-btn" data-index="${index}" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;

            contenedorItems.appendChild(fila);

            // Eventos
            const inputCantidad = fila.querySelector('input[type="number"]');
            inputCantidad.addEventListener('change', (e) => {
                this.actualizarCantidadCarrito(index, e.target.value);
            });

            const btnEliminar = fila.querySelector('.eliminar-btn');
            btnEliminar.addEventListener('click', () => {
                this.removerDelCarrito(index);
            });
        });

        // Calcular impuesto y total
        const impuesto = subtotal * this.impuesto;
        const total = subtotal + impuesto;

        subtotalSpan.textContent = `$${this.formatearMoneda(subtotal)}`;
        impuestoSpan.textContent = `$${this.formatearMoneda(impuesto)}`;
        totalSpan.textContent = `$${this.formatearMoneda(total)}`;
    }

    mostrarFormularioPago() {
        if (this.carrito.length === 0) {
            alert('El carrito está vacío');
            return;
        }

        const formularioHTML = `
            <div class="modal fade" id="modalPago" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Completar Venta</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="form-pago">
                                <div class="mb-3">
                                    <label for="cliente-pago" class="form-label">Cliente (Opcional):</label>
                                    <select id="cliente-pago" class="form-control">
                                        <option value="">-- Sin Cliente --</option>
                                        ${document.getElementById('cliente-select') ? 
                                            Array.from(document.getElementById('cliente-select').options).map(opt => 
                                                `<option value="${opt.value}">${opt.text}</option>`
                                            ).join('') : ''
                                        }
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label for="metodo-pago" class="form-label">Método de Pago:</label>
                                    <select id="metodo-pago" class="form-control" required>
                                        <option value="">-- Seleccione --</option>
                                        <option value="efectivo">Efectivo</option>
                                        <option value="tarjeta_debito">Tarjeta Débito</option>
                                        <option value="tarjeta_credito">Tarjeta Crédito</option>
                                        <option value="transferencia">Transferencia</option>
                                        <option value="cheque">Cheque</option>
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label for="canal-venta" class="form-label">Canal de Venta:</label>
                                    <select id="canal-venta" class="form-control" required>
                                        <option value="">-- Seleccione --</option>
                                        <option value="mostrador">Mostrador</option>
                                        <option value="telefono">Teléfono</option>
                                        <option value="online">Online</option>
                                        <option value="delivery">Delivery</option>
                                    </select>
                                </div>

                                <div class="alert alert-info">
                                    <p><strong>Subtotal:</strong> $<span id="modal-subtotal">0.00</span></p>
                                    <p><strong>Impuestos (19%):</strong> $<span id="modal-impuesto">0.00</span></p>
                                    <p class="fs-5"><strong>Total a Pagar:</strong> $<span id="modal-total">0.00</span></p>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-success" id="btn-confirmar-venta">
                                <i class="bi bi-check-circle me-1"></i>Confirmar Venta
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const modalAnterior = document.getElementById('modalPago');
        if (modalAnterior) {
            modalAnterior.remove();
        }

        document.body.insertAdjacentHTML('beforeend', formularioHTML);

        // Actualizar totales en el modal
        let subtotal = 0;
        this.carrito.forEach(item => {
            subtotal += item.precio * item.cantidad;
        });
        const impuesto = subtotal * this.impuesto;
        const total = subtotal + impuesto;

        document.getElementById('modal-subtotal').textContent = this.formatearMoneda(subtotal);
        document.getElementById('modal-impuesto').textContent = this.formatearMoneda(impuesto);
        document.getElementById('modal-total').textContent = this.formatearMoneda(total);

        const modal = new bootstrap.Modal(document.getElementById('modalPago'));

        document.getElementById('btn-confirmar-venta').addEventListener('click', () => {
            this.confirmarVenta();
            modal.hide();
        });

        modal.show();
    }

    async confirmarVenta() {
        const clienteId = document.getElementById('cliente-pago').value || null;
        const metodoPago = document.getElementById('metodo-pago').value;
        const canalVenta = document.getElementById('canal-venta').value;

        if (!metodoPago || !canalVenta) {
            alert('Por favor complete todos los campos requeridos');
            return;
        }

        // Mostrar indicador de carga
        const btnConfirmar = document.getElementById('btn-confirmar-venta');
        const textoOriginal = btnConfirmar.innerHTML;
        btnConfirmar.disabled = true;
        btnConfirmar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';

        try {
            const response = await fetch('/pos/api/procesar-venta/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.obtenerCSRFToken(),
                },
                body: JSON.stringify({
                    cliente_id: clienteId ? parseInt(clienteId) : null,
                    metodo_pago: metodoPago,
                    canal_venta: canalVenta,
                    items: this.carrito
                })
            });

            const datos = await response.json();

            if (response.ok && datos.success) {
                this.mostrarNotificacion(datos.mensaje, 'success');
                this.vaciarCarrito();
                this.redirigirAVentaDetalle(datos.venta_id);
            } else {
                alert('Error: ' + (datos.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Error al procesar venta:', error);
            alert('Error al procesar la venta');
        } finally {
            btnConfirmar.disabled = false;
            btnConfirmar.innerHTML = textoOriginal;
        }
    }

    redirigirAVentaDetalle(ventaId) {
        setTimeout(() => {
            window.location.href = `/pos/venta/${ventaId}/`;
        }, 1500);
    }

    vaciarCarrito() {
        this.carrito = [];
        this.guardarCarritoEnLocalStorage();
        this.actualizarVistaCarrito();
    }

    guardarCarritoEnLocalStorage() {
        localStorage.setItem('carrito_pos', JSON.stringify(this.carrito));
    }

    cargarCarritoDelLocalStorage() {
        const carritoGuardado = localStorage.getItem('carrito_pos');
        if (carritoGuardado) {
            try {
                this.carrito = JSON.parse(carritoGuardado);
            } catch (error) {
                this.carrito = [];
            }
        }
    }

    mostrarNotificacion(mensaje, tipo = 'info') {
        const alertaHTML = `
            <div class="alert alert-${tipo} alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 9999;" role="alert">
                ${mensaje}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', alertaHTML);

        const alerta = document.querySelector('.alert');
        setTimeout(() => {
            alerta.remove();
        }, 4000);
    }

    escaparHTML(texto) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return texto.replace(/[&<>"']/g, m => map[m]);
    }

    formatearMoneda(valor) {
        return parseFloat(valor).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    obtenerCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }
}

// Inicializar el carrito cuando el documento esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.carritoPOS = new CarritoPOS();
});
