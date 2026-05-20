-- =====================================
-- BASIC KPI
-- =====================================

-- Total revenue
SELECT SUM(revenue) AS total_revenue FROM sales;

-- Total orders
SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales;

-- Average order value
SELECT SUM(revenue) / COUNT(DISTINCT order_id) AS avg_order_value FROM sales;


-- =====================================
-- TIME ANALYSIS
-- =====================================

-- Revenue by month
SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(revenue) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- Growth month over month
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month) AS previous_month,
       revenue - LAG(revenue) OVER (ORDER BY month) AS growth
FROM (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY month
) t;


-- =====================================
-- PRODUCT ANALYSIS
-- =====================================

-- Top 10 products
SELECT product,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 10;

-- Revenue by category
SELECT category,
       SUM(revenue) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;


-- =====================================
-- CUSTOMER ANALYSIS
-- =====================================

-- Top customers
SELECT customer_id,
       SUM(revenue) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- Number of customers
SELECT COUNT(DISTINCT customer_id) FROM sales;


-- =====================================
-- GEOGRAPHICAL ANALYSIS
-- =====================================

-- Revenue by country
SELECT country,
       SUM(revenue) AS revenue
FROM sales
GROUP BY country
ORDER BY revenue DESC;


-- =====================================
-- ADVANCED (TRÈS IMPORTANT 💼)
-- =====================================

-- Ranking products
SELECT product,
       SUM(revenue) AS revenue,
       RANK() OVER (ORDER BY SUM(revenue) DESC) AS rank
FROM sales
GROUP BY product;

-- Running total revenue
SELECT order_date,
       SUM(revenue) OVER (ORDER BY order_date) AS cumulative_revenue
FROM sales;