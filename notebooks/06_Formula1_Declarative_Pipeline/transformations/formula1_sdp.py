from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.table(
    name="bronze_sprint_qualifying_results_cdc",
    comment="Raw sprint qualifying results incrementally ingested from cloud object storage"
)
def bronze_sprint_qualifying_results_cdc():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("header", "true")
        .load("/Volumes/main/default/streaming_formula1/")
    )

@dp.view(
    name="bronze_sprint_qualifying_results_cdc_clean",
    comment="Cleansed CDC data for sprint qualifying results"
)
@dp.expect_or_drop("no_rescued_data", "_rescued_data IS NULL")
@dp.expect_or_drop("valid_track", "Track IS NOT NULL")
@dp.expect_or_drop("valid_driver", "Driver IS NOT NULL")
def bronze_sprint_qualifying_results_cdc_clean():
    return spark.readStream.table("bronze_sprint_qualifying_results_cdc")

dp.create_streaming_table(
    name="bronze_sprint_qualifying_results"
)

dp.create_auto_cdc_flow(
    target="bronze_sprint_qualifying_results",
    source="bronze_sprint_qualifying_results_cdc_clean",
    keys=["Track", "Driver"],
    sequence_by=col("Q1")
)