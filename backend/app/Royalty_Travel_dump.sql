-- MySQL dump Distrib 8.4
--
-- Host: localhost   Database: royalty-travel_db
-------------------------------------------------
-- Server Version 8.4

-- Optionally, set back the settings to previous values
/*!80101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!80101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!80101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!80103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!80014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=1 */;
/*!80014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=1 */;
/*!80101 SET @OLD_SQL_MODE=@@SQL_MODE */;
/*!80111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=1 */;


-- Drop the existing database if it exists
DROP DATABASE IF EXISTS royalty_travel_db;

-- Create a new database
CREATE DATABASE IF NOT EXISTS royalty_travel_db;

-- Create a new user if it doesn't exist and grant all permissions
CREATE USER IF NOT EXISTS 'royalty_user'@'localhost' IDENTIFIED BY 'royalty_pw';
GRANT ALL ON royalty_travel_db.* TO 'royalty_user'@'localhost';
FLUSH PRIVILEGES;

-- Switch to the new database
USE royalty_travel_db;

-- Table structure for table `bookings`
DROP TABLE IF EXISTS `bookings`;
CREATE TABLE `bookings` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `passenger_name` varchar(128) NOT NULL,
  `departure_place` varchar(128) NOT NULL,
  `destination` varchar(128) NOT NULL,
  `travel_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table `bookings`
LOCK TABLES `bookings` WRITE;
INSERT INTO `bookings` VALUES 
('1','2024-07-09 10:00:00','2024-07-09 10:00:00','John Doe','New York','Los Angeles','2024-08-01 09:00:00'),
('2','2024-07-09 10:05:00','2024-07-09 10:05:00','Jane Smith','San Francisco','Las Vegas','2024-08-05 15:00:00');
UNLOCK TABLES;

