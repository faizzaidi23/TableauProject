"""
STEP 3 — All Visualizations
=============================
Generates and saves all required charts to the /charts/ folder.
Run this AFTER 01_database_setup.py

Charts produced
---------------
01  2019 State Consumption        (horizontal bar)
02  2020 State Consumption        (horizontal bar)
03  Total Consumption             (stacked bar by year)
04  Usage By Region               (grouped bar)
05  Top N / Bottom N States       (2 side-by-side bars)
06  2019 & 2020 Month-wise        (line chart)
07  Total Consumption Region-wise (pie chart)
08  Before & After Lockdown       (grouped bar)
09  Region-wise State Usage       (heatmap)
10  Quarter Usage                 (line chart)
11  Metro City State Usage        (bar chart)
12  Usage by Year                 (box plot)
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # headless backend – no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sqlalchemy import create_engine

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "consumption.db")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# ── Global style ───────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
TITLE_PAD = 16


def save(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  ✅  Saved: charts/{name}")


def load(sql):
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


# ══════════════════════════════════════════════════════════════════════════════
# 01 → 2019 State Consumption
# ══════════════════════════════════════════════════════════════════════════════
print("\n[Chart 01] 2019 State Consumption")
df = load("SELECT States, SUM(Usage) AS Usage FROM consumption WHERE Year=2019 GROUP BY States ORDER BY Usage")
fig, ax = plt.subplots(figsize=(10, 9))
colors = sns.color_palette("Blues_d", len(df))
ax.barh(df["States"], df["Usage"], color=colors, edgecolor="white")
ax.set_xlabel("Total Electricity Consumption (MU)", labelpad=10)
ax.set_title("2019 — State-wise Electricity Consumption", pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
for bar, val in zip(ax.patches, df["Usage"]):
    ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f}", va="center", fontsize=8)
fig.tight_layout()
save(fig, "01_2019_state_consumption.png")

# ══════════════════════════════════════════════════════════════════════════════
# 02 → 2020 State Consumption
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 02] 2020 State Consumption")
df = load("SELECT States, SUM(Usage) AS Usage FROM consumption WHERE Year=2020 GROUP BY States ORDER BY Usage")
fig, ax = plt.subplots(figsize=(10, 9))
colors = sns.color_palette("Oranges_d", len(df))
ax.barh(df["States"], df["Usage"], color=colors, edgecolor="white")
ax.set_xlabel("Total Electricity Consumption (MU)", labelpad=10)
ax.set_title("2020 — State-wise Electricity Consumption", pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
for bar, val in zip(ax.patches, df["Usage"]):
    ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f}", va="center", fontsize=8)
fig.tight_layout()
save(fig, "02_2020_state_consumption.png")

# ══════════════════════════════════════════════════════════════════════════════
# 03 → Total Consumption (both years stacked)
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 03] Total Consumption — stacked by year")
df = load("""
    SELECT States,
           SUM(CASE WHEN Year=2019 THEN Usage ELSE 0 END) AS Y2019,
           SUM(CASE WHEN Year=2020 THEN Usage ELSE 0 END) AS Y2020
    FROM consumption
    GROUP BY States
    ORDER BY (Y2019+Y2020) DESC
""")
x = range(len(df))
fig, ax = plt.subplots(figsize=(14, 6))
bars1 = ax.bar(x, df["Y2019"], label="2019", color="#4C72B0", width=0.6)
bars2 = ax.bar(x, df["Y2020"], bottom=df["Y2019"], label="2020", color="#DD8452", width=0.6)
ax.set_xticks(list(x))
ax.set_xticklabels(df["States"], rotation=55, ha="right", fontsize=9)
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Total Electricity Consumption — 2019 & 2020 (Stacked)", pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend(title="Year")
fig.tight_layout()
save(fig, "03_total_consumption.png")

# ══════════════════════════════════════════════════════════════════════════════
# 04 → Usage by Region (grouped bar)
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 04] Usage by Region")
df = load("""
    SELECT Region_Full, Year, SUM(Usage) AS Usage
    FROM consumption
    GROUP BY Region_Full, Year
    ORDER BY Region_Full, Year
