# 🏎️ Databricks 101 Workshop: Formula 1 Analytics

*Build a complete data lakehouse in 45 minutes using real Formula 1 data*

## 🚀 Quick Start

**[Start Your Free Databricks Trial](https://login.databricks.com/signup?)**

### 3-Step Setup
1. **Sign up** for Databricks trial (no credit card required)
2. **Clone** this repository into your workspace (see detailed steps below)
3. **Run** the notebooks in order (00-11)

---

## 📂 How to Clone This Repository

### Step 1: Copy the GitHub Repository URL
1. **Click the green "Code" button** on this GitHub repository
2. **Copy the repository URL** to your clipboard

![Copy Github clone link.png](notebooks/Images/Copy%20Github%20clone%20link.png "Copy Github clone link.png")

### Step 2: Access Your Databricks Workspace
1. **Open your Databricks workspace** in your browser
2. **Navigate to the Workspace section** in the left sidebar

![Open Workspace.png](notebooks/Images/Open%20Workspace.png "Open Workspace.png")

### Step 3: Create Git Folder
1. **Right-click in your workspace** or click the dropdown menu
2. **Select "Create" → "Git folder"**

![Create Git Folder.png](notebooks/Images/Create%20Git%20Folder.png "Create Git Folder.png")

### Step 4: Paste Repository URL
1. **Paste the GitHub repository URL** you copied in Step 1
2. **Click "Clone"** to import the workshop notebooks

![Paste the Github Link into the Github Folder.png](notebooks/Images/Paste%20the%20Github%20Link%20into%20the%20Github%20Folder.png "Paste the Github Link into the Github Folder.png")

**🎉 You're ready to start the workshop!** Navigate to `00_Setup.ipynb` to begin.

---

## 🏗️ What You'll Build

**🏎️ Complete F1 Data Lakehouse Pipeline:**

* **📥 Data Ingestion** - Download F1 CSV files into Databricks Volumes
* **🥉 Bronze Layer** - Raw race results, driver data, and qualifying times  
* **🥈 Silver Layer** - Cleaned and validated F1 data with quality checks
* **🥇 Gold Layer** - Analytics-ready driver standings and team performance metrics
* **🔄 Automated Jobs** - Scheduled data refreshes and pipeline monitoring
* **🗄️ Unity Catalog** - Data governance, lineage tracking, and security
* **📊 Interactive Dashboards** - Visual F1 analytics and race insights
* **🤖 AI Features** - Natural language queries and intelligent applications

**All built using real Formula 1 data from 1950-2023 seasons!**

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
- ✅ Lakeflow Designer for no-code ETL with live previews
- ✅ Dashboards built end-to-end with Genie Code
- ✅ AI-powered features (Genie spaces, Databricks Assistant)

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
| 00 | [Setup](notebooks/00_Setup.ipynb) | 5 min | **Data Preparation** | Download F1 data, create Volume |
| 01 | [Platform Tour](notebooks/01_Platform_Tour.ipynb) | 5 min | Navigation | Workspace layout, key features |
| 02 | [Notebook Tour](notebooks/02_Databricks_Notebook_Tour.ipynb) | 5 min | Basics | Notebook fundamentals + Genie hooks |
| 03 | [Medallion Architecture](notebooks/03_Medallion%20Architecture.ipynb) | 15 min | **Core Pipeline** | Complete Bronze → Silver → Gold |
| 04 | [Unity Catalog](notebooks/04_Unity_Catalog.ipynb) | 5 min | Governance | Lineage, security, organization |
| 05 | [Job Creation](notebooks/05_Job_Creation.ipynb) | 3 min | Automation | Scheduling, monitoring workflows |
| 06 | [Lakeflow Designer](notebooks/06_Lakeflow_Designer.ipynb) | 5 min | No-code ETL | Visual pipeline builder, live previews |
| 07 | [Dashboard Builder](notebooks/07_Dashboard_Builder.ipynb) | 5 min | BI | Build the F1 dashboard via Genie Code |
| 08 | [Dashboard (reference)](notebooks/08_Formula_1_Dashboard.lvdash.json) | - | Reference | Pre-baked dashboard JSON to import |
| 09 | [Genie Room](notebooks/09_Genie_Room.ipynb) | 5 min | Natural Language | One-shot Genie space setup |
| 10 | [Databricks One](notebooks/10_Databricks_One.ipynb) | 3 min | Business UI | Simplified stakeholder interface |

**🔥 Start with Notebook 00_Setup** - it downloads and creates all the data you'll use in other notebooks!

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

#### **"Cannot create Volume" / "Cannot create Catalog" Error**
```
Problem: Volume or catalog creation fails in notebook 00_Setup
Solution: If you can't use the `main` catalog, use the catalog override
          markdown cell in 00_Setup — paste the Genie Code prompt to
          rewrite every notebook to use a catalog you DO have access to.
Verify: Check catalog permissions in left sidebar → Catalog
```

```
Problem: COPY INTO Failed" Error
Solution: Check internet connection and retry notebook 00_Setup
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
Problem: Silver/Gold tables missing in notebooks 03-11
Solution: Complete notebook 00_Setup fully first (downloads all data)
Alternative: Check notebook 03 creates all tables from downloaded data
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
- 📖 [Lakeflow Pipelines](https://docs.databricks.com/lakeflow/index.html)
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

*Last updated: May 2026*
