-- Databricks SQL Editor: F1 Analytics Queries
-- Build interactive visualizations and dashboards in 10 minutes

-- ================================================================================
-- 🏎️ Formula 1 Analytics: 8 Essential Queries for Data-Driven Insights
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
  full_name as "Driver Name",
  nationality as "Country",
  total_career_points as "Career Points",
  wins as "Race Wins", 
  podiums as "Podium Finishes",
  total_races as "Total Races",
  ROUND(points_per_race, 2) as "Points per Race",
  ROUND(win_percentage, 2) as "Win Rate %"
FROM main.default.gold_driver_standings
WHERE total_races >= 20  -- Focus on drivers with substantial careers
ORDER BY total_career_points DESC
LIMIT 10;

-- 💡 Visualization Tips:
-- • Chart Type: Horizontal Bar Chart
-- • X-Axis: Career Points
-- • Y-Axis: Driver Name  
-- • Color: By Country for geographic insights
-- • Title: "Top 10 F1 Drivers by Career Points"

-- ================================================================================
-- 📈 Query 2: F1 Growth Over Time - Races and Participation by Decade
-- Visualization: Line chart with dual Y-axis
-- ================================================================================

SELECT 
  CASE 
    WHEN season < 1960 THEN '1950s'
    WHEN season < 1970 THEN '1960s'
    WHEN season < 1980 THEN '1970s'
    WHEN season < 1990 THEN '1980s'
    WHEN season < 2000 THEN '1990s'
    WHEN season < 2010 THEN '2000s'
    WHEN season < 2020 THEN '2010s'
    ELSE '2020s'
  END as "Decade",
  ROUND(AVG(total_races), 1) as "Average Races per Season",
  ROUND(AVG(unique_drivers), 1) as "Average Drivers per Season",
  ROUND(AVG(completion_rate), 1) as "Average Completion Rate %",
  COUNT(*) as "Seasons in Decade"
FROM main.default.gold_season_stats
GROUP BY 
  CASE 
    WHEN season < 1960 THEN '1950s'
    WHEN season < 1970 THEN '1960s'
    WHEN season < 1980 THEN '1970s'
    WHEN season < 1990 THEN '1980s'
    WHEN season < 2000 THEN '1990s'
    WHEN season < 2010 THEN '2000s'
    WHEN season < 2020 THEN '2010s'
    ELSE '2020s'
  END
ORDER BY "Decade";

-- 💡 Visualization Tips:
-- • Chart Type: Line Chart (dual Y-axis)
-- • X-Axis: Decade
-- • Y-Axis 1: Average Races per Season  
-- • Y-Axis 2: Average Drivers per Season
-- • Title: "F1 Evolution: Races and Participation by Decade"

-- ================================================================================
-- 🌍 Query 3: National F1 Success - Countries with Most Successful Drivers
-- Visualization: World map or horizontal bar chart
-- ================================================================================

SELECT 
  nationality as "Country",
  COUNT(DISTINCT driverId) as "Total Drivers",
  SUM(wins) as "Total Wins",
  SUM(podiums) as "Total Podiums", 
  SUM(total_career_points) as "Total Points",
  ROUND(AVG(total_career_points), 0) as "Avg Points per Driver",
  ROUND(SUM(wins) * 100.0 / SUM(total_races), 2) as "National Win Rate %",
  -- Top driver from each country
  MAX(CASE WHEN total_career_points = max_points_in_country THEN full_name END) as "Top Driver"
FROM main.default.gold_driver_standings ds
JOIN (
  SELECT 
    nationality,
    MAX(total_career_points) as max_points_in_country
  FROM main.default.gold_driver_standings
  GROUP BY nationality
) top_by_country ON ds.nationality = top_by_country.nationality
WHERE total_races >= 10  -- Drivers with meaningful careers
GROUP BY nationality
HAVING COUNT(DISTINCT driverId) >= 3  -- Countries with at least 3 drivers
ORDER BY "Total Wins" DESC;

