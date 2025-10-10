# Databricks notebook source
# MAGIC %md
# MAGIC # 🏎️ Databricks Notebook Tour: Build F1 Data Pipeline
# MAGIC *Create a complete medallion architecture in 15 minutes*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 What We'll Build
# MAGIC
# MAGIC **Complete Formula 1 Data Lakehouse:**
# MAGIC ```
# MAGIC 📁 Volume (Raw Files)    →    🥉 Bronze (Raw Tables)    →    🥈 Silver (Clean Tables)    →    🥇 Gold (Analytics)
# MAGIC ├── races.csv                 ├── bronze_races              ├── silver_races               ├── gold_driver_standings
# MAGIC ├── drivers.csv               ├── bronze_drivers            ├── silver_drivers             └── gold_season_stats  
# MAGIC └── results.csv               └── bronze_results            └── silver_results
# MAGIC ```
# MAGIC
# MAGIC **🔥 Key Features:**
# MAGIC - ⚡ **Serverless compute** (no cluster management)
# MAGIC - 📁 **Volumes** for file storage (no DBFS)
# MAGIC - 🔄 **COPY INTO** for production-ready ingestion
# MAGIC - 🐍 **Python + SQL** multi-language development
# MAGIC - 📊 **8 tables** across medallion layers
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚡ Step 1: Serverless Compute Setup
# MAGIC
# MAGIC **📌 IMPORTANT:** Make sure you're using **Serverless compute** for this workshop!
# MAGIC
# MAGIC ### How to Verify Serverless Compute:
# MAGIC 1. Look at the top-right of this notebook
# MAGIC 2. You should see "Serverless" in the compute dropdown
# MAGIC 3. If not, click the dropdown and select "Serverless"
# MAGIC
# MAGIC ### Why Serverless?
# MAGIC - ✅ **No cluster management** - starts instantly
# MAGIC - ✅ **Auto-scaling** - handles any workload size
# MAGIC - ✅ **Cost efficient** - pay per second of actual usage
# MAGIC - ✅ **Always up-to-date** - latest Databricks runtime
# MAGIC
# MAGIC *🎯 Once you see "Serverless" in the compute dropdown, continue to the next cell!*

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🌟 Step 2: Multi-Language Demo
# MAGIC
# MAGIC One of Databricks' superpowers is **seamless multi-language support**. Let's see it in action:

# COMMAND ----------

# Python cell - let's start with some basic info
print("🏎️ Welcome to the F1 Data Pipeline!")
print("=" * 50)

# Get current user and workspace info
current_user = spark.sql("SELECT current_user() as user").collect()[0].user
workspace_id = spark.conf.get("spark.databricks.workspaceUrl", "databricks-workspace")

print(f"👤 Current user: {current_user}")
print(f"🏢 Workspace: {workspace_id}")
print(f"⚡ Compute: Serverless")
print(f"📚 Catalog: main.default")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SQL cell - let's check our catalog structure
# MAGIC SELECT 
# MAGIC   "🏁 Starting F1 Data Pipeline Build!" as message,
# MAGIC   current_catalog() as current_catalog,
# MAGIC   current_schema() as current_schema,
# MAGIC   current_timestamp() as build_started_at

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📁 Step 3: Create Volume for Data Storage
# MAGIC
# MAGIC **Volumes** are the modern way to store files in Databricks. No more DBFS!
# MAGIC
# MAGIC ### Why Volumes?
# MAGIC - 🔒 **Unity Catalog integration** - full governance
# MAGIC - 🌐 **Cloud-native** - direct cloud storage access  
# MAGIC - 📁 **File system semantics** - works like local folders
# MAGIC - 🔄 **Version control friendly** - easy backup and sync

# COMMAND ----------

# Create our Volume for storing raw F1 data files
# This is where we'll download and store our CSV files

%sql
CREATE VOLUME IF NOT EXISTS main.default.f1_raw_data
COMMENT 'Raw Formula 1 datasets for workshop - races, drivers, and results'

# COMMAND ----------

