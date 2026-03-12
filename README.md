# ⚡ India Electricity Consumption Analytics Dashboard

A **comprehensive data analytics and visualization project** analyzing state-wise electricity consumption across India for 2019–2020, with a focus on the impact of the COVID-19 lockdown (March 25, 2020).

---

## 📋 Project Overview

This project processes a dataset of daily electricity consumption records across all Indian states and union territories, performs data cleaning and transformation, and provides:

- ✅ **Structured SQLite Database** with aggregated views for fast querying
- ✅ **12 Production-Quality Visualizations** (static PNG charts)
- ✅ **Interactive Streamlit Dashboard** with real-time filtering and drill-downs
- ✅ **Complete Data Integrity Report** with null/duplicate validation
- ✅ **Clean exported CSV** for external use

### Key Objectives
1. **Acquire & Clean** raw electricity consumption data
2. **Transform & Enrich** data with time-based features (month, quarter, lockdown flag)
3. **Analyze Trends** across regions, states, metro cities, and before/after lockdown
4. **Visualize** patterns for stakeholder communication
5. **Enable Interactive Exploration** via Streamlit dashboard

---

## 📊 Dataset

**Source:** `Consumption.csv`  
**Format:** CSV (16,599 rows, 6 columns)  
**Time Period:** January 2, 2019 — December 5, 2020  
**Geographic Coverage:** All 33 Indian states & union territories

### Original Columns
- `States` — State/Union Territory name
- `Regions` — Region code (NR, WR, SR, ER, NER)
- `latitude` — Geographic latitude
- `longitude` — Geographic longitude
- `Dates` — Date of measurement (DD/MM/YYYY format)
- `Usage` — Electricity consumption (in MU — Million Units)

### Derived Columns (added during ETL)
- `Year` — Extracted year
- `Month` — Extracted month (1–12)
- `Month_Name` — Month name (January, February, etc.)
- `Quarter` — Quarter (Q1–Q4)
- `Date_Str` — Standardized date (YYYY-MM-DD)
- `Lockdown` — Flag: "Before Lockdown" or "After Lockdown" (cutoff: 2020-03-25)
- `Region_Full` — Full region name (Northern Region, Western Region, etc.)
- `Is_Metro` — Binary flag for metro states (Delhi, Maharashtra, Tamil Nadu, etc.)

---

## 📂 Project Structure

```
tableau/
├── requirements.txt                    # Python dependencies
├── Consumption.csv                     # Raw input dataset
├── Consumption_Clean.csv               # Cleaned dataset (exported)
├── consumption.db                      # SQLite database (auto-generated)
│
├── 01_database_setup.py               # Step 1: Load & prepare database
├── 02_data_cleaning.py                # Step 2: Validate data integrity
├── 03_visualizations.py               # Step 3: Generate 12 PNG charts
├── 04_dashboard.py                    # Step 4: Launch Streamlit app
│
├── charts/                            # Generated visualizations
│   ├── 01_2019_state_consumption.png
│   ├── 02_2020_state_consumption.png
│   ├── 03_total_consumption.png
│   ├── 04_usage_by_region.png
│   ├── 05_top_bottom_n.png
│   ├── 06_monthwise_consumption.png
│   ├── 07_region_total_pie.png
│   ├── 08_before_after_lockdown.png
│   ├── 09_region_state_heatmap.png
│   ├── 10_quarter_usage.png
│   ├── 11_metro_city_usage.png
│   └── 12_usage_by_year_boxplot.png
│
├── .venv/                             # Virtual environment
└── README.md                          # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** (tested on Python 3.12)
- **pip** or **conda**

### 1. Install Dependencies

```bash
cd tableau
pip install -r requirements.txt
```

**Packages installed:**
- `pandas` — Data manipulation
- `matplotlib` — Static plotting
- `seaborn` — Statistical visualization
- `plotly` — Interactive charts
- `streamlit` — Web dashboard framework
- `sqlalchemy` — SQL toolkit & ORM
- `openpyxl` — Excel support

### 2. Run the ETL Pipeline (3 steps)

#### Step 1: Database Setup & Load
```bash
python 01_database_setup.py
```
**Output:**
- Creates `consumption.db` (SQLite)
- Loads 16,587 records
- Creates 6 aggregate tables
- Shows data summary

#### Step 2: Data Cleaning & Validation
```bash
python 02_data_cleaning.py
```
**Output:**
- Validates null values ✅ (none found)
- Checks for duplicates ✅ (none found)
- Generates statistics
- Exports `Consumption_Clean.csv`
- Prints integrity report

#### Step 3: Generate Visualizations
```bash
python 03_visualizations.py
```
**Output:**
- Saves 12 PNG charts to `charts/` folder
- Uses matplotlib, seaborn, plotly
- High DPI (150) for presentation quality
- ~2-3 minutes to complete

### 3. Launch Interactive Dashboard

```bash
streamlit run 04_dashboard.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open **http://localhost:8501** in your browser.