-- 💡 Visualization Tips:
-- • Chart Type: Horizontal Bar Chart or World Map
-- • X-Axis: Total Wins (bar) or Country (map)
-- • Y-Axis: Country (bar)
-- • Color: By Total Points for intensity
-- • Title: "F1 Success by Nation: Wins and Driver Count"

-- ================================================================================
-- 🏆 Query 4: Driver Performance Tiers - Career Achievement Categories  
-- Visualization: Stacked bar chart or pie chart
-- ================================================================================

SELECT 
  CASE 
    WHEN wins >= 20 THEN 'F1 Legends (20+ Wins)'
    WHEN wins >= 5 THEN 'Race Winners (5-19 Wins)'
    WHEN podiums >= 10 THEN 'Podium Regulars (10+ Podiums)'
    WHEN total_career_points >= 100 THEN 'Points Scorers (100+ Points)'
    WHEN total_races >= 20 THEN 'Veterans (20+ Races)'
    ELSE 'Newcomers'
  END as "Performance Tier",
  COUNT(*) as "Driver Count",
  ROUND(AVG(total_career_points), 0) as "Avg Career Points",
  ROUND(AVG(wins), 1) as "Avg Wins",
  ROUND(AVG(podiums), 1) as "Avg Podiums",
  ROUND(AVG(points_per_race), 2) as "Avg Points per Race",
  -- Example drivers in each tier
  STRING_AGG(
    CASE WHEN 
      ROW_NUMBER() OVER (PARTITION BY 
        CASE 
          WHEN wins >= 20 THEN 'F1 Legends (20+ Wins)'
          WHEN wins >= 5 THEN 'Race Winners (5-19 Wins)'
          WHEN podiums >= 10 THEN 'Podium Regulars (10+ Podiums)'
          WHEN total_career_points >= 100 THEN 'Points Scorers (100+ Points)'
          WHEN total_races >= 20 THEN 'Veterans (20+ Races)'
          ELSE 'Newcomers'
        END 
        ORDER BY total_career_points DESC
      ) <= 3 
    THEN full_name 
    END, 
    ', '
  ) as "Example Drivers (Top 3)"
FROM main.default.gold_driver_standings
WHERE total_races >= 1
GROUP BY 
  CASE 
    WHEN wins >= 20 THEN 'F1 Legends (20+ Wins)'
    WHEN wins >= 5 THEN 'Race Winners (5-19 Wins)'
    WHEN podiums >= 10 THEN 'Podium Regulars (10+ Podiums)'
    WHEN total_career_points >= 100 THEN 'Points Scorers (100+ Points)'
    WHEN total_races >= 20 THEN 'Veterans (20+ Races)'
    ELSE 'Newcomers'
  END
ORDER BY "Avg Career Points" DESC;

-- 💡 Visualization Tips:
-- • Chart Type: Pie Chart or Donut Chart
-- • Values: Driver Count
-- • Labels: Performance Tier
-- • Title: "F1 Driver Performance Distribution"

-- ================================================================================
-- ⏰ Query 5: Recent F1 Activity - Most Active Seasons Analysis
-- Visualization: Area chart or column chart
-- ================================================================================

SELECT 
  season as "Season",
  f1_era as "F1 Era",
  total_races as "Races",
  unique_drivers as "Drivers",
  unique_constructors as "Teams",
  ROUND(completion_rate, 1) as "Completion Rate %",
  unique_race_winners as "Different Winners",
  unique_winning_constructors as "Winning Teams",
  ROUND(unique_race_winners * 100.0 / total_races, 1) as "Winner Diversity %",
  total_points_awarded as "Total Points Awarded"
FROM main.default.gold_season_stats
WHERE season >= 2000  -- Focus on modern F1
ORDER BY season DESC;

-- 💡 Visualization Tips:
-- • Chart Type: Area Chart or Column Chart
-- • X-Axis: Season
-- • Y-Axis: Multiple metrics (races, drivers, completion rate)
-- • Color: By F1 Era
-- • Title: "Modern F1 Trends: Participation and Competition (2000+)"

-- ================================================================================
-- 🎯 Query 6: Win Concentration Analysis - Dominance vs Competition Eras
-- Visualization: Scatter plot or bubble chart
-- ================================================================================