# Verify our Volume was created successfully
%sql
DESCRIBE VOLUME main.default.f1_raw_data

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📥 Step 4: Download F1 Data to Volume
# MAGIC
# MAGIC Time to get our Formula 1 data! We'll download 3 CSV files from GitHub and store them in our Volume.
# MAGIC
# MAGIC **📊 Data Overview:**
# MAGIC - **races.csv** - Race information (circuits, dates, seasons)
# MAGIC - **drivers.csv** - Driver profiles (names, nationalities, birth dates)  
# MAGIC - **results.csv** - Race results (positions, points, lap times)
# MAGIC
# MAGIC *📈 Dataset size: ~25,000 race results from 1950-2023*

# COMMAND ----------

import requests
import os

# F1 data source URLs from GitHub
base_url = "https://raw.githubusercontent.com/toUpperCase78/formula1-datasets/master"
files_to_download = {
    "races.csv": f"{base_url}/races.csv",
    "drivers.csv": f"{base_url}/drivers.csv", 
    "results.csv": f"{base_url}/results.csv"
}

# Volume path where we'll store the files
volume_path = "/Volumes/main/default/f1_raw_data"

print("🏎️ Downloading Formula 1 datasets...")
print("=" * 50)

for filename, url in files_to_download.items():
    print(f"📥 Downloading {filename}...")
    
    try:
        # Download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Write to Volume
        file_path = f"{volume_path}/{filename}"
        with open(file_path, 'wb') as f:
            f.write(response.content)
            
        # Check file size
        file_size = len(response.content)
        print(f"   ✅ Downloaded {filename} ({file_size:,} bytes)")
        
    except Exception as e:
        print(f"   ❌ Error downloading {filename}: {str(e)}")

print("\n🎯 Download complete! Ready to build our pipeline.")

# COMMAND ----------

