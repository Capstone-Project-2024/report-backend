/*The following script can be run in MySQL Workbench or DBeaver on your
local machine to create the database schema for our project.*/

CREATE DATABASE IF NOT EXISTS datadive;

USE datadive;

CREATE TABLE IF NOT EXISTS users (
    user_id int AUTO_INCREMENT,
    user_name varchar(255) NOT NULL,
    user_password varchar(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS calls (
    call_id int AUTO_INCREMENT,
    user_id int,
    api_url varchar(255) NOT NULL,
    PRIMARY KEY (call_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
