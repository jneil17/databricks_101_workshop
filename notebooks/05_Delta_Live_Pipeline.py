# Databricks notebook source
# MAGIC %md
# MAGIC # 🔄 Delta Live Tables: Managed ETL Pipeline
# MAGIC *Build declarative, production-ready data pipelines in 5 minutes*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you'll understand:
# MAGIC - ✅ **Delta Live Tables (DLT) fundamentals** and decorators
# MAGIC - ✅ **Data quality expectations** with built-in monitoring
# MAGIC - ✅ **Managed pipeline execution** and dependency management
# MAGIC - ✅ **DLT vs Jobs comparison** and when to use each
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🏗️ What We'll Build
# MAGIC
# MAGIC **Managed F1 Data Pipeline with DLT:**
# MAGIC ```
# MAGIC 📁 Volume Files           🥉 DLT Bronze              🥈 DLT Silver              🥇 DLT Gold
# MAGIC ┌─────────────────┐      ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
# MAGIC │ drivers.csv     │  →   │ dlt_bronze_     │   →   │ dlt_silver_     │   →   │ dlt_gold_driver_│
# MAGIC │ results.csv     │      │ drivers         │       │ drivers_clean   │       │ stats           │
# MAGIC └─────────────────┘      │ dlt_bronze_     │       │ dlt_silver_     │       │ dlt_gold_top_   │
# MAGIC                          │ results         │       │ results_clean   │       │ performers      │
# MAGIC                          └─────────────────┘       └─────────────────┘       └─────────────────┘
# MAGIC ```
# MAGIC
# MAGIC **🔥 Key Features:**
# MAGIC - ⚡ **Declarative syntax** - focus on what, not how
# MAGIC - 🎯 **Data quality expectations** - automatic monitoring
# MAGIC - 🔄 **Automatic dependency management** - smart execution order
# MAGIC - 📊 **Built-in monitoring** - pipeline health and lineage

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Delta Live Tables Overview
# MAGIC
# MAGIC **Delta Live Tables (DLT)** is Databricks' framework for building reliable, maintainable, and testable data processing pipelines.
# MAGIC
# MAGIC ### 🌟 Key Benefits:
# MAGIC
# MAGIC #### 🎯 **Declarative Development**
# MAGIC - Write **what** you want, not **how** to compute it
# MAGIC - Automatic dependency resolution and execution order
# MAGIC - Focus on business logic, not infrastructure
# MAGIC
# MAGIC #### 🔍 **Built-in Data Quality**
# MAGIC - **Expectations** define data quality rules
# MAGIC - **Quarantine** bad data instead of failing pipelines  
# MAGIC - **Monitoring** with automatic quality metrics
# MAGIC
# MAGIC #### ⚡ **Managed Operations**
# MAGIC - **Auto-scaling** compute based on workload
# MAGIC - **Error recovery** and automatic retries
# MAGIC - **Incremental processing** for efficiency
# MAGIC
# MAGIC #### 📊 **Observability**
# MAGIC - **Lineage tracking** shows data flow
# MAGIC - **Performance metrics** and optimization suggestions
# MAGIC - **Data freshness** monitoring

# COMMAND ----------

import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥉 Bronze Layer: Raw Data Ingestion
# MAGIC
# MAGIC Bronze tables in DLT ingest raw data with minimal transformation.

# COMMAND ----------

@dlt.table(
    name="dlt_bronze_drivers",
    comment="DLT Bronze: Raw driver data from Volume CSV files",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def bronze_drivers():
    """
    Ingest raw driver data from Volume CSV files.
    DLT automatically handles schema inference and evolution.
    """
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", "/Volumes/main/default/f1_raw_data/dlt_schema/drivers/")
        .option("header", "true")
        .load("/Volumes/main/default/f1_raw_data/drivers.csv")
        .select(
            col("driverId").cast("int").alias("driver_id"),
            col("driverRef").alias("driver_ref"),
            col("number").alias("car_number"),
            col("code").alias("driver_code"),
            col("forename").alias("first_name"),
            col("surname").alias("last_name"),
            col("dob").alias("date_of_birth"),
            col("nationality"),
            col("url").alias("wiki_url"),
            current_timestamp().alias("ingested_at"),
            lit("dlt_bronze_pipeline").alias("ingestion_method")
        )
    )

