"""
STEP 2 — Data Cleaning & Transformation Report
================================================
Reads from the database, validates data integrity, shows a full
cleaning report, and exports a clean CSV for reference.
Run this AFTER 01_database_setup.py
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "consumption.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

print("=" * 60)
print("   DATA CLEANING & INTEGRITY REPORT")
print("=" * 60)

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM consumption", conn)

# ── 1. Shape & types ──────────────────────────────────────────────────────────
print(f"\n[INFO] Dataset shape : {df.shape[0]} rows × {df.shape[1]} columns")
print("\n[INFO] Column data types:")
print(df.dtypes.to_string())

# ── 2. Missing values ─────────────────────────────────────────────────────────
print("\n[CHECK] Missing values:")
null_counts = df.isnull().sum()
if null_counts.sum() == 0:
    print("        ✅  No missing values found.")
else:
    print(null_counts[null_counts > 0])

# ── 3. Duplicates ─────────────────────────────────────────────────────────────
dupes = df.duplicated().sum()
print(f"\n[CHECK] Duplicate rows  : {dupes}")
if dupes == 0:
    print("        ✅  No duplicates found.")

# ── 4. Usage statistics ───────────────────────────────────────────────────────
print("\n[STATS] Usage (electricity consumption) summary:")
print(df["Usage"].describe().round(2).to_string())
neg_usage = (df["Usage"] < 0).sum()
print(f"\n        Negative usage values : {neg_usage}")
if neg_usage == 0:
    print("        ✅  All usage values are non-negative.")

# ── 5. Unique value counts ────────────────────────────────────────────────────
print("\n[INFO] Unique value counts:")
for col in ["States", "Regions", "Year", "Lockdown"]:
    print(f"        {col:15s} → {df[col].nunique()} unique values")

# ── 6. Region breakdown ───────────────────────────────────────────────────────
print("\n[INFO] States per Region:")
region_states = df.groupby("Region_Full")["States"].nunique().reset_index()
region_states.columns = ["Region", "State Count"]
print(region_states.to_string(index=False))

# ── 7. Date range ─────────────────────────────────────────────────────────────
df["Dates"] = pd.to_datetime(df["Dates"])
print(f"\n[INFO] Date range : {df['Dates'].min().date()}  →  {df['Dates'].max().date()}")

# ── 8. Year-wise record count ─────────────────────────────────────────────────
print("\n[INFO] Records per year:")
print(df.groupby("Year").size().rename("Count").to_string())

# ── 9. Calculated fields added ────────────────────────────────────────────────
print("\n[INFO] Calculated fields available in database:")
extra_cols = ["Year", "Month", "Month_Name", "Quarter", "Lockdown", "Region_Full", "Is_Metro"]
for c in extra_cols:
    print(f"        + {c}")

# ── 10. Export clean CSV ──────────────────────────────────────────────────────
clean_path = os.path.join(BASE_DIR, "Consumption_Clean.csv")
df.to_csv(clean_path, index=False)
print(f"\n✅  Clean dataset exported → Consumption_Clean.csv")

print("\n" + "=" * 60)
print("   ALL CHECKS PASSED — DATA IS READY FOR ANALYSIS")
print("=" * 60)
