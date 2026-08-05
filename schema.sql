-- Petroleum Expense Management System - Database Schema

CREATE DATABASE IF NOT EXISTS petrol_expense;
USE petrol_expense;

-- Stores registered users
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Stores fuel expense records
CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    litres FLOAT NOT NULL,
    price_per_litre FLOAT NOT NULL,
    amount FLOAT NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (username) REFERENCES users(username)
);
