"""
STEP 1 — Database Setup & Data Load
====================================
Loads Consumption.csv into a local SQLite database (consumption.db),
applies SQL-level cleaning, and creates derived/aggregate views that
are later used by the visualizations and dashboard.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "Consumption.csv")
DB_PATH  = os.path.join(BASE_DIR, "consumption.db")

# ── Load raw CSV ───────────────────────────────────────────────────────────────
print("[1/6] Loading raw CSV …")
df = pd.read_csv(CSV_PATH)

# ── Basic validation ───────────────────────────────────────────────────────────
print(f"      Rows: {len(df)} | Columns: {list(df.columns)}")
print(f"      Null values per column:\n{df.isnull().sum()}")

# ── Parse & enrich dates ───────────────────────────────────────────────────────
print("[2/6] Parsing dates and extracting time features …")
df["Dates"]   = pd.to_datetime(df["Dates"], dayfirst=True)
df["Year"]    = df["Dates"].dt.year
df["Month"]   = df["Dates"].dt.month
df["Month_Name"] = df["Dates"].dt.strftime("%B")
df["Quarter"] = df["Dates"].dt.quarter
df["Date_Str"] = df["Dates"].dt.strftime("%Y-%m-%d")

# ── Lockdown flag (India lockdown started 25-Mar-2020) ─────────────────────────
df["Lockdown"] = df["Dates"].apply(
    lambda d: "After Lockdown" if d >= pd.Timestamp("2020-03-25") else "Before Lockdown"
)

# ── Region full names ──────────────────────────────────────────────────────────
region_map = {
    "NR" : "Northern Region",
    "WR" : "Western Region",
    "SR" : "Southern Region",
    "ER" : "Eastern Region",
    "NER": "North-Eastern Region",
}
df["Region_Full"] = df["Regions"].map(region_map)

# ── Metro city flag ────────────────────────────────────────────────────────────
metro_states = ["Delhi", "Maharashtra", "Tamil Nadu", "West Bengal",
                "Karnataka", "Telangana"]
df["Is_Metro"] = df["States"].isin(metro_states)

# ── Fill/drop nulls ────────────────────────────────────────────────────────────
print("[3/6] Handling null values …")
df["Usage"] = df["Usage"].fillna(df["Usage"].median())
df.dropna(subset=["States", "Regions", "Dates"], inplace=True)
df.drop_duplicates(inplace=True)

# ── Write to SQLite ────────────────────────────────────────────────────────────
print("[4/6] Writing to SQLite database …")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

with engine.begin() as conn:
    df.to_sql("consumption", conn, if_exists="replace", index=False)
    print("      Table 'consumption' created.")

# ── Create SQL views / aggregate tables ───────────────────────────────────────
print("[5/6] Creating aggregate tables …")

queries = {
    # ── Total consumption per state per year
    "state_year": """
        CREATE TABLE IF NOT EXISTS state_year AS
        SELECT States, Regions, Region_Full, Year,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        GROUP BY States, Regions, Region_Full, Year
    """,
    # ── Monthly consumption
    "monthly": """
        CREATE TABLE IF NOT EXISTS monthly AS
        SELECT Year, Month, Month_Name,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        GROUP BY Year, Month, Month_Name
    """,
    # ── Region wise total
    "region_total": """
        CREATE TABLE IF NOT EXISTS region_total AS
        SELECT Regions, Region_Full, Year,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        GROUP BY Regions, Region_Full, Year
    """,
    # ── Before / After lockdown
    "lockdown": """
        CREATE TABLE IF NOT EXISTS lockdown AS
        SELECT Lockdown, Regions, Region_Full, States,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        GROUP BY Lockdown, Regions, Region_Full, States
    """,
    # ── Quarter usage
    "quarter": """
        CREATE TABLE IF NOT EXISTS quarter AS
        SELECT Year, Quarter,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        GROUP BY Year, Quarter
    """,
    # ── Metro city usage
    "metro": """
        CREATE TABLE IF NOT EXISTS metro AS
        SELECT States, Year,
               ROUND(SUM(Usage),2) AS Total_Usage
        FROM consumption
        WHERE Is_Metro = 1
        GROUP BY States, Year
    """,
}

with engine.begin() as conn:
    for tbl, sql in queries.items():
        conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
        conn.execute(text(sql))
        print(f"      Table '{tbl}' created.")

# ── Quick summary ──────────────────────────────────────────────────────────────
print("[6/6] Summary of loaded data:")
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM consumption")).scalar()
    years = conn.execute(text("SELECT DISTINCT Year FROM consumption ORDER BY Year")).fetchall()
    states = conn.execute(text("SELECT COUNT(DISTINCT States) FROM consumption")).scalar()
    print(f"      Total records : {count}")
    print(f"      Years covered : {[r[0] for r in years]}")
    print(f"      Unique states : {states}")

print("\n✅  Database ready → consumption.db")
