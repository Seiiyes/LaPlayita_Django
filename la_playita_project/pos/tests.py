from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
import json

from inventory.models import Categoria, Producto, Lote
from clients.models import Cliente
from .models import Venta, VentaDetalle, Pedido, PedidoDetalle, Pago

User = get_user_model()


class VentaModelTests(TestCase):
    """Tests para el modelo Venta"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.usuario = User.objects.create_user(
            username='vendedor',
            password='testpass123',
            email='vendedor@test.com'
        )
        self.cliente = Cliente.objects.create(
            nombres='Juan',
            apellidos='Pérez',
            correo='juan@test.com',
            telefono='1234567890'
        )
    
    def test_crear_venta(self):
        """Test para crear una venta"""
        venta = Venta.objects.create(
            usuario=self.usuario,
            cliente=self.cliente,
            canal_venta='mostrador',
            total_venta=Decimal('100.00')
        )

        # Registrar pago asociado (antes era campo en Venta)
        Pago.objects.create(
            venta=venta,
            monto=venta.total_venta,
            metodo_pago='efectivo',
            estado='completado'
        )

        self.assertEqual(venta.usuario, self.usuario)
        self.assertEqual(venta.cliente, self.cliente)
        pago = Pago.objects.get(venta=venta)
        self.assertEqual(pago.metodo_pago, 'efectivo')
        self.assertEqual(venta.total_venta, Decimal('100.00'))
    
    def test_venta_sin_cliente(self):
        """Test para crear una venta sin cliente"""
        venta = Venta.objects.create(
            usuario=self.usuario,
            canal_venta='online',
            total_venta=Decimal('250.50')
        )

        Pago.objects.create(
            venta=venta,
            monto=venta.total_venta,
            metodo_pago='tarjeta_debito',
            estado='completado'
        )

        self.assertIsNone(venta.cliente)
        self.assertEqual(venta.total_venta, Decimal('250.50'))


class VentaDetalleModelTests(TestCase):
    """Tests para el modelo VentaDetalle"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.usuario = User.objects.create_user(username='vendedor', password='testpass123')
        self.cliente = Cliente.objects.create(nombres='Juan', apellidos='Pérez', correo='juan@test.com')
        
        self.categoria = Categoria.objects.create(nombre='Bebidas')
        self.producto = Producto.objects.create(
            nombre='Refresco Cola',
            precio_unitario=Decimal('2.50'),
            descripcion='Bebida refrescante',
            categoria=self.categoria
        )
        
        self.lote = Lote.objects.create(
            producto=self.producto,
            numero_lote='LOT-001',
            cantidad_disponible=100,
            costo_unitario_lote=Decimal('1.50'),
            fecha_caducidad='2025-12-31'
        )
        
        self.venta = Venta.objects.create(
            usuario=self.usuario,
            cliente=self.cliente,
            canal_venta='mostrador',
            total_venta=Decimal('0.00')
        )
        Pago.objects.create(
            venta=self.venta,
            monto=self.venta.total_venta,
            metodo_pago='efectivo',
            estado='completado'
        )
    
    def test_crear_venta_detalle(self):
        """Test para crear un detalle de venta"""
        detalle = VentaDetalle.objects.create(
            venta=self.venta,
            producto=self.producto,
            lote=self.lote,
            cantidad=5,
            subtotal=Decimal('12.50')
        )
        
        self.assertEqual(detalle.venta, self.venta)
        self.assertEqual(detalle.producto, self.producto)
        self.assertEqual(detalle.cantidad, 5)
        self.assertEqual(detalle.subtotal, Decimal('12.50'))


class POSViewTests(TestCase):
    """Tests para las vistas del POS"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='vendedor',
            password='testpass123'
        )
        
        self.cliente = Cliente.objects.create(nombres='Test Cliente', apellidos='Cliente', correo='testcliente@example.com')
        
        self.categoria = Categoria.objects.create(nombre='Test')
        self.producto = Producto.objects.create(
            nombre='Test Producto',
            precio_unitario=Decimal('10.00'),
            stock_actual=100,
            categoria=self.categoria
        )
        
        self.lote = Lote.objects.create(
            producto=self.producto,
            numero_lote='LOT-TEST',
            cantidad_disponible=100,
            costo_unitario_lote=Decimal('5.00'),
            fecha_caducidad='2025-12-31'
        )
    
    def test_pos_view_sin_autenticacion(self):
        """Test para validar que la vista POS requiere autenticación"""
        response = self.client.get(reverse('pos:pos_view'))
        self.assertEqual(response.status_code, 302)  # Redirige a login
    
    def test_pos_view_con_autenticacion(self):
        """Test para validar que la vista POS carga correctamente"""
        self.client.login(username='vendedor', password='testpass123')
        response = self.client.get(reverse('pos:pos_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Punto de Venta')
        self.assertContains(response, 'Carrito de Compras')
    
    def test_buscar_productos(self):
        """Test para la búsqueda de productos"""
        self.client.login(username='vendedor', password='testpass123')
        response = self.client.get(
            reverse('pos:buscar_productos'),
            {'q': 'Test Producto'}
        )
        
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertIn('productos', datos)
        self.assertEqual(len(datos['productos']), 1)
        self.assertEqual(datos['productos'][0]['nombre'], 'Test Producto')
    
    def test_obtener_producto(self):
        """Test para obtener detalles de un producto"""
        self.client.login(username='vendedor', password='testpass123')
        response = self.client.get(
            reverse('pos:obtener_producto', args=[self.producto.id])
        )
        
        self.assertEqual(response.status_code, 200)
        datos = response.json()
        self.assertEqual(datos['nombre'], 'Test Producto')
        self.assertEqual(datos['precio'], '10.00')
        self.assertEqual(datos['stock'], 100)
    
    def test_procesar_venta_carrito_vacio(self):
        """Test para validar error cuando el carrito está vacío"""
        self.client.login(username='vendedor', password='testpass123')
        
        payload = {
            'metodo_pago': 'efectivo',
            'canal_venta': 'mostrador',
            'items': []
        }
        
        response = self.client.post(
            reverse('pos:procesar_venta'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        datos = response.json()
        self.assertIn('error', datos)
    
    def test_venta_detalle(self):
        """Test para ver detalle de una venta"""
        self.client.login(username='vendedor', password='testpass123')
        
        # Crear una venta
        venta = Venta.objects.create(
            usuario=self.usuario,
            cliente=self.cliente,
            canal_venta='mostrador',
            total_venta=Decimal('50.00')
        )
        Pago.objects.create(
            venta=venta,
            monto=venta.total_venta,
            metodo_pago='efectivo',
            estado='completado'
        )

        VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto,
            lote=self.lote,
            cantidad=5,
            subtotal=Decimal('50.00')
        )
        
        response = self.client.get(
            reverse('pos:venta_detalle', args=[venta.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Venta #{venta.id}')
        self.assertContains(response, 'Test Producto')
    
    def test_listar_ventas(self):
        """Test para listar todas las ventas"""
        self.client.login(username='vendedor', password='testpass123')
        
        # Crear varias ventas
        for i in range(3):
            v = Venta.objects.create(
                usuario=self.usuario,
                canal_venta='mostrador',
                total_venta=Decimal('100.00')
            )
            Pago.objects.create(
                venta=v,
                monto=v.total_venta,
                metodo_pago='efectivo',
                estado='completado'
            )
        
        response = self.client.get(reverse('pos:listar_ventas'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Historial de Ventas')
        # Verificar que se muestran las 3 ventas
        self.assertEqual(len(response.context['ventas']), 3)


