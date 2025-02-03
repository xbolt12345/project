-- Create database
CREATE DATABASE IF NOT EXISTS inventory_system;

-- Use the created database
USE inventory_system;

-- Create inventory table
CREATE TABLE `inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(300) NOT NULL,
  `stock` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ;

-- Create transaction table
CREATE TABLE `transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(300) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` varchar(30) NOT NULL,
  `date` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
);

-- Insert data into inventory table
INSERT INTO `inventory` (`id`, `name`, `stock`, `price`) VALUES
(1, 'Milkybar', 500, 10),
(2, 'Cadbury Dairy Milk', 400, 10),
(3, 'Nestle KitKat', 450, 20),
(4, 'Mars', 700, 40),
(5, 'Galaxy', 650, 30);
