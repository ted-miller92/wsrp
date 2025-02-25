DROP DATABASE IF EXISTS `banking_db_v0`;
CREATE DATABASE IF NOT EXISTS `banking_db_v0`;

USE `banking_db_v0`;

-- Create a user for the server
CREATE USER IF NOT EXISTS 'server_user'@'localhost' IDENTIFIED BY 'server_password';
GRANT ALL PRIVILEGES ON `banking_db_v0`.* TO 'server_user'@'localhost';


-- adjusted for 2 new columns for hashed passwords (weak and strong)
-- CRC32 hash (8 characters)
-- bcrypt hash (60 characters)
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_type` ENUM('CUSTOMER', 'EMPLOYEE') NOT NULL,
    `user_name` VARCHAR(50) NOT NULL UNIQUE,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `weak_password` CHAR(8),
    `strong_password` CHAR(60)
);

CREATE TABLE IF NOT EXISTS `accounts` (
    `account_id` INT AUTO_INCREMENT PRIMARY KEY,
    `account_number` VARCHAR(20) NOT NULL UNIQUE,
    `account_type` ENUM('CHECKING', 'SAVINGS', 'INVESTMENT') NOT NULL,
    `account_balance` DECIMAL(15,2) DEFAULT 0.00,
    `account_interest_rate` DECIMAL(5,4) DEFAULT 0.00
);

-- Intersection table for many-to-many relationship
CREATE TABLE IF NOT EXISTS `user_accounts` (
    `user_id` INT NOT NULL,
    `account_id` INT NOT NULL,
    PRIMARY KEY (`user_id`, `account_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`),
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`)
);

CREATE TABLE IF NOT EXISTS `transactions` (
    `transaction_id` INT AUTO_INCREMENT PRIMARY KEY,
    `account_id` INT NOT NULL,
    `transaction_type` ENUM('DEPOSIT', 'WITHDRAWAL', 'TRANSFER') NOT NULL,
    `transaction_amount` DECIMAL(15,2) NOT NULL,
    `transaction_description` VARCHAR(255),
    `transaction_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`account_id`) REFERENCES `accounts`(`account_id`)
);

-- Adjusted for new password hashing
INSERT INTO `users` 
(`user_type`, `user_name`, `first_name`, `last_name`, `email`, `weak_password`, `strong_password`) 
VALUES
('EMPLOYEE', 'rwilson', 'Robert', 'Wilson', 'robert.wilson@bank.com', 
 '7d79033c', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewF3LQMUZHFPCCui'),
('EMPLOYEE', 'lchen', 'Lisa', 'Chen', 'lisa.chen@bank.com', 
 '89a69b6f', '$2b$12$FdTLGHM9TpxqQqwvkJHiU.6GRjpxh7GZxwqKV/D8sM6pYVHHAjmOq'),
('EMPLOYEE', 'dthomas', 'David', 'Thomas', 'david.thomas@bank.com', 
 '11a81e67', '$2b$12$QG3wXNH8f4gZCVvz8wGU4.Sx6Yx4TzDYLGz3HyWh1jFA/NK3Kk3sq'),
('CUSTOMER', 'jsmith', 'John', 'Smith', 'john.smith@gmail.com', 
 '98b4f4b2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewF3LQMUZHFPCCui'),
('CUSTOMER', 'sjohnson', 'Sarah', 'Johnson', 'sarah.johnson@hotmail.com', 
 '734f98e1', '$2b$12$QG3wXNH8f4gZCVvz8wGU4.Sx6Yx4TzDYLGz3HyWh1jFA/NK3Kk3sq'),
('CUSTOMER', 'mbrown', 'Michael', 'Brown', 'michael.brown@yahoo.com', 
 '45aa23e9', '$2b$12$FdTLGHM9TpxqQqwvkJHiU.6GRjpxh7GZxwqKV/D8sM6pYVHHAjmOq');


INSERT INTO `accounts` (`account_number`, `account_type`, `account_balance`, `account_interest_rate`) VALUES 
    ('1001-2345', 'CHECKING', 5000.00, 0.0005),
    ('1001-2346', 'SAVINGS', 10000.00, 0.0015),
    ('1001-2347', 'INVESTMENT', 25000.00, 0.0025);

-- Link users to accounts (many-to-many)
INSERT INTO `user_accounts` (`user_id`, `account_id`) VALUES 
    (4, 1),
    (4, 2),
    (5, 2),
    (6, 3);

INSERT INTO `transactions` (`account_id`, `transaction_type`, `transaction_amount`, `transaction_description`) VALUES 
    (1, 'DEPOSIT', 1000.00, 'Initial deposit'),
    (1, 'WITHDRAWAL', 200.00, 'ATM withdrawal'),
    (2, 'TRANSFER', 500.00, 'Transfer to checking'),
    (3, 'DEPOSIT', 5000.00, 'Investment contribution');

-- Select statements to verify data
-- SELECT * FROM `users`;
-- SELECT * FROM `accounts`;
-- SELECT * FROM `user_accounts`;
-- SELECT * FROM `transactions`;   

-- Example join to see all accounts for a specific user
-- SELECT 
--     u.first_name,
--     u.last_name,
--     a.account_number,
--     a.account_type
-- FROM users u
-- JOIN user_accounts ua ON u.user_id = ua.user_id
-- JOIN accounts a ON ua.account_id = a.account_id;
