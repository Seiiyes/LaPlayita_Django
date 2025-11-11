-- Creación y selección de la base de datos
CREATE DATABASE IF NOT EXISTS `laplayita` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `laplayita`;

-- MariaDB dump 10.19-12.0.2-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: laplayita
-- ------------------------------------------------------
-- Server version	12.0.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Estructura de tablas independientes
--

DROP TABLE IF EXISTS `categoria`;
CREATE TABLE `categoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `categoria` WRITE;
INSERT INTO `categoria` VALUES (1,'Lacteos'),(2,'Quesos'),(3,'Cerveza'),(4,'Gaseosa'),(5,'Dulces');
UNLOCK TABLES;

DROP TABLE IF EXISTS `cliente`;
CREATE TABLE `cliente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `documento` varchar(20) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `correo` varchar(60) NOT NULL,
  `telefono` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `documento` (`documento`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `cliente` WRITE;
INSERT INTO `cliente` VALUES (1,'12345678','Pepito','Perez','pepito@gmail.com','12342155124'),(2,'10001','Laura','Martinez','laura.m@gmail.com','3124567890');
UNLOCK TABLES;

--
-- TABLA MODIFICADA: `proveedor` ahora incluye NIT
--
DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE `proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nit` varchar(20) NOT NULL,
  `nombre_empresa` varchar(100) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nit` (`nit`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `proveedor` WRITE;
INSERT INTO `proveedor` VALUES 
(1,'800.123.456-7','Proveedor de Lacteos S.A.','123456789','contacto@lacteos.com','Calle Falsa 123'),
(2,'890.903.635-1','Postobon S.A.','3573612371','postobon@gmail.com','kra93 #32-13'),
(3,'860.005.224-6','Bavaria S.A.','2131456','contacto@bavaria.com','cra105 #21-65'),
(4,'800.22 margarita-9','Papas Margarita','235156023','margaritas@gmail.com','cra100 #95-54');
UNLOCK TABLES;

DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(35) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `rol` WRITE;
INSERT INTO `rol` VALUES (1,'Administrador'),(2,'Vendedor');
UNLOCK TABLES;

--
-- Estructura de tablas con dependencias básicas
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `documento` varchar(20) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `correo` varchar(60) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `ultimo_login` timestamp NULL DEFAULT NULL,
  `rol_id` int(11) NOT NULL,
  PRIMARY KEY (`id`), UNIQUE KEY `documento` (`documento`), UNIQUE KEY `correo` (`correo`), KEY `rol_id` (`rol_id`),
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `usuario` WRITE;
INSERT INTO `usuario` VALUES
(1,'1014477103','Juan','Lizarazo','juan.vendedor@laplayita.com','3105416287','hash_contrasena_vendedor','activo','2025-10-10 22:48:22',NULL,2),
(2,'1234567','Admin','Principal','admin@laplayita.com','32124551','hash_contrasena_admin','activo','2025-10-10 22:48:22','2025-11-09 07:03:56',1),
(4,'10000000','Laura','Gomez','laura.admin@laplayita.com',NULL,'hash_contrasena_laura','activo','2025-10-13 19:08:10','2025-11-11 07:08:00',1);
UNLOCK TABLES;

DROP TABLE IF EXISTS `producto`;
CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `precio_unitario` decimal(12,2) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `stock_minimo` int(11) NOT NULL DEFAULT 10,
  `categoria_id` int(11) NOT NULL,
  `stock_actual` int(10) unsigned NOT NULL,
  `costo_promedio` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`), UNIQUE KEY `uq_producto_nombre` (`nombre`), KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `producto` WRITE;
INSERT INTO `producto` VALUES (1,'Leche Entera 1L',3800.00,'Leche pasteurizada',10,1,80,2500.00),(2,'Queso Campesino 500g',9500.00,'Queso fresco de vaca',5,2,59,7000.00),(3,'Yogurt',3000.00,NULL,10,1,0,0.00),(4,'Manzana Postobon 1L',4500.00,'Sabor a manzana, 1L',3,4,0,0.00),(7,'Cerveza Aguila',4500.00,'Tipo lager',1,3,341,4500.00),(8,'Papas Fritas',2500.00,'Paquete de papas',5,5,0,0.00);
UNLOCK TABLES;

