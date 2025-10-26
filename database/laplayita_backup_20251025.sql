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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
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
(35,'core','0014_alter_reabastecimiento_estado','2025-10-26 00:50:45.898286');
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
('ftj2d52gst4hofmn62mw5p7zi097cst0','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1v93GL:3HVC5ubuE-hkX9nVWmMlm_3gJsNCM1VI8S4yypUG4NU','2025-10-29 15:18:01.358432'),
('sjnz0yqi5bn3fz11ys5xcye4p1v051x2','.eJxVjDsOAiEUAO9CbQjyx9LeM5AHjyerBpJltzLe3ZBsoe3MZN4swr7VuI-yxgXZhWl2-mUJ8rO0KfAB7d557m1bl8Rnwg87-K1jeV2P9m9QYdS5JZsdaY1ZmaCMCsI4KTBQkkGADMUGe1ZaeKnAF7KETtgEmrQr4JJnny_F9Ddd:1vCqgL:ef5ligieaA5LOeZrnQ0aaPwe7QHpSGbRG3rIIXAH1jg','2025-10-26 03:10:33.064355');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `lote` VALUES
(1,1,1,'LCH-A1',98,2500.00,'2025-10-30','2025-09-01 10:00:00'),
(2,2,2,'QSO-C3',59,7000.00,'2025-11-15','2025-09-05 14:00:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
(4,2,2,-1,'SALIDA','2025-10-10 22:48:22','Venta ID 2',2,NULL);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_producto_nombre` (`nombre`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `fk_producto_categoria` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `producto` VALUES
(1,'Leche Entera 1L',3800.00,'Leche pasteurizada',10,1,98),
(2,'Queso Campesino 500g',9500.00,'Queso fresco de vaca',5,2,59),
(3,'Yogurt',3000.00,NULL,10,1,0),
(4,'Manzana',4500.00,'Sabor a manzana, 1L',3,4,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `proveedor` VALUES
(1,'Proveedor de Lacteos S.A.','123456789','contacto@lacteos.com','Calle Falsa 123'),
(2,'postobn','3573612371','postobon@gmail.com','kra93 #32-13');
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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reabastecimiento`
--

LOCK TABLES `reabastecimiento` WRITE;
/*!40000 ALTER TABLE `reabastecimiento` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reabastecimiento` VALUES
(1,'2025-09-01 09:00:00',670000.00,'recibido','Efectivo','Reabastecimiento inicial',1);
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
  PRIMARY KEY (`id`),
  KEY `reabastecimiento_id` (`reabastecimiento_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `fk_reabastecimiento_detalle_reabastecimiento` FOREIGN KEY (`reabastecimiento_id`) REFERENCES `reabastecimiento` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reabastecimiento_detalle_producto_id_63c5cefe_fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reabastecimiento_detalle`
--

LOCK TABLES `reabastecimiento_detalle` WRITE;
/*!40000 ALTER TABLE `reabastecimiento_detalle` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reabastecimiento_detalle` VALUES
(1,1,1,100,2500.00,NULL),
(2,1,2,60,7000.00,NULL);
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
(3,'1014477104','Juan Andres','Lizarazo Capera','lizarazojuanandres@gmail.com','3105416287','pbkdf2_sha256$1000000$hu9yv6CnIzhw8H5E2tSJqe$3yPdIilL05BDEyOudNH7R+sZE8UwFT/i57yJXVyA5Fk=','activo','2025-10-13 23:05:38','2025-10-14 00:45:26',2,NULL,NULL),
(4,'10000000','Admin','ROL 1','admin_final_rol1@laplayita.com',NULL,'pbkdf2_sha256$1000000$5IUYpFqgilB2EvaR9GQJya$hH7HV5VkSrpqZSxNsg5r9+/o+2BQyzYwWbPiyTDV204=','activo','2025-10-13 19:08:10','2025-10-26 05:07:40',1,NULL,NULL);
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
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `fk_venta_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_venta_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `venta` VALUES
(1,'2025-09-02 10:00:00','Efectivo','Tienda',1,1),
(2,'2025-09-03 11:30:00','Tarjeta','Domicilio',2,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_detalle`
--

LOCK TABLES `venta_detalle` WRITE;
/*!40000 ALTER TABLE `venta_detalle` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `venta_detalle` VALUES
(1,1,1,1,2,7600.00),
(2,2,2,2,1,9500.00);
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
-- Final view structure for view `vista_historial_movimientos`
--

/*!50001 DROP VIEW IF EXISTS `vista_historial_movimientos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
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
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
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
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
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
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
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
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
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

-- Dump completed on 2025-10-25 21:43:20