SELECT 
  season as "Season",
  f1_era as "Era",
  total_races as "Total Races",
  unique_race_winners as "Different Winners",
  unique_winning_constructors as "Winning Constructors",
  ROUND(unique_race_winners * 100.0 / total_races, 1) as "Winner Diversity %",
  ROUND(unique_winning_constructors * 100.0 / total_races, 1) as "Constructor Diversity %",
  -- Dominance indicators
  CASE 
    WHEN unique_race_winners * 100.0 / total_races >= 80 THEN 'Highly Competitive'
    WHEN unique_race_winners * 100.0 / total_races >= 60 THEN 'Competitive'  
    WHEN unique_race_winners * 100.0 / total_races >= 40 THEN 'Moderately Competitive'
    ELSE 'Dominated'
  END as "Competition Level",
  total_points_awarded as "Points Awarded"
FROM main.default.gold_season_stats
WHERE season >= 1970  -- Modern points system era
ORDER BY "Winner Diversity %" DESC;

-- 💡 Visualization Tips:
-- • Chart Type: Scatter Plot
-- • X-Axis: Season
-- • Y-Axis: Winner Diversity %
-- • Size: Total Races (bubble size)
-- • Color: Competition Level
-- • Title: "F1 Competition Analysis: Winner Diversity by Season"

-- ================================================================================
-- 📅 Query 7: Decade-by-Decade F1 Comparison - Era Performance Analysis
-- Visualization: Grouped column chart
-- ================================================================================

WITH decade_analysis AS (
  SELECT 
    CONCAT(FLOOR(season/10)*10, 's') as decade,
    season,
    total_races,
    unique_drivers,
    completion_rate,
    unique_race_winners,
    total_points_awarded
  FROM main.default.gold_season_stats
  WHERE season >= 1950
)
SELECT 
  decade as "Decade",
  COUNT(*) as "Seasons",
  ROUND(AVG(total_races), 1) as "Avg Races per Season",
  ROUND(AVG(unique_drivers), 1) as "Avg Drivers per Season",
  ROUND(AVG(completion_rate), 1) as "Avg Completion Rate %",
  ROUND(AVG(unique_race_winners), 1) as "Avg Different Winners",
  ROUND(AVG(total_points_awarded), 0) as "Avg Points per Season",
  -- Calculate decade competitiveness
  ROUND(AVG(unique_race_winners * 100.0 / total_races), 1) as "Avg Winner Diversity %",
  -- Identify key characteristics
  CASE 
    WHEN AVG(completion_rate) < 70 THEN 'Reliability Era' 
    WHEN AVG(unique_race_winners * 100.0 / total_races) > 60 THEN 'Competitive Era'
    WHEN AVG(total_races) < 12 THEN 'Limited Calendar'
    ELSE 'Stable Era'
  END as "Era Characteristic"
FROM decade_analysis
GROUP BY decade
ORDER BY decade;

-- 💡 Visualization Tips:
-- • Chart Type: Grouped Column Chart
-- • X-Axis: Decade
-- • Y-Axis: Multiple metrics (races, drivers, competition)
-- • Grouping: Different metrics as series
-- • Title: "F1 Evolution by Decade: Key Performance Indicators"

-- ================================================================================
-- ⚡ Query 8: High-Performance Driver Identification - Elite vs Consistent
-- Visualization: Quadrant scatter plot
-- ================================================================================

SELECT 
  full_name as "Driver",
  nationality as "Country",
  total_races as "Career Races",
  wins as "Wins",
  podiums as "Podiums",
  ROUND(points_per_race, 2) as "Points per Race",
  ROUND(win_percentage, 2) as "Win Rate %",
  ROUND(podiums * 100.0 / total_races, 2) as "Podium Rate %",
  -- Performance categorization
  CASE 
    WHEN win_percentage >= 15 AND points_per_race >= 8 THEN 'Elite Champions'
    WHEN win_percentage >= 15 THEN 'Elite Winners'
    WHEN points_per_race >= 8 THEN 'Consistent Performers'  
    WHEN podiums * 100.0 / total_races >= 25 THEN 'Podium Specialists'
    WHEN total_races >= 100 THEN 'Veteran Campaigners'
    ELSE 'Developing Drivers'
  END as "Performance Category",
  -- Career span
  career_start_year as "Debut Year",
  career_end_year as "Final Year", 
  career_span_years as "Career Length"
