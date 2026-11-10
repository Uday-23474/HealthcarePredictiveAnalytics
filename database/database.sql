-- ============================================
-- Healthcare Predictive Analytics Database
-- ============================================

CREATE DATABASE IF NOT EXISTS healthcare_predictive_analytics;

USE healthcare_predictive_analytics;


-- ============================================
-- 1. Patients Table
-- ============================================

CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    sex VARCHAR(20) NOT NULL,
    chest_pain_type VARCHAR(50) NOT NULL,
    resting_blood_pressure INT NOT NULL,
    cholestoral INT NOT NULL,
    fasting_blood_sugar VARCHAR(50) NOT NULL,
    rest_ecg VARCHAR(50) NOT NULL,
    max_heart_rate INT NOT NULL,
    exercise_induced_angina VARCHAR(10) NOT NULL,
    oldpeak DECIMAL(5,2) NOT NULL,
    slope VARCHAR(30) NOT NULL,
    vessels_colored_by_flourosopy VARCHAR(20) NOT NULL,
    thalassemia VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- 2. Predictions Table
-- ============================================

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    prediction_result VARCHAR(50) NOT NULL,
    probability DECIMAL(6,2) NOT NULL,
    risk_level VARCHAR(30) NOT NULL,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);