--
-- NUEVAS TABLAS: Flujo de Pedidos
--

DROP TABLE IF EXISTS `pedido`;
CREATE TABLE `pedido` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha_pedido` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL DEFAULT 'pendiente' COMMENT 'Posibles estados: pendiente, en_proceso, completado, cancelado',
  `total_pedido` decimal(12,2) NOT NULL DEFAULT 0.00,
  `observaciones` text DEFAULT NULL,
  PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_pedido_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `pedido_detalle`;
CREATE TABLE `pedido_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pedido_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(12,2) NOT NULL COMMENT 'Precio del producto en el momento del pedido',
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`), KEY `pedido_id` (`pedido_id`), KEY `producto_id` (`producto_id`),
  CONSTRAINT `fk_pedido_detalle_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pedido_detalle_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- TABLA MODIFICADA: `venta` ahora se vincula a `pedido` y delega el pago
--

DROP TABLE IF EXISTS `venta`;
CREATE TABLE `venta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_venta` datetime NOT NULL,
  `canal_venta` varchar(20) NOT NULL DEFAULT 'Tienda',
  `cliente_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `pedido_id` int(11) DEFAULT NULL COMMENT 'Vincula la venta a un pedido original',
  `total_venta` decimal(12,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `usuario_id` (`usuario_id`), KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `fk_venta_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_pedido` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `venta` WRITE;
INSERT INTO `venta` VALUES (1,'2025-09-02 10:00:00','Tienda',1,1,NULL,7600.00),(2,'2025-09-03 11:30:00','Domicilio',2,1,NULL,9500.00),(3,'2025-11-05 12:24:54','local',1,4,NULL,4500.00),(4,'2025-11-05 12:25:24','local',1,4,NULL,54000.00),(5,'2025-11-05 12:25:41','local',2,4,NULL,45600.00),(6,'2025-11-05 12:40:34','local',2,4,NULL,4500.00),(7,'2025-11-05 12:44:58','local',1,4,NULL,22800.00),(8,'2025-11-05 13:48:30','local',2,4,NULL,25000.00),(9,'2025-11-06 22:52:29','local',2,4,NULL,18000.00);
UNLOCK TABLES;

--
-- NUEVA TABLA: `pago` para registrar transacciones
--

DROP TABLE IF EXISTS `pago`;
CREATE TABLE `pago` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `metodo_pago` varchar(25) NOT NULL,
  `fecha_pago` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL DEFAULT 'completado' COMMENT 'Posibles: completado, fallido, reembolsado',
  `referencia_transaccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`), KEY `venta_id` (`venta_id`),
  CONSTRAINT `fk_pago_venta` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `pago` WRITE;
INSERT INTO `pago` (`venta_id`, `monto`, `metodo_pago`, `fecha_pago`) VALUES (1,7600.00,'Efectivo','2025-09-02 10:00:00'),(2,9500.00,'Tarjeta','2025-09-03 11:30:00'),(3,4500.00,'Efectivo','2025-11-05 12:24:54'),(4,54000.00,'Efectivo','2025-11-05 12:25:24'),(5,45600.00,'Efectivo','2025-11-05 12:25:41'),(6,4500.00,'Efectivo','2025-11-05 12:40:34'),(7,22800.00,'Efectivo','2025-11-05 12:44:58'),(8,25000.00,'Efectivo','2025-11-05 13:48:30'),(9,18000.00,'Efectivo','2025-11-06 22:52:29');
UNLOCK TABLES;

--
-- Estructura de tablas de inventario y reabastecimiento
--

DROP TABLE IF EXISTS `reabastecimiento`;
CREATE TABLE `reabastecimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `costo_total` decimal(12,2) NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'solicitado' COMMENT 'Posibles: solicitado, cancelado, recibido',
  `forma_pago` varchar(25) DEFAULT 'Efectivo',
  `observaciones` text DEFAULT NULL,
  `proveedor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`), KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `fk_reabastecimiento_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `reabastecimiento` WRITE;
INSERT INTO `reabastecimiento` VALUES (1,'2025-09-01 09:00:00',670000.00,'recibido','Efectivo','Reabastecimiento inicial',1),(36,'2025-11-05 11:38:27',270000.00,'recibido','pse','',3),(37,'2025-11-05 13:45:25',25000.00,'recibido','pse','',4),(38,'2025-11-06 22:53:32',450000.00,'recibido','pse','',3),(40,'2025-11-06 22:54:41',900000.00,'recibido','pse','',3);
UNLOCK TABLES;

DROP TABLE IF EXISTS `reabastecimiento_detalle`;
CREATE TABLE `reabastecimiento_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reabastecimiento_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `costo_unitario` decimal(12,2) NOT NULL,
  `fecha_caducidad` date DEFAULT NULL,
  `cantidad_recibida` int(11) NOT NULL,
  PRIMARY KEY (`id`), KEY `reabastecimiento_id` (`reabastecimiento_id`), KEY `producto_id` (`producto_id`),
  CONSTRAINT `fk_reabastecimiento_detalle_reabastecimiento` FOREIGN KEY (`reabastecimiento_id`) REFERENCES `reabastecimiento` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reabastecimiento_detalle_producto_id_63c5cefe_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `reabastecimiento_detalle` WRITE;
