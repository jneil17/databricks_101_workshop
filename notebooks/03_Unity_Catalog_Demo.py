# Databricks notebook source
# MAGIC %md
# MAGIC # 🗄️ Unity Catalog Demo: Data Governance & Lineage
# MAGIC *Explore Unity Catalog features with Formula 1 data lineage in 5 minutes*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Learning Objectives
# MAGIC
# MAGIC By the end of this demo, you'll understand:
# MAGIC - ✅ **Unity Catalog's 3-level namespace** (catalog.schema.table)
# MAGIC - ✅ **Data lineage tracking** and visualization
# MAGIC - ✅ **Governance features** for enterprise data management
# MAGIC - ✅ **Best practices** for organizing data assets
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📊 What We'll Build
# MAGIC
# MAGIC **Data Lineage Demo Pipeline:**
# MAGIC ```
# MAGIC Source Tables               Intermediate Tables           Final Analytics
# MAGIC ┌──────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
# MAGIC │ lineage_drivers_ │   →   │ lineage_driver_     │   →   │ lineage_championship│
# MAGIC │ source           │       │ performance         │       │ _tiers              │
# MAGIC └──────────────────┘       └─────────────────────┘       └─────────────────────┘
# MAGIC ┌──────────────────┐                    ↑               
# MAGIC │ lineage_results_ │   ─────────────────┘
# MAGIC │ source           │                    ↓
# MAGIC └──────────────────┘       ┌─────────────────────┐
# MAGIC                            │ lineage_career_     │
# MAGIC                            │ stats               │
# MAGIC                            └─────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC **🎯 Goal:** Create clear data lineage that you can visualize in the Catalog UI

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏗️ Unity Catalog Overview
# MAGIC
# MAGIC **Unity Catalog** is Databricks' unified governance solution for data and AI assets.
# MAGIC
# MAGIC ### 🔧 Key Features:
# MAGIC - **🗂️ 3-Level Namespace:** `catalog.schema.table` hierarchy
# MAGIC - **📈 Data Lineage:** Automatic tracking of data dependencies  
# MAGIC - **🔒 Access Control:** Fine-grained permissions (row/column level)
# MAGIC - **📋 Metadata Management:** Rich descriptions, tags, and discovery
# MAGIC - **🌍 Cross-Cloud:** Works across AWS, Azure, and GCP
# MAGIC - **🔄 Version Control:** Schema evolution and time travel
# MAGIC
# MAGIC ### 🏢 Enterprise Benefits:
# MAGIC - **Compliance:** GDPR, CCPA, SOX compliance support
# MAGIC - **Audit:** Complete audit trail of data access
# MAGIC - **Collaboration:** Shared catalogs across workspaces
# MAGIC - **Discovery:** Data marketplace for self-service analytics

# COMMAND ----------

# Let's start by exploring our current Unity Catalog setup
print("🗄️ Unity Catalog Environment")
print("=" * 40)

# Show current catalog context
current_catalog = spark.sql("SELECT current_catalog()").collect()[0][0]
current_schema = spark.sql("SELECT current_schema()").collect()[0][0]
current_user = spark.sql("SELECT current_user()").collect()[0][0]