# Let's verify our files are in the Volume
%sql
LIST '/Volumes/main/default/f1_raw_data/'

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥉 Step 5: Bronze Layer - Raw Data Ingestion
# MAGIC
# MAGIC The **Bronze layer** stores raw data exactly as received. We'll use **COPY INTO** for production-ready data ingestion.
# MAGIC
# MAGIC ### Why COPY INTO?
# MAGIC - 🔄 **Idempotent** - safe to run multiple times
# MAGIC - 📊 **Schema evolution** - handles changing data structures
# MAGIC - 🎯 **Performance** - optimized for bulk loading
# MAGIC - 🔍 **Monitoring** - detailed load statistics

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze Table 1: Races
# MAGIC CREATE OR REPLACE TABLE main.default.bronze_races
# MAGIC (
# MAGIC   raceId INT,
# MAGIC   year INT,
# MAGIC   round INT,
# MAGIC   circuitId INT,
# MAGIC   name STRING,
# MAGIC   date STRING,
# MAGIC   time STRING,
# MAGIC   url STRING,
# MAGIC   fp1_date STRING,
# MAGIC   fp1_time STRING,
# MAGIC   fp2_date STRING,
# MAGIC   fp2_time STRING,
# MAGIC   fp3_date STRING,
# MAGIC   fp3_time STRING,
# MAGIC   quali_date STRING,
# MAGIC   quali_time STRING,
# MAGIC   sprint_date STRING,
# MAGIC   sprint_time STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Bronze layer: Raw F1 race data from CSV files'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Load races data using COPY INTO
# MAGIC COPY INTO main.default.bronze_races
# MAGIC FROM '/Volumes/main/default/f1_raw_data/races.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS (
# MAGIC   'header' = 'true',
# MAGIC   'inferSchema' = 'false'
# MAGIC )
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify races data loaded
# MAGIC SELECT 
# MAGIC   '🏁 Bronze Races' as table_name,
# MAGIC   COUNT(*) as row_count,
# MAGIC   MIN(year) as earliest_year,
# MAGIC   MAX(year) as latest_year
# MAGIC FROM main.default.bronze_races

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze Table 2: Drivers  
# MAGIC CREATE OR REPLACE TABLE main.default.bronze_drivers
# MAGIC (
# MAGIC   driverId INT,
# MAGIC   driverRef STRING,
# MAGIC   number STRING,
# MAGIC   code STRING,
# MAGIC   forename STRING,
# MAGIC   surname STRING,
# MAGIC   dob STRING,
# MAGIC   nationality STRING,
# MAGIC   url STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Bronze layer: Raw F1 driver data from CSV files'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Load drivers data using COPY INTO
# MAGIC COPY INTO main.default.bronze_drivers
# MAGIC FROM '/Volumes/main/default/f1_raw_data/drivers.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS (
# MAGIC   'header' = 'true',
# MAGIC   'inferSchema' = 'false'
# MAGIC )
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify drivers data loaded
# MAGIC SELECT 
# MAGIC   '🏎️ Bronze Drivers' as table_name,
# MAGIC   COUNT(*) as row_count,
# MAGIC   COUNT(DISTINCT nationality) as countries_represented
# MAGIC FROM main.default.bronze_drivers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze Table 3: Results
# MAGIC CREATE OR REPLACE TABLE main.default.bronze_results
# MAGIC (
# MAGIC   resultId INT,
# MAGIC   raceId INT,
# MAGIC   driverId INT,
# MAGIC   constructorId INT,
# MAGIC   number STRING,
# MAGIC   grid INT,
# MAGIC   position STRING,
# MAGIC   positionText STRING,
# MAGIC   positionOrder INT,
# MAGIC   points DOUBLE,
# MAGIC   laps INT,
# MAGIC   time STRING,
# MAGIC   milliseconds STRING,
# MAGIC   fastestLap STRING,
# MAGIC   rank STRING,
# MAGIC   fastestLapTime STRING,
# MAGIC   fastestLapSpeed STRING,
# MAGIC   statusId INT
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Bronze layer: Raw F1 race results from CSV files'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Load results data using COPY INTO
# MAGIC COPY INTO main.default.bronze_results
# MAGIC FROM '/Volumes/main/default/f1_raw_data/results.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS (
# MAGIC   'header' = 'true',
# MAGIC   'inferSchema' = 'false'
# MAGIC )
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify results data loaded
# MAGIC SELECT 
# MAGIC   '🏆 Bronze Results' as table_name,
# MAGIC   COUNT(*) as row_count,
# MAGIC   COUNT(DISTINCT raceId) as unique_races,
# MAGIC   COUNT(DISTINCT driverId) as unique_drivers
# MAGIC FROM main.default.bronze_results

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥈 Step 6: Silver Layer - Clean and Validated Data
# MAGIC
# MAGIC The **Silver layer** contains cleaned, validated, and enriched data. We'll fix data types, handle nulls, and add business logic.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Silver Table 1: Clean Races with proper date types
# MAGIC CREATE OR REPLACE TABLE main.default.silver_races
# MAGIC USING DELTA
# MAGIC COMMENT 'Silver layer: Cleaned F1 race data with proper data types'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   raceId,
# MAGIC   year,
# MAGIC   round,
# MAGIC   circuitId,
# MAGIC   name as race_name,
# MAGIC   CAST(date as DATE) as race_date,
# MAGIC   time as race_time,
# MAGIC   url as race_url,
# MAGIC   -- Clean practice and qualifying sessions
# MAGIC   CASE WHEN fp1_date != '\\N' THEN CAST(fp1_date as DATE) END as fp1_date,
# MAGIC   CASE WHEN quali_date != '\\N' THEN CAST(quali_date as DATE) END as qualifying_date,
# MAGIC   -- Add derived fields
# MAGIC   CASE 
# MAGIC     WHEN year < 1980 THEN 'Classic Era'
# MAGIC     WHEN year < 2000 THEN 'Modern Era' 
# MAGIC     WHEN year < 2014 THEN 'V8 Era'
# MAGIC     ELSE 'Hybrid Era'
# MAGIC   END as f1_era,
# MAGIC   current_timestamp() as processed_at
# MAGIC FROM main.default.bronze_races
# MAGIC WHERE year IS NOT NULL 
# MAGIC   AND name IS NOT NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Silver Table 2: Clean Drivers with full names and age calculations  
# MAGIC CREATE OR REPLACE TABLE main.default.silver_drivers
# MAGIC USING DELTA
# MAGIC COMMENT 'Silver layer: Cleaned F1 driver data with enriched fields'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   driverId,
# MAGIC   driverRef,
# MAGIC   CAST(number as INT) as permanent_number,
# MAGIC   code as driver_code,
# MAGIC   forename,
# MAGIC   surname,
# MAGIC   CONCAT(forename, ' ', surname) as full_name,
# MAGIC   CAST(dob as DATE) as date_of_birth,
# MAGIC   nationality,
# MAGIC   url as driver_url,
# MAGIC   -- Calculate age (approximate)
# MAGIC   YEAR(current_date()) - YEAR(CAST(dob as DATE)) as current_age,
# MAGIC   current_timestamp() as processed_at
# MAGIC FROM main.default.bronze_drivers
# MAGIC WHERE forename IS NOT NULL 
# MAGIC   AND surname IS NOT NULL
# MAGIC   AND dob != '\\N'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Silver Table 3: Clean Results with proper position handling
# MAGIC CREATE OR REPLACE TABLE main.default.silver_results  
# MAGIC USING DELTA
# MAGIC COMMENT 'Silver layer: Cleaned F1 results with proper data types and handling'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   resultId,
# MAGIC   raceId,
# MAGIC   driverId,
# MAGIC   constructorId,
# MAGIC   CAST(number as INT) as car_number,
# MAGIC   grid as grid_position,
# MAGIC   -- Clean position data (handle DNS, DNF, etc.)
# MAGIC   CASE 
# MAGIC     WHEN position RLIKE '^[0-9]+$' THEN CAST(position as INT)
# MAGIC     ELSE NULL 
# MAGIC   END as finish_position,
# MAGIC   positionText as position_text,
# MAGIC   positionOrder as position_order,
# MAGIC   points,
# MAGIC   laps,
# MAGIC   -- Convert milliseconds to proper numeric
# MAGIC   CASE 
# MAGIC     WHEN milliseconds != '\\N' AND milliseconds RLIKE '^[0-9]+$' 
# MAGIC     THEN CAST(milliseconds as BIGINT) 
# MAGIC     ELSE NULL 
# MAGIC   END as race_time_ms,
# MAGIC   CASE 
# MAGIC     WHEN fastestLap != '\\N' AND fastestLap RLIKE '^[0-9]+$'
# MAGIC     THEN CAST(fastestLap as INT)
# MAGIC     ELSE NULL 
# MAGIC   END as fastest_lap_number,
# MAGIC   statusId,
# MAGIC   -- Add derived fields
# MAGIC   CASE WHEN points > 0 THEN TRUE ELSE FALSE END as points_scored,
# MAGIC   CASE WHEN position = '1' THEN TRUE ELSE FALSE END as race_winner,
# MAGIC   current_timestamp() as processed_at
# MAGIC FROM main.default.bronze_results

