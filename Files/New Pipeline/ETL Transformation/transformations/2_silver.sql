CREATE OR REFRESH STREAMING TABLE orders_cleaned (
    CONSTRAINT positive_quantity EXPECT (quantity > 0) ON VIOLATION DROP ROW,
    CONSTRAINT valid_customer EXPECT (customer_first_name IS NOT NULL AND customer_last_name IS NOT NULL) ON VIOLATION FAIL UPDATE,
    CONSTRAINT recent_order EXPECT (purchased_at >= "2026-01-01")
)
COMMENT "The cleaned books orders with custom-renamed columns and constraints"
AS
SELECT 
    order_id AS order_reference_id, 
    quantity, 
    total,
    o.customer_id, 
    c.profile.first_name AS customer_first_name, 
    c.profile.last_name AS customer_last_name,
    cast(timestamp AS timestamp) AS purchased_at, 
    o.books,
    c.profile.address.country AS shipping_country
FROM STREAM(bronze_orders) o
LEFT JOIN customers c
ON o.customer_id = c.customer_id;