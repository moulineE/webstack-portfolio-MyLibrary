-- prepares a MySQL server for the project

SET @dbname = 'MyLibrary_webstack_dev_db';
SET @username = 'MyLibrary_dev';
SET @password = 'MyLibrary_dev_pwd';

SET @create_database = CONCAT('CREATE DATABASE IF NOT EXISTS ', @dbname);
PREPARE stmt FROM @create_database;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @create_user = CONCAT("CREATE USER IF NOT EXISTS '", @username, "'@'localhost' IDENTIFIED BY '", @password, "'");
PREPARE stmt FROM @create_user;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @grant_privileges = CONCAT("GRANT ALL PRIVILEGES ON `", @dbname, "`.* TO '", @username, "'@'localhost'");
PREPARE stmt FROM @grant_privileges;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @grant_select = CONCAT("GRANT SELECT ON `performance_schema`.* TO '", @username, "'@'localhost'");
PREPARE stmt FROM @grant_select;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

FLUSH PRIVILEGES;