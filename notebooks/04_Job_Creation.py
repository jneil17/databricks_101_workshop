# Databricks notebook source
# MAGIC %md
# MAGIC # ⏰ Job Creation: Automate Your Data Pipelines
# MAGIC *Learn to schedule and monitor data workflows in 3 minutes*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you'll know how to:
# MAGIC - ✅ **Create automated jobs** to refresh data regularly
# MAGIC - ✅ **Configure scheduling** for different business needs
# MAGIC - ✅ **Set up monitoring and alerts** for job failures
# MAGIC - ✅ **Track job execution** with logging and history
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 What We'll Build
# MAGIC
# MAGIC **Automated Data Refresh Job:**
# MAGIC ```
# MAGIC 📅 Daily Schedule (6 AM)
# MAGIC     ↓
# MAGIC 🔄 Refresh Driver Standings
# MAGIC     ↓  
# MAGIC 📊 Update job_driver_standings_daily
# MAGIC     ↓
# MAGIC 📝 Log Execution Status
# MAGIC     ↓
# MAGIC 📧 Send Alerts (if needed)
# MAGIC ```
# MAGIC
# MAGIC **🎯 Goal:** Create a production-ready job that can run automatically to keep our F1 data fresh!

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Step 1: Create Job-Ready Data Table
# MAGIC
# MAGIC First, let's create a table that our job will refresh daily with the latest F1 driver standings.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create a table for daily driver standings refresh
# MAGIC CREATE OR REPLACE TABLE main.default.job_driver_standings_daily
# MAGIC USING DELTA
# MAGIC COMMENT 'Daily refreshed driver standings - maintained by automated job'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   driverId,
# MAGIC   full_name,
# MAGIC   nationality,
# MAGIC   total_career_points,
# MAGIC   wins,
# MAGIC   podiums,
# MAGIC   total_races,
# MAGIC   points_per_race,
# MAGIC   win_percentage,
# MAGIC   -- Add job execution metadata
# MAGIC   'manual_creation' as refresh_method,
# MAGIC   current_timestamp() as last_updated,
# MAGIC   current_user() as updated_by
# MAGIC FROM main.default.gold_driver_standings
# MAGIC ORDER BY total_career_points DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify our job table was created
# MAGIC SELECT 
# MAGIC   'job_driver_standings_daily' as table_name,
# MAGIC   COUNT(*) as driver_count,
# MAGIC   MAX(last_updated) as last_refresh,
# MAGIC   MAX(updated_by) as last_updated_by
# MAGIC FROM main.default.job_driver_standings_daily

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📝 Step 2: Create Job Execution Log Table
# MAGIC
# MAGIC Good production jobs always log their execution for monitoring and debugging.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create job execution log table
# MAGIC CREATE OR REPLACE TABLE main.default.job_run_log
# MAGIC (
# MAGIC   job_run_id STRING,
# MAGIC   job_name STRING,
# MAGIC   start_time TIMESTAMP,
# MAGIC   end_time TIMESTAMP,
# MAGIC   status STRING,
# MAGIC   records_processed BIGINT,
# MAGIC   error_message STRING,
# MAGIC   execution_user STRING,
# MAGIC   execution_details MAP<STRING, STRING>
# MAGIC )
# MAGIC USING DELTA
# MAGIC COMMENT 'Job execution tracking and monitoring log'

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 Step 3: Build Job Logic with Logging
# MAGIC
# MAGIC This is the core logic that our scheduled job will execute.

# COMMAND ----------

import uuid
from datetime import datetime

