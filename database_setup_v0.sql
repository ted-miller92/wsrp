DROP DATABASE IF EXISTS `banking_db_v0`;
CREATE DATABASE IF NOT EXISTS `banking_db_v0`;

USE `banking_db_v0`;

-- Create a user for the server
CREATE USER IF NOT EXISTS 'server_user'@'localhost' IDENTIFIED BY 'server_password';
GRANT ALL PRIVILEGES ON `banking_db_v0`.* TO 'server_user'@'localhost';

CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_type` ENUM('CUSTOMER', 'EMPLOYEE') NOT NULL,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE
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

-- Insert sample data
INSERT INTO `users` (`user_type`, `username`, `first_name`, `last_name`, `email`) VALUES 
    ('EMPLOYEE', 'rwilson', 'Robert', 'Wilson', 'robert.wilson@bank.com'),
    ('EMPLOYEE', 'lchen', 'Lisa', 'Chen', 'lisa.chen@bank.com'),
    ('EMPLOYEE', 'dthomas', 'David', 'Thomas', 'david.thomas@bank.com'),
    ('CUSTOMER', 'jsmith', 'John', 'Smith', 'john.smith@gmail.com'),
    ('CUSTOMER', 'sjohnson', 'Sarah', 'Johnson', 'sarah.johnson@hotmail.com'),
    ('CUSTOMER', 'mbrown', 'Michael', 'Brown', 'michael.brown@yahoo.com');


INSERT INTO `accounts` (`account_number`, `account_type`, `account_balance`, `account_interest_rate`) VALUES 
    ('1001-2345', 'CHECKING', 5000.00, 0.0005),
    ('1001-2346', 'SAVINGS', 10000.00, 0.0015),
    ('1001-2347', 'INVESTMENT', 25000.00, 0.0025);

-- Link users to accounts (many-to-many)
INSERT INTO `user_accounts` (`user_id`, `account_id`, `access_level`) VALUES 
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 3);

-- Sample transactions
-- INSERT INTO `transactions` (`account_id`, `transaction_type`, `amount`, `description`) VALUES 
--     (1, 'DEPOSIT', 1000.00, 'Initial deposit'),
--     (1, 'WITHDRAWAL', 200.00, 'ATM withdrawal'),
--     (2, 'TRANSFER', 500.00, 'Transfer to checking'),
--     (3, 'DEPOSIT', 5000.00, 'Investment contribution');

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
