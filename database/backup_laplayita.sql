/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.0.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: laplayita
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
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Current Database: `laplayita`
--

/*!40000 DROP DATABASE IF EXISTS `laplayita`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `laplayita` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;

USE `laplayita`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_group` VALUES
(1,'Admin'),
(3,'Vendedor');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add categoria',9,'add_categoria'),
(26,'Can change categoria',9,'change_categoria'),
(27,'Can delete categoria',9,'delete_categoria'),
(28,'Can view categoria',9,'view_categoria'),
(29,'Can add cliente',10,'add_cliente'),
(30,'Can change cliente',10,'change_cliente'),
(31,'Can delete cliente',10,'delete_cliente'),
(32,'Can view cliente',10,'view_cliente'),
(33,'Can add lote',11,'add_lote'),
(34,'Can change lote',11,'change_lote'),
(35,'Can delete lote',11,'delete_lote'),
(36,'Can view lote',11,'view_lote'),
(37,'Can add movimiento inventario',12,'add_movimientoinventario'),
(38,'Can change movimiento inventario',12,'change_movimientoinventario'),
(39,'Can delete movimiento inventario',12,'delete_movimientoinventario'),
(40,'Can view movimiento inventario',12,'view_movimientoinventario'),
(41,'Can add pqrs',8,'add_pqrs'),
(42,'Can change pqrs',8,'change_pqrs'),
(43,'Can delete pqrs',8,'delete_pqrs'),
(44,'Can view pqrs',8,'view_pqrs'),
(45,'Can add pqrs historial',13,'add_pqrshistorial'),
(46,'Can change pqrs historial',13,'change_pqrshistorial'),
(47,'Can delete pqrs historial',13,'delete_pqrshistorial'),
(48,'Can view pqrs historial',13,'view_pqrshistorial'),
(49,'Can add producto',14,'add_producto'),
(50,'Can change producto',14,'change_producto'),
(51,'Can delete producto',14,'delete_producto'),
(52,'Can view producto',14,'view_producto'),
(53,'Can add proveedor',15,'add_proveedor'),
(54,'Can change proveedor',15,'change_proveedor'),
(55,'Can delete proveedor',15,'delete_proveedor'),
(56,'Can view proveedor',15,'view_proveedor'),
(57,'Can add reabastecimiento',16,'add_reabastecimiento'),
(58,'Can change reabastecimiento',16,'change_reabastecimiento'),
(59,'Can delete reabastecimiento',16,'delete_reabastecimiento'),
(60,'Can view reabastecimiento',16,'view_reabastecimiento'),
(61,'Can add reabastecimiento detalle',17,'add_reabastecimientodetalle'),
(62,'Can change reabastecimiento detalle',17,'change_reabastecimientodetalle'),
(63,'Can delete reabastecimiento detalle',17,'delete_reabastecimientodetalle'),
(64,'Can view reabastecimiento detalle',17,'view_reabastecimientodetalle'),
(65,'Can add venta',18,'add_venta'),
(66,'Can change venta',18,'change_venta'),
(67,'Can delete venta',18,'delete_venta'),
(68,'Can view venta',18,'view_venta'),
(69,'Can add venta detalle',19,'add_ventadetalle'),
(70,'Can change venta detalle',19,'change_ventadetalle'),
(71,'Can delete venta detalle',19,'delete_ventadetalle'),
(72,'Can view venta detalle',19,'view_ventadetalle'),
(73,'Can add usuario',7,'add_usuario'),
(74,'Can change usuario',7,'change_usuario'),
(75,'Can delete usuario',7,'delete_usuario'),
(76,'Can view usuario',7,'view_usuario'),
(77,'Can add rol',20,'add_rol'),
(78,'Can change rol',20,'change_rol'),
(79,'Can delete rol',20,'delete_rol'),
(80,'Can view rol',20,'view_rol'),
(81,'Can add usuario groups',21,'add_usuariogroups'),
(82,'Can change usuario groups',21,'change_usuariogroups'),
(83,'Can delete usuario groups',21,'delete_usuariogroups'),
(84,'Can view usuario groups',21,'view_usuariogroups'),
(85,'Can add usuario user permissions',22,'add_usuariouserpermissions'),
(86,'Can change usuario user permissions',22,'change_usuariouserpermissions'),
(87,'Can delete usuario user permissions',22,'delete_usuariouserpermissions'),
(88,'Can view usuario user permissions',22,'view_usuariouserpermissions');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$KKq6trfdqC14HjIERQdPOM$XrduLhiFn5WoIszW+qf+xJtIYtqcFJUUHCAMxhFmcqQ=','2025-10-12 02:08:11.941309',1,'JuanL','','','lizarazojuanandres@gmail.com',1,1,'2025-10-11 22:59:12.411276');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `categoria` VALUES
(1,'Lacteos'),
(2,'Quesos'),
(3,'CERVEZA'),
(4,'GASEOSA');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `cliente` VALUES
(1,'12345678','Pepito','Perez','pepito@gmail.com','12342155124'),
(2,'10001','Laura','Martinez','laura.m@gmail.com','3124567890');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(9,'core','categoria'),
(10,'core','cliente'),
(11,'core','lote'),
(12,'core','movimientoinventario'),
(8,'core','pqrs'),
(13,'core','pqrshistorial'),
(14,'core','producto'),
(15,'core','proveedor'),
(16,'core','reabastecimiento'),
(17,'core','reabastecimientodetalle'),
(20,'core','rol'),
(7,'core','usuario'),
(21,'core','usuariogroups'),
(22,'core','usuariouserpermissions'),
(18,'core','venta'),
(19,'core','ventadetalle'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-10-11 22:51:04.363904'),
(2,'auth','0001_initial','2025-10-11 22:51:05.766512'),
(3,'admin','0001_initial','2025-10-11 22:51:06.039243'),
(4,'admin','0002_logentry_remove_auto_add','2025-10-11 22:51:06.048474'),
(5,'admin','0003_logentry_add_action_flag_choices','2025-10-11 22:51:06.057449'),
(6,'contenttypes','0002_remove_content_type_name','2025-10-11 22:51:06.255404'),
(7,'auth','0002_alter_permission_name_max_length','2025-10-11 22:51:06.374191'),
(8,'auth','0003_alter_user_email_max_length','2025-10-11 22:51:06.454777'),
(9,'auth','0004_alter_user_username_opts','2025-10-11 22:51:06.464117'),
(10,'auth','0005_alter_user_last_login_null','2025-10-11 22:51:06.586230'),
(11,'auth','0006_require_contenttypes_0002','2025-10-11 22:51:06.592882'),
(12,'auth','0007_alter_validators_add_error_messages','2025-10-11 22:51:06.602056'),
(13,'auth','0008_alter_user_username_max_length','2025-10-11 22:51:06.684927'),
(14,'auth','0009_alter_user_last_name_max_length','2025-10-11 22:51:06.768705'),
(15,'auth','0010_alter_group_name_max_length','2025-10-11 22:51:06.851770'),
(16,'auth','0011_update_proxy_permissions','2025-10-11 22:51:06.861409'),
(17,'auth','0012_alter_user_first_name_max_length','2025-10-11 22:51:06.944073'),
(18,'sessions','0001_initial','2025-10-11 22:51:07.084059'),
(19,'core','0001_initial','2025-10-12 15:20:03.000000'),
(20,'core','0002_alter_usuario_password','2025-10-13 17:59:50.974518'),
(21,'core','0003_rol_remove_usuario_is_staff_and_more','2025-10-13 18:05:06.000614'),
(22,'core','0004_usuariogroups_usuariouserpermissions_and_more','2025-10-13 18:22:19.301791'),
(26,'core','0005_create_groups','2025-10-15 15:35:45.182914'),
(27,'core','0006_alter_producto_options','2025-10-15 15:35:45.185273'),
(28,'core','0007_auto_20251014_2210','2025-10-15 15:35:45.223918'),
(29,'core','0008_alter_lote_options_alter_proveedor_options_and_more','2025-10-23 16:20:52.069331'),
(30,'core','0009_lote_producto_lote_reabastecimiento_detalle_and_more','2025-10-23 16:21:36.117305'),
(31,'core','0010_alter_reabastecimientodetalle_producto','2025-10-23 16:24:55.647127'),
(32,'core','0011_alter_reabastecimiento_fecha','2025-10-24 19:47:00.851459'),
(33,'core','0012_alter_reabastecimiento_estado_and_more','2025-10-24 20:06:26.150271'),
(34,'core','0013_reabastecimientodetalle_fecha_caducidad','2025-10-24 20:11:09.401309'),
(35,'core','0014_alter_reabastecimiento_estado','2025-10-26 00:50:45.898286'),
(36,'core','0015_alter_venta_options','2025-11-04 12:44:09.192231'),
(37,'core','0016_venta_cliente_venta_total_venta_venta_usuario_and_more','2025-11-04 12:44:41.941894'),
(38,'core','0017_producto_costo_promedio','2025-11-04 12:45:04.813291'),
(39,'core','0018_reabastecimientodetalle_cantidad_recibida','2025-11-06 22:59:17.591418');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('1b0s2p82hi4jxv00zbq5o6v23uqc9las','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vDNIk:WJXxf3WffpPPuyXZ8VeYH91SHkICb81joOItM6BLhUg','2025-10-27 14:00:22.963471'),
('3ixjfnm43kc8fei8x7n1jmx3427nws3s','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGdsg:dybS3mRLVlga_AQ4IjCzs7xu6VpUswoE63DmDWEFiqY','2025-11-05 14:18:58.435462'),
('5zmbxix9g674opu0o13f8yguxb1jolhs','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vDMQa:MKyETvR3mKXSaRX61w5wCpxw71-VS4u8JzVzwxpPPJQ','2025-10-27 13:04:24.852602'),
('e5p2qa0m7ggpdj37ca6aci5abo1zmfk6','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGGJR:ilnIf4Fp8GsD0RIWmx00mhnHsgT4Ox2emo8RyIWQ1Ec','2025-11-04 13:09:01.845530'),
('ftj2d52gst4hofmn62mw5p7zi097cst0','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1v93GL:3HVC5ubuE-hkX9nVWmMlm_3gJsNCM1VI8S4yypUG4NU','2025-10-29 15:18:01.358432'),
('irq7kp9atw7604oaghxixv61ixtcsrr7','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGf5u:mWQBGdcCstXV-SIfWxJmtSLDNlXJmxPk40bLuAytJDY','2025-11-05 15:36:42.361404'),
('m553scah018bzxoikksk6pv2j9ook5zi','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vERiL:aXMCM2z1kHWSymTHvSgawklkuwGbWKM6m4zYwvhg6zw','2025-10-30 12:55:13.601706'),
('m8yeqh2u4e17xd1vyy4zrhouxb1ywm9s','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGGQK:-zLDFgcs-H5ckFETtXwyB46YxHtRalsFmLfJL0kK4Zw','2025-11-04 13:16:08.898180'),
('nmgu3hbp8sprxne8le2824fi6bv31i1r','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGGHY:byZNQCUGkh7PnzRJnGhkbo4Nsuz3Y0EMxgIudTpg810','2025-11-04 13:07:04.578558'),
('ps0zj1lnx515tr43jn2zcfwemqpuhr1v','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vH9TA:iuV_BffGoKM0PvKO0wPeJdiNG2xDdipOWJvpKt2SWI8','2025-11-07 00:02:44.163897'),
('sjnz0yqi5bn3fz11ys5xcye4p1v051x2','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vCqgL:ef5ligieaA5LOeZrnQ0aaPwe7QHpSGbRG3rIIXAH1jg','2025-10-26 03:10:33.064355'),
('t2ptv9dabngxc6rt55knh6v62w7m4km6','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vGGLI:YE_eS-4yHMzm0_Vd2EEcaTK6B3HkzNN3_usWLjhPdrw','2025-11-04 13:10:56.021555'),
('tlu2nyufphs2o7q25eczxae7yvbx7kn6','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vESll:2eNMORbJRvbys5Csa8aYupeOEpNOMx6NOZ7G9_9wYvI','2025-10-30 14:02:49.552270'),
('uulejdyo0kdfavhgwqhf6faownxqvr8t','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vDO9U:Ss1GjJiHlTMlo--75rRFSNvddGqz45cb8yBG-2idSYU','2025-10-27 14:54:52.848535'),
('uzicz2pty1swc8a5nz57r3znisodiqhv','.eJxVjDEOgzAMAP_iuYoCJYnN2J03RElsF9oKJAJT1b9XSAztene6N8S0b2Pcq6xxYujhCpdfllN5ynwIfqT5vpiyzNs6ZXMk5rTVDAvL63a2f4Mx1RF6SJ1VcRo4kHeWqC2KRKg2M5K3jpoGORH6tulykCLceg3qLTGjSoHPF9oGOA8:1vGbmH:Gxvkejt-0mnvQJofvEe6CLkx1Mbd-RNVJM7rls3fT7M','2025-11-05 12:04:13.892971');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `lote`
--

DROP TABLE IF EXISTS `lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `lote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) NOT NULL,
  `reabastecimiento_detalle_id` int(11) DEFAULT NULL,
  `numero_lote` varchar(50) NOT NULL,
  `cantidad_disponible` int(11) unsigned NOT NULL,
  `costo_unitario_lote` decimal(12,2) NOT NULL,
  `fecha_caducidad` date NOT NULL,
  `fecha_entrada` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_lote_producto_numero` (`producto_id`,`numero_lote`),
  KEY `fk_lote_producto` (`producto_id`),
  KEY `fk_lote_reabastecimiento_detalle` (`reabastecimiento_detalle_id`),
  CONSTRAINT `fk_lote_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_lote_reabastecimiento_detalle` FOREIGN KEY (`reabastecimiento_detalle_id`) REFERENCES `reabastecimiento_detalle` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `lote` VALUES
(1,1,1,'LCH-A1',80,2500.00,'2025-10-30','2025-09-01 10:00:00'),
(2,2,2,'QSO-C3',59,7000.00,'2025-11-15','2025-09-05 14:00:00'),
(3,7,38,'R36-P7-38',42,4500.00,'2025-12-31','2025-11-05 11:38:47'),
(4,8,39,'R37-P8-39',0,2500.00,'2025-12-06','2025-11-05 13:45:41'),
(5,7,42,'R40-P7-42',199,4500.00,'2026-01-15','2025-11-06 23:06:20'),
(6,7,40,'R38-P7-40',100,4500.00,'2026-01-17','2025-11-06 23:08:20');
/*!40000 ALTER TABLE `lote` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `movimiento_inventario`
--

DROP TABLE IF EXISTS `movimiento_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
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
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  KEY `lote_id` (`lote_id`),
  KEY `venta_id` (`venta_id`),
  KEY `reabastecimiento_id` (`reabastecimiento_id`),
  CONSTRAINT `fk_movimiento_inventario_lote` FOREIGN KEY (`lote_id`) REFERENCES `lote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_reabastecimiento` FOREIGN KEY (`reabastecimiento_id`) REFERENCES `reabastecimiento` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_movimiento_inventario_venta` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimiento_inventario`
--

LOCK TABLES `movimiento_inventario` WRITE;
/*!40000 ALTER TABLE `movimiento_inventario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `movimiento_inventario` VALUES
(1,1,1,100,'ENTRADA','2025-10-10 22:48:22','Reabastecimiento inicial Lote A1',NULL,1),
(2,2,2,60,'ENTRADA','2025-10-10 22:48:22','Reabastecimiento inicial Lote C3',NULL,1),
(3,1,1,-2,'SALIDA','2025-10-10 22:48:22','Venta ID 1',1,NULL),
(4,2,2,-1,'SALIDA','2025-10-10 22:48:22','Venta ID 2',2,NULL),
(5,7,3,60,'entrada','2025-11-05 11:38:47','Entrada por reabastecimiento #36',NULL,36),
(6,7,3,1,'salida','2025-11-05 12:40:34','Venta #6',6,NULL),
(7,1,1,6,'salida','2025-11-05 12:44:58','Venta #7',7,NULL),
(8,8,4,10,'entrada','2025-11-05 13:45:41','Entrada por reabastecimiento #37',NULL,37),
(9,8,4,10,'salida','2025-11-05 13:48:30','Venta #8',8,NULL),
(10,7,3,4,'salida','2025-11-06 22:52:29','Venta #9',9,NULL),
(11,7,5,199,'entrada','2025-11-06 23:06:20','Entrada por reabastecimiento #40',NULL,40),
(12,7,6,100,'entrada','2025-11-06 23:08:20','Entrada por reabastecimiento #38',NULL,38);
/*!40000 ALTER TABLE `movimiento_inventario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pqrs`
--

DROP TABLE IF EXISTS `pqrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
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
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_pqrs_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_pqrs_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pqrs`
--

LOCK TABLES `pqrs` WRITE;
/*!40000 ALTER TABLE `pqrs` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `pqrs` VALUES
(1,'SUGERENCIA','Más productos saludables',NULL,'en_proceso','2025-07-01 10:00:00',NULL,1,2);
/*!40000 ALTER TABLE `pqrs` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pqrs_historial`
--

DROP TABLE IF EXISTS `pqrs_historial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pqrs_historial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pqrs_id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `estado_anterior` varchar(20) NOT NULL,
  `estado_nuevo` varchar(20) NOT NULL,
  `descripcion_cambio` text DEFAULT NULL,
  `fecha_cambio` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `pqrs_id` (`pqrs_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_pqrs_historial_pqrs` FOREIGN KEY (`pqrs_id`) REFERENCES `pqrs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pqrs_historial_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pqrs_historial`
--

LOCK TABLES `pqrs_historial` WRITE;
/*!40000 ALTER TABLE `pqrs_historial` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `pqrs_historial` VALUES
(1,1,2,'pendiente','en_proceso','Se asigna el caso al administrador para evaluar la solicitud.','2025-10-10 22:48:22');
/*!40000 ALTER TABLE `pqrs_historial` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `precio_unitario` decimal(12,2) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `stock_minimo` int(11) NOT NULL DEFAULT 10,
  `categoria_id` int(11) NOT NULL,
  `stock_actual` int(10) unsigned NOT NULL CHECK (`stock_actual` >= 0),
  `costo_promedio` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_producto_nombre` (`nombre`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `producto` VALUES
(1,'Leche Entera 1L',3800.00,'Leche pasteurizada',10,1,80,2500.00),
(2,'Queso Campesino 500g',9500.00,'Queso fresco de vaca',5,2,59,7000.00),
(3,'Yogurt',3000.00,NULL,10,1,0,0.00),
(4,'Manzana',4500.00,'Sabor a manzana, 1L',3,4,0,0.00),
(7,'aguila',4500.00,'tipo lager',1,3,341,4500.00),
(8,'papas fritas',2500.00,'',5,1,0,0.00);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(100) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `proveedor` VALUES
(1,'Proveedor de Lacteos S.A.','123456789','contacto@lacteos.com','Calle Falsa 123'),
(2,'postobn','3573612371','postobon@gmail.com','kra93 #32-13'),
(3,'poker','2131456','lizarazojuanandres@gmail.com','cra1052165'),
(4,'papas margarita','235156023','margaritas@gmail.com','cra100$#95-54');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reabastecimiento`
--

DROP TABLE IF EXISTS `reabastecimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reabastecimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `costo_total` decimal(12,2) NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'solicitado' COMMENT 'Posibles valores: solicitado, cancelado, recibido',
  `forma_pago` varchar(25) DEFAULT 'Efectivo',
  `observaciones` text DEFAULT NULL,
  `proveedor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `fk_reabastecimiento_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reabastecimiento`
--

LOCK TABLES `reabastecimiento` WRITE;
/*!40000 ALTER TABLE `reabastecimiento` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reabastecimiento` VALUES
(1,'2025-09-01 09:00:00',670000.00,'recibido','Efectivo','Reabastecimiento inicial',1),
(36,'2025-11-05 11:38:27',270000.00,'recibido','pse','',3),
(37,'2025-11-05 13:45:25',25000.00,'recibido','pse','',4),
(38,'2025-11-06 22:53:32',450000.00,'recibido','pse','',3),
(40,'2025-11-06 22:54:41',900000.00,'recibido','pse','',3);
/*!40000 ALTER TABLE `reabastecimiento` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reabastecimiento_detalle`
--

DROP TABLE IF EXISTS `reabastecimiento_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reabastecimiento_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reabastecimiento_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `costo_unitario` decimal(12,2) NOT NULL,
  `fecha_caducidad` date DEFAULT NULL,
  `cantidad_recibida` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reabastecimiento_id` (`reabastecimiento_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `fk_reabastecimiento_detalle_reabastecimiento` FOREIGN KEY (`reabastecimiento_id`) REFERENCES `reabastecimiento` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reabastecimiento_detalle_producto_id_63c5cefe_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reabastecimiento_detalle`
--

LOCK TABLES `reabastecimiento_detalle` WRITE;
/*!40000 ALTER TABLE `reabastecimiento_detalle` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reabastecimiento_detalle` VALUES
(1,1,1,100,2500.00,NULL,0),
(2,1,2,60,7000.00,NULL,0),
(38,36,7,60,4500.00,'2025-12-31',0),
(39,37,8,10,2500.00,'2025-12-06',0),
(40,38,7,100,4500.00,'2026-01-17',100),
(42,40,7,200,4500.00,'2026-01-15',199);
/*!40000 ALTER TABLE `reabastecimiento_detalle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(35) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `rol` VALUES
(1,'Administrador'),
(2,'Vendedor');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
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
  `reset_token` varchar(36) DEFAULT NULL,
  `reset_token_expiracion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `documento` (`documento`),
  UNIQUE KEY `correo` (`correo`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `usuario` VALUES
(1,'1014477103','Juan Andres','Lizarazo','liza@gmail.com','3105416287','$2a$10$NFwQSzu8/6T5IZTPGEKStu89rBkNLd1VloKWkIvXROYJlh.f6m4G.','activo','2025-10-10 22:48:22',NULL,2,NULL,NULL),
(2,'1234567','Admin','Principal','admin@playita.com','32124551','admin_hash','activo','2025-10-10 22:48:22',NULL,1,NULL,NULL),
(3,'1014477104','Juan Andres','Lizarazo Capera','lizarazojuanandres@gmail.com','3105416287','pbkdf2_sha256$1000000$NNKz1R6vzGnVe3mTKnztCL$dZiRmnhpPnu7TBSvMYh2BVIhu+mCbk4T780036dA9GY=','activo','2025-10-13 23:05:38','2025-11-05 16:34:04',2,NULL,NULL),
(4,'10000000','Admin','ROL 1','admin_final_rol1@laplayita.com',NULL,'pbkdf2_sha256$1000000$5IUYpFqgilB2EvaR9GQJya$hH7HV5VkSrpqZSxNsg5r9+/o+2BQyzYwWbPiyTDV204=','activo','2025-10-13 19:08:10','2025-11-07 03:52:20',1,NULL,NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_venta` datetime NOT NULL,
  `metodo_pago` varchar(25) NOT NULL DEFAULT 'Efectivo',
  `canal_venta` varchar(20) NOT NULL DEFAULT 'Tienda',
  `cliente_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `total_venta` decimal(12,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_venta_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `venta` VALUES
(1,'2025-09-02 10:00:00','Efectivo','Tienda',1,1,0.00),
(2,'2025-09-03 11:30:00','Tarjeta','Domicilio',2,1,0.00),
(3,'2025-11-05 12:24:54','efectivo','local',1,4,4500.00),
(4,'2025-11-05 12:25:24','efectivo','local',1,4,54000.00),
(5,'2025-11-05 12:25:41','efectivo','local',2,4,45600.00),
(6,'2025-11-05 12:40:34','efectivo','local',2,4,4500.00),
(7,'2025-11-05 12:44:58','efectivo','local',1,4,22800.00),
(8,'2025-11-05 13:48:30','efectivo','local',2,4,25000.00),
(9,'2025-11-06 22:52:29','efectivo','local',2,4,18000.00);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `venta_detalle`
--

DROP TABLE IF EXISTS `venta_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_detalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `lote_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_id` (`producto_id`),
  KEY `lote_id` (`lote_id`),
  CONSTRAINT `fk_venta_detalle_lote` FOREIGN KEY (`lote_id`) REFERENCES `lote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_detalle_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_detalle_venta` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_detalle`
--

LOCK TABLES `venta_detalle` WRITE;
/*!40000 ALTER TABLE `venta_detalle` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `venta_detalle` VALUES
(1,1,1,1,2,7600.00),
(2,2,2,2,1,9500.00),
(3,3,7,3,1,4500.00),
(4,4,7,3,12,54000.00),
(5,5,1,1,12,45600.00),
(6,6,7,3,1,4500.00),
(7,7,1,1,6,22800.00),
(8,8,8,4,10,25000.00),
(9,9,7,3,4,18000.00);
/*!40000 ALTER TABLE `venta_detalle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Temporary table structure for view `vista_historial_movimientos`
--

DROP TABLE IF EXISTS `vista_historial_movimientos`;
/*!50001 DROP VIEW IF EXISTS `vista_historial_movimientos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_historial_movimientos` AS SELECT
 1 AS `fecha_movimiento`,
  1 AS `tipo_movimiento`,
  1 AS `nombre_producto`,
  1 AS `cantidad`,
  1 AS `numero_lote`,
  1 AS `descripcion`,
  1 AS `origen_transaccion` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_lotes_activos`
--

DROP TABLE IF EXISTS `vista_lotes_activos`;
/*!50001 DROP VIEW IF EXISTS `vista_lotes_activos`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_lotes_activos` AS SELECT
 1 AS `lote_id`,
  1 AS `producto_id`,
  1 AS `nombre_producto`,
  1 AS `numero_lote`,
  1 AS `cantidad_disponible`,
  1 AS `costo_unitario_lote`,
  1 AS `fecha_caducidad`,
  1 AS `dias_para_caducar`,
  1 AS `cantidad_inicial` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_margen_por_venta_detalle`
--

DROP TABLE IF EXISTS `vista_margen_por_venta_detalle`;
/*!50001 DROP VIEW IF EXISTS `vista_margen_por_venta_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_margen_por_venta_detalle` AS SELECT
 1 AS `venta_id`,
  1 AS `nombre_producto`,
  1 AS `numero_lote`,
  1 AS `cantidad`,
  1 AS `subtotal_venta`,
  1 AS `costo_unitario_lote`,
  1 AS `costo_total_vendido`,
  1 AS `margen_bruto` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_stock_consolidado`
--

DROP TABLE IF EXISTS `vista_stock_consolidado`;
/*!50001 DROP VIEW IF EXISTS `vista_stock_consolidado`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_stock_consolidado` AS SELECT
 1 AS `producto_id`,
  1 AS `nombre_producto`,
  1 AS `stock_minimo`,
  1 AS `stock_actual_total`,
  1 AS `categoria`,
  1 AS `estado_stock` */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vista_venta_con_total`
--

DROP TABLE IF EXISTS `vista_venta_con_total`;
/*!50001 DROP VIEW IF EXISTS `vista_venta_con_total`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vista_venta_con_total` AS SELECT
 1 AS `venta_id`,
  1 AS `fecha_venta`,
  1 AS `metodo_pago`,
  1 AS `canal_venta`,
  1 AS `nombre_cliente`,
  1 AS `nombre_vendedor`,
  1 AS `total_venta` */;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'laplayita'