# COMMAND ----------

# Let's verify our Silver layer data quality
print("🥈 Silver Layer Data Quality Check")
print("=" * 40)

# Check each silver table
silver_tables = ['silver_races', 'silver_drivers', 'silver_results']

for table in silver_tables:
    result = spark.sql(f"SELECT COUNT(*) as count FROM main.default.{table}").collect()[0]
    print(f"✅ {table}: {result.count:,} records")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Quick sample of our cleaned data
# MAGIC SELECT 
# MAGIC   sr.race_name,
# MAGIC   sr.race_date,
# MAGIC   sr.f1_era,
# MAGIC   sd.full_name,
# MAGIC   sd.nationality,
# MAGIC   res.finish_position,
# MAGIC   res.points
# MAGIC FROM main.default.silver_results res
# MAGIC JOIN main.default.silver_races sr ON res.raceId = sr.raceId  
# MAGIC JOIN main.default.silver_drivers sd ON res.driverId = sd.driverId
# MAGIC WHERE res.finish_position = 1  -- Race winners only
# MAGIC ORDER BY sr.race_date DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🥇 Step 7: Gold Layer - Analytics-Ready Data
# MAGIC
# MAGIC The **Gold layer** contains business-ready aggregated data for analytics and reporting.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Gold Table 1: Driver Career Statistics
# MAGIC CREATE OR REPLACE TABLE main.default.gold_driver_standings
# MAGIC USING DELTA
# MAGIC COMMENT 'Gold layer: Comprehensive driver career statistics for analytics'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   d.driverId,
# MAGIC   d.full_name,
# MAGIC   d.nationality,
# MAGIC   d.current_age,
# MAGIC   -- Career statistics
# MAGIC   COUNT(DISTINCT r.raceId) as total_races,
# MAGIC   SUM(res.points) as total_career_points,
# MAGIC   COUNT(CASE WHEN res.finish_position = 1 THEN 1 END) as wins,
# MAGIC   COUNT(CASE WHEN res.finish_position <= 3 THEN 1 END) as podiums,
# MAGIC   COUNT(CASE WHEN res.points_scored THEN 1 END) as points_finishes,
# MAGIC   -- Performance metrics  
# MAGIC   ROUND(AVG(res.finish_position), 2) as avg_finish_position,
# MAGIC   ROUND(SUM(res.points) / COUNT(DISTINCT r.raceId), 2) as points_per_race,
# MAGIC   ROUND(COUNT(CASE WHEN res.finish_position = 1 THEN 1 END) * 100.0 / COUNT(DISTINCT r.raceId), 2) as win_percentage,
# MAGIC   -- Career span
# MAGIC   MIN(r.year) as career_start_year,
# MAGIC   MAX(r.year) as career_end_year,
# MAGIC   MAX(r.year) - MIN(r.year) + 1 as career_span_years,
# MAGIC   current_timestamp() as calculated_at
# MAGIC FROM main.default.silver_drivers d
# MAGIC JOIN main.default.silver_results res ON d.driverId = res.driverId
# MAGIC JOIN main.default.silver_races r ON res.raceId = r.raceId
# MAGIC GROUP BY d.driverId, d.full_name, d.nationality, d.current_age
# MAGIC HAVING COUNT(DISTINCT r.raceId) >= 1  -- At least 1 race

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Gold Table 2: Season-by-Season Statistics
# MAGIC CREATE OR REPLACE TABLE main.default.gold_season_stats
# MAGIC USING DELTA  
# MAGIC COMMENT 'Gold layer: Annual F1 season statistics and trends'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   r.year as season,
# MAGIC   r.f1_era,
# MAGIC   -- Season overview
# MAGIC   COUNT(DISTINCT r.raceId) as total_races,
# MAGIC   COUNT(DISTINCT res.driverId) as unique_drivers,
# MAGIC   COUNT(DISTINCT res.constructorId) as unique_constructors,
# MAGIC   -- Points and competition
# MAGIC   SUM(res.points) as total_points_awarded,
# MAGIC   ROUND(AVG(res.points), 2) as avg_points_per_result,
# MAGIC   -- Race completion stats
# MAGIC   COUNT(CASE WHEN res.finish_position IS NOT NULL THEN 1 END) as completed_races,
# MAGIC   COUNT(res.resultId) as total_entries,
# MAGIC   ROUND(COUNT(CASE WHEN res.finish_position IS NOT NULL THEN 1 END) * 100.0 / COUNT(res.resultId), 2) as completion_rate,
# MAGIC   -- Winner diversity
# MAGIC   COUNT(DISTINCT CASE WHEN res.finish_position = 1 THEN res.driverId END) as unique_race_winners,
# MAGIC   COUNT(DISTINCT CASE WHEN res.finish_position = 1 THEN res.constructorId END) as unique_winning_constructors,
# MAGIC   current_timestamp() as calculated_at
# MAGIC FROM main.default.silver_races r
# MAGIC JOIN main.default.silver_results res ON r.raceId = res.raceId
# MAGIC GROUP BY r.year, r.f1_era
# MAGIC ORDER BY r.year