# Job execution function with comprehensive logging
def refresh_driver_standings_job():
    """
    Refreshes the driver standings table and logs execution details.
    This function will be called by our scheduled job.
    """
    
    # Generate unique job run ID
    job_run_id = str(uuid.uuid4())
    job_name = "daily_driver_standings_refresh"
    start_time = datetime.now()
    
    print(f"🚀 Starting job: {job_name}")
    print(f"📝 Job Run ID: {job_run_id}")
    print(f"⏰ Start Time: {start_time}")
    
    try:
        # Step 1: Refresh the driver standings data
        print("📊 Refreshing driver standings data...")
        
        # Get current record count before refresh
        old_count = spark.sql("SELECT COUNT(*) as count FROM main.default.job_driver_standings_daily").collect()[0].count
        
        # Refresh with latest data from gold layer
        spark.sql("""
            CREATE OR REPLACE TABLE main.default.job_driver_standings_daily
            USING DELTA
            AS
            SELECT 
              driverId,
              full_name,
              nationality,
              total_career_points,
              wins,
              podiums,
              total_races,
              points_per_race,
              win_percentage,
              'automated_job_refresh' as refresh_method,
              current_timestamp() as last_updated,
              current_user() as updated_by
            FROM main.default.gold_driver_standings
            ORDER BY total_career_points DESC
        """)
        
        # Get new record count
        new_count = spark.sql("SELECT COUNT(*) as count FROM main.default.job_driver_standings_daily").collect()[0].count
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Job completed successfully!")
        print(f"📊 Records processed: {new_count}")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        
        # Log successful execution
        spark.sql(f"""
            INSERT INTO main.default.job_run_log VALUES (
                '{job_run_id}',
                '{job_name}',
                timestamp('{start_time}'),
                timestamp('{end_time}'),
                'SUCCESS',
                {new_count},
                NULL,
                current_user(),
                map('duration_seconds', '{duration:.2f}', 'old_count', '{old_count}', 'new_count', '{new_count}')
            )
        """)
        
        return {"status": "SUCCESS", "records_processed": new_count, "duration": duration}
        
    except Exception as e:
        end_time = datetime.now()
        error_message = str(e)
        
        print(f"❌ Job failed: {error_message}")
        
        # Log failed execution
        spark.sql(f"""
            INSERT INTO main.default.job_run_log VALUES (
                '{job_run_id}',
                '{job_name}',
                timestamp('{start_time}'),
                timestamp('{end_time}'),
                'FAILED',
                0,
                '{error_message}',
                current_user(),
                map('error_type', 'execution_error')
            )
        """)
        
        raise e

