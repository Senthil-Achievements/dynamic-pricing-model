-- Create Database
CREATE DATABASE IF NOT EXISTS smart_price_db;
USE smart_price_db;

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    barcode VARCHAR(50) NOT NULL,
    mrp DECIMAL(10, 2) NOT NULL,
    manufacture_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    discount_percentage DECIMAL(5, 2) DEFAULT 0.00,
    store_name VARCHAR(100) NOT NULL,
    index (barcode)
);

-- Insert Sample Data
INSERT INTO products (product_name, barcode, mrp, manufacture_date, expiry_date, discount_percentage, store_name) VALUES
('Maggi Noodles 2-Pack', '8901058000161', 28.00, '2025-01-01', '2026-06-30', 5.0, 'Reliance Fresh'),
('Maggi Noodles 2-Pack', '8901058000161', 28.00, '2025-01-01', '2026-06-30', 2.0, 'Big Bazaar'),
('Maggi Noodles 2-Pack', '8901058000161', 28.00, '2025-01-01', '2026-06-30', 7.0, 'DMart'),
('Amul Butter 100g', '8901262010018', 56.00, '2026-02-01', '2026-02-10', 10.0, 'Reliance Fresh'),
('Amul Butter 100g', '8901262010018', 56.00, '2026-02-01', '2026-02-09', 15.0, 'Big Bazaar'),
('Milk 500ml', '1234567890123', 30.00, '2026-02-05', '2026-02-08', 0.0, 'Local Dairy'),
('Expired Bread', '9876543210987', 40.00, '2025-12-01', '2025-12-05', 50.0, 'Corner Store'),
('Lays Chips', '8901491101831', 20.00, '2025-11-01', '2026-05-01', 0.0, 'Reliance Fresh');
