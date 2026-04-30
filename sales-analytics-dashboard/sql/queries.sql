/* Total ventes */
SELECT SUM(sales) AS total_sales
FROM sales;

/* Total Profit */
SELECT SUM(profit) AS total_profit
FROM  sales;

/* Top 10 des produits les plus vendu*/
SELECT product_name, SUM(sales) AS total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

/* Vente par region */
SELECT region, SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

/* ventes par mois */
SELECT month, SUM(SAELS) AS total_sales
FROM sales
GROUP BY month
ORDER BY month DESC;

/* Profit par categorie */
SELECT category, SUM(profit) AS total_profit
FROM sales
GROUP BY category
ORDER BY total_profit DESC;

/* Produit en perte */
SELECT product_name, SUM(profit) AS total_profit
FROM sales
GROUP BY product_name 
HAVING total_profit < 0
ORDER BY total_profit ASC;

/* top 10 meilleurs clients */
SELECT customer_name, SUM(sales) AS total_sales
FROM sales
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;