# Test our job function
print("🧪 Testing job execution...")
result = refresh_driver_standings_job()
print(f"🎯 Job test result: {result}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Check our job execution log
# MAGIC SELECT 
# MAGIC   job_name,
# MAGIC   start_time,
# MAGIC   end_time,
# MAGIC   status,
# MAGIC   records_processed,
# MAGIC   execution_details
# MAGIC FROM main.default.job_run_log
# MAGIC ORDER BY start_time DESC
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏗️ Step 4: Complete Job Creation Guide
# MAGIC
# MAGIC Now let's learn how to create an automated job in the Databricks workspace.
# MAGIC
# MAGIC ### 📋 Job Creation Steps:
# MAGIC
# MAGIC #### 1. Navigate to Workflows 🔄
# MAGIC - Click **"Workflows"** in the left sidebar
# MAGIC - Click **"Create Job"** button
# MAGIC - You'll see the job configuration interface
# MAGIC
# MAGIC #### 2. Configure Basic Job Settings ⚙️
# MAGIC ```
# MAGIC Job Name: "F1 Driver Standings Daily Refresh"
# MAGIC Description: "Automated daily refresh of F1 driver standings data"
# MAGIC ```
# MAGIC
# MAGIC #### 3. Add Job Task 📝
# MAGIC - **Task Name:** `refresh_driver_standings`
# MAGIC - **Type:** `Notebook`
# MAGIC - **Source:** Select this notebook (`04_Job_Creation.py`)
# MAGIC - **Cluster:** Choose `Serverless` compute
# MAGIC
# MAGIC #### 4. Set Schedule ⏰
# MAGIC - **Trigger Type:** `Scheduled`
# MAGIC - **Schedule:** `0 6 * * *` (Daily at 6 AM)
# MAGIC - **Timezone:** Your local timezone
# MAGIC
# MAGIC #### 5. Configure Notifications 📧
# MAGIC - **On Success:** Email notification (optional)
# MAGIC - **On Failure:** Email + Slack alert (recommended)
# MAGIC - **Recipients:** Your email or team distribution list
# MAGIC
# MAGIC #### 6. Advanced Options 🎛️
# MAGIC - **Max Concurrent Runs:** `1` (prevent overlapping executions)
# MAGIC - **Timeout:** `30 minutes` (reasonable for this job)
# MAGIC - **Retry Policy:** `Retry 2 times with 5 minute intervals`

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚙️ Common Job Configuration Examples
# MAGIC
# MAGIC Here are some typical scheduling patterns for different business needs:

# COMMAND ----------

print("⏰ Common Job Scheduling Patterns")
print("=" * 45)

schedules = {
    "Every Hour": "0 * * * *",
    "Daily at 6 AM": "0 6 * * *", 
    "Daily at Midnight": "0 0 * * *",
    "Weekly on Monday": "0 6 * * 1",
    "Monthly on 1st": "0 6 1 * *",
    "Business Days Only": "0 6 * * 1-5",
    "Every 15 minutes": "*/15 * * * *",
    "Twice Daily": "0 6,18 * * *"
}

for description, cron in schedules.items():
    print(f"📅 {description:<20} {cron}")

print("\n💡 Cron format: minute hour day month day-of-week")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Job Monitoring and Troubleshooting
# MAGIC
# MAGIC ### 🔍 Monitoring Your Jobs:
# MAGIC
# MAGIC #### Job Run History 📈
# MAGIC - **View runs:** Workflows → Your Job → "Runs" tab
# MAGIC - **Check status:** SUCCESS, FAILED, RUNNING, CANCELED
# MAGIC - **View logs:** Click on any run to see detailed logs
# MAGIC - **Performance:** Check duration trends over time
# MAGIC
# MAGIC #### Common Job Issues & Solutions 🔧
# MAGIC
# MAGIC | **Issue** | **Symptoms** | **Solution** |
# MAGIC |-----------|-------------|-------------|
# MAGIC | **Timeout** | Job runs too long | Optimize queries, increase timeout |
# MAGIC | **Cluster startup** | Slow job start | Use Serverless compute |
# MAGIC | **Data skew** | Uneven task performance | Repartition data, optimize joins |
# MAGIC | **Memory errors** | OOM exceptions | Increase cluster size, optimize code |
# MAGIC | **Dependencies** | Missing tables/files | Check data availability, add retries |

# COMMAND ----------

# Let's create a job monitoring query
print("📊 Job Performance Monitoring")
print("=" * 35)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Job performance monitoring query
# MAGIC SELECT 
# MAGIC   job_name,
# MAGIC   status,
# MAGIC   COUNT(*) as run_count,
# MAGIC   AVG(CAST(execution_details['duration_seconds'] AS DOUBLE)) as avg_duration_seconds,
# MAGIC   MAX(end_time) as last_run,
# MAGIC   SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful_runs,
# MAGIC   SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_runs,
# MAGIC   ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate_pct
# MAGIC FROM main.default.job_run_log
# MAGIC GROUP BY job_name, status
# MAGIC ORDER BY last_run DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 Advanced Job Patterns
# MAGIC
# MAGIC ### Multi-Step Workflows 🔗
# MAGIC
# MAGIC For complex data pipelines, you can create jobs with multiple tasks:
# MAGIC
# MAGIC ```
# MAGIC 📥 Task 1: Data Ingestion
# MAGIC     ↓
# MAGIC 🔄 Task 2: Data Transformation  
# MAGIC     ↓
# MAGIC 📊 Task 3: Generate Reports
# MAGIC     ↓
# MAGIC 📧 Task 4: Send Notifications
# MAGIC ```
# MAGIC
# MAGIC ### Job Dependencies 🔗
# MAGIC - **Sequential:** Tasks run one after another
# MAGIC - **Parallel:** Multiple tasks run simultaneously  
# MAGIC - **Conditional:** Tasks run based on previous results
# MAGIC
# MAGIC ### Resource Management 💰
# MAGIC - **Serverless:** Recommended for most jobs (auto-scaling)
# MAGIC - **Shared clusters:** Cost-effective for multiple small jobs
# MAGIC - **Dedicated clusters:** High-performance critical workloads

# COMMAND ----------

# Example of a more complex job function with multiple steps
def multi_step_etl_job():
    """
    Example of a complex ETL job with multiple steps and error handling.
    """
    job_run_id = str(uuid.uuid4())
    
    try:
        # Step 1: Data validation
        print("🔍 Step 1: Validating source data...")
        validation_result = spark.sql("""
            SELECT COUNT(*) as count 
            FROM main.default.silver_drivers 
            WHERE full_name IS NOT NULL
        """).collect()[0].count
        
        if validation_result == 0:
            raise Exception("No valid driver data found")
            
        # Step 2: Data processing
        print("⚙️ Step 2: Processing data transformations...")
        # (Your transformation logic here)
        
        # Step 3: Data quality checks
        print("✅ Step 3: Running data quality checks...")
        # (Your quality check logic here)
        
        # Step 4: Update production tables
        print("📊 Step 4: Updating production tables...")
        # (Your table update logic here)
        
        print("🎉 Multi-step ETL job completed successfully!")
        return {"status": "SUCCESS", "steps_completed": 4}
        
    except Exception as e:
        print(f"❌ Multi-step ETL job failed: {str(e)}")
        raise e

print("🧪 Example multi-step job structure created")

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Job Creation Complete!
# MAGIC
# MAGIC **🎉 Excellent! You've learned how to create production-ready automated jobs!**
# MAGIC
# MAGIC ### What You've Accomplished:
# MAGIC - ✅ **Created job-ready data table** for daily driver standings
# MAGIC - ✅ **Built execution logging** for monitoring and debugging
# MAGIC - ✅ **Developed job function** with comprehensive error handling
# MAGIC - ✅ **Learned job configuration** (scheduling, notifications, monitoring)
# MAGIC - ✅ **Explored advanced patterns** (multi-step workflows, dependencies)
# MAGIC
# MAGIC ### 🔄 Your Job Architecture:
# MAGIC ```
# MAGIC ⏰ Schedule (Daily 6 AM)
# MAGIC     ↓
# MAGIC 🔄 refresh_driver_standings_job()
# MAGIC     ↓
# MAGIC 📊 job_driver_standings_daily (Updated)
# MAGIC     ↓
# MAGIC 📝 job_run_log (Execution tracked)
# MAGIC ```

# COMMAND ----------

# Final verification of our job-ready components
print("⏰ Job Creation Summary")
print("=" * 30)

# Check our job table
job_table_count = spark.sql("SELECT COUNT(*) as count FROM main.default.job_driver_standings_daily").collect()[0].count
print(f"📊 Driver standings table: {job_table_count:,} records")

# Check our log table  
log_count = spark.sql("SELECT COUNT(*) as count FROM main.default.job_run_log").collect()[0].count
print(f"📝 Job execution logs: {log_count} entries")

print(f"\n✅ Job components ready for scheduling!")
print(f"🎯 Next: Create your job in Workflows → Create Job")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🚀 Next Steps
# MAGIC
# MAGIC Ready to explore more advanced data engineering features?
# MAGIC
# MAGIC ### Immediate Actions:
# MAGIC 1. **🔄 Create Your Job:** 
# MAGIC    - Go to Workflows → Create Job
# MAGIC    - Follow the configuration guide above
# MAGIC    - Schedule your first automated refresh!
# MAGIC
# MAGIC 2. **➡️ Next Notebook:** [05_Delta_Live_Pipeline.py](05_Delta_Live_Pipeline.py)
# MAGIC    - Learn about managed ETL pipelines
# MAGIC    - Declarative data transformations
# MAGIC    - Built-in data quality expectations
# MAGIC
# MAGIC 3. **📊 Monitor Your Jobs:**
# MAGIC    - Check the job_run_log table regularly
# MAGIC    - Set up email notifications for failures
# MAGIC    - Monitor job performance trends
# MAGIC
# MAGIC ### 💡 Pro Tips:
# MAGIC - **🧪 Test thoroughly** before scheduling in production
# MAGIC - **📧 Set up alerts** for job failures (early detection is key)
# MAGIC - **📊 Monitor performance** to optimize job runtime
# MAGIC - **🔄 Use retries** for transient failures
# MAGIC - **📝 Log everything** for easier debugging
# MAGIC
# MAGIC **⏰ Time to automate your data pipelines! 🚀**