---

## 📉 12 Visualizations

| # | Chart | Type | Purpose |
|---|-------|------|---------|
| **01** | 2019 State Consumption | Horizontal Bar | Rank states by 2019 electricity use |
| **02** | 2020 State Consumption | Horizontal Bar | Rank states by 2020 electricity use |
| **03** | Total Consumption | Stacked Bar | Compare 2019 vs 2020 by state |
| **04** | Usage by Region | Grouped Bar | Regional trends (NR, WR, SR, ER, NER) |
| **05** | Top N / Bottom N States | 2×Bar | Highest & lowest 10 consumers |
| **06** | Month-wise Consumption | Line Chart | Monthly trend analysis 2019–2020 |
| **07** | Region-wise Total | Pie Chart | Market share by region |
| **08** | Before & After Lockdown | Grouped Bar | COVID-19 impact (2020-03-25 cutoff) |
| **09** | Region × State Heatmap | Heatmap | State performance by region |
| **10** | Quarter Usage | Line Chart | Quarterly trends across years |
| **11** | Metro City Usage | Grouped Bar | Top 6 metro states (Delhi, Mumbai, TN, etc.) |
| **12** | Usage Distribution | Box Plot | Statistical distribution by year |

---

## 🎛️ Interactive Dashboard Features

### Filters (Sidebar)
- 📅 **Year** — Multi-select (2019, 2020)
- 🌍 **Region** — Multi-select (NR, WR, SR, ER, NER)
- 📍 **State** — Multi-select (all 33 states/UTs)
- 🏆 **Top N** — Slider (5–20) for top/bottom analysis

### Sections
1. **KPI Cards** — Total consumption, averages, YoY change
2. **State Consumption (2019/2020)** — Separate tabs by year
3. **Region Analysis** — Bar & pie charts
4. **Month-wise Trends** — Line chart with annotations
5. **Before & After Lockdown** — Impact visualization
6. **Quarterly Usage** — Trend analysis
7. **Top N / Bottom N** — Configurable ranking
8. **Metro Cities** — Focus on high-consumption states
9. **Heatmap** — State vs Region matrix
10. **Data Table** — Raw filtered data
11. **CSV Download** — Export filtered results

---

## 📊 Key Insights

### Data Quality
✅ **16,587 records** across 33 states/UTs  
✅ **No missing values** in any column  
✅ **No duplicates** found  
✅ **Valid date range** — Jan 2, 2019 to Dec 5, 2020  
✅ **Positive usage values** — All ≥ 0.3 MU  

### Regional Distribution
| Region | States | % of Total |
|--------|--------|-----------|
| Northern Region (NR) | 9 | ~26% |
| Western Region (WR) | 6 | ~28% |
| Southern Region (SR) | 6 | ~22% |
| Eastern Region (ER) | 5 | ~15% |
| North-Eastern Region (NER) | 7 | ~9% |

### Top 5 Consumers (2019–2020 Combined)
1. **Uttar Pradesh** — Largest consumer
2. **Maharashtra** — Major industrial hub
3. **Tamil Nadu** — High manufacturing
4. **Rajasthan** — Large agricultural state
5. **Gujarat** — Industrial powerhouse

### Lockdown Impact
- **Larger decrease expected** after March 25, 2020
- **Industrial & commercial** consumption likely reduced
- **Residential usage** may have increased
- **Regional variation** in lockdown effects

---

## 🛢️ Database Schema

### Main Table: `consumption`
```sql
Column           | Type      | Description
-----------------|-----------|---------------------------
States           | TEXT      | State/UT name
Regions          | TEXT      | Region code (NR, WR, etc.)
latitude         | REAL      | Geographic coordinate
longitude        | REAL      | Geographic coordinate
Dates            | TEXT      | Date (standardized)
Usage            | REAL      | Consumption (MU)
Year             | INTEGER   | Extracted year
Month            | INTEGER   | Month (1–12)
Month_Name       | TEXT      | Month name
Quarter          | INTEGER   | Quarter (1–4)
Date_Str         | TEXT      | Date (YYYY-MM-DD)
Lockdown         | TEXT      | Before/After flag
Region_Full      | TEXT      | Full region name
Is_Metro         | INTEGER   | Metro state flag (0/1)
```

