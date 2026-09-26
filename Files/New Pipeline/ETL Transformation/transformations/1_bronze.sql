CREATE OR REFRESH STREAMING TABLE bronze_orders
COMMENT "The raw orders, ingested incrementally from orders volume path"
AS SELECT * FROM STREAM read_files(
    "${dataset_path}/orders_raw",
    format => "json",
    inferColumnTypes => true
);


CREATE OR REFRESH MATERIALIZED VIEW customers
COMMENT "The customers lookup table, ingested from ecommerce volume"
AS SELECT * FROM read_files(
    "${dataset_path}/customers_raw", 
    format => "json",
    inferColumnTypes => true
);