# COMMAND ----------

# Let's verify our Gold layer is ready for analytics
print("🥇 Gold Layer Analytics Summary")
print("=" * 40)

# Driver standings preview
driver_count = spark.sql("SELECT COUNT(*) as count FROM main.default.gold_driver_standings").collect()[0]
print(f"👥 Driver careers analyzed: {driver_count.count:,}")

# Season stats preview  
season_count = spark.sql("SELECT COUNT(*) as count FROM main.default.gold_season_stats").collect()[0]
print(f"📅 Seasons analyzed: {season_count.count:,}")

print("\n🎯 Gold layer ready for analytics and dashboards!")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Preview: Top 10 F1 drivers by career points
# MAGIC SELECT 
# MAGIC   full_name,
# MAGIC   nationality,
# MAGIC   total_career_points,
# MAGIC   wins,
# MAGIC   podiums,
# MAGIC   total_races,
# MAGIC   CONCAT(career_start_year, '-', career_end_year) as career_span
# MAGIC FROM main.default.gold_driver_standings
# MAGIC ORDER BY total_career_points DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Step 8: Table Types Demo
# MAGIC
# MAGIC Databricks supports different table types for different use cases. Let's create examples:

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Managed Table (what we've been creating)
# MAGIC -- Data is stored in Unity Catalog managed storage
# MAGIC CREATE OR REPLACE TABLE main.default.example_managed_table 
# MAGIC AS SELECT 'This is a managed table' as description, current_timestamp() as created_at

# COMMAND ----------

# MAGIC %sql
# MAGIC -- View (virtual table, no data storage)
# MAGIC CREATE OR REPLACE VIEW main.default.example_view 
# MAGIC AS 
# MAGIC SELECT 
# MAGIC   'This is a view' as description,
# MAGIC   COUNT(*) as total_drivers
# MAGIC FROM main.default.silver_drivers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Materialized View (cached query results, refreshable)
# MAGIC CREATE OR REPLACE MATERIALIZED VIEW main.default.example_materialized_view
# MAGIC AS
# MAGIC SELECT 
# MAGIC   nationality,
# MAGIC   COUNT(*) as driver_count,
# MAGIC   AVG(current_age) as avg_age
# MAGIC FROM main.default.silver_drivers
# MAGIC GROUP BY nationality
# MAGIC ORDER BY driver_count DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Test our different table types
# MAGIC SELECT 'Managed Table' as type, COUNT(*) as records FROM main.default.example_managed_table
# MAGIC UNION ALL
# MAGIC SELECT 'View' as type, total_drivers as records FROM main.default.example_view  
# MAGIC UNION ALL
# MAGIC SELECT 'Materialized View' as type, COUNT(*) as records FROM main.default.example_materialized_view

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 Step 9: Auto Loader Demo (Streaming Ingestion)
# MAGIC
# MAGIC **Auto Loader** provides streaming data ingestion from cloud storage. Perfect for real-time data processing!

# COMMAND ----------

# Auto Loader example for continuous CSV ingestion
# This would typically run as a streaming job

from pyspark.sql.functions import *

print("🔄 Auto Loader Example")
print("=" * 30)

# Create a streaming DataFrame that monitors our Volume for new CSV files
streaming_df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "csv") 
  .option("cloudFiles.schemaLocation", "/Volumes/main/default/f1_raw_data/schema/")
  .option("header", "true")
  .load("/Volumes/main/default/f1_raw_data/")
)