### Aggregate Tables
- `state_year` — Total usage per state per year
- `monthly` — Total usage per month per year
- `region_total` — Total usage per region per year
- `lockdown` — Regional totals before/after lockdown
- `quarter` — Total usage per quarter
- `metro` — Metro state usage by year

---

## 🔄 Data Flow

```
Consumption.csv (raw)
    ↓
01_database_setup.py
    ├─ Parse dates
    ├─ Add time features (Year, Month, Quarter)
    ├─ Flag lockdown period
    ├─ Flag metro cities
    └─ Load to SQLite consumption.db
    ↓
02_data_cleaning.py
    ├─ Validate nulls, duplicates
    ├─ Generate statistics
    └─ Export Consumption_Clean.csv
    ↓
03_visualizations.py (Static)
    └─ Generate 12 PNG charts → charts/
    ↓
04_dashboard.py (Interactive)
    └─ Streamlit web app (http://localhost:8501)
```

---

## 📈 Analysis Use Cases

1. **Policy Makers** — Understand regional consumption patterns for resource planning
2. **Energy Companies** — Forecast demand, plan infrastructure
3. **Researchers** — Study COVID-19 impact on electricity consumption
4. **Business Analysts** — Identify high-opportunity markets (metro vs tier-2)
5. **Students** — Learn ETL, visualization, and dashboard development

---

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Reinstall packages
```bash
pip install -r requirements.txt
```

### Issue: Streamlit won't start
**Solution:** Check if port 8501 is in use, or specify a different port
```bash
streamlit run 04_dashboard.py --server.port 8502
```

### Issue: Database locked
**Solution:** Delete `consumption.db` and rerun `01_database_setup.py`

### Issue: Charts not generated
**Solution:** Ensure `charts/` directory exists; if missing, create it manually
```bash
mkdir charts
```

---

## 📝 File Descriptions

### 01_database_setup.py
- Reads `Consumption.csv`
- Parses dates in DD/MM/YYYY format
- Adds derived columns (Year, Month, Quarter, Lockdown flag, etc.)
- Creates SQLite database with 7 tables (1 main + 6 aggregates)
- Validates data and prints summary

### 02_data_cleaning.py
- Reads from `consumption.db`
- Generates comprehensive data quality report
- Checks for nulls, duplicates, outliers
- Shows statistics and unique value counts
- Exports cleaned data to `Consumption_Clean.csv`

### 03_visualizations.py
- Generates 12 professional charts
- Uses matplotlib, seaborn, plotly backends
- Saves PNG files at 150 DPI
- Includes data labels and proper formatting
- Fully automated — no manual intervention needed

### 04_dashboard.py
- Streamlit-based interactive web application
- Multi-select filters for Year, Region, State
- Dynamic KPI cards (total, average, YoY change)
- 10+ interactive charts (Plotly)
- Raw data table with export button
- Responsive design for desktop & mobile

---

## 📚 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.12** | Core language |
| **Pandas** | Data manipulation & cleaning |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Local database |
| **Matplotlib & Seaborn** | Static visualizations |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard framework |

---

## 📅 Timeline & Milestones

| Step | Description | Time |
|------|-------------|------|
| 1️⃣ | Load CSV → SQLite | < 1 min |
| 2️⃣ | Validate & clean data | < 1 min |
| 3️⃣ | Generate 12 charts | ~2-3 min |
| 4️⃣ | Launch dashboard | Instant |

**Total setup time:** ~5 minutes (one-time)

---

## 📄 License & Attribution

- **Dataset:** Electricity consumption data — Indian states (2019–2020)
- **Project:** Data Analytics & Visualization Pipeline
- **Regions Referenced:** Northern (NR), Western (WR), Southern (SR), Eastern (ER), North-Eastern (NER)

---

## 💡 Future Enhancements

- [ ] Forecast 2021+ consumption using ARIMA/Prophet
- [ ] Add prediction confidence intervals
- [ ] Integration with external weather data
- [ ] Route-based energy distribution modeling
- [ ] Real-time data ingestion from utility APIs
- [ ] Machine learning anomaly detection

---

## 📧 Support & Questions

For issues or improvements, please refer to:
- Python error messages — Check terminal output
- Dashboard errors — Inspect browser console (F12)
- Database issues — Verify `consumption.db` exists and is readable

---

<div align="center">

**Built with ❤️ for India's Energy Analytics**

⚡ [Dashboard](http://localhost:8501) • 📊 [Charts](./charts) • 📖 [Data](./Consumption_Clean.csv)

</div>
