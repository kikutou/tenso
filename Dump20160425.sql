-- MySQL dump 10.13  Distrib 5.6.30, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: qh_logistics
-- ------------------------------------------------------
-- Server version	5.6.30-0ubuntu0.15.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hst_out_box`
--

DROP TABLE IF EXISTS `hst_out_box`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hst_out_box` (
  `hst_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(20) NOT NULL,
  `memo` text,
  `length` int(5) NOT NULL DEFAULT '0',
  `width` int(5) NOT NULL DEFAULT '0',
  `height` int(5) NOT NULL DEFAULT '0',
  `weight` int(5) NOT NULL DEFAULT '0',
  `staff_id` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `customer_id` int(11) DEFAULT '0',
  `delete_flag` tinyint(1) DEFAULT '0',
  `delivery_no` varchar(30) DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hst_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hst_out_box`
--

LOCK TABLES `hst_out_box` WRITE;
/*!40000 ALTER TABLE `hst_out_box` DISABLE KEYS */;
/*!40000 ALTER TABLE `hst_out_box` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_customer`
--

DROP TABLE IF EXISTS `mst_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `real_name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `telephone1` varchar(20) DEFAULT NULL,
  `telephone2` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `id_confirmed_flag` tinyint(1) NOT NULL DEFAULT '0',
  `id_card_no` varchar(50) DEFAULT NULL,
  `id_card_pic_front` varchar(100) DEFAULT NULL,
  `id_card_pic_back` varchar(100) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `company_address` varchar(100) DEFAULT NULL,
  `company_telephone` varchar(20) DEFAULT NULL,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_customer`
--

LOCK TABLES `mst_customer` WRITE;
/*!40000 ALTER TABLE `mst_customer` DISABLE KEYS */;
INSERT INTO `mst_customer` VALUES (1,'メアモール','株式会社メアモール','東京都台東区蔵前4丁目3−4','03-5829-9500','','info@mamol.co.jp',1,'88888888','/img/pic_front.jpg','/img/pic_back.jpg','株式会社メアモール','東京都台東区蔵前4丁目3−4','03-5829-9500',0),(2,'メアモール2No2','株式会社メアモール2','東京都台東区蔵前4丁目3−42','03-5829-95002','','info@mamol.co.jp2',0,'888888882','/img/pic_front.jpg','/img/pic_back.jpg','株式会社メアモール2','東京都台東区蔵前4丁目3−42','03-5829-9500',0),(3,'wenhu','panwenhu','林海町','1234567','7654321','wenhu@gmail.com',0,'',NULL,NULL,'mamol','kuramae','03-9999-9999',1),(4,'jiafu','jiafuchun','kuramae','080-9999-9999','080-8888-8888','jiafuchun@gmail.com',0,'371082198809101015',NULL,NULL,'mamol','kuramae','03-333333',1),(5,'jiafu','jiafuchun','kuramae','080-9999-9999','080-8888-8888','jiafuchun@gmail.com',0,'371082198809101015',NULL,NULL,'mamol','kuramae','03-333333',1),(6,'jiafu','jiafuchun','kuramae','080-9999-9999','080-8888-8888','jiafuchun@gmail.com',0,'371082198809101015',NULL,NULL,'mamol','kuramae','03-333333',1),(7,'jiafu','jiafuchun','kuramae','080-9999-9999','080-8888-8888','jiafuchun@gmail.com',0,'371082198809101015',NULL,NULL,'mamol','kuramae','03-333333',1),(8,'jiafu','jiafuchun','kuramae','080-9999-9999','080-8888-8888','jiafuchun@gmail.com',0,'371082198809101015',NULL,NULL,'mamol','kuramae','03-333333',0),(9,'chenwenj','chenwenhua','ryoukoku','080-5555-5555','080-4444-4444','wenhua@gmail.com',0,'371082198805050505',NULL,NULL,'mamol','kuramae','03-9999-9999',0),(10,'gengguoyao','guoyao','sinnjyuku ','080-9999-9999','080-5555-5555','geng@gmail.com',1,'37454545616456646465',NULL,NULL,'株式会社','浅草桥','03-9999-8888',1),(11,'kiku','鞠','warabi','080-9486-8888','080-4444-5555','juteng@gmail.com',0,'371082198809101014',NULL,NULL,'mamol','kurame','03-9999-8888',1),(12,'gengguo','guo','sinnjyku ','080-8888-8888','080-5888-8888','geng@gmail.com',1,'374841484884',NULL,NULL,'mamol','karamae','03-999-8888',1);
/*!40000 ALTER TABLE `mst_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_in_box`
--

DROP TABLE IF EXISTS `mst_in_box`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_in_box` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `import_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(20) NOT NULL,
  `memo` text,
  `length` int(5) NOT NULL DEFAULT '0',
  `width` int(5) NOT NULL DEFAULT '0',
  `height` int(5) NOT NULL DEFAULT '0',
  `weight` int(5) NOT NULL DEFAULT '0',
  `customer_id` int(11) DEFAULT NULL,
  `staff_id` int(1) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `delete_flag` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_in_box`
--

LOCK TABLES `mst_in_box` WRITE;
/*!40000 ALTER TABLE `mst_in_box` DISABLE KEYS */;
INSERT INTO `mst_in_box` VALUES (1,'2016-04-13 12:58:21','包裹1','34',4,5,6,7,1,5,2,0),(12,'2016-04-13 12:58:21','包裹2','',5,6,1,5,1,5,0,0),(13,'2016-04-13 13:05:57','包裹3','',6,7,4,6,1,5,0,0),(16,'2016-04-20 03:29:08','test','test',100,100,100,50,1,5,0,1),(17,'2016-04-20 04:07:22','test入库','test用',50,60,70,80,1,5,0,1),(18,'2016-04-20 05:55:55','测试删除','测试ceshi',55,66,75,12,1,5,0,1),(19,'2016-04-20 07:07:50','No4aa','4',50,60,70,120,1,5,0,1);
/*!40000 ALTER TABLE `mst_in_box` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_item`
--

DROP TABLE IF EXISTS `mst_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jan_code` varchar(13) DEFAULT NULL,
  `memo` text,
  `en_name` varchar(50) DEFAULT NULL,
  `cn_name` varchar(50) DEFAULT NULL,
  `jp_name` varchar(50) DEFAULT NULL,
  `unit_price` int(5) NOT NULL DEFAULT '0',
  `country_of_origin` int(11) NOT NULL DEFAULT '0',
  `delete_flag` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `jan_code` (`jan_code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_item`
--

LOCK TABLES `mst_item` WRITE;
/*!40000 ALTER TABLE `mst_item` DISABLE KEYS */;
INSERT INTO `mst_item` VALUES (1,'4901201113789','飲料・酒類 清涼飲料 コーヒードリンク','Black coffee','黑咖啡','UCC BLACK無糖 SMOOTH&CLEAR リキャップ缶・375g',155,1,0);
/*!40000 ALTER TABLE `mst_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_made_in`
--

DROP TABLE IF EXISTS `mst_made_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_made_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `made_in_country` varchar(20) NOT NULL,
  `delete_flag` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_made_in`
--

LOCK TABLES `mst_made_in` WRITE;
/*!40000 ALTER TABLE `mst_made_in` DISABLE KEYS */;
INSERT INTO `mst_made_in` VALUES (1,'中国',0),(2,'日本',0);
/*!40000 ALTER TABLE `mst_made_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_out_box`
--

DROP TABLE IF EXISTS `mst_out_box`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_out_box` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `memo` text,
  `length` int(5) NOT NULL DEFAULT '0',
  `width` int(5) NOT NULL DEFAULT '0',
  `height` int(5) NOT NULL DEFAULT '0',
  `weight` int(5) NOT NULL DEFAULT '0',
  `staff_id` int(11) NOT NULL DEFAULT '0',
  `customer_id` int(11) DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `delivery_no` varchar(30) DEFAULT NULL,
  `delete_flag` tinyint(1) DEFAULT '0',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_out_box`
--

LOCK TABLES `mst_out_box` WRITE;
/*!40000 ALTER TABLE `mst_out_box` DISABLE KEYS */;
INSERT INTO `mst_out_box` VALUES (1,'出箱1','test',50,60,78,55,5,1,0,NULL,0,'2016-04-20 10:01:59',0),(2,'出箱2','test2',88,77,66,22,5,1,0,NULL,0,'2016-04-20 10:02:31',0);
/*!40000 ALTER TABLE `mst_out_box` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_staff`
--

DROP TABLE IF EXISTS `mst_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mst_staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_cd` varchar(20) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `telphone` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `authority` tinyint(1) NOT NULL DEFAULT '0',
  `password` varchar(100) DEFAULT NULL,
  `delete_flag` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `staff_cd` (`staff_cd`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_staff`
--

LOCK TABLES `mst_staff` WRITE;
/*!40000 ALTER TABLE `mst_staff` DISABLE KEYS */;
INSERT INTO `mst_staff` VALUES (4,NULL,'鈴木',NULL,'suzuki@gmail.com',0,'pbkdf2:sha1:1000$fXJRktY5$afb7ca28db9d4f40739806768a959078a504ac2e',0),(5,NULL,'田中',NULL,'tanaka@gmail.com',0,'pbkdf2:sha1:1000$b65nNmTl$45ed4069a1d69cf3420b29f4cb597fa1e5fdf82f',0),(6,NULL,'dsf',NULL,'sdfs@sdfsf',0,'pbkdf2:sha1:1000$PyKkLJm6$567517ccd2665a03a4fe400540f31e0ed4b7613b',0);
/*!40000 ALTER TABLE `mst_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rel_in_item`
--

DROP TABLE IF EXISTS `rel_in_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_in_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `check_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `in_box_id` int(11) DEFAULT '0',
  `item_id` int(11) NOT NULL DEFAULT '0',
  `item_num` int(11) NOT NULL DEFAULT '0',
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rel_in_item`
--

LOCK TABLES `rel_in_item` WRITE;
/*!40000 ALTER TABLE `rel_in_item` DISABLE KEYS */;
INSERT INTO `rel_in_item` VALUES (3,'2016-04-25 07:00:27',1,1,41,0);
/*!40000 ALTER TABLE `rel_in_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rel_out_item`
--

DROP TABLE IF EXISTS `rel_out_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_out_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `check_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `out_box_id` int(11) DEFAULT '0',
  `item_id` int(11) NOT NULL DEFAULT '0',
  `item_num` int(11) NOT NULL DEFAULT '0',
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rel_out_item`
--

LOCK TABLES `rel_out_item` WRITE;
/*!40000 ALTER TABLE `rel_out_item` DISABLE KEYS */;
INSERT INTO `rel_out_item` VALUES (3,'2016-04-25 07:00:27',1,1,28,0),(4,'2016-04-25 05:59:47',2,1,13,0);
/*!40000 ALTER TABLE `rel_out_item` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-25 21:52:49
