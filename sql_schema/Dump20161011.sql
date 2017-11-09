CREATE DATABASE  IF NOT EXISTS `stormTest` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `stormTest`;
-- MySQL dump 10.13  Distrib 5.7.15, for Linux (x86_64)
--
-- Host: localhost    Database: stormTest
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.17-MariaDB

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
-- Table structure for table `episode_details`
--

DROP TABLE IF EXISTS `episode_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `episode_details` (
  `episode_id` int(11) NOT NULL,
  `episode_narrative` text,
  PRIMARY KEY (`episode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_details`
--

DROP TABLE IF EXISTS `event_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_details` (
  `event_id` int(11) NOT NULL,
  `event_narrative` text,
  `month_name` varchar(20) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `begin_date_time` datetime DEFAULT NULL,
  `end_date_time` datetime DEFAULT NULL,
  `state_fips` int(11) DEFAULT NULL,
  `cz_fips` int(11) DEFAULT NULL,
  `cz_type` varchar(20) DEFAULT NULL,
  `cz_name` varchar(45) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `wfo` varchar(45) DEFAULT NULL,
  `cz_timezone` varchar(45) DEFAULT NULL,
  `injuries_direct` int(11) DEFAULT NULL,
  `injuries_indirect` int(11) DEFAULT NULL,
  `deaths_direct` int(11) DEFAULT NULL,
  `deaths_indirect` int(11) DEFAULT NULL,
  `event_type` varchar(45) DEFAULT NULL,
  `magnitude` float DEFAULT NULL,
  `magnitude_type` varchar(20) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `tor_f_scale` varchar(20) DEFAULT NULL,
  `tor_length` float DEFAULT NULL,
  `tor_width` float DEFAULT NULL,
  `tor_other_wfo` varchar(45) DEFAULT NULL,
  `tor_other_cz_state` varchar(20) DEFAULT NULL,
  `tor_other_cz_fips` int(11) DEFAULT NULL,
  `tor_other_cz_name` varchar(45) DEFAULT NULL,
  `damage_property` int(11) DEFAULT NULL,
  `damage_crops` int(11) DEFAULT NULL,
  `flood_cause` varchar(45) DEFAULT NULL,
  `event_detailscol` varchar(45) DEFAULT NULL,
  `begin_range` varchar(45) DEFAULT NULL,
  `begin_azimuth` float DEFAULT NULL,
  `begin_location` varchar(45) DEFAULT NULL,
  `end_range` varchar(45) DEFAULT NULL,
  `end_azimuth` float DEFAULT NULL,
  `end_location` varchar(45) DEFAULT NULL,
  `begin_latitute` decimal(10,8) DEFAULT NULL,
  `begin_longitude` decimal(11,8) DEFAULT NULL,
  `end_lattitude` decimal(10,8) DEFAULT NULL,
  `end_longitude` decimal(11,8) DEFAULT NULL,
  `data_source` text,
  `episode_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `fk_episode_idx` (`episode_id`),
  CONSTRAINT `fk_episode` FOREIGN KEY (`episode_id`) REFERENCES `episode_details` (`episode_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fatalities`
--

DROP TABLE IF EXISTS `fatalities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fatalities` (
  `fatality_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `fatality_type` varchar(20) DEFAULT NULL,
  `fatality_date` datetime DEFAULT NULL,
  `fatality_age` int(11) DEFAULT NULL,
  `fatality_sex` varchar(20) DEFAULT NULL,
  `fatality_location` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`fatality_id`,`event_id`),
  KEY `fk_fatality_event_idx` (`event_id`),
  CONSTRAINT `fk_fatality_event` FOREIGN KEY (`event_id`) REFERENCES `event_details` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `episode_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `location_index` int(11) NOT NULL,
  `range` float DEFAULT NULL,
  `azimuth` varchar(20) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `latitudeTwo` float DEFAULT NULL,
  `longitudeTwo` float DEFAULT NULL,
  `location_pk` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`location_pk`),
  KEY `fk_location_event_idx` (`event_id`),
  KEY `fk_episode_idx` (`episode_id`),
  CONSTRAINT `fk_event` FOREIGN KEY (`event_id`) REFERENCES `event_details` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=664063 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-11 14:46:30
