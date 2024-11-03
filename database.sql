-- Create the database
CREATE DATABASE IF NOT EXISTS organic_traceability;
USE organic_traceability;

-- User table to store farmer and customer information
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type ENUM('Farmer', 'Customer') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table to store details of vegetables added by farmers
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Optional table for tracking customer purchases
CREATE TABLE purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Insert sample data (optional)
INSERT INTO users (full_name, email, password_hash, user_type)
VALUES
    ('Alice Farmer', 'alice@farm.com', 'hashed_password_1', 'Farmer'),
    ('Bob Customer', 'bob@shop.com', 'hashed_password_2', 'Customer');
    
INSERT INTO products (farmer_id, product_name, description)
VALUES
    (1, 'Organic Carrots', 'Freshly harvested organic carrots'),
    (1, 'Organic Lettuce', 'Crisp and fresh organic lettuce');

