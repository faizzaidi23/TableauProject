"""
STEP 4 — Interactive Streamlit Dashboard
=========================================
Run with:
    streamlit run 04_dashboard.py

Sections
--------
1. Overview KPIs
2. State Consumption (2019 / 2020)
3. Region Analysis
4. Month-wise Trends
5. Before & After Lockdown
6. Quarter Usage
7. Top N / Bottom N
8. Metro Cities
9. Data Table & Download
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import streamlit as st

# ── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Electricity Consumption Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "consumption.db")


@st.cache_resource
def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


@st.cache_data
def load_data():
    with get_engine().connect() as conn:
        df = pd.read_sql("SELECT * FROM consumption", conn)
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df


df_full = load_data()

# ── Sidebar Filters ────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg",
    width=100,
)
st.sidebar.title("⚡ Filters")

all_years   = sorted(df_full["Year"].unique())
all_regions = sorted(df_full["Region_Full"].unique())
all_states  = sorted(df_full["States"].unique())

sel_years   = st.sidebar.multiselect("Year", all_years, default=all_years)
sel_regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)
sel_states  = st.sidebar.multiselect("State", all_states, default=all_states)

N_val = st.sidebar.slider("Top N / Bottom N", min_value=5, max_value=20, value=10)

# filtered dataset
df = df_full[
    df_full["Year"].isin(sel_years) &
    df_full["Region_Full"].isin(sel_regions) &
    df_full["States"].isin(sel_states)
]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;color:#2c3e50;'>⚡ India Electricity Consumption Dashboard</h1>"
    "<p style='text-align:center;color:#7f8c8d;font-size:16px;'>"
    "State-wise electricity consumption analysis — 2019 &amp; 2020</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: KPI Cards
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("📊 Overview — Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

total   = df["Usage"].sum()
avg_day = df.groupby(["Dates","States"])["Usage"].sum().mean()
max_st  = df.groupby("States")["Usage"].sum().idxmax()
min_st  = df.groupby("States")["Usage"].sum().idxmin()
yoy     = None
if 2019 in sel_years and 2020 in sel_years:
    u19  = df[df["Year"]==2019]["Usage"].sum()
    u20  = df[df["Year"]==2020]["Usage"].sum()
    yoy  = ((u20 - u19) / u19) * 100 if u19 else None

col1.metric("Total Consumption (MU)", f"{total:,.0f}")
col2.metric("Avg Daily per State (MU)", f"{avg_day:,.1f}")
col3.metric("Highest Consuming State", max_st)
col4.metric("Lowest Consuming State", min_st)
col5.metric("YoY Change (2019→2020)", f"{yoy:+.1f}%" if yoy is not None else "N/A")
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: State Consumption by Year
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🗺️ State-wise Consumption")
tab1, tab2 = st.tabs(["2019", "2020"])

for tab, yr in zip([tab1, tab2], [2019, 2020]):
    with tab:
        d = (df[df["Year"]==yr]
             .groupby("States")["Usage"].sum()
             .reset_index()
             .sort_values("Usage"))
        fig = px.bar(d, x="Usage", y="States", orientation="h",
                     color="Usage", color_continuous_scale="Blues",
                     labels={"Usage":"Consumption (MU)","States":"State"},
                     title=f"{yr} — State-wise Electricity Consumption",
                     height=600)
        fig.update_layout(coloraxis_showscale=False,
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Region Analysis
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🌍 Region-wise Analysis")
col_a, col_b = st.columns(2)

with col_a:
    rd = (df.groupby(["Region_Full","Year"])["Usage"].sum()
            .reset_index())
    fig = px.bar(rd, x="Region_Full", y="Usage", color="Year", barmode="group",
                 labels={"Region_Full":"Region","Usage":"Consumption (MU)"},
                 title="Region-wise Consumption (2019 vs 2020)",
                 color_discrete_sequence=["#4C72B0","#DD8452"])
    fig.update_layout(xaxis_tickangle=-30,
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    rpie = (df.groupby("Region_Full")["Usage"].sum().reset_index())
    fig = px.pie(rpie, names="Region_Full", values="Usage",
                 title="Region-wise Total Share",
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 hole=0.35)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Month-wise Trends
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("📅 Month-wise Consumption Trends")
MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
md = (df.groupby(["Year","Month","Month_Name"])["Usage"].sum()
        .reset_index()
        .sort_values(["Year","Month"]))
md["Month_Name"] = pd.Categorical(md["Month_Name"], categories=MONTH_ORDER, ordered=True)
fig = px.line(md, x="Month_Name", y="Usage", color="Year",
              markers=True,
              labels={"Month_Name":"Month","Usage":"Total Consumption (MU)"},
              title="Monthly Electricity Consumption — 2019 & 2020",
              color_discrete_sequence=["#3498db","#e67e22"],
              height=420)
fig.update_layout(xaxis_tickangle=-30,
                  plot_bgcolor="white", paper_bgcolor="white",
                  hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Before & After Lockdown
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🔒 Before & After Lockdown Analysis")
col_l1, col_l2 = st.columns(2)

with col_l1:
    ld = (df.groupby(["Region_Full","Lockdown"])["Usage"].sum().reset_index())
    fig = px.bar(ld, x="Region_Full", y="Usage", color="Lockdown",
                 barmode="group",
                 labels={"Region_Full":"Region","Usage":"Total Consumption (MU)"},
                 title="Before vs After Lockdown — Region-wise",
                 color_discrete_map={
                     "Before Lockdown":"#27ae60",
                     "After Lockdown" :"#c0392b"
                 })
    fig.update_layout(xaxis_tickangle=-30,
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col_l2:
    ld2 = (df.groupby("Lockdown")["Usage"].sum().reset_index())
    fig = px.pie(ld2, names="Lockdown", values="Usage",
                 title="Overall Split — Before vs After Lockdown",
                 color_discrete_map={
                     "Before Lockdown":"#27ae60",
                     "After Lockdown" :"#c0392b"
                 }, hole=0.4)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Quarter Usage
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("📆 Quarterly Consumption")
qd = (df.groupby(["Year","Quarter"])["Usage"].sum().reset_index())
qd["Period"] = qd["Year"].astype(str) + " Q" + qd["Quarter"].astype(str)
fig = px.line(qd, x="Period", y="Usage", color="Year",
              markers=True,
              labels={"Period":"Quarter","Usage":"Total Consumption (MU)"},
              title="Quarterly Electricity Consumption",
              color_discrete_sequence=["#9b59b6","#1abc9c"],
              height=380)
fig.update_layout(hovermode="x unified",
                  plot_bgcolor="white", paper_bgcolor="white")
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Top N / Bottom N
# ══════════════════════════════════════════════════════════════════════════════
st.subheader(f"🏆 Top {N_val} & Bottom {N_val} States")
state_totals = df.groupby("States")["Usage"].sum().reset_index()
top_df = state_totals.nlargest(N_val, "Usage")
bot_df = state_totals.nsmallest(N_val, "Usage").sort_values("Usage")

col_t, col_b = st.columns(2)
with col_t:
    fig = px.bar(top_df.sort_values("Usage"), x="Usage", y="States",
                 orientation="h",
                 color="Usage", color_continuous_scale="Greens",
                 title=f"Top {N_val} States",
                 labels={"Usage":"Total Consumption (MU)"})
    fig.update_layout(coloraxis_showscale=False,
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig = px.bar(bot_df, x="Usage", y="States",
                 orientation="h",
                 color="Usage", color_continuous_scale="Reds",
                 title=f"Bottom {N_val} States",
                 labels={"Usage":"Total Consumption (MU)"})
    fig.update_layout(coloraxis_showscale=False,
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Metro Cities
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🏙️ Metro City States")
METRO = ["Delhi","Maharashtra","Tamil Nadu","West Bengal","Karnataka","Telangana"]
metro_df = (df[df["States"].isin(METRO)]
            .groupby(["States","Year"])["Usage"]
            .sum().reset_index())
fig = px.bar(metro_df, x="States", y="Usage", color="Year", barmode="group",
             labels={"Usage":"Total Consumption (MU)"},
             title="Metro City States — Yearly Consumption",
             color_discrete_sequence=["#8e44ad","#f39c12"])
fig.update_layout(xaxis_tickangle=-20,
                  plot_bgcolor="white", paper_bgcolor="white")
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9: Heatmap — Region × State
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🗂️ Region × State Usage Heatmap")
heat = (df.groupby(["States","Region_Full"])["Usage"].sum().reset_index())
pivot = heat.pivot(index="States", columns="Region_Full", values="Usage").fillna(0)
fig = px.imshow(pivot,
                color_continuous_scale="YlOrRd",
                labels={"color":"Consumption (MU)"},
                title="State vs Region — Electricity Consumption Heatmap",
                height=700,
                aspect="auto")
fig.update_xaxes(tickangle=-30)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10: Raw Data Table + Download
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("📋 Filtered Data Table")
show_cols = ["States","Regions","Region_Full","Dates","Year","Month_Name",
             "Quarter","Usage","Lockdown","Is_Metro"]
st.dataframe(
    df[show_cols].sort_values(["Dates","States"]).reset_index(drop=True),
    use_container_width=True, height=300
)

csv_data = df[show_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_consumption.csv",
    mime="text/csv",
)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#95a5a6;font-size:13px;'>"
    "India Electricity Consumption Analytics | Data: 2019–2020 | Built with Streamlit &amp; Plotly"
    "</p>",
    unsafe_allow_html=True,
)
