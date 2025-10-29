-- Databricks SQL Editor: F1 Analytics Queries

-- ================================================================================
-- 🏎️ Formula 1 Analytics: Writing SQL Queries
-- ================================================================================

-- 📊 SQL Warehouse Setup Guide:
-- 1. Navigate to "SQL Editor" in the left sidebar  
-- 2. Ensure you have a SQL Warehouse selected (Serverless recommended)
-- 3. Run these queries individually to build your F1 dashboard
-- 4. Use the visualization options after each query for charts

-- ================================================================================
-- 📈 Query 1: Top 10 All-Time F1 Drivers by Career Points
-- Visualization: Horizontal bar chart
-- ================================================================================

SELECT
  driver,
  SUM(points) AS points
FROM main.default.bronze_race_results
GROUP BY driver
ORDER BY points DESC
LIMIT 10;