INSERT INTO `reabastecimiento_detalle` VALUES (1,1,1,100,2500.00,NULL,100),(2,1,2,60,7000.00,NULL,60),(38,36,7,60,4500.00,'2025-12-31',60),(39,37,8,10,2500.00,'2025-12-06',10),(40,38,7,100,4500.00,'2026-01-17',100),(42,40,7,200,4500.00,'2026-01-15',199);
UNLOCK TABLES;

DROP TABLE IF EXISTS `lote`;
CREATE TABLE `lote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) NOT NULL,
  `reabastecimiento_detalle_id` int(11) DEFAULT NULL,
  `numero_lote` varchar(50) NOT NULL,
  `cantidad_disponible` int(11) unsigned NOT NULL,
  `costo_unitario_lote` decimal(12,2) NOT NULL,
  `fecha_caducidad` date NOT NULL,
  `fecha_entrada` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`), UNIQUE KEY `uq_lote_producto_numero` (`producto_id`,`numero_lote`), KEY `fk_lote_producto` (`producto_id`), KEY `fk_lote_reabastecimiento_detalle` (`reabastecimiento_detalle_id`),
  CONSTRAINT `fk_lote_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_lote_reabastecimiento_detalle` FOREIGN KEY (`reabastecimiento_detalle_id`) REFERENCES `reabastecimiento_detalle` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `lote` WRITE;
INSERT INTO `lote` VALUES (1,1,1,'LCH-A1',80,2500.00,'2025-10-30','2025-09-01 10:00:00'),(2,2,2,'QSO-C3',59,7000.00,'2025-11-15','2025-09-05 14:00:00'),(3,7,38,'R36-P7-38',42,4500.00,'2025-12-31','2025-11-05 11:38:47'),(4,8,39,'R37-P8-39',0,2500.00,'2025-12-06','2025-11-05 13:45:41'),(5,7,42,'R40-P7-42',199,4500.00,'2026-01-15','2025-11-06 23:06:20'),(6,7,40,'R38-P7-40',100,4500.00,'2026-01-17','2025-11-06 23:08:20');
UNLOCK TABLES;

--
-- Estructura de tablas de detalle y movimientos
--