--

--
-- Dumping routines for database 'laplayita'
--

--
-- Current Database: `laplayita`
--

USE `laplayita`;

--
-- Final view structure for view `vista_historial_movimientos`
--

/*!50001 DROP VIEW IF EXISTS `vista_historial_movimientos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_historial_movimientos` AS select 1 AS `fecha_movimiento`,1 AS `tipo_movimiento`,1 AS `nombre_producto`,1 AS `cantidad`,1 AS `numero_lote`,1 AS `descripcion`,1 AS `origen_transaccion` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_lotes_activos`
--

/*!50001 DROP VIEW IF EXISTS `vista_lotes_activos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_lotes_activos` AS select 1 AS `lote_id`,1 AS `producto_id`,1 AS `nombre_producto`,1 AS `numero_lote`,1 AS `cantidad_disponible`,1 AS `costo_unitario_lote`,1 AS `fecha_caducidad`,1 AS `dias_para_caducar`,1 AS `cantidad_inicial` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_margen_por_venta_detalle`
--

/*!50001 DROP VIEW IF EXISTS `vista_margen_por_venta_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_margen_por_venta_detalle` AS select 1 AS `venta_id`,1 AS `nombre_producto`,1 AS `numero_lote`,1 AS `cantidad`,1 AS `subtotal_venta`,1 AS `costo_unitario_lote`,1 AS `costo_total_vendido`,1 AS `margen_bruto` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_stock_consolidado`
--

/*!50001 DROP VIEW IF EXISTS `vista_stock_consolidado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_stock_consolidado` AS select 1 AS `producto_id`,1 AS `nombre_producto`,1 AS `stock_minimo`,1 AS `stock_actual_total`,1 AS `categoria`,1 AS `estado_stock` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_venta_con_total`
--

/*!50001 DROP VIEW IF EXISTS `vista_venta_con_total`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_uca1400_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_venta_con_total` AS select 1 AS `venta_id`,1 AS `fecha_venta`,1 AS `metodo_pago`,1 AS `canal_venta`,1 AS `nombre_cliente`,1 AS `nombre_vendedor`,1 AS `total_venta` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-11-06 18:36:43
