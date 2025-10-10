# 🎯 Databricks Platform Tour
*Navigate the Databricks workspace like a pro in 5 minutes*

---

## 🎯 Learning Objectives
By the end of this tour, you'll know:
- ✅ How to navigate the Databricks workspace interface
- ✅ Where to find key features and tools
- ✅ How to access data, compute, and development resources
- ✅ Basic workspace organization principles

---

## 🗺️ Workspace Navigation Overview

**[Screenshot: Full Databricks workspace interface showing left sidebar, main area, and key navigation elements]**
*📁 Image location: `images/01_workspace_overview.png`*
*Screenshot guidance: Capture the main workspace with left sidebar expanded, showing the primary navigation menu items (Workspace, Catalog, Compute, Workflows, etc.)*

The Databricks workspace is organized into **logical sections** accessible from the left sidebar. Let's explore each area:

---

## 📂 Left Sidebar Navigation

### 1. Workspace 📁
**Your development environment**

**[Screenshot: Workspace section expanded showing folder structure with notebooks, folders, and file types]**
*📁 Image location: `images/01_workspace_files.png`*
*Screenshot guidance: Show the Workspace section with a few folders expanded, displaying different file types (.py, .sql, .md, folders)*

**What you'll find here:**
- 📓 **Notebooks** (Python, SQL, Scala, R)
- 📁 **Folders** for organization
- 📄 **Files** (dashboards, libraries, etc.)
- 👥 **Shared workspaces** for collaboration

**Navigation tips:**
- Right-click for context menus (create, rename, delete)
- Use folders to organize by project or team
- Star ⭐ frequently used notebooks

### 2. Catalog 🗄️
**Your data universe (Unity Catalog)**

**[Screenshot: Catalog explorer showing the three-level namespace: catalog.schema.table structure]**
*📁 Image location: `images/01_catalog_explorer.png`*
*Screenshot guidance: Show the Catalog section with main catalog expanded, showing schemas, and at least one schema expanded showing tables*

**Three-level namespace:** `catalog.schema.table`
- 📚 **Catalogs** - Top-level containers (like databases)
- 📋 **Schemas** - Logical groupings within catalogs  
- 📊 **Tables/Views** - Your actual data assets

**Key features:**
- 🔍 **Search** for data assets
- 📈 **Lineage** tracking (see data flow)
- 🔒 **Permissions** management
- 📝 **Metadata** and documentation

### 3. Compute ⚡
**Your processing power**

**[Screenshot: Compute section showing serverless compute options and cluster management]**
*📁 Image location: `images/01_compute_options.png`*
*Screenshot guidance: Show the Compute section with Serverless compute highlighted, and any existing clusters or compute policies*

**Compute types:**
- ⚡ **Serverless** (recommended for this workshop)
  - Auto-scaling, managed infrastructure
  - Pay-per-second billing
  - No cluster management needed
- 🖥️ **All-purpose clusters** (interactive development)
- 🔄 **Job clusters** (automated workloads)

**For this workshop:** We'll use **Serverless compute** exclusively!

### 4. Workflows 🔄
**Automation and orchestration**

**[Screenshot: Workflows section showing jobs, job runs, and Delta Live Tables]**
*📁 Image location: `images/01_workflows_overview.png`*
*Screenshot guidance: Show the Workflows interface with the main sections: Jobs, Job runs, and Delta Live Tables tabs*

**What you can orchestrate:**
- 📋 **Jobs** - Scheduled notebook/script execution
- 🔀 **Delta Live Tables** - Managed ETL pipelines
- 📊 **Dashboards** - Automated report generation
- 🔔 **Alerts** - Data quality monitoring

---

## 🚀 Data Ingestion Options

**[Screenshot: Partner Connect interface showing various data integration options]**
*📁 Image location: `images/01_partner_connect.png`*
*Screenshot guidance: Show the Partner Connect page with tiles for different integration partners (Fivetran, Airbyte, etc.)*

### Quick Ingestion Methods

1. **🔗 Partner Connect**
   - Pre-built integrations (Fivetran, Airbyte, Stitch)
   - One-click setup for common data sources
   - Managed pipelines with minimal configuration