print(f"📚 Current Catalog: {current_catalog}")
print(f"📁 Current Schema: {current_schema}")  
print(f"👤 Current User: {current_user}")
print(f"🌐 Full Context: {current_catalog}.{current_schema}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Let's see what tables we have from our previous notebook
# MAGIC SHOW TABLES IN main.default

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📈 Step 1: Create Source Tables for Lineage Demo
# MAGIC
# MAGIC We'll create simplified source tables to demonstrate clear lineage relationships.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Lineage Source 1: Driver Information
# MAGIC CREATE OR REPLACE TABLE main.default.lineage_drivers_source
# MAGIC USING DELTA
# MAGIC COMMENT 'Source table: Driver master data for lineage demonstration'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   driverId,
# MAGIC   full_name,
# MAGIC   nationality,
# MAGIC   current_age,
# MAGIC   'drivers_master_system' as source_system,
# MAGIC   current_timestamp() as ingested_at
# MAGIC FROM main.default.silver_drivers
# MAGIC WHERE driverId IS NOT NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Lineage Source 2: Race Results Information  
# MAGIC CREATE OR REPLACE TABLE main.default.lineage_results_source
# MAGIC USING DELTA
# MAGIC COMMENT 'Source table: Race results data for lineage demonstration'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   r.resultId,
# MAGIC   r.raceId,
# MAGIC   r.driverId,
# MAGIC   r.finish_position,
# MAGIC   r.points,
# MAGIC   r.race_winner,
# MAGIC   race.year as season,
# MAGIC   race.race_name,
# MAGIC   'race_results_system' as source_system,
# MAGIC   current_timestamp() as ingested_at
# MAGIC FROM main.default.silver_results r
# MAGIC JOIN main.default.silver_races race ON r.raceId = race.raceId
# MAGIC WHERE r.driverId IS NOT NULL

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 Step 2: Create Intermediate Processing Tables
# MAGIC
# MAGIC These tables will show how data flows through transformation layers.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Intermediate Table 1: Driver Performance Metrics
# MAGIC CREATE OR REPLACE TABLE main.default.lineage_driver_performance
# MAGIC USING DELTA
# MAGIC COMMENT 'Intermediate table: Driver performance calculated from sources (shows lineage from 2 source tables)'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   d.driverId,
# MAGIC   d.full_name,
# MAGIC   d.nationality,
# MAGIC   d.current_age,
# MAGIC   -- Performance metrics from results
# MAGIC   COUNT(r.resultId) as total_races,
# MAGIC   SUM(r.points) as total_points,
# MAGIC   COUNT(CASE WHEN r.race_winner THEN 1 END) as wins,
# MAGIC   COUNT(CASE WHEN r.finish_position <= 3 THEN 1 END) as podiums,
# MAGIC   ROUND(AVG(r.finish_position), 2) as avg_finish_position,
# MAGIC   -- Data lineage metadata
# MAGIC   ARRAY(d.source_system, r.source_system[0]) as upstream_sources,
# MAGIC   current_timestamp() as processed_at
# MAGIC FROM main.default.lineage_drivers_source d
# MAGIC JOIN main.default.lineage_results_source r ON d.driverId = r.driverId
# MAGIC GROUP BY d.driverId, d.full_name, d.nationality, d.current_age, d.source_system

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Intermediate Table 2: Career Statistics Aggregation
# MAGIC CREATE OR REPLACE TABLE main.default.lineage_career_stats
# MAGIC USING DELTA
# MAGIC COMMENT 'Intermediate table: Career aggregations derived from driver performance'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   driverId,
# MAGIC   full_name,
# MAGIC   nationality,
# MAGIC   total_races,
# MAGIC   total_points,
# MAGIC   wins,
# MAGIC   podiums,
# MAGIC   -- Career performance calculations
# MAGIC   ROUND(total_points / total_races, 2) as points_per_race,
# MAGIC   ROUND(wins * 100.0 / total_races, 2) as win_percentage,
# MAGIC   ROUND(podiums * 100.0 / total_races, 2) as podium_percentage,
# MAGIC   -- Career categories
# MAGIC   CASE 
# MAGIC     WHEN wins >= 20 THEN 'Legend'
# MAGIC     WHEN wins >= 5 THEN 'Star'
# MAGIC     WHEN podiums >= 10 THEN 'Contender'
# MAGIC     WHEN total_points >= 100 THEN 'Regular'
# MAGIC     ELSE 'Rookie'
# MAGIC   END as career_tier,
# MAGIC   upstream_sources,
# MAGIC   current_timestamp() as calculated_at
# MAGIC FROM main.default.lineage_driver_performance
# MAGIC WHERE total_races >= 5  -- Focus on drivers with meaningful careers

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏆 Step 3: Create Final Analytics Table
# MAGIC
# MAGIC This final table shows the complete lineage from sources through to business-ready analytics.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Final Analytics Table: Championship Tier Analysis
# MAGIC CREATE OR REPLACE TABLE main.default.lineage_championship_tiers
# MAGIC USING DELTA
# MAGIC COMMENT 'Analytics table: Final championship tier analysis showing complete data lineage'
# MAGIC AS
# MAGIC SELECT 
# MAGIC   career_tier,
# MAGIC   COUNT(*) as driver_count,
# MAGIC   ROUND(AVG(total_points), 0) as avg_career_points,
# MAGIC   ROUND(AVG(wins), 1) as avg_wins,
# MAGIC   ROUND(AVG(podiums), 1) as avg_podiums,
# MAGIC   ROUND(AVG(points_per_race), 2) as avg_points_per_race,
# MAGIC   ROUND(AVG(win_percentage), 2) as avg_win_percentage,
# MAGIC   -- Data quality metrics
# MAGIC   MIN(total_races) as min_races_in_tier,
# MAGIC   MAX(total_races) as max_races_in_tier,
# MAGIC   -- Lineage tracking
# MAGIC   'Derived from lineage_career_stats → lineage_driver_performance → lineage_*_source' as data_lineage,
# MAGIC   current_timestamp() as analysis_date
# MAGIC FROM main.default.lineage_career_stats
# MAGIC GROUP BY career_tier
# MAGIC ORDER BY 
# MAGIC   CASE career_tier
# MAGIC     WHEN 'Legend' THEN 1
# MAGIC     WHEN 'Star' THEN 2  
# MAGIC     WHEN 'Contender' THEN 3
# MAGIC     WHEN 'Regular' THEN 4
# MAGIC     ELSE 5
# MAGIC   END

# COMMAND ----------

# Let's verify all our lineage tables were created successfully
print("📈 Data Lineage Pipeline Summary")
print("=" * 45)

lineage_tables = [
    'lineage_drivers_source',
    'lineage_results_source', 
    'lineage_driver_performance',
    'lineage_career_stats',
    'lineage_championship_tiers'
]

for table in lineage_tables:
    try:
        count = spark.sql(f"SELECT COUNT(*) as count FROM main.default.{table}").collect()[0].count
        if 'source' in table:
            emoji = '📥'
        elif 'championship' in table:
            emoji = '🏆'
        else:
            emoji = '⚙️'
        print(f"{emoji} {table}: {count:,} records")
    except Exception as e:
        print(f"❌ {table}: Error - {str(e)}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Let's see our final championship tier analysis
# MAGIC SELECT * FROM main.default.lineage_championship_tiers

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔍 Step 4: Viewing Data Lineage in Catalog UI
# MAGIC
# MAGIC Now let's explore how to view the lineage we just created!
# MAGIC
# MAGIC ### 📋 How to View Lineage:
# MAGIC
# MAGIC 1. **📂 Navigate to Catalog Explorer**
# MAGIC    - Click **"Catalog"** in the left sidebar
# MAGIC    - Expand **"main"** catalog
# MAGIC    - Expand **"default"** schema
# MAGIC
# MAGIC 2. **🎯 Select a Table**
# MAGIC    - Click on **`lineage_championship_tiers`** (our final table)
# MAGIC    - This will open the table details page
# MAGIC
# MAGIC 3. **📈 View Lineage Tab**
# MAGIC    - Click the **"Lineage"** tab at the top
# MAGIC    - You'll see a visual graph showing data flow
# MAGIC    - Tables → Intermediate transformations → Final analytics
# MAGIC
# MAGIC 4. **🔍 Explore Dependencies**
# MAGIC    - Click on any table node to see its details
# MAGIC    - Hover over connections to see transformation info
# MAGIC    - Use zoom controls to navigate large lineage graphs
# MAGIC
# MAGIC ### 🎨 What You'll See:
# MAGIC ```
# MAGIC lineage_drivers_source ──┐
# MAGIC                          ├─→ lineage_driver_performance ──┐
# MAGIC lineage_results_source ──┘                                ├─→ lineage_championship_tiers
# MAGIC                                                           │
# MAGIC                              lineage_career_stats ────────┘
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏢 Unity Catalog Enterprise Features
# MAGIC
# MAGIC Unity Catalog provides comprehensive governance capabilities for enterprise data management.

# COMMAND ----------

# Let's explore some Unity Catalog metadata and governance features
print("🏢 Unity Catalog Governance Features")
print("=" * 45)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Explore table metadata and lineage information
# MAGIC DESCRIBE EXTENDED main.default.lineage_championship_tiers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Show table history (Delta Lake time travel)
# MAGIC DESCRIBE HISTORY main.default.lineage_championship_tiers

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Explore catalog-level information
# MAGIC DESCRIBE CATALOG main

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Show all schemas in our catalog
# MAGIC SHOW SCHEMAS IN main

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔒 Access Control & Security Features
# MAGIC
# MAGIC Unity Catalog provides fine-grained access control at multiple levels:
# MAGIC
# MAGIC ### 🛡️ Security Levels:
# MAGIC
# MAGIC 1. **📚 Catalog Level**
# MAGIC    - Control who can access entire data domains
# MAGIC    - Example: Finance catalog vs Marketing catalog
# MAGIC
# MAGIC 2. **📁 Schema Level** 
# MAGIC    - Organize tables by project or team
# MAGIC    - Example: `finance.payroll` vs `finance.budgets`
# MAGIC
# MAGIC 3. **📊 Table Level**
# MAGIC    - Individual table permissions
# MAGIC    - Example: Read-only vs Read-Write access
# MAGIC
# MAGIC 4. **📋 Column Level**
# MAGIC    - Hide sensitive columns from specific users
# MAGIC    - Example: Mask PII data for non-admin users
# MAGIC
# MAGIC 5. **📝 Row Level**
# MAGIC    - Filter data based on user attributes
# MAGIC    - Example: Users only see their region's data
# MAGIC
# MAGIC ### 🔑 Common Permission Patterns:
# MAGIC ```sql
# MAGIC -- Grant read access to analysts
# MAGIC GRANT SELECT ON main.default.lineage_championship_tiers TO analysts;
# MAGIC
# MAGIC -- Grant write access to data engineers  
# MAGIC GRANT MODIFY ON SCHEMA main.default TO data_engineers;
# MAGIC
# MAGIC -- Grant full catalog admin to data platform team
# MAGIC GRANT ALL PRIVILEGES ON CATALOG main TO data_platform_admins;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Best Practices for Data Organization
# MAGIC
# MAGIC ### 🏗️ Recommended Catalog Structure:
# MAGIC
# MAGIC ```
# MAGIC 📚 Enterprise Catalog Layout
# MAGIC ├── 🏢 prod_catalog (Production data)
# MAGIC │   ├── 📁 finance_schema
# MAGIC │   │   ├── 📊 revenue_table
# MAGIC │   │   └── 📊 costs_table
# MAGIC │   ├── 📁 marketing_schema
# MAGIC │   │   ├── 📊 campaigns_table
# MAGIC │   │   └── 📊 leads_table
# MAGIC │   └── 📁 shared_schema
# MAGIC │       ├── 📊 dim_dates
# MAGIC │       └── 📊 dim_geography
# MAGIC ├── 🧪 dev_catalog (Development/Testing)
# MAGIC │   └── 📁 [same schema structure]
# MAGIC └── 📊 analytics_catalog (Curated analytics)
# MAGIC     ├── 📁 executive_dashboards
# MAGIC     └── 📁 self_service_analytics
# MAGIC ```
# MAGIC
# MAGIC ### 🎯 Naming Conventions:
# MAGIC - **Catalogs:** `{environment}_{domain}` (e.g., `prod_finance`, `dev_marketing`)
# MAGIC - **Schemas:** `{team_or_project}` (e.g., `payroll`, `customer_analytics`)
# MAGIC - **Tables:** `{layer}_{entity}_{purpose}` (e.g., `gold_customer_360`, `silver_transactions_clean`)

# COMMAND ----------

# Let's demonstrate some catalog exploration capabilities
print("🔍 Catalog Exploration Demo")
print("=" * 35)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Find all tables with 'lineage' in the name
# MAGIC SHOW TABLES IN main.default LIKE 'lineage*'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Search for tables by comment/description
# MAGIC SELECT 
# MAGIC   table_catalog,
# MAGIC   table_schema,
# MAGIC   table_name,
# MAGIC   table_type,
# MAGIC   comment
# MAGIC FROM information_schema.tables 
# MAGIC WHERE table_schema = 'default' 
# MAGIC   AND comment LIKE '%lineage%'
# MAGIC ORDER BY table_name

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Unity Catalog Demo Complete!
# MAGIC
# MAGIC **🎉 Excellent work! You've explored Unity Catalog's powerful governance features!**
# MAGIC
# MAGIC ### What You've Accomplished:
# MAGIC - ✅ **Built data lineage** with 5 interconnected tables
# MAGIC - ✅ **Explored the 3-level namespace** (catalog.schema.table)
# MAGIC - ✅ **Learned lineage visualization** in the Catalog UI
# MAGIC - ✅ **Discovered governance features** (permissions, metadata, audit)
# MAGIC - ✅ **Applied best practices** for data organization
# MAGIC
# MAGIC ### 🔍 Next Steps to Explore Lineage:
# MAGIC 1. **Navigate to Catalog Explorer** (left sidebar)
# MAGIC 2. **Find your tables:** main → default → `lineage_championship_tiers`
# MAGIC 3. **Click the Lineage tab** to see the visual data flow
# MAGIC 4. **Explore dependencies** by clicking on connected tables
# MAGIC
# MAGIC ### 📊 Your Lineage Pipeline:
# MAGIC ```
# MAGIC Sources → Intermediate → Analytics
# MAGIC ✅ lineage_drivers_source      ✅ lineage_driver_performance    ✅ lineage_championship_tiers
# MAGIC ✅ lineage_results_source      ✅ lineage_career_stats
# MAGIC ```

# COMMAND ----------

# Final summary of what we created
print("🗄️ Unity Catalog Demo Summary")
print("=" * 40)

# Count total tables in our schema
total_tables = spark.sql("SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = 'default'").collect()[0].count
lineage_table_count = len([t for t in lineage_tables])

print(f"📊 Total tables in main.default: {total_tables}")
print(f"📈 Lineage demo tables created: {lineage_table_count}")
print(f"🔗 Data lineage relationships: Established")
print(f"🏢 Governance features: Demonstrated")

print(f"\n🎯 Unity Catalog demo completed at {spark.sql('SELECT current_timestamp()').collect()[0][0]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🚀 Next Steps
# MAGIC
# MAGIC Ready to explore more Databricks features? Here's what's next:
# MAGIC
# MAGIC ### Immediate Next Steps:
# MAGIC 1. **➡️ [04_Job_Creation.py](04_Job_Creation.py)** - Automate your data pipelines
# MAGIC 2. **➡️ [05_Delta_Live_Pipeline.py](05_Delta_Live_Pipeline.py)** - Build managed ETL workflows
# MAGIC 3. **➡️ [07_SQL_Editor.sql](07_SQL_Editor.sql)** - Create analytics queries and dashboards
# MAGIC
# MAGIC ### 🔍 Explore Your Lineage:
# MAGIC - **Open Catalog Explorer** and navigate to your lineage tables
# MAGIC - **Click the Lineage tab** to see visual data flow
# MAGIC - **Try the search functionality** to find tables by name or description
# MAGIC
# MAGIC ### 💡 Pro Tips:
# MAGIC - **📌 Bookmark important tables** for quick access
# MAGIC - **📝 Add rich descriptions** to help team members understand data
# MAGIC - **🏷️ Use tags** to categorize and organize data assets
# MAGIC - **🔒 Set up permissions** based on your team's access needs
# MAGIC
# MAGIC **🗄️ Unity Catalog is your data governance superpower! 🚀**