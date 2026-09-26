from pyspark import pipelines as dp
from pyspark.sql import functions as F

dataset_path = spark.conf.get("dataset_path")

@dp.table(
    name = "orders_raw",
    comment = "The raw books orders, ingested from orders_raw"
)
def process_orders():
    orders_df = (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .load(f"{dataset_path}/orders_raw")
    )
    return orders_df

@dp.materialized_view(
    name = "customers",
    comment = "The customers lookup table, ingested from customers_raw"
)
def customers():
    customers_df = spark.read.json(f"{dataset_path}/customers_raw")
    return customers_df