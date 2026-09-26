from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(
    name="orders_cleaned",
    comment="The cleaned books orders with custom-renamed columns and constraints"
)
@dp.expect_or_drop(
    "positive_quantity",
    "quantity > 0"
)
@dp.expect_or_fail(
    "valid_customer",
    "customer_first_name IS NOT NULL AND customer_last_name IS NOT NULL"
)
@dp.expect(
    "recent_order",
    "purchased_at >= TIMESTAMP '2026-01-01 00:00:00'"
)
def orders_cleaned():

    orders_df = spark.readStream.table("orders_raw")
    customers_df = spark.read.table("customers")

    return (
        orders_df
        .join(
            customers_df,
            "customer_id",
            "left"
        )
        .withColumn(
            "purchased_at",
            F.to_timestamp(F.col("timestamp"))
        )
        .withColumn(
            "customer_first_name",
            F.col("profile.first_name")
        )
        .withColumn(
            "customer_last_name",
            F.col("profile.last_name")
        )
        .withColumn(
            "shipping_country",
            F.col("profile.address.country")
        )
        .select(
            F.col("order_id").alias("order_reference_id"),
            "quantity",
            "total",
            "customer_id",
            "purchased_at",
            "customer_first_name",
            "customer_last_name",
            "books",
            "shipping_country"
        )
    )