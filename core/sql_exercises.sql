-- core/sql_exercises.sql

-- 1. Tables Creation
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    unit_price REAL
);

-- 2. Mock Data Insertion (Includes intentional data bugs for validation)
INSERT INTO customers (customer_id, name, email) VALUES
(1, 'Ali Khan', 'ali@example.com'),
(2, 'Sara Ahmed', 'sara@example.com'),
(3, 'Usman Tariq', 'ali@example.com'), -- Duplicate Email Intentional
(4, 'Zainab Bibi', NULL);              -- NULL Email

INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES
(101, 1, '2026-10-01', 150.0), -- Mismatch total (Items = 200.0)
(102, 2, '2026-10-02', 50.0),  -- Correct total
(103, 99, '2026-10-03', 75.0); -- Orphan Order (Customer 99 missing)

INSERT INTO order_items (item_id, order_id, product_name, quantity, unit_price) VALUES
(1, 101, 'Mouse', 2, 25.0),
(2, 101, 'Keyboard', 1, 150.0), -- Total item price = 200.0
(3, 102, 'USB Cable', 5, 10.0),  -- Total item price = 50.0
(4, 999, 'Headphones', 1, 75.0); -- Orphan Item (Order 999 missing)