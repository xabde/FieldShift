import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import date

st.set_page_config(page_title="FieldShift | Farm Digital Twin", layout="wide", page_icon="🌱")

# ---------- Professional Design System (Slate & Emerald) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    /* Unified Professional Palette */
    --bg-app: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-subtle: #F1F5F9;
    --border: #E2E8F0;
    --border-focus: #166534;
    
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #64748B;
    
    --accent: #166534;
    --accent-hover: #14532D;
    --accent-soft: #DCFCE7;
    
    --danger: #DC2626;
    --warning: #D97706;
    --info: #0284C7;
}

/* Base App Styling */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: var(--bg-app) !important;
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    color: var(--text-primary) !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.75rem !important;
}
h1 { font-size: 2.25rem !important; }
h2 { font-size: 1.75rem !important; }
h3 { font-size: 1.25rem !important; }

p, label, div {
    color: var(--text-secondary) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
}
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption {
    color: var(--text-secondary) !important;
}

/* Form Inputs (Selectbox, Text Input, Number Input) */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
input, textarea {
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover,
input:hover, textarea:hover {
    border-color: var(--text-muted) !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within,
input:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: var(--text-primary) !important;
    fill: var(--text-primary) !important;
}

/* Buttons */
button[kind="primary"] {
    background-color: var(--accent) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--accent) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
button[kind="primary"]:hover {
    background-color: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
}
button[kind="secondary"] {
    background-color: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}
button[kind="secondary"]:hover {
    background-color: var(--bg-subtle) !important;
    border-color: var(--text-muted) !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    padding: 20px 24px !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label p {
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    color: var(--text-primary) !important;
    font-size: 1.75rem !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 500 !important;
}

/* Custom Editorial Cards */
.fs-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    padding: 24px;
    border-radius: 8px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.fs-tag {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
    background-color: var(--accent-soft);
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
}
.fs-big {
    color: var(--text-primary);
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 12px;
}
.fs-muted {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 0;
}
.fs-meta {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 8px;
}

/* Alerts */
div[data-testid="stAlert"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--info) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
}
div[data-testid="stAlert"] p {
    color: var(--text-secondary) !important;
}

/* Tabs */
div[data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 8px !important;
}
button[data-baseweb="tab"] {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"] p {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: var(--bg-app) !important;
    border-bottom: 2px solid var(--accent) !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: var(--accent) !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"]:hover {
    background-color: var(--bg-subtle) !important;
}
button[data-baseweb="tab"]:hover p {
    color: var(--text-primary) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background-color: var(--bg-subtle) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    font-size: 0.9rem !important;
}

/* Expander */
details {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    margin-top: 16px !important;
}
summary {
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    cursor: pointer !important;
}
summary:hover {
    color: var(--accent) !important;
}

/* Dividers */
hr {
    border-color: var(--border) !important;
    margin: 2.5rem 0 !important;
    opacity: 1 !important;
}

/* Slider */
div[data-baseweb="slider"] > div {
    background-color: var(--border) !important;
}
div[data-baseweb="slider"] [role="slider"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* Checkbox / Radio */
div[data-baseweb="checkbox"] > div,
div[data-baseweb="radio"] > div {
    border-color: var(--border) !important;
}
div[data-baseweb="checkbox"][aria-checked="true"] > div,
div[data-baseweb="radio"][aria-checked="true"] > div {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Data helpers ----------
LOCATIONS = {
    "Settat, Morocco": (33.001, -7.616),
    "Berrechid, Morocco": (33.265, -7.587),
    "Beni Mellal, Morocco": (32.337, -6.349),
    "Kénitra, Morocco": (34.261, -6.580),
    "Meknès, Morocco": (33.893, -5.547),
    "Marrakech, Morocco": (31.629, -7.981),
}

def demo_climate(years=10, seed=14):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=years * 12, freq="MS")
    month = dates.month
    temp = 18 + 10 * np.sin((month - 4) / 12 * 2 * np.pi) + rng.normal(0, 1.7, len(dates))
    rain_season = np.where((month >= 10) | (month <= 4), 1, 0)
    rain = np.maximum(0, rain_season * (28 + 18 * np.sin((month + 1) / 6 * np.pi)) + rng.normal(0, 13, len(dates)))
    rain = rain * (1 - np.linspace(0, 0.12, len(dates)))
    return pd.DataFrame({"date": dates, "temperature": temp, "rainfall": rain})

@st.cache_data(ttl=3600)
def nasa_power(lat, lon, start_year, end_year):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": str(start_year),
        "end": str(end_year),
        "format": "JSON"
    }
    r = requests.get(url, params=params, timeout=25)
    r.raise_for_status()
    data = r.json()["properties"]["parameter"]
    t = data.get("T2M", {})
    p = data.get("PRECTOTCORR", {})
    s = data.get("ALLSKY_SFC_SW_DWN", {})
    rows = []
    for key in sorted(set(t) | set(p) | set(s)):
        if key.endswith("13"):
            continue
        try:
            dt = pd.to_datetime(key, format="%Y%m")
        except ValueError:
            continue
        rain_mm_day = float(p.get(key, np.nan))
        rain_mm_month = rain_mm_day * dt.days_in_month if rain_mm_day != -999 else np.nan
        rows.append({
            "date": dt,
            "temperature": float(t.get(key, np.nan)),
            "rainfall": rain_mm_month,
            "solar": float(s.get(key, np.nan)),
        })
    df = pd.DataFrame(rows).replace(-999, np.nan).dropna(subset=["temperature", "rainfall"])
    return df

def crop_score(crop, climate, priority, soil, irrigation):
    temp_mean = float(climate.temperature.mean())
    rain_annual = float(climate.groupby(climate.date.dt.year).rainfall.sum().mean())
    moisture_stress = max(0, min(100, (650 - rain_annual) / 6.5))
    soil_bonus = {"Clay": 4, "Loam": 10, "Sandy": -4, "Unknown": 0}.get(soil, 0)
    water_penalty = {"Low": 0, "Medium": 12, "High": 24}[crop["water"]]
    irrigation_bonus = {"Rainfed": 0, "Limited": 5, "Available": 12}[irrigation]
    nitrogen_bonus = 12 if crop["legume"] else 0
    cover_bonus = 8 if crop["cover"] else 0
    climate_fit = max(0, 100 - abs(temp_mean - crop["temp_opt"]) * 5 - moisture_stress * 0.35)
    water_score = max(0, 100 - water_penalty - moisture_stress * 0.35 + irrigation_bonus)
    soil_score = max(0, min(100, 55 + nitrogen_bonus + cover_bonus + soil_bonus))
    weights = {"Water": (0.55, 0.25, 0.20), "Soil": (0.20, 0.55, 0.25), "Balanced": (0.35, 0.35, 0.30)}
    w = weights[priority]
    total = w[0] * water_score + w[1] * soil_score + w[2] * climate_fit
    return {
        "score": round(total, 1),
        "water": round(water_score, 1),
        "soil": round(soil_score, 1),
        "climate": round(climate_fit, 1),
        "stress": round(moisture_stress, 1),
    }

CROPS = {
    "Wheat": {"water": "High", "legume": False, "cover": False, "temp_opt": 17},
    "Chickpea": {"water": "Low", "legume": True, "cover": False, "temp_opt": 18},
    "Lentil": {"water": "Low", "legume": True, "cover": False, "temp_opt": 16},
    "Barley": {"water": "Medium", "legume": False, "cover": False, "temp_opt": 16},
    "Cover crop mix": {"water": "Medium", "legume": True, "cover": True, "temp_opt": 15},
    "Faba bean": {"water": "Medium", "legume": True, "cover": False, "temp_opt": 15},
}

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("###  FieldShift")
    st.caption("Farm Digital Twin · Prototype")
    st.markdown("---")
    location = st.selectbox("Farm location", list(LOCATIONS.keys()), index=0)
    lat, lon = LOCATIONS[location]
    farm_name = st.text_input("Farm name", "Chaouia Field 01")
    hectares = st.number_input("Farm size (ha)", min_value=0.1, max_value=10000.0, value=12.0, step=1.0)
    soil = st.selectbox("Soil texture", ["Unknown", "Clay", "Loam", "Sandy"], index=2)
    irrigation = st.selectbox("Water access", ["Rainfed", "Limited", "Available"])
    priority = st.select_slider(
        "Farmer priority",
        options=["Water", "Balanced", "Soil"],
        value="Balanced",
        help="Water = conserve water | Soil = prioritize soil-supporting rotations"
    )
    st.markdown("---")
    years = st.slider("Historical window (years)", 5, 20, 10)
    use_live = st.toggle("Fetch live NASA POWER data", value=False)
    st.caption("Live mode requires internet access. Demo mode uses illustrative data.")

# ---------- Header ----------
st.markdown('<div class="fs-tag">NASA Earth Observation / Agronomic Decision Support</div>', unsafe_allow_html=True)
st.title(f"FieldShift — {farm_name}")
st.markdown("Review local environmental history and compare crop rotation scenarios before making a field decision.")
st.markdown(f'<div class="fs-meta">{location} · {lat:.3f}, {lon:.3f} · {hectares:g} ha · {soil} soil</div>', unsafe_allow_html=True)

# ---------- Data ----------
data_mode = "Illustrative demo"
climate = None
if use_live:
    try:
        end_year = date.today().year - 1
        start_year = end_year - years + 1
        climate = nasa_power(lat, lon, start_year, end_year)
        data_mode = f"NASA POWER live monthly data ({start_year}–{end_year})"
        st.success(f"NASA POWER data loaded ({start_year}–{end_year}).")
    except Exception as e:
        st.warning(f"NASA request could not be completed ({e}). Showing illustrative demo data.")
if climate is None:
    climate = demo_climate(years)

climate = climate.copy()
climate["year"] = climate.date.dt.year
climate["month"] = climate.date.dt.month

annual = climate.groupby("year").agg(rainfall=("rainfall", "sum"), temperature=("temperature", "mean")).reset_index()
rain_avg = annual.rainfall.mean()
temp_avg = climate.temperature.mean()
rain_delta = (annual.rainfall.iloc[-1] - annual.rainfall.iloc[0]) if len(annual) > 1 else 0
heat_months = int((climate.temperature > 30).sum())

# ---------- Overview ----------
st.markdown("---")
st.markdown("### 1. Earth Memory — Climate History")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mean temperature", f"{temp_avg:.1f} °C")
m2.metric("Annual rainfall", f"{rain_avg:.0f} mm")
m3.metric("Rainfall change (1st to last yr)", f"{rain_delta:+.0f} mm")
m4.metric("Hot months (>30 °C)", f"{heat_months}")

left, right = st.columns([1.6, 1])
with left:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=annual.year, y=annual.rainfall, name="Rainfall (mm)", marker_color="#15803D"))
    fig.add_trace(go.Scatter(
        x=annual.year, y=annual.temperature, name="Mean temp (°C)", yaxis="y2",
        line=dict(color="#0284C7", width=2.5), marker=dict(size=6)
    ))
    fig.update_layout(
        title=dict(text="Annual rainfall and mean temperature", font=dict(size=15, color="#0F172A", family="IBM Plex Sans")),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#0F172A", family="IBM Plex Sans"),
        legend=dict(orientation="h", y=1.12, font=dict(color="#475569")),
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(tickfont=dict(color="#475569"), linecolor="#E2E8F0"),
        yaxis=dict(title="Rainfall (mm)", title_font=dict(color="#475569"), tickfont=dict(color="#475569"), gridcolor="#F1F5F9"),
        yaxis2=dict(title="Temperature (°C)", title_font=dict(color="#475569"), tickfont=dict(color="#475569"), overlaying="y", side="right", showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown(
        '<div class="fs-card">'
        '<div class="fs-tag">Field Signal</div>'
        '<div class="fs-big">Multi-year context matters.</div>'
        '<p class="fs-muted">A single season is not a trend. Comparing multiple years highlights structural shifts in rainfall and heat while keeping data limitations visible.</p>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("**Data provenance**")
    st.caption(f"Source mode: {data_mode}")
    st.caption("POWER: monthly point data (T2M, PRECTOTCORR). Demo values are synthetic and must not be presented as NASA observations.")
    st.caption("Satellite pixels and climate grids are not equivalent to field measurements.")

# ---------- Environmental pressure ----------
st.markdown("---")
st.markdown("### 2. Soil Debt — Environmental Pressure")
st.markdown("A transparent screening indicator of environmental pressure, not a laboratory soil-health measurement.")

recent = climate.tail(24)
rain_recent = float(recent.rainfall.sum())
rain_baseline = float(climate.head(max(24, len(climate) // 2)).rainfall.sum())
rain_pressure = max(0, min(100, (rain_baseline - rain_recent) / max(rain_baseline, 1) * 100))
heat_pressure = max(0, min(100, (recent.temperature.mean() - 20) * 5))
bare_days_proxy = max(0, min(100, 100 - rain_recent / 6))
pressure = float(np.mean([rain_pressure, heat_pressure, bare_days_proxy]))

c1, c2, c3 = st.columns(3)
c1.metric("Rainfall pressure proxy", f"{rain_pressure:.0f} / 100")
c2.metric("Heat pressure proxy", f"{heat_pressure:.0f} / 100")
c3.metric("Soil Debt index", f"{pressure:.0f} / 100")

figp = go.Figure(go.Indicator(
    mode="gauge+number",
    value=pressure,
    number={"font": {"color": "#0F172A", "family": "IBM Plex Mono"}},
    title={"text": "Environmental Pressure Index (experimental)", "font": {"size": 14, "color": "#0F172A", "family": "IBM Plex Sans"}},
    gauge={
        "axis": {"range": [0, 100], "tickcolor": "#64748B", "tickfont": {"color": "#475569"}},
        "bar": {"color": "#166534"},
        "steps": [
            {"range": [0, 35], "color": "#DCFCE7"},
            {"range": [35, 65], "color": "#FEF9C3"},
            {"range": [65, 100], "color": "#FEE2E2"}
        ]
    }
))
figp.update_layout(paper_bgcolor="#FFFFFF", font=dict(color="#0F172A"), height=240, margin=dict(t=45, b=10, l=25, r=25))
st.plotly_chart(figp, use_container_width=True)
st.info("Interpretation: this index is a prototype composite of climate proxies. It does not diagnose soil organic matter, salinity, nutrients, compaction, or actual soil health. Calibration and local agronomic validation are required.")

# ---------- What-if lab ----------
st.markdown("---")
st.markdown("### 3. What If? — Rotation Laboratory")
st.markdown("Compare rotation scenarios against your baseline. Scores are heuristic screening indicators, not yield forecasts.")

existing = st.multiselect("Current rotation (reference)", list(CROPS.keys()), default=["Wheat", "Wheat", "Wheat"], max_selections=3)
if not existing:
    existing = ["Wheat"]
scenario_a = existing
scenario_b = ["Wheat", "Chickpea", "Wheat"]
scenario_c = ["Barley", "Lentil", "Cover crop mix"]
custom = st.multiselect("Build your own alternative", list(CROPS.keys()), default=["Wheat", "Faba bean", "Barley"], max_selections=3)
scenarios = {
    "A · Current": scenario_a,
    "B · Legume rotation": scenario_b,
    "C · Water/cover strategy": scenario_c,
    "D · Custom experiment": custom or scenario_c
}

def rotation_metrics(rot):
    vals = [crop_score(CROPS[x], climate, priority, soil, irrigation) for x in rot]
    return {
        "Scenario": " -> ".join(rot),
        "Score": np.mean([x["score"] for x in vals]),
        "Water": np.mean([x["water"] for x in vals]),
        "Soil": np.mean([x["soil"] for x in vals]),
        "Climate": np.mean([x["climate"] for x in vals]),
        "Legume share (%)": round(sum(CROPS[x]["legume"] for x in rot) / len(rot) * 100, 1),
        "Crop diversity": len(set(rot))
    }

rows = []
for label, rot in scenarios.items():
    mm = rotation_metrics(rot)
    mm["Scenario"] = label
    mm["Sequence"] = " -> ".join(rot)
    rows.append(mm)

res = pd.DataFrame(rows)
for col in ["Score", "Water", "Soil", "Climate"]:
    res[col] = res[col].round(1)

st.dataframe(
    res[["Scenario", "Sequence", "Score", "Water", "Soil", "Climate", "Legume share (%)", "Crop diversity"]],
    hide_index=True,
    use_container_width=True
)

figs = px.bar(
    res, x="Scenario", y="Score", color_discrete_sequence=["#166534"]
)
figs.update_layout(
    title=dict(text="Scenario screening score (0–100)", font=dict(size=15, color="#0F172A", family="IBM Plex Sans")),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font=dict(color="#0F172A", family="IBM Plex Sans"),
    xaxis=dict(title="", tickfont=dict(color="#475569"), linecolor="#E2E8F0"),
    yaxis=dict(title="Score", range=[0, 100], title_font=dict(color="#475569"), tickfont=dict(color="#475569"), gridcolor="#F1F5F9"),
    margin=dict(t=55, b=20, l=20, r=20)
)
st.plotly_chart(figs, use_container_width=True)

best = res.sort_values("Score", ascending=False).iloc[0]
st.markdown(
    f'<div class="fs-card">'
    f'<div class="fs-tag">Top-Scoring Option</div>'
    f'<div class="fs-big">{best["Scenario"]} ({best["Sequence"]})</div>'
    f'<p class="fs-muted">Highest screening score under the selected priority (<b>{priority}</b>) and current climate inputs. This score reflects water, soil-support proxies, and climate-fit assumptions—not a guaranteed outcome.</p>'
    f'</div>',
    unsafe_allow_html=True
)

with st.expander("How rotations are scored"):
    st.markdown("""
    - **Water score:** crop water class, climate moisture-stress proxy, and irrigation availability.
    - **Soil-support score:** legume/cover-crop traits and user-selected soil texture.
    - **Climate-fit score:** distance between mean temperature and an illustrative crop optimum, adjusted for rainfall stress.
    - **Priority weights:** Water (55/25/20), Soil (20/55/25), Balanced (35/35/30) across Water, Soil, and Climate dimensions.

    These are demonstration assumptions, not calibrated Moroccan agronomic coefficients. Replace them with locally validated parameters before operational use.
    """)

# ---------- Time machine / explanation ----------
st.markdown("---")
st.markdown("### 4. Farm Time Machine")
t1, t2, t3 = st.tabs(["Past · Memory", "Present · Signals", "Future · Scenarios"])
with t1:
    st.write("**Past:** explore annual climate patterns and compare early vs. recent periods.")
    if len(annual) >= 4:
        split = max(2, len(annual) // 2)
        old = annual.iloc[:split].rainfall.mean()
        new = annual.iloc[split:].rainfall.mean()
        st.metric("Mean annual rainfall (early vs. recent)", f"{old:.0f} → {new:.0f} mm", f"{new-old:+.0f} mm")
with t2:
    st.write("**Present:** latest available monthly climate values.")
    st.dataframe(
        climate.tail(6)[["date", "temperature", "rainfall"]].rename(
            columns={"date": "Month", "temperature": "Temperature (°C)", "rainfall": "Rainfall (mm)"}
        ),
        hide_index=True,
        use_container_width=True
    )
with t3:
    st.write("**Future:** scenario outcomes are conditional simulations, not predictions.")
    st.write("Adjust rotation, soil context, irrigation, and farmer priority above to compare dimension scores.")

st.markdown("---")
st.markdown("### 5. Decision Transparency & Limitations")
st.markdown("""
**Before acting, review:**
- Local planting calendar and cultivar suitability;
- Laboratory soil test (pH, organic carbon, nutrients, salinity, texture);
- Field pest and disease history;
- Water rights/availability, equipment, labor, and market demand;
- Crop-specific rooting depth, residue management, and nutrient needs;
- Satellite data resolution, missing observations, and uncertainty.
""")
st.warning("FieldShift is an educational decision-support prototype. It does not replace farmers, agronomists, laboratory soil tests, or local extension services.")

st.markdown("<div style='text-align:center;color:#64748B;font-size:0.84rem;padding:24px 0;'>FieldShift — Agronomic Decision Support Prototype</div>", unsafe_allow_html=True)