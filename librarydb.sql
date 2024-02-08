-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: newdb
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book_details`
--

DROP TABLE IF EXISTS `book_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_details` (
  `acc_no` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(25) NOT NULL,
  `status` varchar(15) NOT NULL,
  `dept` varchar(10) NOT NULL,
  `purchase_dt` varchar(15) NOT NULL,
  PRIMARY KEY (`acc_no`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_details`
--

LOCK TABLES `book_details` WRITE;
/*!40000 ALTER TABLE `book_details` DISABLE KEYS */;
INSERT INTO `book_details` VALUES (2,'1109410700','Available','Library','2/2/2003'),(3,'1109410700','Available','Library','2/2/2003'),(5,'1345009845','Available','Library','2/2/2023'),(6,'1674563200','Issued','Library','30/3/2023'),(8,'1674563200','Available','Library','30/3/2023'),(10,'1111','Available','Library','17/11/2023'),(11,'1111','Available','Library','17/11/2023'),(12,'1200984567','Available','Library','17/11/23'),(13,'1200984567','Available','Library','17/11/23'),(14,'1200984567','Available','Library','17/11/23'),(15,'1276899045','Available','Library','17/11/2023'),(16,'1276899045','Available','Library','17/11/2023'),(17,'1276899045','Available','Library','17/11/2023'),(18,'1276899045','Available','Library','17/11/2023');
/*!40000 ALTER TABLE `book_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_delete_book` BEFORE DELETE ON `book_details` FOR EACH ROW BEGIN
    DECLARE book_status VARCHAR(255);

    -- Check the availability status of the book
    SELECT status INTO book_status FROM book_details WHERE acc_no = OLD.acc_no;

    -- Check if the book is issued or unavailable, prevent deletion
    IF book_status = 'Issued' OR book_status = 'Unavailable' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete book. Book is currently issued or unavailable.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `book_master`
--

DROP TABLE IF EXISTS `book_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_master` (
  `isbn` varchar(15) NOT NULL,
  `bk_title` varchar(30) NOT NULL,
  `author1` varchar(25) NOT NULL,
  `author2` varchar(25) DEFAULT NULL,
  `author3` varchar(25) DEFAULT NULL,
  `edition` varchar(5) DEFAULT NULL,
  `vol` int DEFAULT NULL,
  `publication` varchar(25) NOT NULL,
  `no_of_pg` int NOT NULL,
  `bk_lang` varchar(5) NOT NULL,
  `bk_sub` varchar(10) NOT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_master`
--

LOCK TABLES `book_master` WRITE;
/*!40000 ALTER TABLE `book_master` DISABLE KEYS */;
INSERT INTO `book_master` VALUES ('1109410700','Basic electrical Engineering','Ritu Gupta','R.C Sharma','Ravi Narayan','4th',2,'Khanna Publications',450,'Eng','BEE'),('1111','testbook','testauthor1','testauthor2','','5th',2,'testpub',300,'eng','testsub'),('1156732009','Programming in C','Leela Shah',NULL,NULL,'5th',3,'Royal Book Company',550,'Eng','CPC'),('1195012121','Basic Electrical Engineering','Sita Varma','N.C Patil',NULL,'2nd',1,'Khanna Publications',200,'Eng','BEE'),('1200984567','Let us C','Yashwant Kanetkar',NULL,NULL,'5th',9,'Pearson Publications',300,'Eng','CPC'),('12345678','testbook','testaut','testaut2','','3rd',2,'xyz',30,'eng','klm'),('123456789','abcd','xyz','klm','','4th',2,'tatamcgraw',200,'eng','alpha'),('1276899045','Engineering Graphics','R.C Varma','Sahedev Murti',NULL,'9th',4,'Tata MCgraw Hill',560,'Eng','EG'),('1345009845','Software Testing','Sapna Singh','Aakash Gupta',NULL,'5th',3,'Royal Book Company',890,'Eng','SE'),('1674563200','Database Management','C.V Rangnath',NULL,NULL,'3rd',1,'Khanna Publications',650,'Eng','ADBS'),('1789445600','Basic Mech Engineering','Shilpa Lalsare','Rakesh Singh','Seema Noida','4th',2,'Tata MCgraw Hill',650,'Eng','BM'),('1923459980','ML Algorithms','R.M Mathive','Robert Shef',NULL,'2nd',5,'Pearson Publications',780,'Eng','ML'),('1976409982','Basic Engineering Drawings','R.C Varma',NULL,NULL,'2nd',1,'Crown Groups',420,'Eng','EG');
/*!40000 ALTER TABLE `book_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issues`
--

DROP TABLE IF EXISTS `issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issues` (
  `prn` int NOT NULL,
  `acc_no` int NOT NULL,
  `issue_dt` date DEFAULT NULL,
  `due_dt` date DEFAULT NULL,
  `return_dt` date DEFAULT NULL,
  `fine` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issues`
--

LOCK TABLES `issues` WRITE;
/*!40000 ALTER TABLE `issues` DISABLE KEYS */;
INSERT INTO `issues` VALUES (212142,1,'2023-11-08','2023-11-15','2023-11-16',1,1),(212152,3,'2023-11-08','2023-11-15','2023-11-20',5,2),(212166,6,'2023-11-16','2023-11-23','2023-11-30',7,4),(212271,7,'2023-11-16','2023-11-23','2023-11-17',0,5),(212153,4,'2023-11-17','2023-11-24',NULL,0,7),(212153,9,'2023-11-17','2023-11-24',NULL,0,8),(212271,12,'2023-11-17','2023-11-24',NULL,0,9),(212266,5,'2023-11-17','2023-11-24',NULL,0,10),(212182,15,'2023-11-18','2023-11-25','2023-11-30',5,11);
/*!40000 ALTER TABLE `issues` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `generate_due_dt` BEFORE INSERT ON `issues` FOR EACH ROW BEGIN
         SET NEW.due_dt = DATE_ADD(NEW.issue_dt, INTERVAL 7 DAY);
     END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `UpdateBookStatus` AFTER INSERT ON `issues` FOR EACH ROW BEGIN
    DECLARE acc_no INT;
    SELECT acc_no INTO acc_no FROM issues WHERE acc_no = NEW.acc_no;
    UPDATE book_details SET status = 'Issued' WHERE acc_no = acc_no;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `publication`
--

DROP TABLE IF EXISTS `publication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publication` (
  `pub_id` int NOT NULL,
  `pub_name` varchar(25) NOT NULL,
  `ph_no` varchar(15) NOT NULL,
  `addr` varchar(30) NOT NULL,
  `email` varchar(20) NOT NULL,
  PRIMARY KEY (`pub_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publication`
--

LOCK TABLES `publication` WRITE;
/*!40000 ALTER TABLE `publication` DISABLE KEYS */;
INSERT INTO `publication` VALUES (741,'Khanna Publications','9987654409','GandhiNagar, Gujrat','khanna@gmail.com'),(7234,'testpub','923892898','test address','testemail@gmail.com'),(7522,'Pearson Publications','8446523000','Ravi Plaza, Aurangabad','pear@gmail.com'),(7560,'Tata MCgraw Hill','9877604532','Complex Pride, Chennai','tata@gmail.com'),(7788,'Crown Groups','8766547900','City Road, Agra','crown@gmail.com'),(7942,'Royal Book Company','7655400988','Max Site, Mumbai','royal@gmail.com');
/*!40000 ALTER TABLE `publication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `invoice_no` int NOT NULL,
  `pub_id` int NOT NULL,
  `isbn` varchar(15) NOT NULL,
  `quantity` int NOT NULL,
  `purchase_dt` varchar(15) NOT NULL,
  `price` varchar(10) NOT NULL,
  PRIMARY KEY (`invoice_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES (1,7412,'1109410700',3,'1/1/2001','650'),(2,7412,'1156732009',1,'11/5/2008','2000'),(3,7942,'1195012121',2,'11/5/2008','950'),(4,7560,'1200984567',4,'9/10/2007','540'),(5,7788,'1276899045',1,'10/5/2014','780'),(6,7522,'1345009845',1,'8/9/2001','450'),(7,7560,'1674563200',1,'14/7/2007','230'),(8,7522,'1789445600',1,'15/11/2015','580'),(9,7942,'1923459980',1,'19/3/2001','950'),(10,7412,'1976409982',2,'27/12/2019','400');
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `PRN` int NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Dept` varchar(6) NOT NULL,
  `PH_NO` varchar(14) NOT NULL,
  `Email` varchar(25) NOT NULL,
  PRIMARY KEY (`PRN`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `PH_NO_UNIQUE` (`PH_NO`),
  UNIQUE KEY `PRN_UNIQUE` (`PRN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (212142,'Deepak Pande','AIML','7210748901','deep@gmail.com'),(212153,'Pooja Dange','AIML','7658900985','poo@gmail.com'),(212166,'Shruti Shinde','AIML','9721070177','shruti@gmail.com'),(212182,'Anuja Shinde','Aiml','9893847563','anuja@gmail.com'),(212241,'Aarti Varma','CSE','8272070122','aarti@gmail.com'),(212271,'Rushi Jagtap','CSE','8275099733','rush@gmail.com'),(212301,'Sahil Rathod','CIVIL','9763856599','sahil@gmail.com'),(212318,'Neha Sharma','CIVIL','9543675098','neha@gmail.com'),(212420,'Sakshi Tilkari','ENTC','8763787900','sak@gmail.com'),(212450,'Tanvi Raje','ENTC','8976864570','tanu@gmail.com'),(212561,'Shravani Sathe','MECH','7057059752','shr@gmail.com');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'newdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-08 15:45:30
