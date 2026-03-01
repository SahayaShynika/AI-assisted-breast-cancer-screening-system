-- Breast Cancer Detection Database Setup
-- MySQL Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS breast_cancer_db;
USE breast_cancer_db;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    user_type ENUM('doctor', 'patient') NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_type (user_type)
);

-- Predictions table to store scan results
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(200) NOT NULL,
    prediction_result ENUM('normal', 'benign', 'malignant') NOT NULL,
    confidence_score FLOAT NOT NULL,
    cancer_stage VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_result (prediction_result),
    INDEX idx_created_at (created_at)
);

-- Insert sample data (optional)
-- Sample Doctor
INSERT INTO users (email, password, user_type, name, phone_number) VALUES 
('doctor@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'doctor', 'Dr. Sarah Johnson', '+1234567890');

-- Sample Patient
INSERT INTO users (email, password, user_type, name, phone_number) VALUES 
('patient@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'patient', 'Emily Smith', '+0987654321');

-- Sample Prediction
INSERT INTO predictions (user_id, image_path, prediction_result, confidence_score, cancer_stage) VALUES 
(2, 'sample_mammogram.jpg', 'normal', 0.95, 'No Cancer');

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON breast_cancer_db.* TO 'your_username'@'localhost';
-- FLUSH PRIVILEGES;