print("✅ Auto Loader configured for Volume: /Volumes/main/default/f1_raw_data/")
print("📁 Schema evolution: Enabled")  
print("📊 Format: CSV with headers")
print("🔄 Mode: Streaming (would run continuously in production)")

# In production, you would write this to a Delta table:
# streaming_df.writeStream.format("delta").outputMode("append").table("main.default.streaming_bronze_data")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🤖 Step 10: Databricks Assistant Usage
# MAGIC
# MAGIC The **Databricks Assistant** can help you write code, explain queries, and debug issues!
# MAGIC
# MAGIC ### How to Use the Assistant:
# MAGIC 1. **Highlight code** and click the sparkle ✨ icon
# MAGIC 2. **Ask questions** like "Explain this query" or "Optimize this code"
# MAGIC 3. **Generate code** with natural language prompts
# MAGIC 4. **Debug errors** by sharing error messages
# MAGIC
# MAGIC ### Try These Prompts:
# MAGIC - "Write a query to find the driver with the most wins"
# MAGIC - "Explain this Delta table's structure"
# MAGIC - "How can I optimize this aggregation query?"
# MAGIC - "Create a visualization for season trends"

# COMMAND ----------

# Example query you can ask the Assistant to explain or optimize
# Highlight this and click the sparkle icon!