# COMMAND ----------

@dlt.table(
    name="dlt_bronze_results",
    comment="DLT Bronze: Raw race results data from Volume CSV files",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def bronze_results():
    """
    Ingest raw race results data from Volume CSV files.
    Includes all original columns for complete data preservation.
    """
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", "/Volumes/main/default/f1_raw_data/dlt_schema/results/")
        .option("header", "true")
        .load("/Volumes/main/default/f1_raw_data/results.csv")
        .select(
            col("resultId").cast("int").alias("result_id"),
            col("raceId").cast("int").alias("race_id"),
            col("driverId").cast("int").alias("driver_id"),
            col("constructorId").cast("int").alias("constructor_id"),
            col("number").alias("car_number"),
            col("grid").cast("int").alias("grid_position"),
            col("position").alias("finish_position_text"),
            col("positionOrder").cast("int").alias("position_order"),
            col("points").cast("double").alias("points_scored"),
            col("laps").cast("int").alias("laps_completed"),
            col("time").alias("race_time"),
            col("milliseconds").alias("race_time_ms"),
            col("statusId").cast("int").alias("status_id"),
            current_timestamp().alias("ingested_at"),
            lit("dlt_bronze_pipeline").alias("ingestion_method")
        )
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥈 Silver Layer: Clean and Validated Data
# MAGIC
# MAGIC Silver tables implement data quality expectations and transformations.

# COMMAND ----------

@dlt.table(
    name="dlt_silver_drivers_clean",
    comment="DLT Silver: Cleaned and validated driver data with quality expectations"
)
@dlt.expect_or_drop("valid_driver_id", "driver_id IS NOT NULL")
@dlt.expect_or_drop("valid_names", "first_name IS NOT NULL AND last_name IS NOT NULL")
@dlt.expect("reasonable_birth_date", "date_of_birth >= '1900-01-01' AND date_of_birth <= current_date()")
def silver_drivers_clean():
    """
    Clean and validate driver data with data quality expectations.
    - Drop records with missing critical fields
    - Warn on suspicious birth dates
    - Enrich with calculated fields
    """
    return (
        dlt.read("dlt_bronze_drivers")
        .filter(col("driver_id").isNotNull())
        .select(
            col("driver_id"),
            col("driver_ref"),
            col("car_number"),
            col("driver_code"),
            col("first_name"),
            col("last_name"),
            concat(col("first_name"), lit(" "), col("last_name")).alias("full_name"),
            # Clean and convert date of birth
            when(col("date_of_birth") != "\\N", 
                 to_date(col("date_of_birth"), "yyyy-MM-dd")
            ).alias("birth_date"),
            col("nationality"),
            # Calculate current age
            when(col("date_of_birth") != "\\N",
                 floor(datediff(current_date(), to_date(col("date_of_birth"), "yyyy-MM-dd")) / 365)
            ).alias("current_age"),
            col("wiki_url"),
            col("ingested_at"),
            current_timestamp().alias("processed_at"),
            lit("silver_quality_processed").alias("processing_stage")
        )
    )

# COMMAND ----------

@dlt.table(
    name="dlt_silver_results_clean",
    comment="DLT Silver: Cleaned race results with data quality validations"
)
@dlt.expect_or_drop("valid_result_id", "result_id IS NOT NULL")
@dlt.expect_or_drop("valid_race_and_driver", "race_id IS NOT NULL AND driver_id IS NOT NULL")
@dlt.expect("valid_points", "points_scored >= 0")
@dlt.expect("reasonable_laps", "laps_completed >= 0 AND laps_completed <= 200")
def silver_results_clean():
    """
    Clean and validate race results with comprehensive quality checks.
    - Ensure critical IDs are present
    - Validate points and lap counts
    - Convert position data to proper types
    """
    return (
        dlt.read("dlt_bronze_results")
        .filter(col("result_id").isNotNull())
        .select(
            col("result_id"),
            col("race_id"),
            col("driver_id"),
            col("constructor_id"),
            col("car_number"),
            col("grid_position"),
            # Clean finish position - handle DNF, DNS, etc.
            when(col("finish_position_text").rlike("^[0-9]+$"), 
                 col("finish_position_text").cast("int")
            ).alias("finish_position"),
            col("finish_position_text"),
            col("position_order"),
            col("points_scored"),
            col("laps_completed"),
            col("race_time"),
            # Convert milliseconds if numeric
            when(col("race_time_ms").rlike("^[0-9]+$"),
                 col("race_time_ms").cast("bigint")
            ).alias("race_duration_ms"),
            col("status_id"),
            # Add derived fields
            when(col("points_scored") > 0, true).otherwise(false).alias("scored_points"),
            when(col("finish_position_text") == "1", true).otherwise(false).alias("race_winner"),
            when(col("finish_position_text").isin("1", "2", "3"), true).otherwise(false).alias("podium_finish"),
            col("ingested_at"),
            current_timestamp().alias("processed_at"),
            lit("silver_quality_processed").alias("processing_stage")
        )
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥇 Gold Layer: Analytics-Ready Aggregations
# MAGIC
# MAGIC Gold tables provide business-ready analytics with complex aggregations.

# COMMAND ----------

@dlt.table(
    name="dlt_gold_driver_stats",
    comment="DLT Gold: Comprehensive driver career statistics and performance metrics"
)
@dlt.expect("drivers_with_races", "total_races > 0")
def gold_driver_stats():
    """
    Calculate comprehensive driver career statistics.
    Aggregates from clean silver tables to create analytics-ready data.
    """
    drivers = dlt.read("dlt_silver_drivers_clean")
    results = dlt.read("dlt_silver_results_clean")
    
    return (
        drivers.alias("d")
        .join(results.alias("r"), col("d.driver_id") == col("r.driver_id"), "inner")
        .groupBy(
            col("d.driver_id"),
            col("d.full_name"),
            col("d.nationality"),
            col("d.current_age"),
            col("d.birth_date")
        )
        .agg(
            count("r.result_id").alias("total_races"),
            sum("r.points_scored").alias("career_points"),
            sum(when(col("r.race_winner"), 1).otherwise(0)).alias("wins"),
            sum(when(col("r.podium_finish"), 1).otherwise(0)).alias("podiums"),
            sum(when(col("r.scored_points"), 1).otherwise(0)).alias("points_finishes"),
            avg("r.finish_position").alias("avg_finish_position"),
            min("r.finish_position").alias("best_finish"),
            max("r.finish_position").alias("worst_finish"),
            sum("r.laps_completed").alias("total_laps"),
            # Performance ratios
            round(sum("r.points_scored") / count("r.result_id"), 2).alias("points_per_race"),
            round(sum(when(col("r.race_winner"), 1).otherwise(0)) * 100.0 / count("r.result_id"), 2).alias("win_percentage"),
            round(sum(when(col("r.podium_finish"), 1).otherwise(0)) * 100.0 / count("r.result_id"), 2).alias("podium_percentage"),
            # Data lineage
            current_timestamp().alias("calculated_at"),
            lit("dlt_gold_aggregation").alias("calculation_method")
        )
        .filter(col("total_races") >= 1)  # Only drivers with actual race participation
    )

# COMMAND ----------

@dlt.table(
    name="dlt_gold_top_performers",
    comment="DLT Gold: Top performing drivers across different performance categories"
)
@dlt.expect("performance_categories", "performance_tier IS NOT NULL")
def gold_top_performers():
    """
    Create performance tiers and identify top performers.
    Builds on driver stats to create business-friendly categorizations.
    """
    return (
        dlt.read("dlt_gold_driver_stats")
        .select(
            col("driver_id"),
            col("full_name"),
            col("nationality"),
            col("total_races"),
            col("career_points"),
            col("wins"),
            col("podiums"),
            col("points_per_race"),
            col("win_percentage"),
            col("podium_percentage"),
            # Create performance tiers
            when(col("wins") >= 20, "F1 Legend")
            .when(col("wins") >= 5, "Race Winner")
            .when(col("podiums") >= 10, "Podium Regular")
            .when(col("career_points") >= 100, "Points Scorer")
            .when(col("total_races") >= 20, "Veteran")
            .otherwise("Rookie").alias("performance_tier"),
            # Excellence indicators
            when(col("win_percentage") >= 25, "Elite Winner")
            .when(col("podium_percentage") >= 50, "Consistent Podium")
            .when(col("points_per_race") >= 5, "Strong Performer")
            .otherwise("Developing").alias("consistency_rating"),
            # Experience categorization
            when(col("total_races") >= 200, "Ultra Veteran")
            .when(col("total_races") >= 100, "Veteran")
            .when(col("total_races") >= 50, "Experienced")
            .otherwise("Newcomer").alias("experience_level"),
            col("calculated_at"),
            current_timestamp().alias("categorized_at")
        )
        .filter(col("total_races") >= 5)  # Focus on drivers with meaningful careers
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Data Quality Expectations Explained
# MAGIC
# MAGIC DLT provides powerful data quality features through **expectations**:
# MAGIC
# MAGIC ### 🎯 Expectation Types:
# MAGIC
# MAGIC #### 1. `@dlt.expect()`
# MAGIC ```python
# MAGIC @dlt.expect("reasonable_birth_date", "date_of_birth >= '1900-01-01'")
# MAGIC ```
# MAGIC - **Behavior:** Records violation but continues processing
# MAGIC - **Use case:** Data quality monitoring and alerts
# MAGIC - **Result:** Violating records included in output with quality metrics tracked
# MAGIC
# MAGIC #### 2. `@dlt.expect_or_drop()`
# MAGIC ```python
# MAGIC @dlt.expect_or_drop("valid_driver_id", "driver_id IS NOT NULL")
# MAGIC ```
# MAGIC - **Behavior:** Drops records that fail the expectation
# MAGIC - **Use case:** Critical data quality requirements
# MAGIC - **Result:** Only valid records in output table
# MAGIC
# MAGIC #### 3. `@dlt.expect_or_fail()`
# MAGIC ```python
# MAGIC @dlt.expect_or_fail("critical_data", "COUNT(*) > 0")
# MAGIC ```
# MAGIC - **Behavior:** Stops pipeline execution if expectation fails
# MAGIC - **Use case:** Critical business rules that cannot be violated
# MAGIC - **Result:** Pipeline failure with clear error message
# MAGIC
# MAGIC ### 📈 Quality Monitoring:
# MAGIC - **Automatic dashboards** show data quality trends
# MAGIC - **Alerting** when quality degrades
# MAGIC - **Historical tracking** of data quality over time

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🚀 DLT Pipeline Creation Guide
# MAGIC
# MAGIC ### 📋 How to Create a DLT Pipeline:
# MAGIC
# MAGIC #### 1. Navigate to Delta Live Tables 🔄
# MAGIC - Click **"Workflows"** in the left sidebar
# MAGIC - Click **"Delta Live Tables"** tab
# MAGIC - Click **"Create Pipeline"** button
# MAGIC
# MAGIC #### 2. Configure Pipeline Settings ⚙️
# MAGIC ```
# MAGIC Pipeline Name: "F1 Data Pipeline with DLT"
# MAGIC Description: "Managed ETL pipeline for Formula 1 analytics with data quality"
# MAGIC ```
# MAGIC
# MAGIC #### 3. Source Configuration 📝
# MAGIC - **Source Type:** `Notebook`
# MAGIC - **Notebook Path:** Select this notebook (`05_Delta_Live_Pipeline.py`)
# MAGIC - **Source:** Your workspace location
# MAGIC
# MAGIC #### 4. Target Configuration 🎯
# MAGIC ```
# MAGIC Target Catalog: main
# MAGIC Target Schema: default
# MAGIC Storage Location: Managed (Unity Catalog)
# MAGIC ```
# MAGIC
# MAGIC #### 5. Compute Configuration ⚡
# MAGIC ```
# MAGIC Cluster Mode: Serverless (recommended)
# MAGIC Min Workers: 1
# MAGIC Max Workers: 5 (auto-scaling)
# MAGIC ```
# MAGIC
# MAGIC #### 6. Advanced Settings 🎛️
# MAGIC - **Pipeline Mode:** `Triggered` (manual) or `Continuous` (streaming)
# MAGIC - **Channel:** `Current` (latest features)
# MAGIC - **Edition:** `Advanced` (for expectations and monitoring)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 DLT vs Jobs: When to Use Each
# MAGIC
# MAGIC ### 🏗️ **Use Delta Live Tables When:**
# MAGIC
# MAGIC ✅ **Complex ETL with dependencies**
# MAGIC - Multiple transformation layers (Bronze → Silver → Gold)
# MAGIC - Automatic dependency resolution needed
# MAGIC - Schema evolution and data quality critical
# MAGIC
# MAGIC ✅ **Data quality is paramount**
# MAGIC - Need built-in expectations and monitoring
# MAGIC - Automatic quarantine of bad data
# MAGIC - Quality metrics and alerting required
# MAGIC
# MAGIC ✅ **Streaming and incremental processing**
# MAGIC - Near real-time data processing
# MAGIC - Change data capture (CDC) patterns
# MAGIC - Efficient incremental updates
# MAGIC
# MAGIC ✅ **Team collaboration on pipelines**
# MAGIC - Declarative code is easier to understand
# MAGIC - Built-in lineage and documentation
# MAGIC - Standardized patterns across teams
# MAGIC
# MAGIC ### ⚙️ **Use Jobs When:**
# MAGIC
# MAGIC ✅ **Simple, scheduled tasks**
# MAGIC - Single notebook execution
# MAGIC - Basic data refresh operations
# MAGIC - Notification and reporting workflows
# MAGIC
# MAGIC ✅ **Custom orchestration logic**
# MAGIC - Complex conditional workflows
# MAGIC - Integration with external systems
# MAGIC - Custom retry and error handling
# MAGIC
# MAGIC ✅ **Ad-hoc or exploratory processing**
# MAGIC - One-time data migration
# MAGIC - Experimental data processing
# MAGIC - Quick fixes and patches
# MAGIC
# MAGIC ### 📊 **Feature Comparison:**
# MAGIC
# MAGIC | **Feature** | **Delta Live Tables** | **Jobs** |
# MAGIC |-------------|----------------------|----------|
# MAGIC | **Dependency Management** | ✅ Automatic | ⚙️ Manual |
# MAGIC | **Data Quality** | ✅ Built-in expectations | ⚙️ Custom code |
# MAGIC | **Streaming** | ✅ Native support | ⚙️ Structured streaming |
# MAGIC | **Monitoring** | ✅ Automatic dashboards | ⚙️ Custom monitoring |
# MAGIC | **Cost** | 💰 DLT premium | 💰 Standard compute |
# MAGIC | **Flexibility** | 🎯 Declarative patterns | 🔧 Full control |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📈 Advanced DLT Features
# MAGIC
# MAGIC ### 🔄 **Change Data Capture (CDC)**
# MAGIC ```python
# MAGIC @dlt.table
# MAGIC def customers_cdc():
# MAGIC     return dlt.read_stream("customers_raw").apply_changes(
# MAGIC         keys=["customer_id"],
# MAGIC         sequence_by="update_timestamp",
# MAGIC         apply_as_deletes=expr("operation = 'DELETE'"),
# MAGIC         except_column_list=["operation", "update_timestamp"]
# MAGIC     )
# MAGIC ```
# MAGIC
# MAGIC ### 📊 **Pipeline Dependencies**
# MAGIC ```python
# MAGIC # Automatic dependency resolution
# MAGIC @dlt.table
# MAGIC def downstream_table():
# MAGIC     return dlt.read("upstream_table_1").join(dlt.read("upstream_table_2"))
# MAGIC ```
# MAGIC
# MAGIC ### 🎯 **Custom Expectations**
# MAGIC ```python
# MAGIC @dlt.expect_or_fail("freshness_check", "max(update_time) > current_timestamp() - interval 1 day")
# MAGIC def time_sensitive_data():
# MAGIC     return dlt.read("source_data")
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Delta Live Tables Complete!
# MAGIC
# MAGIC **🎉 Outstanding! You've mastered Delta Live Tables fundamentals!**
# MAGIC
# MAGIC ### What You've Accomplished:
# MAGIC - ✅ **Built DLT pipeline** with Bronze, Silver, and Gold layers
# MAGIC - ✅ **Implemented data quality expectations** for automatic monitoring
# MAGIC - ✅ **Used declarative transformations** with automatic dependencies
# MAGIC - ✅ **Learned DLT vs Jobs** comparison and use cases
# MAGIC - ✅ **Explored advanced features** (CDC, streaming, quality monitoring)
# MAGIC
# MAGIC ### 🏗️ Your DLT Pipeline Architecture:
# MAGIC ```
# MAGIC 📁 Volume CSV Files
# MAGIC     ↓ (Auto Loader)
# MAGIC 🥉 DLT Bronze Tables (Raw ingestion)
# MAGIC     ↓ (Quality expectations)
# MAGIC 🥈 DLT Silver Tables (Clean & validated)  
# MAGIC     ↓ (Business aggregations)
# MAGIC 🥇 DLT Gold Tables (Analytics ready)
# MAGIC ```
# MAGIC
# MAGIC ### 📊 Tables Created:
# MAGIC - **Bronze:** `dlt_bronze_drivers`, `dlt_bronze_results`
# MAGIC - **Silver:** `dlt_silver_drivers_clean`, `dlt_silver_results_clean`  
# MAGIC - **Gold:** `dlt_gold_driver_stats`, `dlt_gold_top_performers`

# COMMAND ----------

# Let's show what DLT tables would be created (this is descriptive since DLT runs in pipeline mode)
print("🔄 Delta Live Tables Pipeline Summary")
print("=" * 45)

dlt_tables = [
    "🥉 dlt_bronze_drivers - Raw driver data ingestion",
    "🥉 dlt_bronze_results - Raw results data ingestion", 
    "🥈 dlt_silver_drivers_clean - Validated driver data",
    "🥈 dlt_silver_results_clean - Validated results data",
    "🥇 dlt_gold_driver_stats - Driver career statistics",
    "🥇 dlt_gold_top_performers - Performance categorization"
]

for table in dlt_tables:
    print(f"{table}")

print(f"\n📊 Data Quality: Built-in expectations and monitoring")
print(f"🔄 Dependencies: Automatic resolution and execution order")
print(f"⚡ Compute: Serverless managed infrastructure")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🚀 Next Steps
# MAGIC
# MAGIC Ready to explore AI-powered features and advanced analytics?
# MAGIC
# MAGIC ### Immediate Actions:
# MAGIC 1. **🔄 Create Your DLT Pipeline:**
# MAGIC    - Go to Workflows → Delta Live Tables → Create Pipeline
# MAGIC    - Use this notebook as the source
# MAGIC    - Configure with Serverless compute
# MAGIC
# MAGIC 2. **📊 Monitor Pipeline Execution:**
# MAGIC    - Watch automatic dependency resolution
# MAGIC    - Check data quality expectation results
# MAGIC    - Explore generated lineage graphs
# MAGIC
# MAGIC 3. **➡️ Next Notebook:** [06_AI_Agent_Bricks.md](06_AI_Agent_Bricks.md)
# MAGIC    - Explore AI Agents and intelligent applications
# MAGIC    - Build F1 Q&A chatbots with your data
# MAGIC
# MAGIC ### 🎯 Best Practices Checklist:
# MAGIC - ✅ **Start simple** with basic Bronze → Silver → Gold
# MAGIC - ✅ **Add expectations gradually** as you understand your data
# MAGIC - ✅ **Use descriptive table names** for clarity
# MAGIC - ✅ **Document transformations** with comments
# MAGIC - ✅ **Monitor data quality** trends over time
# MAGIC - ✅ **Test expectations** before production deployment
# MAGIC
# MAGIC ### 💡 Pro Tips:
# MAGIC - **🔧 Start with `@dlt.expect()`** to understand data patterns
# MAGIC - **📊 Use DLT dashboards** for quality monitoring
# MAGIC - **⚡ Leverage Serverless** for cost-effective execution
# MAGIC - **🔄 Design for incremental processing** from day one
# MAGIC
# MAGIC **🔄 Your data pipelines are now production-ready! 🚀**