FROM main.default.gold_driver_standings
WHERE total_races >= 20  -- Focus on substantial careers
ORDER BY points_per_race DESC, win_percentage DESC;

-- 💡 Visualization Tips:
-- • Chart Type: Scatter Plot (Quadrant Analysis)
-- • X-Axis: Win Rate %
-- • Y-Axis: Points per Race
-- • Size: Total Races (bubble size)
-- • Color: Performance Category
-- • Quadrant Lines: At median win rate and points per race
-- • Title: "Driver Performance Matrix: Elite vs Consistent"

-- ================================================================================
-- 📊 Dashboard Creation Guide
-- ================================================================================

-- 🎯 Step 1: Create New Dashboard
-- 1. Click "Dashboards" in the left sidebar
-- 2. Click "Create Dashboard" 
-- 3. Name: "Formula 1 Analytics Dashboard"
-- 4. Description: "Comprehensive F1 data insights from 1950-2023"

-- 🎯 Step 2: Add Visualizations  
-- 1. Click "Add" → "Visualization"
-- 2. Select each query above
-- 3. Configure chart types as suggested
-- 4. Customize colors, titles, and formatting

-- 🎯 Step 3: Dashboard Layout (4 Rows)
-- Row 1: KPI Cards
-- • Total Drivers (count from gold_driver_standings)
-- • Total Races (sum from gold_season_stats)  
-- • Years of F1 (max year - min year + 1)
-- • Countries Represented (distinct nationalities)

-- Row 2: Core Analytics  
-- • Query 1: Top 10 Drivers (horizontal bar)
-- • Query 3: Success by Nation (world map)

-- Row 3: Trends and Competition
-- • Query 2: F1 Growth Over Time (line chart)
-- • Query 6: Win Concentration (scatter plot)

-- Row 4: Performance Analysis
-- • Query 4: Performance Tiers (pie chart)
-- • Query 8: Performance Matrix (scatter plot)

-- 🎯 Step 4: Add Filters
-- • Era Filter: dropdown for f1_era
-- • Country Filter: multi-select for nationality
-- • Minimum Races: slider for career length

-- 🎯 Step 5: Dashboard Best Practices
-- • Consistent color scheme (F1 red, black, white)
-- • Clear titles and axis labels
-- • Responsive layout for different screen sizes
-- • Regular refresh schedule (daily/weekly)
-- • User permissions for sharing

-- ================================================================================
-- 🔧 Advanced SQL Features Demonstrated
-- ================================================================================

-- 📈 Window Functions (used in Query 4)
-- ROW_NUMBER() OVER (PARTITION BY category ORDER BY points DESC)

-- 🎯 Common Table Expressions (CTEs) (used in Query 7) 
-- WITH decade_analysis AS (SELECT ...)

-- 📊 String Aggregation (used in Query 4)
-- STRING_AGG(driver_name, ', ') for concatenating values

-- 🔄 Conditional Aggregation (used throughout)
-- SUM(CASE WHEN condition THEN 1 ELSE 0 END)

-- 📋 Complex Case Statements (used in Query 7)
-- Multi-level categorization and analysis

-- ================================================================================
-- 🎉 SQL Analytics Complete!
-- ================================================================================

-- Congratulations! You've built comprehensive F1 analytics with:
-- ✅ 8 analytical queries covering all major F1 insights
-- ✅ Visualization recommendations for each query type
-- ✅ Complete dashboard layout and design guide
-- ✅ Advanced SQL techniques and best practices
-- ✅ Interactive filters and user experience features

-- 🚀 Next Steps:
-- 1. Run each query individually in SQL Editor
-- 2. Create visualizations using the chart recommendations
-- 3. Build your dashboard following the 4-row layout
-- 4. Share with your team and gather feedback
-- 5. Set up automated refresh schedules

-- 🏎️ Ready to become an F1 data expert! 📊