%sql
SELECT 
  d.nationality,
  COUNT(DISTINCT d.driverId) as driver_count,
  SUM(gs.wins) as total_wins,
  AVG(gs.total_career_points) as avg_career_points
FROM main.default.gold_driver_standings gs
JOIN main.default.silver_drivers d ON gs.driverId = d.driverId  
GROUP BY d.nationality
HAVING total_wins > 10
ORDER BY total_wins DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pipeline Complete! 
# MAGIC
# MAGIC **🎉 Congratulations! You've built a complete Formula 1 data lakehouse!**
# MAGIC
# MAGIC ### What You've Accomplished:
# MAGIC - ✅ **Downloaded real F1 data** from GitHub to Volume storage
# MAGIC - ✅ **Created 8 Delta tables** across Bronze, Silver, and Gold layers
# MAGIC - ✅ **Used COPY INTO** for production-ready data ingestion
# MAGIC - ✅ **Implemented data quality** checks and transformations
# MAGIC - ✅ **Built analytics-ready** aggregated datasets
# MAGIC - ✅ **Demonstrated streaming** with Auto Loader
# MAGIC - ✅ **Explored table types** (managed, views, materialized views)
# MAGIC
# MAGIC ### Your Data Architecture:
# MAGIC ```
# MAGIC 📁 Volume: main.default.f1_raw_data (3 CSV files)
# MAGIC    ↓
# MAGIC 🥉 Bronze: bronze_races, bronze_drivers, bronze_results  
# MAGIC    ↓
# MAGIC 🥈 Silver: silver_races, silver_drivers, silver_results
# MAGIC    ↓ 
# MAGIC 🥇 Gold: gold_driver_standings, gold_season_stats
# MAGIC ```

# COMMAND ----------

# Final verification - let's check all our tables
print("🏁 F1 Data Pipeline Summary")
print("=" * 50)

tables_to_check = [
    'bronze_races', 'bronze_drivers', 'bronze_results',
    'silver_races', 'silver_drivers', 'silver_results', 
    'gold_driver_standings', 'gold_season_stats'
]

for table in tables_to_check:
    try:
        count = spark.sql(f"SELECT COUNT(*) as count FROM main.default.{table}").collect()[0].count
        layer = table.split('_')[0].upper()
        emoji = {'BRONZE': '🥉', 'SILVER': '🥈', 'GOLD': '🥇'}.get(layer, '📊')
        print(f"{emoji} {table}: {count:,} records")
    except Exception as e:
        print(f"❌ {table}: Error - {str(e)}")

print(f"\n🎯 Pipeline built successfully at {spark.sql('SELECT current_timestamp()').collect()[0][0]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🚀 Next Steps
# MAGIC
# MAGIC Your F1 data lakehouse is ready! Here's what to explore next:
# MAGIC
# MAGIC ### Immediate Next Steps:
# MAGIC 1. **➡️ [03_Unity_Catalog_Demo.py](03_Unity_Catalog_Demo.py)** - Explore data lineage and governance
# MAGIC 2. **➡️ [04_Job_Creation.py](04_Job_Creation.py)** - Schedule automated data refreshes  
# MAGIC 3. **➡️ [07_SQL_Editor.sql](07_SQL_Editor.sql)** - Build analytics queries and visualizations
# MAGIC
# MAGIC ### Advanced Features:
# MAGIC - **Delta Live Tables** - Managed ETL pipelines
# MAGIC - **AI Agents** - Build F1 Q&A chatbots
# MAGIC - **Dashboards** - Interactive data visualizations
# MAGIC - **Genie** - Natural language queries
# MAGIC
# MAGIC ### Production Considerations:
# MAGIC - Set up **automated scheduling** for data refreshes
# MAGIC - Implement **data quality monitoring** 
# MAGIC - Add **access controls** and permissions
# MAGIC - Create **alerting** for pipeline failures
# MAGIC
# MAGIC **🏎️ Ready to dive deeper into the world of data + AI? Let's go!**