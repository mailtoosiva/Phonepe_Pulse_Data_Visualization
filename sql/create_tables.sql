-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS phonepe_pulse_db;

-- Use the database
USE phonepe_pulse_db;

-- Drop tables if they already exist (for clean re-runs during development)
DROP TABLE IF EXISTS aggregated_transactions;
DROP TABLE IF EXISTS aggregated_users;
DROP TABLE IF EXISTS map_transactions;
DROP TABLE IF EXISTS map_users;
DROP TABLE IF EXISTS top_transactions_state;
DROP TABLE IF EXISTS top_transactions_district;
DROP TABLE IF EXISTS top_transactions_pincode;
DROP TABLE IF EXISTS top_users_state;
DROP TABLE IF EXISTS top_users_district;
DROP TABLE IF EXISTS top_users_pincode;

-- Table for aggregated transactions
CREATE TABLE aggregated_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    transaction_type VARCHAR(255) NOT NULL,
    transaction_count BIGINT NOT NULL,
    transaction_amount DECIMAL(18, 2) NOT NULL
);

-- Table for aggregated users
CREATE TABLE aggregated_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    brand VARCHAR(255), -- NULLABLE as some users might not have brand info
    registered_users BIGINT NOT NULL,
    app_openings BIGINT NOT NULL
);

-- Table for map transactions (state/district level)
CREATE TABLE map_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    district VARCHAR(255) NOT NULL,
    transaction_count BIGINT NOT NULL,
    transaction_amount DECIMAL(18, 2) NOT NULL
);

-- Table for map users (state/district level)
CREATE TABLE map_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    district VARCHAR(255) NOT NULL,
    registered_users BIGINT NOT NULL,
    app_openings BIGINT NOT NULL
);

-- Table for top transactions by state (pincode level data)
CREATE TABLE top_transactions_state (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    pincode INT NOT NULL,
    transaction_count BIGINT NOT NULL,
    transaction_amount DECIMAL(18, 2) NOT NULL
);

-- Table for top transactions by district (usually 'top_transactions_state' has pincode directly for map_transactions, let's keep consistent)
-- PhonePe data has top transactions per state, broken down by pincode. No separate "top_transactions_district" by district directly.
-- If needed, this table structure can be adapted or derived from 'map_transactions' for top districts
CREATE TABLE top_transactions_district (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    district VARCHAR(255) NOT NULL,
    transaction_count BIGINT NOT NULL,
    transaction_amount DECIMAL(18, 2) NOT NULL
);

-- Table for top transactions by pincode
CREATE TABLE top_transactions_pincode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    pincode INT NOT NULL,
    transaction_count BIGINT NOT NULL,
    transaction_amount DECIMAL(18, 2) NOT NULL
);

-- Table for top users by state (pincode level data)
CREATE TABLE top_users_state (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    pincode INT NOT NULL,
    registered_users BIGINT NOT NULL
);

-- Table for top users by district
-- Similar to top_transactions_district, PhonePe data primarily has top users by state (pincode).
CREATE TABLE top_users_district (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    district VARCHAR(255) NOT NULL,
    registered_users BIGINT NOT NULL
);

-- Table for top users by pincode
CREATE TABLE top_users_pincode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT   NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    pincode INT NOT NULL,
    registered_users BIGINT NOT NULL
);