""")
pivot = df.pivot(index="Region_Full", columns="Year", values="Usage").reset_index()
fig, ax = plt.subplots(figsize=(11, 6))
pivot.plot(kind="bar", x="Region_Full", ax=ax, width=0.65,
           color=["#4C72B0","#DD8452"], edgecolor="white")
ax.set_xlabel("")
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Region-wise Electricity Consumption (2019 vs 2020)", pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.set_xticklabels(pivot["Region_Full"], rotation=25, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend(title="Year")
fig.tight_layout()
save(fig, "04_usage_by_region.png")

# ══════════════════════════════════════════════════════════════════════════════
# 05 → Top N / Bottom N
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 05] Top N / Bottom N States")
df_all = load("SELECT States, ROUND(SUM(Usage),2) AS Usage FROM consumption GROUP BY States ORDER BY Usage DESC")
N = 10
top_n   = df_all.head(N)
bot_n   = df_all.tail(N).sort_values("Usage")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].barh(top_n["States"], top_n["Usage"], color="#2ecc71", edgecolor="white")
axes[0].set_title(f"Top {N} States by Total Consumption", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Total Consumption (MU)")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

axes[1].barh(bot_n["States"], bot_n["Usage"], color="#e74c3c", edgecolor="white")
axes[1].set_title(f"Bottom {N} States by Total Consumption", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Total Consumption (MU)")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
fig.suptitle("Top & Bottom States — Electricity Consumption", fontsize=15, fontweight="bold", y=1.01)
fig.tight_layout()
save(fig, "05_top_bottom_n.png")

# ══════════════════════════════════════════════════════════════════════════════
# 06 → 2019 & 2020 Month-wise Consumption
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 06] Month-wise Consumption")
df = load("""
    SELECT Year, Month, Month_Name, ROUND(SUM(Usage),2) AS Usage
    FROM consumption
    GROUP BY Year, Month, Month_Name
    ORDER BY Year, Month
""")
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
df["Month_Name"] = pd.Categorical(df["Month_Name"], categories=month_order, ordered=True)
df = df.sort_values(["Year","Month_Name"])

fig, ax = plt.subplots(figsize=(13, 6))
for year, grp in df.groupby("Year"):
    ax.plot(grp["Month_Name"], grp["Usage"], marker="o", linewidth=2.5, label=str(year))
    for _, row in grp.iterrows():
        ax.annotate(f"{row['Usage']:,.0f}", (row["Month_Name"], row["Usage"]),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7.5)
ax.set_xlabel("Month")
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Month-wise Electricity Consumption — 2019 & 2020", pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=35)
ax.legend(title="Year")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
fig.tight_layout()
save(fig, "06_monthwise_consumption.png")

# ══════════════════════════════════════════════════════════════════════════════
# 07 → Total Consumption Region-wise (pie chart)
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 07] Region-wise Total (Pie)")
df = load("SELECT Region_Full, ROUND(SUM(Usage),2) AS Usage FROM consumption GROUP BY Region_Full ORDER BY Usage DESC")
explode = [0.04] * len(df)
fig, ax = plt.subplots(figsize=(9, 9))
wedges, texts, autotexts = ax.pie(
    df["Usage"], labels=df["Region_Full"], autopct="%1.1f%%",
    explode=explode, startangle=140,
    colors=sns.color_palette("Set2", len(df)),
    textprops={"fontsize": 11},
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
for at in autotexts:
    at.set_fontsize(10)
ax.set_title("Total Electricity Consumption — Region-wise Share\n(2019 + 2020)",
             pad=TITLE_PAD, fontsize=14, fontweight="bold")
fig.tight_layout()
save(fig, "07_region_total_pie.png")

# ══════════════════════════════════════════════════════════════════════════════
# 08 → Before & After Lockdown
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 08] Before & After Lockdown")
df = load("""
    SELECT Lockdown, Region_Full, ROUND(SUM(Usage),2) AS Usage
    FROM consumption
    GROUP BY Lockdown, Region_Full
    ORDER BY Region_Full