DROP TABLE IF EXISTS `venta_detalle`;
CREATE TABLE `venta_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `lote_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`), KEY `venta_id` (`venta_id`), KEY `producto_id` (`producto_id`), KEY `lote_id` (`lote_id`),
  CONSTRAINT `fk_venta_detalle_lote` FOREIGN KEY (`lote_id`) REFERENCES `lote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_detalle_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_detalle_venta` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `venta_detalle` WRITE;
INSERT INTO `venta_detalle` VALUES (1,1,1,1,2,7600.00),(2,2,2,2,1,9500.00),(3,3,7,3,1,4500.00),(4,4,7,3,12,54000.00),(5,5,1,1,12,45600.00),(6,6,7,3,1,4500.00),(7,7,1,1,6,22800.00),(8,8,8,4,10,25000.00),(9,9,7,3,4,18000.00);
UNLOCK TABLES;

DROP TABLE IF EXISTS `movimiento_inventario`;
CREATE TABLE `movimiento_inventario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) NOT NULL,
  `lote_id` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `tipo_movimiento` varchar(20) NOT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT current_timestamp(),
  `descripcion` varchar(255) DEFAULT NULL,
  `venta_id` int(11) DEFAULT NULL,
  `reabastecimiento_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`), KEY `producto_id` (`producto_id`), KEY `lote_id` (`lote_id`), KEY `venta_id` (`venta_id`), KEY `reabastecimiento_id` (`reabastecimiento_id`),
  CONSTRAINT `fk_movimiento_inventario_lote` FOREIGN KEY (`lote_id`) REFERENCES `lote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_reabastecimiento` FOREIGN KEY (`reabastecimiento_id`) REFERENCES `reabastecimiento` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_venta` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `movimiento_inventario` WRITE;
INSERT INTO `movimiento_inventario` VALUES (1,1,1,100,'ENTRADA','2025-10-10 22:48:22','Reabastecimiento inicial Lote A1',NULL,1),(2,2,2,60,'ENTRADA','2025-10-10 22:48:22','Reabastecimiento inicial Lote C3',NULL,1),(3,1,1,-2,'SALIDA','2025-10-10 22:48:22','Venta ID 1',1,NULL),(4,2,2,-1,'SALIDA','2025-10-10 22:48:22','Venta ID 2',2,NULL),(5,7,3,60,'entrada','2025-11-05 11:38:47','Entrada por reabastecimiento #36',NULL,36),(6,7,3,-1,'salida','2025-11-05 12:40:34','Venta #6',6,NULL),(7,1,1,-6,'salida','2025-11-05 12:44:58','Venta #7',7,NULL),(8,8,4,10,'entrada','2025-11-05 13:45:41','Entrada por reabastecimiento #37',NULL,37),(9,8,4,-10,'salida','2025-11-05 13:48:30','Venta #8',8,NULL),(10,7,3,-4,'salida','2025-11-06 22:52:29','Venta #9',9,NULL),(11,7,5,199,'entrada','2025-11-06 23:06:20','Entrada por reabastecimiento #40',NULL,40),(12,7,6,100,'entrada','2025-11-06 23:08:20','Entrada por reabastecimiento #38',NULL,38);
UNLOCK TABLES;

--
-- Estructura de tablas de servicio al cliente
--

DROP TABLE IF EXISTS `pqrs`;
CREATE TABLE `pqrs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  `descripcion` text NOT NULL,
  `respuesta` text DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  `fecha_creacion` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  `cliente_id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_pqrs_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pqrs_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `pqrs` WRITE;
INSERT INTO `pqrs` VALUES (1,'SUGERENCIA','Más productos saludables',NULL,'en_proceso','2025-07-01 10:00:00',NULL,1,2);
UNLOCK TABLES;

DROP TABLE IF EXISTS `pqrs_historial`;
CREATE TABLE `pqrs_historial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pqrs_id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `estado_anterior` varchar(20) NOT NULL,
  `estado_nuevo` varchar(20) NOT NULL,
  `descripcion_cambio` text DEFAULT NULL,
  `fecha_cambio` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`), KEY `pqrs_id` (`pqrs_id`), KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_pqrs_historial_pqrs` FOREIGN KEY (`pqrs_id`) REFERENCES `pqrs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pqrs_historial_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
LOCK TABLES `pqrs_historial` WRITE;
INSERT INTO `pqrs_historial` VALUES (1,1,2,'pendiente','en_proceso','Se asigna el caso al administrador para evaluar la solicitud.','2025-10-10 22:48:22');
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 22:00:00