2. **🌐 Lakehouse Federation**
   - Query external databases directly (MySQL, PostgreSQL, Snowflake)
   - No data movement required
   - Real-time access to source systems

3. **📁 Volume Upload**
   - Drag-and-drop file uploads
   - Support for CSV, JSON, Parquet, Delta
   - Perfect for getting started quickly

4. **📝 Custom Scripts**
   - Python/SQL notebooks for custom logic
   - API integrations and web scraping
   - Maximum flexibility and control

---

## 🤖 Machine Learning Features

**[Screenshot: ML section showing Experiments, Models, Feature Store, and AutoML]**
*📁 Image location: `images/01_ml_features.png`*
*Screenshot guidance: Show the machine learning workspace with the main ML sections visible in the sidebar or main interface*

### Key ML Capabilities

1. **🧪 Experiments**
   - Track model training runs
   - Compare model performance
   - Version control for ML workflows

2. **📦 Model Registry**
   - Centralized model storage
   - Model versioning and lifecycle management
   - Model serving and deployment

3. **🏪 Feature Store**
   - Centralized feature management
   - Feature discovery and reuse
   - Consistent feature engineering

4. **🎯 AutoML**
   - Automated model training
   - No-code ML for business users
   - Best practices built-in

---

## 📊 SQL Editor & Analytics

**[Screenshot: SQL Editor interface with query editor, data explorer, and visualization options]**
*📁 Image location: `images/01_sql_editor.png`*
*Screenshot guidance: Show the SQL Editor with a sample query, data explorer on the left, and visualization options visible*

### Analytics Workspace

1. **💻 SQL Editor**
   - Interactive query development
   - Built-in visualizations
   - Collaborative query sharing

2. **📈 Dashboards**
   - Interactive data visualizations
   - Real-time dashboard updates
   - Scheduled report delivery

3. **🎯 Genie Spaces**
   - Natural language querying
   - AI-powered data insights
   - Business user-friendly interface

---

## 🧭 Navigation Best Practices

### Organization Tips
```
📁 Workspace Structure (Recommended)
├── 📂 Projects/
│   ├── 📂 f1_analytics/
│   │   ├── 📓 01_data_ingestion.py
│   │   ├── 📓 02_transformations.sql
│   │   └── 📈 f1_dashboard
│   └── 📂 sales_analysis/
├── 📂 Shared/
│   ├── 📂 team_resources/
│   └── 📂 common_utilities/
└── 📂 Experiments/
    └── 📓 scratch_work.py
```

### Keyboard Shortcuts
- `Ctrl/Cmd + P` - Quick command palette
- `Ctrl/Cmd + ,` - Open workspace settings
- `Ctrl/Cmd + Shift + P` - Command palette (advanced)
- `Ctrl/Cmd + B` - Toggle sidebar visibility

### Search & Discovery
- 🔍 **Global search** - Find notebooks, tables, or people
- 🏷️ **Tags** - Label and categorize resources
- ⭐ **Favorites** - Quick access to important items
- 📚 **Recent** - Access recently used files

---

## ✅ Platform Tour Checklist

Before moving to the next notebook, make sure you can:

- [ ] Navigate between Workspace, Catalog, Compute, and Workflows
- [ ] Find the Catalog explorer and understand the catalog.schema.table structure
- [ ] Locate Serverless compute options
- [ ] Access the SQL Editor from the main navigation
- [ ] Understand where to upload files or create notebooks

---

## 🎯 Next Steps

Now that you know your way around the platform, let's build something amazing!

**➡️ Next: [02_Notebook_Tour.py](02_Notebook_Tour.py)**

*In the next notebook, we'll create a complete Formula 1 data pipeline using everything you just learned!*

---

## 💡 Pro Tips

🔥 **Bookmark this:** Use `Ctrl/Cmd + D` to bookmark this tour for quick reference

🎯 **Stay organized:** Create folders early and name them clearly

⚡ **Use Serverless:** Perfect for workshops and development work

🔍 **Search first:** Before creating, search to see if it already exists

📱 **Mobile friendly:** Databricks works great on tablets for viewing dashboards

---

*Ready to dive deeper? Let's build your first data pipeline! 🚀*