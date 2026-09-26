CREATE OR REFRESH MATERIALIZED VIEW usa_daily_customer_books
COMMENT "Daily number of books purchased per customer in the USA"
AS 
SELECT 
    customer_id, 
    customer_first_name, 
    customer_last_name, 
    date_trunc("DD", purchased_at) AS order_date, 
    sum(quantity) AS books_counts
FROM orders_cleaned
WHERE shipping_country = "USA"
GROUP BY 
    customer_id, 
    customer_first_name, 
    customer_last_name, 
    date_trunc("DD", purchased_at);