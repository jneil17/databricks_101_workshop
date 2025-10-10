# 🏎️ Databricks 101 Workshop: Formula 1 Analytics

*Build a complete data lakehouse in 45 minutes using real Formula 1 data*

## 🚀 Quick Start

**[👉 Start Your Free Databricks Trial](https://databricks.com/try-databricks)**

### 3-Step Setup
1. **Sign up** for Databricks trial (no credit card required)
2. **Clone** this repository into your workspace
3. **Run** the notebooks in order (01-10)

---

## 🏗️ What You'll Build

```
📊 Formula 1 Data Lakehouse Architecture

Raw Data (Volume)          Bronze Layer              Silver Layer             Gold Layer
┌─────────────────┐       ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  📁 f1_raw_data │  →    │  bronze_races    │  →  │  silver_races   │  →  │ gold_driver_     │
│  • races.csv    │       │  bronze_drivers  │     │  silver_drivers │     │   standings      │
│  • drivers.csv  │       │  bronze_results  │     │  silver_results │     │ gold_season_     │
│  • results.csv  │       └──────────────────┘     └─────────────────┘     │   stats          │
└─────────────────┘                                                        └──────────────────┘
        ↑                           ↑                         ↑                       ↑
    Download CSVs              COPY INTO               Clean & Validate         Analytics Ready
```

**Plus:** Unity Catalog lineage, scheduled jobs, Delta Live Tables, AI agents, and interactive dashboards!

---

## 🎯 Skills You'll Learn

### Core Databricks Platform
- ✅ Navigate the Databricks workspace and key features
- ✅ Create and use Volumes for data storage (no DBFS needed)
- ✅ Build multi-language notebooks (Python + SQL)
- ✅ Implement medallion architecture (Bronze → Silver → Gold)

### Data Engineering
- ✅ Ingest data using COPY INTO pattern
- ✅ Create and manage Delta tables
- ✅ Build data quality checks and transformations
- ✅ Set up automated workflows and scheduling

### Advanced Features
- ✅ Unity Catalog for governance and lineage tracking
- ✅ Delta Live Tables for managed ETL pipelines
- ✅ SQL Editor for analytics and visualization
- ✅ AI-powered features (Genie, Databricks Assistant)

### Real-World Patterns
- ✅ Serverless compute for cost efficiency
- ✅ Volume-based data organization
- ✅ Production-ready data pipelines
- ✅ Best practices for team collaboration

---

## 📅 Workshop Structure

| **Phase** | **Duration** | **Content** |
|-----------|-------------|-------------|
| 🎤 **Presentation** | 30 minutes | Platform overview, use cases, architecture |
| 💻 **Hands-On Demo** | 45 minutes | Build complete F1 analytics solution |
| ❓ **Q&A** | 15 minutes | Questions and next steps |

---

## 📚 Workshop Notebooks

| **#** | **Notebook** | **Duration** | **Focus Area** | **Key Takeaways** |
|-------|-------------|-------------|---------------|------------------|
| 01 | [Platform Tour](notebooks/01_Platform_Tour.md) | 5 min | Navigation | Workspace layout, key features |
| 02 | [Notebook Tour](notebooks/02_Notebook_Tour.py) | 15 min | **Core Setup** | Complete medallion pipeline |
| 03 | [Unity Catalog Demo](notebooks/03_Unity_Catalog_Demo.py) | 5 min | Governance | Lineage, security, organization |
| 04 | [Job Creation](notebooks/04_Job_Creation.py) | 3 min | Automation | Scheduling, monitoring workflows |
| 05 | [Delta Live Pipeline](notebooks/05_Delta_Live_Pipeline.py) | 5 min | Managed ETL | Declarative pipelines, data quality |
| 06 | [AI Agent Bricks](notebooks/06_AI_Agent_Bricks.md) | 3 min | AI/ML | Intelligent applications, RAG |
| 07 | [SQL Editor](notebooks/07_SQL_Editor.sql) | 10 min | Analytics | Interactive queries, visualizations |
| 08 | [Dashboard Placeholder](notebooks/08_Dashboard_Placeholder.md) | - | Reference | Dashboard templates, best practices |
| 09 | [Genie Room](notebooks/09_Genie_Room.md) | 3 min | Natural Language | Ask questions in plain English |
| 10 | [Databricks One](notebooks/10_Databricks_One.md) | 3 min | AI Assistant | Code help, explanations, debugging |

**🔥 Start with Notebook 02** - it creates all the data you'll use in other notebooks!

---

## 📋 Prerequisites

### Technical Requirements
- **Compute:** Serverless compute (included in trial)
- **Data:** ~3MB of Formula 1 CSV files (automatically downloaded)
- **Storage:** Unity Catalog with Volumes (no DBFS needed)
- **Browser:** Chrome, Firefox, Safari, or Edge

### Knowledge Level
- **Beginner-friendly:** No prior Databricks experience required
- **SQL:** Basic SELECT statements helpful but not required
- **Python:** Basic familiarity helpful for data manipulation

### Account Setup
- Free Databricks trial (14-day access to all features)
- No credit card required for trial signup

---

## 🗂️ Data Source

**Formula 1 Datasets:** https://github.com/toUpperCase78/formula1-datasets

### Files Used
- `races.csv` - Race information (circuits, dates, rounds)
- `drivers.csv` - Driver profiles (names, nationalities, DOB)
- `results.csv` - Race results (positions, points, lap times)

*Data covers F1 seasons from 1950-2023 with ~25,000 race results*

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### **"Cannot create Volume" Error**
```
Problem: Volume creation fails in notebook 02
Solution: Ensure you're using main.default catalog (trial default)
Verify: Check catalog permissions in left sidebar → Catalog
```

#### **"COPY INTO Failed" Error**
```
Problem: CSV download or COPY INTO operation fails
Solution: Check internet connection and retry notebook 02
Alternative: Download CSVs manually to Volume via UI
```

#### **"Serverless Compute Unavailable"**
```
Problem: Serverless option not showing in compute selection
Solution: 1. Refresh browser page
          2. Try creating new notebook
          3. Contact support if trial limitation
```

#### **"Table Not Found" in Later Notebooks**
```
Problem: Silver/Gold tables missing in notebooks 03-10
Solution: Complete notebook 02 fully first (creates all tables)
Verify: Check Data Explorer → main → default for 8 tables
```

#### **Screenshot Placeholders Not Rendering**
```
Problem: Markdown files show raw text instead of placeholder
Solution: View in Databricks workspace (not GitHub preview)
Note: Screenshots will be added to images/ folder
```

### Getting Help
- **Documentation:** [Databricks Documentation](https://docs.databricks.com/)
- **Community:** [Databricks Community Forum](https://community.databricks.com/)
- **Training:** [Databricks Academy](https://academy.databricks.com/)
- **Support:** Use in-platform chat during trial period

---

## 📚 Additional Resources

### Learning Paths
- 🎓 [Data Engineer Learning Path](https://academy.databricks.com/path/data-engineer)
- 🎓 [Data Analyst Learning Path](https://academy.databricks.com/path/data-analyst)
- 🎓 [ML Engineer Learning Path](https://academy.databricks.com/path/machine-learning)

### Documentation
- 📖 [Unity Catalog Guide](https://docs.databricks.com/unity-catalog/index.html)
- 📖 [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
- 📖 [SQL Reference](https://docs.databricks.com/sql/index.html)
- 📖 [Python on Databricks](https://docs.databricks.com/python/index.html)

### Community & Events
- 🌐 [Data + AI Summit](https://databricks.com/dataaisummit/) (Annual conference)
- 🌐 [User Groups](https://databricks.com/company/events/user-groups) (Local meetups)
- 🌐 [Databricks Blog](https://databricks.com/blog) (Latest updates)

---

## 📜 License

This workshop is provided for **educational use only**. 

- Formula 1 data used under fair use for educational purposes
- Workshop content available under MIT License
- Databricks platform subject to trial terms and conditions

---

## 🏁 Ready to Start?

1. **[Sign up for Databricks trial](https://databricks.com/try-databricks)** (2 minutes)
2. **Import this repository** to your workspace (1 minute)  
3. **Open notebook 01** and begin your journey! (2 minutes)

*Questions? Check the troubleshooting section above or reach out to the Databricks community.*

---

**Built with ❤️ for the Databricks community**

*Last updated: October 2025*