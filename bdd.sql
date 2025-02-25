DROP DATABASE IF EXISTS Calculs;

CREATE DATABASE Calculs;

USE Calculs;

CREATE TABLE formules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    formula TEXT NOT NULL
);

CREATE TABLE variables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
