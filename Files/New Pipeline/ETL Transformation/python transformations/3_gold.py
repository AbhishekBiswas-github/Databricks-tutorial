from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view(
    name = "usa_daily_customer_books",
    comment = "Daily number of books purchased per customer in the USA"
)
def usa_daily_customer_books():
    return (
        spark.read.table("orders_cleaned")
        .filter(F.col("shipping_country") == "USA")
        .groupBy(
            "customer_id",
            "customer_first_name",
            "customer_last_name",
            F.date_trunc("DD", F.col("purchased_at")).alias("order_date")
        )
        .agg(
            F.sum("quantity").alias("books_counts")
        )
    )