""")
pivot = df.pivot(index="Region_Full", columns="Lockdown", values="Usage").reset_index()
pivot.fillna(0, inplace=True)
fig, ax = plt.subplots(figsize=(11, 6))
pivot.plot(kind="bar", x="Region_Full", ax=ax, width=0.65,
           color=["#c0392b","#27ae60"], edgecolor="white")
ax.set_xlabel("")
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Electricity Consumption — Before vs After Lockdown (Region-wise)",
             pad=TITLE_PAD, fontsize=13, fontweight="bold")
ax.set_xticklabels(pivot["Region_Full"], rotation=25, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend(title="Period")
fig.tight_layout()
save(fig, "08_before_after_lockdown.png")

# ══════════════════════════════════════════════════════════════════════════════
# 09 → Region-wise State Usage (Heatmap)
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 09] Region-wise State Usage Heatmap")
df = load("""
    SELECT States, Region_Full, ROUND(SUM(Usage),2) AS Usage
    FROM consumption
    GROUP BY States, Region_Full
""")
pivot = df.pivot(index="States", columns="Region_Full", values="Usage")
pivot.fillna(0, inplace=True)

fig, ax = plt.subplots(figsize=(12, 13))
sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.5,
            linecolor="white", annot=True, fmt=".0f", annot_kws={"size": 7.5})
ax.set_title("Region-wise State Electricity Usage Heatmap",
             pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.set_xlabel("Region", labelpad=10)
ax.set_ylabel("State", labelpad=10)
ax.tick_params(axis="x", rotation=30)
fig.tight_layout()
save(fig, "09_region_state_heatmap.png")

# ══════════════════════════════════════════════════════════════════════════════
# 10 → Quarter Usage
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 10] Quarter Usage")
df = load("""
    SELECT Year, Quarter, ROUND(SUM(Usage),2) AS Usage
    FROM consumption
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter
""")
df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)

fig, ax = plt.subplots(figsize=(11, 6))
for year, grp in df.groupby("Year"):
    ax.plot(grp["Period"], grp["Usage"], marker="s", linewidth=2.5,
            markersize=7, label=str(year))
    for _, row in grp.iterrows():
        ax.annotate(f"{row['Usage']:,.0f}", (row["Period"], row["Usage"]),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
ax.set_xlabel("Quarter")
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Quarterly Electricity Consumption — 2019 & 2020",
             pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.tick_params(axis="x", rotation=25)
ax.legend(title="Year")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
fig.tight_layout()
save(fig, "10_quarter_usage.png")

# ══════════════════════════════════════════════════════════════════════════════
# 11 → Metro City State Usage
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 11] Metro City Usage")
df = load("""
    SELECT States, Year, ROUND(SUM(Usage),2) AS Usage
    FROM consumption
    WHERE Is_Metro = 1
    GROUP BY States, Year
    ORDER BY States, Year
""")
pivot = df.pivot(index="States", columns="Year", values="Usage").reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
pivot.plot(kind="bar", x="States", ax=ax, width=0.6,
           color=["#8e44ad","#f39c12"], edgecolor="white")
ax.set_xlabel("Metro State")
ax.set_ylabel("Total Consumption (MU)")
ax.set_title("Metro City States — Yearly Electricity Consumption",
             pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.set_xticklabels(pivot["States"], rotation=20, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend(title="Year")
fig.tight_layout()
save(fig, "11_metro_city_usage.png")

# ══════════════════════════════════════════════════════════════════════════════
# 12 → Usage Distribution by Year (Box plot)
# ══════════════════════════════════════════════════════════════════════════════
print("[Chart 12] Usage Distribution by Year (Box Plot)")
df = load("SELECT States, Year, Usage FROM consumption")
df["Year"] = df["Year"].astype(str)

fig, ax = plt.subplots(figsize=(9, 6))
sns.boxplot(data=df, x="Year", y="Usage", palette=["#3498db","#e67e22"], ax=ax,
            width=0.5, flierprops={"marker":"o","markerfacecolor":"red","markersize":4})
ax.set_xlabel("Year")
ax.set_ylabel("Daily Consumption (MU)")
ax.set_title("Distribution of Daily Electricity Consumption — 2019 vs 2020",
             pad=TITLE_PAD, fontsize=14, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
fig.tight_layout()
save(fig, "12_usage_by_year_boxplot.png")

print(f"\n✅  All 12 charts saved to → charts/")
