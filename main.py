import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from streamlit_folium import st_folium
from folium.plugins import MeasureControl, Fullscreen, MousePosition
import branca.colormap as bcm
from scipy import stats
import os, warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(page_title="Tunisia Climate WebGIS", page_icon="🌍",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════
# CSS — Glassmorphism · Neon Glow · Animations
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

@keyframes glow-pulse {
  0%,100% { box-shadow: 0 0 8px rgba(56,189,248,0.25),0 0 20px rgba(56,189,248,0.08); }
  50%      { box-shadow: 0 0 20px rgba(56,189,248,0.55),0 0 50px rgba(56,189,248,0.18); }
}
@keyframes border-glow {
  0%,100% { border-color: rgba(56,189,248,0.18); }
  50%      { border-color: rgba(56,189,248,0.55); }
}
@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes float-up {
  0%,100% { transform: translateY(0px); }
  50%      { transform: translateY(-5px); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes fade-in {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
@keyframes risk-pulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(248,113,113,0.4); }
  70%      { box-shadow: 0 0 0 10px rgba(248,113,113,0); }
}

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* ── Layout ── */
.block-container { padding: 3.5rem 2rem 2rem; max-width: 1700px; }
.stApp {
  background: radial-gradient(ellipse at 20% 20%, #071828 0%, #060d1a 40%, #04080f 100%);
  min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #040c18 0%, #060e1c 100%);
  border-right: 1px solid rgba(56,189,248,0.1);
  backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] .stRadio label {
  font-size: 12.5px; color: #64748b; padding: 8px 12px;
  border-radius: 10px; transition: all 0.2s; display: block;
  margin: 2px 0; border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(56,189,248,0.06); color: #94a3b8;
  border-color: rgba(56,189,248,0.12);
}
[data-testid="stSidebar"] * { color: #94a3b8; }

/* ── Hero ── */
.hero {
  background: linear-gradient(135deg,
    rgba(56,189,248,0.05) 0%, rgba(129,140,248,0.04) 50%, rgba(52,211,153,0.03) 100%);
  border: 1px solid rgba(56,189,248,0.15);
  border-radius: 24px; padding: 36px 48px 30px;
  margin-bottom: 28px; text-align: center;
  animation: fade-in 0.6s ease both;
  position: relative; overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, rgba(56,189,248,0.03), transparent);
  animation: shimmer 4s linear infinite;
  background-size: 200% 100%;
}
.hero-title {
  font-size: 42px; font-weight: 900;
  background: linear-gradient(90deg, #38bdf8 0%, #818cf8 40%, #34d399 80%, #38bdf8 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 6s linear infinite;
  margin: 0 0 10px; line-height: 1.15;
}
.hero-badges { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 12px; }
.hero-badge {
  background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2);
  border-radius: 20px; padding: 4px 14px; font-size: 11px; color: #38bdf8;
  font-weight: 600; letter-spacing: 0.5px;
}
.hero-sub { color: #475569; font-size: 14px; margin: 0; }

/* ── Glass Card ── */
.glass-card {
  background: rgba(15,23,42,0.6);
  border: 1px solid rgba(56,189,248,0.12);
  border-radius: 20px; padding: 22px 24px;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  animation: fade-in 0.5s ease both;
}
.glass-card:hover {
  border-color: rgba(56,189,248,0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(56,189,248,0.08);
}

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 24px; }
.kpi-card {
  background: rgba(10,17,30,0.8);
  border: 1px solid rgba(56,189,248,0.12);
  border-radius: 18px; padding: 18px 20px;
  transition: all 0.3s ease;
  position: relative; overflow: hidden;
  animation: fade-in 0.4s ease both;
}
.kpi-card::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(56,189,248,0.4), transparent);
}
.kpi-card:hover {
  border-color: rgba(56,189,248,0.35);
  transform: translateY(-3px);
  box-shadow: 0 12px 36px rgba(56,189,248,0.1);
  animation: glow-pulse 2s ease infinite;
}
.kpi-icon { font-size: 18px; margin-bottom: 8px; }
.kpi-label { font-size: 9.5px; text-transform: uppercase; letter-spacing: 1.2px; color: #334155; font-weight: 700; margin-bottom: 6px; }
.kpi-value { font-size: 28px; font-weight: 800; color: #f1f5f9; line-height: 1; }
.kpi-unit { font-size: 11px; color: #475569; margin-left: 3px; font-weight: 500; }
.kpi-delta { font-size: 10.5px; margin-top: 6px; font-weight: 600; }
.kpi-delta.up { color: #34d399; } .kpi-delta.down { color: #f87171; }

/* ── Section headers ── */
.sec-header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 22px; padding-bottom: 14px;
  border-bottom: 1px solid rgba(56,189,248,0.08);
  animation: fade-in 0.4s ease;
}
.sec-icon { font-size: 24px; animation: float-up 3s ease infinite; }
.sec-title { font-size: 22px; font-weight: 800; color: #e2e8f0; margin: 0; }
.sec-sub { font-size: 12px; color: #475569; margin: 2px 0 0; }

/* ── Info box ── */
.info-box {
  background: linear-gradient(135deg, rgba(56,189,248,0.05), rgba(129,140,248,0.03));
  border: 1px solid rgba(56,189,248,0.14); border-radius: 14px;
  padding: 13px 18px; margin-bottom: 18px; font-size: 13px; color: #64748b;
  animation: fade-in 0.5s ease;
}

/* ── Risk indicators ── */
.risk-high  { background:rgba(248,113,113,0.12); color:#f87171; border:1px solid rgba(248,113,113,0.25); border-radius:20px; padding:3px 12px; font-size:11px; font-weight:700; display:inline-block; animation: risk-pulse 2s infinite; }
.risk-med   { background:rgba(251,191,36,0.12);  color:#fbbf24; border:1px solid rgba(251,191,36,0.25);  border-radius:20px; padding:3px 12px; font-size:11px; font-weight:700; display:inline-block; }
.risk-low   { background:rgba(52,211,153,0.12);  color:#34d399; border:1px solid rgba(52,211,153,0.25);  border-radius:20px; padding:3px 12px; font-size:11px; font-weight:700; display:inline-block; }

/* ── Metrics ── */
div[data-testid="metric-container"] {
  background: rgba(10,17,30,0.8); border: 1px solid rgba(56,189,248,0.1);
  border-radius: 16px; padding: 14px 18px;
  transition: all 0.3s; animation: fade-in 0.5s ease;
}
div[data-testid="metric-container"]:hover {
  border-color: rgba(56,189,248,0.28); transform: translateY(-2px);
}
div[data-testid="metric-container"] label { color:#475569!important; font-size:10px!important; text-transform:uppercase; letter-spacing:1px; }
div[data-testid="metric-container"] [data-testid="metric-value"] { color:#f1f5f9!important; font-size:24px!important; font-weight:800!important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
  background: transparent; color: #475569;
  border-radius: 10px 10px 0 0; padding: 9px 20px;
  font-size: 12.5px; font-weight: 600;
  border: 1px solid transparent; transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
  background: rgba(56,189,248,0.08)!important;
  color: #38bdf8!important; border-color: rgba(56,189,248,0.2)!important;
}
.stTabs [data-baseweb="tab"]:hover { color: #94a3b8; background: rgba(56,189,248,0.04)!important; }

/* ── Map iframe ── */
iframe { border-radius: 18px!important; border: 1px solid rgba(56,189,248,0.1)!important; }

/* ── Selectbox / inputs ── */
.stSelectbox>div>div, .stMultiSelect>div>div {
  background: rgba(10,17,30,0.9); border: 1px solid rgba(56,189,248,0.14);
  border-radius: 12px; color: #e2e8f0;
}
.stSlider [data-baseweb="slider"] { color: #38bdf8; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #04080f; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

/* ── Sidebar logo ── */
.sb-logo { text-align:center; padding:20px 0 24px; border-bottom:1px solid rgba(56,189,248,0.08); margin-bottom:18px; }
.sb-logo-icon { font-size:36px; animation: float-up 4s ease infinite; display:block; }
.sb-logo-title { font-size:14px; font-weight:800; color:#38bdf8; margin-top:8px; }
.sb-logo-ver   { font-size:10px; color:#1e3a5f; margin-top:4px; }

/* ── Trend badge ── */
.trend-up   { color:#34d399; font-weight:700; }
.trend-down { color:#f87171; font-weight:700; }
.trend-flat { color:#fbbf24; font-weight:700; }

/* ── Chart container ── */
.chart-wrap {
  background: rgba(10,17,30,0.5); border: 1px solid rgba(56,189,248,0.07);
  border-radius: 18px; padding: 4px; margin-bottom: 16px;
  animation: fade-in 0.6s ease;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#64748b", family="Inter, sans-serif", size=11),
    title_font=dict(color="#e2e8f0", size=15, family="Inter, sans-serif"),
    legend=dict(bgcolor="rgba(10,17,30,0.85)", bordercolor="rgba(56,189,248,0.15)",
                borderwidth=1, font=dict(size=11)),
    xaxis=dict(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
               tickfont=dict(size=10)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.03)", linecolor="rgba(255,255,255,0.06)",
               tickfont=dict(size=10)),
    margin=dict(l=50, r=30, t=55, b=50),
    hoverlabel=dict(bgcolor="rgba(10,17,30,0.95)", bordercolor="rgba(56,189,248,0.3)",
                    font=dict(color="#e2e8f0", size=12)),
)

C_PALETTE = ["#38bdf8","#818cf8","#34d399","#fb923c","#f472b6","#fbbf24","#a78bfa","#22d3ee","#86efac","#fdba74"]
SEASON_COLORS = {"Winter":"#818cf8","Spring":"#34d399","Summer":"#fb923c","Autumn":"#f59e0b"}
SEAS_DASH  = {"Winter":"solid","Spring":"dash","Summer":"dot","Autumn":"dashdot"}
SEAS_SYM   = {"Winter":"circle","Spring":"square","Summer":"diamond","Autumn":"cross"}
MONTHS     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
BASE       = "data"
SHAPE_DIR  = os.path.join(BASE,"shapefiles")
NASA_DIR   = os.path.join(BASE,"nasa_power")
PRED_DIR   = os.path.join(BASE,"predictions")
EXCEL_PATH = os.path.join(BASE,"Prediction_2030_2035","Prediction_2030_2035.xlsx")

# ═══════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_shapes():
    t = gpd.read_file(os.path.join(SHAPE_DIR,"Tunisia_adm.shp"))
    b = gpd.read_file(os.path.join(SHAPE_DIR,"Basins.shp"))
    s = gpd.read_file(os.path.join(SHAPE_DIR,"StudyZone.shp"))
    return t, b, s

@st.cache_data(show_spinner=False)
def load_excel(): return pd.read_excel(EXCEL_PATH)

@st.cache_data(show_spinner=False)
def load_csv(path):
    df = pd.read_csv(path)
    for col in ("Date","ds"):
        if col in df.columns:
            df["Date"] = pd.to_datetime(df[col], errors="coerce"); break
    return df

_ok = True
try:
    tunisia, basins, study_zone = load_shapes()
    pred_df = load_excel()
except Exception as e:
    _ok = False
    st.error(f"⚠️ Could not load spatial data: {e}")

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
def num_cols(df, exclude=()):
    return [c for c in df.select_dtypes(include=np.number).columns if c not in exclude]

def add_trend(df, col):
    try:
        x = np.arange(len(df)); c = np.polyfit(x, df[col], 2)
        df = df.copy(); df["__trend__"] = np.poly1d(c)(x)
    except: df["__trend__"] = np.nan
    return df

def add_season(df, date_col="Date"):
    df = df.copy()
    m = df[date_col].dt.month
    df["Season"] = np.select(
        [m.isin([12,1,2]),m.isin([3,4,5]),m.isin([6,7,8]),m.isin([9,10,11])],
        ["Winter","Spring","Summer","Autumn"], default="Unknown")
    df["Year"]  = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["DOY"]   = df[date_col].dt.dayofyear
    return df

def monthly_clim(df, col):
    df["_m"] = df["Date"].dt.month
    return df.groupby("_m")[col].agg(["mean","std"]).reset_index().rename(columns={"_m":"month"})

def idw_fast(x, y, z, xi, yi, power=2):
    from scipy.spatial import cKDTree
    tree = cKDTree(np.c_[x,y])
    k = min(12, len(x))
    d, idx = tree.query(np.c_[xi,yi], k=k, workers=-1)
    d = np.where(d==0, 1e-12, d)
    w = 1.0/d**power
    return np.sum(w*z[idx],axis=1)/np.sum(w,axis=1)

def scatter_stats(a, b):
    mask = ~(np.isnan(a)|np.isnan(b)); a,b = a[mask],b[mask]
    if len(a)<3: return None
    sl,ic,r,*_ = stats.linregress(a,b)
    return sl, ic, r**2, np.sqrt(np.mean((a-b)**2))

def mann_kendall(data):
    data = np.array(data).astype(float)
    data = data[~np.isnan(data)]
    n = len(data)
    if n < 4: return 0, 1, "N/A"
    s = sum(np.sign(data[j]-data[i]) for i in range(n-1) for j in range(i+1,n))
    vs = n*(n-1)*(2*n+5)/18
    z = (s-1)/np.sqrt(vs) if s>0 else (s+1)/np.sqrt(vs) if s<0 else 0.0
    p = 2*(1-stats.norm.cdf(abs(z)))
    trend = ("Increasing ↑" if z>0 else "Decreasing ↓") if p<0.05 else "No trend →"
    return z, p, trend

def resolve_col(df, *candidates):
    cl = {c.lower():c for c in df.columns}
    for cand in candidates:
        if cand in df.columns: return cand
        if cand.lower() in cl: return cl[cand.lower()]
    for cand in candidates:
        for col in df.columns:
            if cand.lower() in col.lower() or col.lower() in cand.lower(): return col
    return None

COL_ALIASES = {
    "H_max_m":  ["H_max_m","H_max","Hmax","alt_max"],
    "H_min_m":  ["H_min_m","H_min","Hmin","alt_min"],
    "Pente":    ["Pente","pente_moy","slope"],
    "Area_km2": ["Area_km2","Area","superficie","aire_km2"],
    "Perimetre_km": ["Perimetre_km","Perimetre","Perimeter"],
    "Compaction_Index": ["Compaction_Index","Kc","Gravelius","Compact"],
    "Elongation_Ratio": ["Elongation_Ratio","Re","elongation"],
    "Circularity":  ["Circularity","Rc","circularite"],
    "Relief_Ratio": ["Relief_Ratio","Rh","relief_ratio"],
    "Hypsometric_Integral": ["Hypsometric_Integral","HI","hypsometric"],
    "Drainage_density": ["Drainage_density","drainage_d","Dd"],
    "Stream_frequency": ["Stream_frequency","stream_f","Fs"],
    "Tc_Tixeront":  ["Tc_Tixeront","temps_conc","Tc"],
    "Debit_de_pointe": ["Debit_de_pointe","debit","peak_flow","Qp"],
    "Drainage_texture": ["Drainage_texture","drainage_t"],
    "Constant_Channel_maintenance": ["Constant_Channel_maintenance","constant_c","maintenance","Cm"],
    "Relative_relief":  ["Relative_relief","relative_r","Rrel"],
    "Ruggedness_number":["Ruggedness_number","ruggedness","Rn"],
    "Name": ["Name","name","Nom","nom","Basin"],
}
def rc(df, canon): return resolve_col(df, *COL_ALIASES.get(canon,[canon]))

def compute_risk(df):
    df = df.copy()
    risk_def = {
        "Pente":("pos",rc(df,"Pente")), "Drainage_density":("pos",rc(df,"Drainage_density")),
        "Debit_de_pointe":("pos",rc(df,"Debit_de_pointe")), "Relief_Ratio":("pos",rc(df,"Relief_Ratio")),
        "Tc_Tixeront":("neg",rc(df,"Tc_Tixeront")),
    }
    present = [(s,c) for _,(s,c) in risk_def.items() if c]
    if len(present)<2: df["Risk_Score"]=np.nan; return df
    score = pd.Series(np.zeros(len(df)),index=df.index)
    for sign,col in present:
        rng = df[col].max()-df[col].min()
        if rng>0:
            norm=(df[col]-df[col].min())/rng
            score = score+norm if sign=="pos" else score-norm
    df["Risk_Score"]=(score-score.min())/(score.max()-score.min()+1e-9)
    return df

# ── UI helpers ──
def section(icon, title, sub=""):
    st.markdown(f"""
    <div class="sec-header">
      <span class="sec-icon">{icon}</span>
      <div><div class="sec-title">{title}</div>
      {'<div class="sec-sub">'+sub+'</div>' if sub else ''}</div>
    </div>""", unsafe_allow_html=True)

def kpi_card(label, value, unit="", delta=None, up=True, icon=""):
    d = f'<div class="kpi-delta {"up" if up else "down"}">{"▲" if up else "▼"} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card">
      {'<div class="kpi-icon">'+icon+'</div>' if icon else ''}
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
      {d}
    </div>""", unsafe_allow_html=True)


CHART_EXPLANATIONS = {
    "dual_profile": (
        "**Dual-axis profile** — bars show the absolute magnitude of the primary parameter across basins; "
        "the line overlays a secondary parameter on a different scale (right axis). "
        "Useful for spotting basins where both attributes are simultaneously elevated."
    ),
    "altitudinal": (
        "**Altitudinal profile** — the shaded band represents the elevation range (H_max - H_min) for each basin. "
        "Taller bands indicate higher relief energy and greater potential for flash floods. "
        "Basins are sorted by H_max (descending). Formula: Relief = H_max - H_min."
    ),
    "relative_relief": (
        "**Relative relief (Rrel, m/km)** — ratio of max height difference to basin perimeter. "
        "High Rrel = steep terrain = faster runoff concentration. Formula: Rrel = (H_max - H_min) / Perimeter."
    ),
    "hypsometric": (
        "**Hypsometric Integral (HI)** classifies basin geomorphological maturity: "
        "HI > 0.60 = Youth (tectonically active, high erosion); "
        "0.35-0.60 = Equilibrium; HI < 0.35 = Monadnock/Old age (depositional). "
        "Formula: HI = (H_mean - H_min) / (H_max - H_min)."
    ),
    "risk_ranking": (
        "**Hydrological Risk Score (0-1)** — normalised composite of slope, drainage density, "
        "concentration time (inverse), peak discharge, and relief ratio. "
        "Score = weighted sum of normalised factors. Red > 0.70 (High) | Yellow 0.40-0.70 (Medium) | Green < 0.40 (Low)."
    ),
    "critical_scatter": (
        "**Slope x Peak Discharge** — basins in the top-right quadrant combine steep slopes with high "
        "peak discharge = prime flash-flood candidates. Bubble size = basin area; colour = relief ratio."
    ),
    "area_tc": (
        "**Area vs Concentration Time** — larger basins generally have longer Tc. "
        "Deviations reveal basins that respond faster/slower than their size suggests "
        "(driven by slope, drainage density, channel roughness). Bubble size = Gravelius Index (Kc)."
    ),
    "shape_scatter": (
        "**Compaction Index (Kc) vs Elongation Ratio (Re)** — describes basin shape: "
        "Kc=1, Re~1 = circular basin (rapid peaked response); Kc>1.5, Re<0.5 = elongated (attenuated response). "
        "Vertical dashed line marks the theoretical circle (Kc=1). Colour = concentration time; size = area."
    ),
    "drainage_law": (
        "**Drainage Law** — Constant of Channel Maintenance C = 1/Dd = minimum area per unit channel length. "
        "Higher Dd (lower C) = denser network = faster storm response. "
        "Regression line shows the empirical relationship for these basins."
    ),
    "radar": (
        "**Spider/Radar chart** — each polygon = one basin; each axis = normalised (0-1) morphometric parameter. "
        "Larger polygons indicate overall higher morpho-hydrological intensity. "
        "Overlapping polygons share similar hydrological signatures."
    ),
    "correlation": (
        "**Pearson correlation matrix** (lower triangle) — red = strong positive (r near +1); "
        "blue = strong negative (r near -1); white/pale = weak relationship. "
        "Values with |r| > 0.7 are physically meaningful. Correlation does not imply causation."
    ),
    "regression": (
        "**OLS Regression** — ordinary least-squares fit. R2 = fraction of variance explained (0=none, 1=perfect). "
        "p-value < 0.05 indicates statistical significance. "
        "Bubble size = basin area. Points far from the line are morphometric outliers."
    ),
    "pca": (
        "**PCA Biplot** — Principal Component Analysis compresses the parameter space into two orthogonal axes "
        "(PC1, PC2) capturing maximum variance. Arrows = variable contributions (length proportional to weight). "
        "Clustered points share similar morpho-hydrological profiles."
    ),
    "parallel": (
        "**Parallel Coordinates** — each vertical axis = one parameter; each line = one basin. "
        "Crossing lines = inverse relationships; parallel lines = correlations. "
        "Colour = selected target variable. Drag axis handles to interactively filter ranges."
    ),
    "scatter_matrix": (
        "**Scatter Matrix (SPLOM)** — all pairwise scatterplots in a grid. "
        "Diagonal = marginal distribution of each variable. "
        "A quick overview of all bivariate relationships across selected parameters."
    ),
    "3d_scatter": (
        "**3D Scatter** — three parameters on X/Y/Z axes; colour and size encode a 4th and 5th variable. "
        "Rotate the plot to find 3D clusters invisible in 2D projections."
    ),
}


def explain(key: str):
    """Render a styled explanatory caption beneath a chart."""
    text = CHART_EXPLANATIONS.get(key, "")
    if not text:
        return
    st.markdown(
        f'<div style="background:rgba(10,20,40,0.55);border-left:3px solid rgba(56,189,248,0.4);'        f'border-radius:0 10px 10px 0;padding:10px 14px;margin:-2px 0 18px;'        f'font-size:12px;color:#64748b;line-height:1.65">{text}</div>',
        unsafe_allow_html=True
    )


def kpi_row(cards):
    cols = st.columns(len(cards))
    for col, args in zip(cols, cards):
        with col: kpi_card(*args)

def trend_badge(z, p):
    if p >= 0.05: return '<span class="trend-flat">→ No Trend</span>'
    return f'<span class="trend-{"up" if z>0 else "down"}">{"↑ Increasing" if z>0 else "↓ Decreasing"} (p={p:.3f})</span>'

def wrap_chart(fig, height=None):
    if height: fig.update_layout(height=height)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <span class="sb-logo-icon">🌍</span>
      <div class="sb-logo-title">Tunisia Climate WebGIS</div>
      <div class="sb-logo-ver">AI · Spatial · v1.1 · 2025</div>
    </div>""", unsafe_allow_html=True)

    menu = st.radio("", [
        "🏠  Dashboard",
        "🛰️  NASA Time Series",
        "🔮  Prediction Series",
        "🌿  Seasonal Analysis",
        "🌡️  Climate Trends",
        "🎬  Animation Studio",
        "🗺️  Prediction Mapping",
        "🌊  Basins Mapping",
        "🏔️  Morpho-Hydrology",
        "📊  NASA vs Prediction",
    ], label_visibility="collapsed")

    st.markdown("---")
    with st.expander("⚙️ Global settings"):
        ALPHA = st.slider("Chart opacity", 0.5, 1.0, 0.85, 0.05)
        SHOW_TREND = st.checkbox("Show trend lines", True)
        ANIM_SPEED = st.slider("Animation speed (ms)", 100, 800, 300, 50)

PAGE = menu.split("  ",1)[-1]

# ═══════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-title">🌍 Tunisia Climate &amp; WebGIS Intelligence</div>
  <p class="hero-sub">AI-Powered Climate Prediction · Morpho-Hydrological Analysis · Animated Spatial Analytics</p>
  <div class="hero-badges">
    <span class="hero-badge">🛰️ NASA POWER</span>
    <span class="hero-badge">🔮 NeuralProphet</span>
    <span class="hero-badge">📡 WebGIS</span>
    <span class="hero-badge">🏔️ Morpho-Hydrology</span>
    <span class="hero-badge">🎬 Animated Charts</span>
  </div>
</div>""", unsafe_allow_html=True)

# ╔═══════════════════════════════════════════════════════╗
# ║  🏠 DASHBOARD                                         ║
# ╚═══════════════════════════════════════════════════════╝
if PAGE == "Dashboard":
    section("🏠", "Overview Dashboard", "System summary · KPIs · Quick analytics")

    nasa_files = sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    pred_files = sorted([f for f in os.listdir(PRED_DIR) if f.endswith(".csv")]) if os.path.isdir(PRED_DIR) else []

    # ── Global KPIs ──
    kpi_row([
        ("NASA Stations",  str(len(nasa_files)), " files", None, True, "🛰️"),
        ("Pred Datasets",  str(len(pred_files)), " files", None, True, "🔮"),
        ("Basins",  str(len(basins)) if _ok else "—", " basins", None, True, "🌊"),
        ("Status", "Online" if _ok else "⚠️ Error", "", None, _ok, "✅"),
        ("Platform", "v2.0", "", None, True, "🚀"),
    ])
    st.markdown("")

    if nasa_files and pred_files:
        c1, c2 = st.columns(2)
        with c1:
            sel_f = st.selectbox("Quick preview — NASA file", nasa_files, key="db_nasa")
        with c2:
            df_q = load_csv(os.path.join(NASA_DIR, sel_f))
            col_q = st.selectbox("Parameter", num_cols(df_q), key="db_par")

        df_q = add_trend(df_q, col_q)
        df_q = add_season(df_q)

        # ── Animated area chart ──
        fig_dash = go.Figure()
        fig_dash.add_trace(go.Scatter(
            x=df_q["Date"], y=df_q[col_q], mode="lines", name=col_q,
            line=dict(color="#38bdf8", width=1.6),
            fill="tozeroy", fillcolor="rgba(56,189,248,0.05)"
        ))
        if SHOW_TREND:
            fig_dash.add_trace(go.Scatter(
                x=df_q["Date"], y=df_q["__trend__"], mode="lines", name="Trend",
                line=dict(color="#f472b6", width=2.5, dash="dot")
            ))
        fig_dash.update_layout(height=300, title=f"📈 {col_q} Overview — {sel_f}", **PLOT_LAYOUT)
        wrap_chart(fig_dash)

        # ── Side-by-side: seasonal pie + monthly bar ──
        c1, c2, c3 = st.columns(3)
        with c1:
            seas_mean = df_q.groupby("Season")[col_q].mean()
            fig_pie = go.Figure(go.Pie(
                labels=seas_mean.index, values=seas_mean.values,
                marker_colors=[SEASON_COLORS[s] for s in seas_mean.index],
                hole=0.55, textinfo="label+percent",
                textfont=dict(size=11)
            ))
            fig_pie.update_layout(height=280, title="Seasonal Share",
                                   showlegend=False, **PLOT_LAYOUT)
            wrap_chart(fig_pie)

        with c2:
            clim = monthly_clim(df_q, col_q)
            fig_bar = go.Figure(go.Bar(
                x=MONTHS, y=clim["mean"],
                marker_color=[f"rgba(56,189,248,{0.4+0.05*i})" for i in range(12)],
                error_y=dict(type="data", array=clim["std"], color="rgba(255,255,255,0.2)")
            ))
            fig_bar.update_layout(height=280, title="Monthly Climatology", **PLOT_LAYOUT)
            wrap_chart(fig_bar)

        with c3:
            ann = df_q.groupby("Year")[col_q].mean().reset_index()
            z_mk, p_mk, tr_mk = mann_kendall(ann[col_q].values)
            fig_ann = go.Figure()
            fig_ann.add_trace(go.Scatter(
                x=ann["Year"], y=ann[col_q], mode="lines+markers", name="Annual mean",
                line=dict(color="#34d399", width=2), marker=dict(size=5)
            ))
            fig_ann.update_layout(height=280, title="Annual Mean", **PLOT_LAYOUT)
            wrap_chart(fig_ann)
            st.markdown(f"**Mann-Kendall:** {trend_badge(z_mk, p_mk)}", unsafe_allow_html=True)

        # ── Gauges ──
        if _ok and "Risk_Score" in compute_risk(basins).columns:
            bdf_g = compute_risk(basins)
            name_c = rc(bdf_g,"Name")
            mean_risk = bdf_g["Risk_Score"].mean()
            max_risk  = bdf_g["Risk_Score"].max()
            high_risk = (bdf_g["Risk_Score"]>0.7).sum()

            st.markdown("### ⚠️ Basin Risk Overview")
            gc1, gc2, gc3 = st.columns(3)
            for gcol, val, title, ref in [
                (gc1, mean_risk*100, "Average Risk", 50),
                (gc2, max_risk*100,  "Peak Risk",    70),
                (gc3, high_risk,     "High-Risk Basins", 0),
            ]:
                with gcol:
                    fig_g = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=round(val,1),
                        title=dict(text=title, font=dict(color="#94a3b8", size=13)),
                        number=dict(font=dict(color="#f1f5f9", size=28)),
                        gauge=dict(
                            axis=dict(range=[0,100 if title!="High-Risk Basins" else len(bdf_g)],
                                      tickcolor="#334155", tickfont=dict(color="#475569")),
                            bar=dict(color="#38bdf8", thickness=0.25),
                            bgcolor="rgba(15,23,42,0)",
                            bordercolor="rgba(56,189,248,0.1)",
                            steps=[
                                dict(range=[0,40], color="rgba(52,211,153,0.12)"),
                                dict(range=[40,70], color="rgba(251,191,36,0.12)"),
                                dict(range=[70,100], color="rgba(248,113,113,0.12)"),
                            ],
                            threshold=dict(line=dict(color="#f87171",width=3), thickness=0.7, value=70)
                        )
                    ))
                    fig_g.update_layout(height=230, **PLOT_LAYOUT)
                    fig_g.update_layout(margin=dict(l=20,r=20,t=60,b=10))
                    wrap_chart(fig_g)

    # ── Dashboard extra: Radar seasonal comparison + waterfall ──
    if nasa_files:
        st.markdown("---")
        st.markdown("### 🕸️ Seasonal Radar & 📊 Parameter Waterfall")
        c_rad, c_wat = st.columns(2)

        # Radar: seasonal profile of selected station
        with c_rad:
            df_rad = load_csv(os.path.join(NASA_DIR, sel_f if 'sel_f' in dir() else nasa_files[0]))
            p_rad  = col_q if 'col_q' in dir() else num_cols(df_rad)[0]
            df_rad = add_season(df_rad)
            clim_rad = monthly_clim(df_rad, p_rad)
            r_vals_r = list(clim_rad["mean"]) + [clim_rad["mean"].iloc[0]]
            theta_r  = MONTHS + [MONTHS[0]]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=r_vals_r, theta=theta_r, mode="lines+markers", fill="toself",
                fillcolor="rgba(56,189,248,0.1)", name=p_rad,
                line=dict(color="#38bdf8", width=2.5),
                marker=dict(size=7, color="#38bdf8", line=dict(color="white", width=1.5))
            ))
            fig_radar.update_layout(
                height=310, title=f"{p_rad} — Seasonal Radar",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#475569", size=8)),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=9),
                                     direction="clockwise")
                ),
                **PLOT_LAYOUT
            )
            wrap_chart(fig_radar)

        # Waterfall: monthly cumulative anomaly
        with c_wat:
            df_wf = df_rad.copy()
            baseline_wf = df_wf[p_rad].mean()
            monthly_anom = df_wf.groupby("Month")[p_rad].mean() - baseline_wf
            values_wf = list(monthly_anom)
            fig_wf = go.Figure(go.Waterfall(
                x=MONTHS, y=values_wf,
                measure=["relative"]*12,
                connector=dict(line=dict(color="rgba(255,255,255,0.08)", width=1)),
                increasing=dict(marker=dict(color="#34d399")),
                decreasing=dict(marker=dict(color="#f87171")),
                totals=dict(marker=dict(color="#818cf8")),
                text=[f"{v:+.3f}" for v in values_wf],
                textposition="outside", textfont=dict(color="white", size=9)
            ))
            fig_wf.update_layout(height=310, title=f"{p_rad} — Monthly Anomaly Waterfall",
                                  showlegend=False, **PLOT_LAYOUT)
            wrap_chart(fig_wf)


elif PAGE == "NASA Time Series":
    section("🛰️","NASA Climate Time Series","Raw observations from NASA POWER")

    nasa_files = sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    if not nasa_files: st.warning("No NASA CSV files found."); st.stop()

    c1,c2,c3 = st.columns([2,2,1])
    with c1: station = st.selectbox("Station",nasa_files,key="ns")
    df = load_csv(os.path.join(NASA_DIR,station))
    cols = num_cols(df)
    with c2: param = st.selectbox("Parameter",cols,key="np")
    with c3: smooth = st.slider("Smoothing",1,90,1)

    df = add_trend(df,param); df_s = add_season(df)
    if smooth>1: df["__smooth__"] = df[param].rolling(smooth,center=True,min_periods=1).mean()

    pct=(df[param].iloc[-1]-df[param].iloc[0])/abs(df[param].iloc[0])*100 if df[param].iloc[0]!=0 else 0
    z_mk,p_mk,tr_mk = mann_kendall(df[param].dropna().values)

    kpi_row([
        ("Mean",    f"{df[param].mean():.3f}", "", None, True, "📊"),
        ("Max",     f"{df[param].max():.3f}",  "", None, True, "⬆️"),
        ("Min",     f"{df[param].min():.3f}",  "", None, False,"⬇️"),
        ("Std Dev", f"{df[param].std():.3f}",  "", None, True, "📉"),
        ("Total Δ", f"{pct:+.1f}",  "%", f"{pct:.1f}%", pct>=0,"📈"),
    ])
    st.markdown(f"**Trend:** {trend_badge(z_mk,p_mk)} &nbsp;|&nbsp; **Z={z_mk:.2f}** &nbsp;|&nbsp; **p={p_mk:.4f}**",
                unsafe_allow_html=True)
    st.markdown("")

    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "📈 Time Series","🌡️ Climatology","🔄 Repeatability",
        "📉 Rolling Trend","📅 Calendar","🎬 Animated Replay","🔴 Anomaly Detection"
    ])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"],y=df[param],mode="lines",name=param,
            line=dict(color="#38bdf8",width=1.5),fill="tozeroy",fillcolor="rgba(56,189,248,0.05)"))
        if smooth>1:
            fig.add_trace(go.Scatter(x=df["Date"],y=df["__smooth__"],mode="lines",
                name=f"{smooth}d smooth",line=dict(color="#fbbf24",width=2.2)))
        if SHOW_TREND:
            fig.add_trace(go.Scatter(x=df["Date"],y=df["__trend__"],mode="lines",name="Quadratic trend",
                line=dict(color="#f472b6",width=2.2,dash="dot")))
        fig.update_layout(height=420,title=f"{param} — {station}",**PLOT_LAYOUT)
        wrap_chart(fig)

        c1,c2 = st.columns(2)
        with c1:
            fig2=go.Figure(go.Histogram(x=df[param],nbinsx=45,
                marker=dict(color="#818cf8",opacity=0.8,line=dict(color="rgba(129,140,248,0.5)",width=0.5))))
            fig2.update_layout(height=260,title="Distribution",**PLOT_LAYOUT)
            wrap_chart(fig2)
        with c2:
            ann=df_s.groupby("Year")[param].agg(["mean","std"]).reset_index()
            fig3=go.Figure()
            fig3.add_trace(go.Scatter(x=ann["Year"],y=ann["mean"],mode="lines+markers",
                name="Annual mean",line=dict(color="#34d399",width=2),marker=dict(size=6)))
            fig3.add_trace(go.Scatter(
                x=pd.concat([ann["Year"],ann["Year"][::-1]]),
                y=pd.concat([ann["mean"]+ann["std"],(ann["mean"]-ann["std"])[::-1]]),
                fill="toself",fillcolor="rgba(52,211,153,0.07)",
                line=dict(color="rgba(0,0,0,0)"),name="±1σ",hoverinfo="skip"))
            fig3.update_layout(height=260,title="Annual Mean ± σ",**PLOT_LAYOUT)
            wrap_chart(fig3)

    with tab2:
        clim=monthly_clim(df.copy(),param)
        fig_c=go.Figure()
        fig_c.add_trace(go.Scatter(
            x=list(range(1,13))+list(range(12,0,-1)),
            y=list(clim["mean"]+clim["std"])+list((clim["mean"]-clim["std"])[::-1]),
            fill="toself",fillcolor="rgba(56,189,248,0.08)",
            line=dict(color="rgba(0,0,0,0)"),hoverinfo="skip",name="±1σ"))
        fig_c.add_trace(go.Scatter(x=clim["month"],y=clim["mean"],mode="lines+markers",
            name="Monthly mean",line=dict(color="#38bdf8",width=2.5),
            marker=dict(size=8,color="#38bdf8",line=dict(color="white",width=1.5))))
        fig_c.update_layout(height=360,title=f"{param} — Monthly Climatology (Mean ± 1σ)",**PLOT_LAYOUT)
        fig_c.update_xaxes(tickmode="array",tickvals=list(range(1,13)),ticktext=MONTHS)
        wrap_chart(fig_c)

        seas_mean=df_s.groupby("Season")[param].mean().reindex(["Winter","Spring","Summer","Autumn"])
        fig_sb=go.Figure(go.Bar(x=seas_mean.index,y=seas_mean.values,
            marker_color=[SEASON_COLORS[s] for s in seas_mean.index],
            text=[f"{v:.3f}" for v in seas_mean.values],textposition="outside",
            marker_line_color="rgba(255,255,255,0.1)",marker_line_width=0.5))
        fig_sb.update_layout(height=290,title="Seasonal Mean",**PLOT_LAYOUT)
        wrap_chart(fig_sb)

    with tab3:
        import plotly.colors as pc
        years=sorted(df_s["Year"].dropna().unique())
        n_yr=max(len(years),2)
        year_colors=pc.sample_colorscale("Turbo",[i/(n_yr-1) for i in range(n_yr)])
        fig_rep=go.Figure()
        for i,yr in enumerate(years):
            g=df_s[df_s["Year"]==yr].sort_values("DOY")
            fig_rep.add_trace(go.Scatter(x=g["DOY"],y=g[param],mode="lines",name=str(int(yr)),
                line=dict(color=year_colors[i],width=1.2),
                showlegend=(i % max(n_yr//8,1)==0)))
        fig_rep.update_layout(height=420,title=f"{param} — Year-by-Year Repeatability",**PLOT_LAYOUT)
        fig_rep.update_xaxes(title_text="Day of Year"); fig_rep.update_yaxes(title_text=param)
        wrap_chart(fig_rep)

    with tab4:
        rw=st.slider("Rolling window (days)",30,730,365,30)
        df_r=df.copy()
        df_r["rolling"]=df_r[param].rolling(rw,center=True,min_periods=20).mean()
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatter(x=df_r["Date"],y=df_r[param],mode="lines",name="Raw",
            line=dict(color="rgba(56,189,248,0.3)",width=1)))
        fig_r.add_trace(go.Scatter(x=df_r["Date"],y=df_r["rolling"],mode="lines",
            name=f"{rw}d mean",line=dict(color="#38bdf8",width=2.5)))
        if SHOW_TREND:
            fig_r.add_trace(go.Scatter(x=df_r["Date"],y=df_r["__trend__"],mode="lines",
                name="Trend",line=dict(color="#f472b6",width=2,dash="dot")))
        fig_r.update_layout(height=400,title=f"{param} — Trend vs Seasonality",**PLOT_LAYOUT)
        wrap_chart(fig_r)

    with tab5:
        st.markdown('<div class="info-box">📅 GitHub-style calendar heatmap — daily intensity across the full year. Select year to explore.</div>',unsafe_allow_html=True)
        avail_years=sorted(df_s["Year"].dropna().unique().astype(int))
        if avail_years:
            sel_yr=st.selectbox("Year",avail_years,index=len(avail_years)-1)
            dy=df_s[df_s["Year"]==sel_yr].copy()
            dy["Week"]=dy["Date"].dt.isocalendar().week.astype(int)
            dy["DayOfWeek"]=dy["Date"].dt.dayofweek
            piv=dy.pivot_table(index="DayOfWeek",columns="Week",values=param,aggfunc="mean")
            fig_cal=go.Figure(go.Heatmap(
                z=piv.values, x=piv.columns.tolist(), y=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][:len(piv)],
                colorscale="Blues",showscale=True,
                colorbar=dict(title=param,thickness=12,len=0.8)))
            fig_cal.update_layout(height=260,title=f"{param} — Calendar Heatmap {sel_yr}",**PLOT_LAYOUT)
            fig_cal.update_xaxes(title_text="Week of Year")
            wrap_chart(fig_cal)

    # ── Tab 6: Animated Replay ──
    with tab6:
        st.markdown('<div class="info-box">🎬 Watch the time series build year by year. Use the ▶ Play button or drag the year slider below the chart.</div>', unsafe_allow_html=True)
        import plotly.colors as pc
        years_anim = sorted(df_s["Year"].dropna().unique().astype(int))
        if len(years_anim) < 2:
            st.info("Need at least 2 years of data for animation.")
        else:
            frames_anim = []
            for yr in years_anim:
                sub = df[df["Date"].dt.year <= yr].copy()
                frames_anim.append(go.Frame(
                    data=[
                        go.Scatter(x=sub["Date"], y=sub[param], mode="lines", name=param,
                            line=dict(color="#38bdf8", width=1.8),
                            fill="tozeroy", fillcolor="rgba(56,189,248,0.07)"),
                        go.Scatter(x=sub["Date"], y=sub["__trend__"], mode="lines", name="Trend",
                            line=dict(color="#f472b6", width=2, dash="dot"))
                    ],
                    name=str(yr)
                ))
            fig_anim = go.Figure(
                data=frames_anim[0].data,
                frames=frames_anim,
                layout=go.Layout(
                    height=440, title=f"{param} — {station} · Animated Replay",
                    updatemenus=[dict(
                        type="buttons", showactive=False,
                        bgcolor="rgba(10,17,30,0.9)", bordercolor="rgba(56,189,248,0.2)",
                        font=dict(color="#e2e8f0"),
                        x=0.12, y=1.14, xanchor="right",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": ANIM_SPEED, "redraw": True},
                                              "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"mode": "immediate", "frame": {"duration": 0}}])
                        ]
                    )],
                    sliders=[dict(
                        currentvalue=dict(prefix="Year: ", font=dict(color="#94a3b8", size=12)),
                        pad=dict(b=10, t=10),
                        bgcolor="#0f172a", bordercolor="#1e3a5f",
                        activebgcolor="#38bdf8",
                        font=dict(color="#64748b", size=10),
                        steps=[dict(args=[[f.name], {"frame": {"duration": 300}, "mode": "immediate"}],
                                    method="animate", label=f.name) for f in frames_anim]
                    )]
                )
            )
            fig_anim.update_layout(**PLOT_LAYOUT)
            wrap_chart(fig_anim)

    # ── Tab 7: Anomaly Detection ──
    with tab7:
        st.markdown('<div class="info-box">🔴 Anomalies detected using a rolling μ ± n·σ envelope. Points outside the band are flagged as outliers.</div>', unsafe_allow_html=True)
        c1a, c2a = st.columns([2, 1])
        with c1a: sigma_n = st.slider("Sigma threshold (n)", 1.0, 4.0, 2.5, 0.1)
        with c2a: roll_w  = st.slider("Rolling window (days)", 30, 365, 90, 15)

        df_ano = df[["Date", param]].copy().dropna()
        df_ano["roll_mean"] = df_ano[param].rolling(roll_w, center=True, min_periods=20).mean()
        df_ano["roll_std"]  = df_ano[param].rolling(roll_w, center=True, min_periods=20).std()
        df_ano["upper"] = df_ano["roll_mean"] + sigma_n * df_ano["roll_std"]
        df_ano["lower"] = df_ano["roll_mean"] - sigma_n * df_ano["roll_std"]
        df_ano["is_anomaly"] = (df_ano[param] > df_ano["upper"]) | (df_ano[param] < df_ano["lower"])
        df_ano["type"] = np.where(df_ano[param] > df_ano["upper"], "High anomaly",
                          np.where(df_ano[param] < df_ano["lower"], "Low anomaly", "Normal"))

        fig_ano = go.Figure()
        # Uncertainty band
        fig_ano.add_trace(go.Scatter(
            x=pd.concat([df_ano["Date"], df_ano["Date"][::-1]]),
            y=pd.concat([df_ano["upper"], df_ano["lower"][::-1]]),
            fill="toself", fillcolor="rgba(56,189,248,0.06)",
            line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", name=f"±{sigma_n}σ band"
        ))
        # Envelope lines
        fig_ano.add_trace(go.Scatter(x=df_ano["Date"], y=df_ano["upper"], mode="lines",
            line=dict(color="rgba(56,189,248,0.25)", width=1, dash="dot"), name="Upper bound", showlegend=False))
        fig_ano.add_trace(go.Scatter(x=df_ano["Date"], y=df_ano["lower"], mode="lines",
            line=dict(color="rgba(56,189,248,0.25)", width=1, dash="dot"), name="Lower bound", showlegend=False))
        # Raw signal
        fig_ano.add_trace(go.Scatter(x=df_ano["Date"], y=df_ano[param], mode="lines", name="Signal",
            line=dict(color="rgba(148,163,184,0.5)", width=1)))
        # Rolling mean
        fig_ano.add_trace(go.Scatter(x=df_ano["Date"], y=df_ano["roll_mean"], mode="lines", name="Rolling mean",
            line=dict(color="#38bdf8", width=2)))
        # High anomalies
        hi_ano = df_ano[df_ano["type"] == "High anomaly"]
        fig_ano.add_trace(go.Scatter(x=hi_ano["Date"], y=hi_ano[param], mode="markers",
            name=f"High anomaly ({len(hi_ano)})",
            marker=dict(color="#f87171", size=5, symbol="circle", line=dict(color="white", width=0.5))))
        # Low anomalies
        lo_ano = df_ano[df_ano["type"] == "Low anomaly"]
        fig_ano.add_trace(go.Scatter(x=lo_ano["Date"], y=lo_ano[param], mode="markers",
            name=f"Low anomaly ({len(lo_ano)})",
            marker=dict(color="#818cf8", size=5, symbol="triangle-down", line=dict(color="white", width=0.5))))

        fig_ano.update_layout(height=460, title=f"{param} — Anomaly Detection (±{sigma_n}σ, {roll_w}d window)", **PLOT_LAYOUT)
        wrap_chart(fig_ano)

        kpi_row([
            ("High Anomalies", str(len(hi_ano)), "", None, False, "🔴"),
            ("Low Anomalies",  str(len(lo_ano)), "", None, True,  "🔵"),
            ("Normal Points",  str((df_ano["is_anomaly"]==False).sum()), "", None, True, "🟢"),
            ("Anomaly Rate",   f"{100*df_ano['is_anomaly'].mean():.1f}", "%", None, False, "📊"),
            ("Window σ",       f"{sigma_n}", "σ", None, True, "🎯"),
        ])

        if len(df_ano[df_ano["is_anomaly"]]) > 0:
            st.markdown("##### 🔍 Top Anomalous Events")
            top_ano = df_ano[df_ano["is_anomaly"]].copy()
            top_ano["deviation"] = (top_ano[param] - top_ano["roll_mean"]).abs()
            st.dataframe(
                top_ano.nlargest(15, "deviation")[["Date", param, "roll_mean", "type", "deviation"]]
                .rename(columns={"roll_mean": "Expected", "deviation": "|Δ|"})
                .round(4).reset_index(drop=True),
                use_container_width=True, height=300
            )

# ╔═══════════════════════════════════════════════════════╗
# ║  🔮 PREDICTION TIME SERIES                            ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "Prediction Series":
    section("🔮","Prediction Climate Time Series","NeuralProphet forecasts 2030–2035")

    pred_files=sorted([f for f in os.listdir(PRED_DIR) if f.endswith(".csv")]) if os.path.isdir(PRED_DIR) else []
    if not pred_files: st.warning("No prediction CSV files found."); st.stop()

    c1,c2,c3=st.columns([2,2,1])
    with c1: station=st.selectbox("Dataset",pred_files,key="prs")
    df=load_csv(os.path.join(PRED_DIR,station))
    cols=num_cols(df)
    with c2: param=st.selectbox("Parameter",cols,key="prp")
    with c3: show_ci=st.checkbox("±σ band",True)

    df=add_trend(df,param); df_s=add_season(df)
    df["__lo__"]=df[param].rolling(30,center=True,min_periods=1).mean()-df[param].rolling(30,center=True,min_periods=1).std()
    df["__hi__"]=df[param].rolling(30,center=True,min_periods=1).mean()+df[param].rolling(30,center=True,min_periods=1).std()
    pct=(df[param].iloc[-1]-df[param].iloc[0])/abs(df[param].iloc[0])*100 if df[param].iloc[0]!=0 else 0

    kpi_row([
        ("Projected Mean",f"{df[param].mean():.3f}","",None,True,"🔮"),
        ("Peak Value",    f"{df[param].max():.3f}","",None,True,"⬆️"),
        ("Min Value",     f"{df[param].min():.3f}","",None,False,"⬇️"),
        ("Variability",   f"{df[param].std():.3f}","",None,True,"📉"),
        ("Proj. Change",  f"{pct:+.1f}","%",f"{pct:.1f}%",pct>=0,"📈"),
    ])

    tab1,tab2,tab3,tab4,tab5=st.tabs(["📈 Forecast","🌡️ Climatology","🎬 Animated Evolution","🕯️ Candlestick","🌐 Polar Seasonal"])

    with tab1:
        fig=go.Figure()
        if show_ci:
            fig.add_trace(go.Scatter(
                x=pd.concat([df["Date"],df["Date"][::-1]]),
                y=pd.concat([df["__hi__"],df["__lo__"][::-1]]),
                fill="toself",fillcolor="rgba(52,211,153,0.07)",
                line=dict(color="rgba(0,0,0,0)"),hoverinfo="skip",name="±σ"))
        fig.add_trace(go.Scatter(x=df["Date"],y=df[param],mode="lines",name=param,
            line=dict(color="#34d399",width=2)))
        if SHOW_TREND:
            fig.add_trace(go.Scatter(x=df["Date"],y=df["__trend__"],mode="lines",name="Trend",
                line=dict(color="#f472b6",width=2.2,dash="dot")))
        fig.update_layout(height=400,title=f"{param} — {station} (Predicted)",**PLOT_LAYOUT)
        wrap_chart(fig)

        c1,c2=st.columns(2)
        with c1:
            fig_v=go.Figure()
            for seas,col in SEASON_COLORS.items():
                sg=df_s[df_s["Season"]==seas][param].dropna()
                if not sg.empty:
                    fig_v.add_trace(go.Violin(y=sg,name=seas,line_color=col,
                        fillcolor=f"rgba{tuple(int(col.lstrip('#')[i:i+2],16) for i in (0,2,4))+(0.18,)}",
                        box_visible=True,meanline_visible=True,points=False))
            fig_v.update_layout(height=300,title="Seasonal Violin",**PLOT_LAYOUT)
            wrap_chart(fig_v)
        with c2:
            clim=monthly_clim(df.copy(),param)
            fig_c=go.Figure()
            fig_c.add_trace(go.Scatter(
                x=list(range(1,13))+list(range(12,0,-1)),
                y=list(clim["mean"]+clim["std"])+list((clim["mean"]-clim["std"])[::-1]),
                fill="toself",fillcolor="rgba(52,211,153,0.08)",
                line=dict(color="rgba(0,0,0,0)"),hoverinfo="skip",name="±1σ"))
            fig_c.add_trace(go.Scatter(x=clim["month"],y=clim["mean"],mode="lines+markers",
                name="Monthly mean",line=dict(color="#34d399",width=2.5),marker=dict(size=7)))
            fig_c.update_layout(height=300,title="Monthly Climatology",**PLOT_LAYOUT)
            fig_c.update_xaxes(tickmode="array",tickvals=list(range(1,13)),ticktext=MONTHS)
            wrap_chart(fig_c)

    with tab2:
        seas_mean=df_s.groupby("Season")[param].mean().reindex(["Winter","Spring","Summer","Autumn"])
        c1,c2=st.columns(2)
        with c1:
            fig_sun=go.Figure(go.Sunburst(
                labels=["All","Winter","Spring","Summer","Autumn"]+MONTHS,
                parents=["","All","All","All","All"]+
                        ["Winter"]*3+["Spring"]*3+["Summer"]*3+["Autumn"]*3,
                values=[df_s[param].sum()]+
                       [df_s[df_s["Season"]==s][param].sum() for s in ["Winter","Spring","Summer","Autumn"]]+
                       [df_s[df_s["Month"]==m][param].sum() for m in [12,1,2,3,4,5,6,7,8,9,10,11]],
                branchvalues="total",
                marker=dict(colors=["#0f172a","#818cf8","#34d399","#fb923c","#f59e0b"]+
                            ["#818cf8"]*3+["#34d399"]*3+["#fb923c"]*3+["#f59e0b"]*3,
                            line=dict(color="#0f172a",width=1)),
                textfont=dict(size=11)
            ))
            fig_sun.update_layout(height=350,title="Seasonal Sunburst",**PLOT_LAYOUT)
            wrap_chart(fig_sun)
        with c2:
            fig_bar=go.Figure(go.Bar(
                x=seas_mean.index,y=seas_mean.values,
                marker_color=[SEASON_COLORS[s] for s in seas_mean.index],
                text=[f"{v:.3f}" for v in seas_mean.values],textposition="outside",
                marker_line_color="rgba(255,255,255,0.1)",marker_line_width=0.5))
            fig_bar.update_layout(height=350,title="Seasonal Average",**PLOT_LAYOUT)
            wrap_chart(fig_bar)

    with tab3:
        st.markdown('<div class="info-box">🎬 Animated monthly evolution by year — press ▶ Play to watch the forecast unfold.</div>',unsafe_allow_html=True)
        agg_anim=df_s.groupby(["Year","Month"])[param].mean().reset_index()
        agg_anim["Month_name"]=agg_anim["Month"].apply(lambda x: MONTHS[x-1])
        if len(agg_anim)>0:
            fig_anim=px.bar(agg_anim,x="Month_name",y=param,animation_frame="Year",
                color=param,color_continuous_scale="blues",
                title=f"{param} — Monthly Evolution by Year (Animated)",
                category_orders={"Month_name":MONTHS})
            fig_anim.update_layout(height=400,**PLOT_LAYOUT)
            fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"]=ANIM_SPEED
            wrap_chart(fig_anim)

    with tab4:
        st.markdown('<div class="info-box">🕯️ Monthly OHLC-style candlestick — Open=monthly start, Close=monthly end, High/Low from daily data.</div>', unsafe_allow_html=True)
        df_candle = df[["Date", param]].copy().dropna()
        df_candle["YM"] = df_candle["Date"].dt.to_period("M")
        candle_grp = df_candle.groupby("YM")[param].agg(
            open_val="first", close_val="last", high_val="max", low_val="min"
        ).reset_index()
        candle_grp["Date_str"] = candle_grp["YM"].astype(str)
        candle_grp["color"] = np.where(candle_grp["close_val"] >= candle_grp["open_val"], "#34d399", "#f87171")
        fig_cand = go.Figure(go.Candlestick(
            x=candle_grp["Date_str"],
            open=candle_grp["open_val"],
            high=candle_grp["high_val"],
            low=candle_grp["low_val"],
            close=candle_grp["close_val"],
            increasing=dict(line=dict(color="#34d399"), fillcolor="rgba(52,211,153,0.6)"),
            decreasing=dict(line=dict(color="#f87171"), fillcolor="rgba(248,113,113,0.6)"),
            name=param
        ))
        fig_cand.update_layout(height=430, title=f"{param} — Monthly Candlestick",
                               xaxis_rangeslider_visible=False, **PLOT_LAYOUT)
        fig_cand.update_xaxes(type="category", tickangle=-60, nticks=20)
        wrap_chart(fig_cand)

    with tab5:
        st.markdown('<div class="info-box">🌐 Polar/radial chart — each month is an angle, distance = mean value. Reveals the seasonal shape of the signal.</div>', unsafe_allow_html=True)
        clim_polar = monthly_clim(df.copy(), param)
        # Close the loop
        theta_vals = MONTHS + [MONTHS[0]]
        r_vals = list(clim_polar["mean"]) + [clim_polar["mean"].iloc[0]]
        r_upper = list(clim_polar["mean"] + clim_polar["std"]) + [clim_polar["mean"].iloc[0] + clim_polar["std"].iloc[0]]
        r_lower = list(clim_polar["mean"] - clim_polar["std"]) + [clim_polar["mean"].iloc[0] - clim_polar["std"].iloc[0]]

        fig_pol = go.Figure()
        fig_pol.add_trace(go.Scatterpolar(
            r=r_upper + r_lower[::-1], theta=theta_vals + theta_vals[::-1],
            fill="toself", fillcolor="rgba(52,211,153,0.08)",
            line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", name="±1σ"
        ))
        fig_pol.add_trace(go.Scatterpolar(
            r=r_vals, theta=theta_vals, mode="lines+markers", name="Monthly Mean",
            line=dict(color="#34d399", width=2.5),
            marker=dict(size=7, color="#34d399", line=dict(color="white", width=1.5))
        ))
        fig_pol.update_layout(
            height=430, title=f"{param} — Polar Seasonal Profile",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#475569", size=9)),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=10))
            ),
            **PLOT_LAYOUT
        )
        wrap_chart(fig_pol)


elif PAGE == "Seasonal Analysis":
    section("🌿","Seasonal Climate Analysis","Multi-station seasonal diagnostics")

    nasa_files=sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    pred_files=sorted([f for f in os.listdir(PRED_DIR) if f.endswith(".csv")]) if os.path.isdir(PRED_DIR) else []

    src=st.radio("Data source",["NASA","Prediction","Both"],horizontal=True)
    all_files=[]
    if src in ["NASA","Both"]: all_files+=[(f,"NASA",NASA_DIR) for f in nasa_files]
    if src in ["Prediction","Both"]: all_files+=[(f,"Pred",PRED_DIR) for f in pred_files]
    if not all_files: st.warning("No data files found."); st.stop()

    c1,c2=st.columns([3,2])
    with c1:
        opts=[f"{l}:{f}" for f,l,_ in all_files]
        sel=st.multiselect("Stations",opts,default=[opts[0]])
    if not sel: st.warning("Select at least one station."); st.stop()

    fn0,l0,d0=next((f,l,d) for f,l,d in all_files if f"{l}:{f}"==sel[0])
    df0=load_csv(os.path.join(d0,fn0))
    with c2: param=st.selectbox("Parameter",num_cols(df0),key="sap")

    frames=[]
    for tag in sel:
        lbl,fn=tag.split(":",1)
        info=next(((f,l,d) for f,l,d in all_files if f"{l}:{f}"==tag),None)
        if not info: continue
        fn_,_,dir_=info
        try:
            tmp=load_csv(os.path.join(dir_,fn_)); tmp=add_season(tmp)
            tmp["Station"]=fn_.replace(".csv",""); tmp["Source"]=lbl; frames.append(tmp)
        except: pass

    if not frames: st.warning("Could not load data."); st.stop()
    df_all=pd.concat(frames,ignore_index=True)
    stations=list(df_all["Station"].unique())
    SCOL={st:C_PALETTE[i%len(C_PALETTE)] for i,st in enumerate(stations)}

    tab1,tab2,tab3,tab4,tab5=st.tabs(["📦 Violin+Box","📅 Heatmap","📈 Evolution","🎬 Animated","📋 Table"])

    with tab1:
        fig_v=go.Figure()
        for sta in stations:
            bc=SCOL[sta]
            sub=df_all[df_all["Station"]==sta]
            for seas in ["Winter","Spring","Summer","Autumn"]:
                sg=sub[sub["Season"]==seas][param].dropna()
                if sg.empty: continue
                r,g,b=tuple(int(bc.lstrip("#")[i:i+2],16) for i in (0,2,4))
                op={"Winter":1.0,"Spring":0.8,"Summer":0.65,"Autumn":0.5}[seas]
                fig_v.add_trace(go.Violin(y=sg,name=f"{sta}·{seas}",
                    line_color=bc,fillcolor=f"rgba({r},{g},{b},{op*0.25})",
                    box_visible=True,meanline_visible=True,points=False,
                    legendgroup=sta,showlegend=(seas=="Winter")))
        fig_v.update_layout(height=480,title=f"{param} — Violin by Station & Season",violinmode="group",**PLOT_LAYOUT)
        wrap_chart(fig_v)

    with tab2:
        pivot=df_all.groupby(["Station","Month"])[param].mean().unstack(fill_value=np.nan)
        pivot.columns=MONTHS[:len(pivot.columns)]
        fig_h=go.Figure(go.Heatmap(z=pivot.values,x=pivot.columns.tolist(),y=pivot.index.tolist(),
            colorscale="RdYlBu_r",text=np.round(pivot.values,2),texttemplate="%{text}",
            colorbar=dict(title=param,thickness=14)))
        fig_h.update_layout(height=320,title=f"{param} — Monthly Climatology Heatmap",**PLOT_LAYOUT)
        wrap_chart(fig_h)

    with tab3:
        seas_yr=df_all.groupby(["Station","Year","Season"])[param].mean().reset_index()
        fig_e=go.Figure()
        for sta in stations:
            bc=SCOL[sta]
            for seas in ["Winter","Spring","Summer","Autumn"]:
                sg=seas_yr[(seas_yr["Station"]==sta)&(seas_yr["Season"]==seas)]
                if sg.empty: continue
                fig_e.add_trace(go.Scatter(x=sg["Year"],y=sg[param],mode="lines+markers",
                    name=f"{sta}·{seas}",legendgroup=sta,
                    line=dict(color=bc,width=1.8,dash=SEAS_DASH[seas]),
                    marker=dict(size=5,color=bc,symbol=SEAS_SYM[seas])))
        fig_e.update_layout(height=420,title=f"{param} — Seasonal Evolution by Station",**PLOT_LAYOUT)
        fig_e.update_xaxes(title_text="Year"); fig_e.update_yaxes(title_text=param)
        wrap_chart(fig_e)

    with tab4:
        st.markdown('<div class="info-box">🎬 Animated seasonal bar race — watch how each season evolves year by year.</div>',unsafe_allow_html=True)
        agg_a=df_all.groupby(["Year","Season"])[param].mean().reset_index()
        if len(agg_a)>0:
            fig_anim=px.bar(agg_a,x="Season",y=param,animation_frame="Year",
                color="Season",color_discrete_map=SEASON_COLORS,
                title=f"{param} — Seasonal Animation by Year",
                category_orders={"Season":["Winter","Spring","Summer","Autumn"]})
            fig_anim.update_layout(height=380,showlegend=False,**PLOT_LAYOUT)
            fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"]=ANIM_SPEED
            wrap_chart(fig_anim)

    with tab5:
        agg=df_all.groupby(["Station","Season"])[param].agg(["mean","std","min","max"]).round(3).reset_index()
        agg.columns=["Station","Season","Mean","Std","Min","Max"]
        st.dataframe(agg,use_container_width=True,height=360)
        st.download_button("⬇️ Download CSV",agg.to_csv(index=False).encode(),"seasonal.csv","text/csv")

# ╔═══════════════════════════════════════════════════════╗
# ║  🎬 ANIMATION STUDIO                                  ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "Animation Studio":
    section("🎬","Animation Studio","Animated racing charts · Bubble evolution · Multi-station sweep")

    nasa_files=sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    if not nasa_files: st.warning("No NASA CSV files found."); st.stop()

    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "🏎️ Bar Race","🫧 Bubble Evolution","🌊 Wave Chart","⚡ Multi-Station Sweep","🎡 Radial Animation"
    ])

    # ── Tab 1: Animated bar race (stations × year) ──
    with tab1:
        st.markdown('<div class="info-box">🏎️ Racing bar chart — shows how each station\'s annual mean value evolves year by year. Select multiple stations to race.</div>', unsafe_allow_html=True)
        sel_race = st.multiselect("Stations to race", nasa_files, default=nasa_files[:min(5, len(nasa_files))], key="race_st")
        if not sel_race: st.warning("Select at least one station."); st.stop()
        c1r, c2r = st.columns(2)
        df_r0 = load_csv(os.path.join(NASA_DIR, sel_race[0]))
        with c1r: param_race = st.selectbox("Parameter", num_cols(df_r0), key="race_p")

        all_race = []
        for fn in sel_race:
            try:
                tmp = load_csv(os.path.join(NASA_DIR, fn))
                tmp = add_season(tmp)
                tmp["Station"] = fn.replace(".csv","")
                all_race.append(tmp)
            except: pass

        if all_race:
            df_race = pd.concat(all_race, ignore_index=True)
            race_agg = df_race.groupby(["Year","Station"])[param_race].mean().reset_index().dropna()
            race_agg["Year"] = race_agg["Year"].astype(int)

            # Build animated frames
            years_r = sorted(race_agg["Year"].unique())
            frames_r = []
            all_stations_r = sorted(race_agg["Station"].unique())
            col_map_r = {st: C_PALETTE[i%len(C_PALETTE)] for i,st in enumerate(all_stations_r)}

            for yr in years_r:
                sub = race_agg[race_agg["Year"] == yr].sort_values(param_race)
                frames_r.append(go.Frame(
                    data=[go.Bar(
                        x=sub[param_race], y=sub["Station"],
                        orientation="h", name=str(yr),
                        marker=dict(color=[col_map_r[s] for s in sub["Station"]],
                                    line=dict(color="rgba(0,0,0,0)")),
                        text=sub[param_race].round(3), textposition="auto",
                        textfont=dict(color="white", size=11)
                    )],
                    name=str(yr),
                    layout=go.Layout(title_text=f"{param_race} — Station Rankings · Year {yr}")
                ))

            first_sub = race_agg[race_agg["Year"] == years_r[0]].sort_values(param_race)
            fig_race = go.Figure(
                data=frames_r[0].data,
                frames=frames_r,
                layout=go.Layout(
                    height=max(350, len(all_stations_r)*55),
                    title=f"{param_race} — Station Bar Race",
                    xaxis=dict(range=[race_agg[param_race].min()*0.95, race_agg[param_race].max()*1.05]),
                    updatemenus=[dict(
                        type="buttons", showactive=False,
                        bgcolor="rgba(10,17,30,0.9)", bordercolor="rgba(56,189,248,0.2)",
                        font=dict(color="#e2e8f0"),
                        x=0.12, y=1.12, xanchor="right",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": ANIM_SPEED, "redraw": True}, "fromcurrent": True}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"mode": "immediate", "frame": {"duration": 0}}])
                        ]
                    )],
                    sliders=[dict(
                        currentvalue=dict(prefix="Year: ", font=dict(color="#94a3b8", size=12)),
                        bgcolor="#0f172a", bordercolor="#1e3a5f", activebgcolor="#38bdf8",
                        font=dict(color="#64748b", size=10),
                        steps=[dict(args=[[f.name], {"frame": {"duration": 300}, "mode": "immediate"}],
                                    method="animate", label=f.name) for f in frames_r]
                    )]
                )
            )
            fig_race.update_layout(**PLOT_LAYOUT)
            wrap_chart(fig_race)

    # ── Tab 2: Bubble Evolution ──
    with tab2:
        st.markdown('<div class="info-box">🫧 Each bubble = one station per year. Size = standard deviation. Color = value magnitude. Watch the climate drift over decades.</div>', unsafe_allow_html=True)
        sel_bub = st.multiselect("Stations", nasa_files, default=nasa_files[:min(4, len(nasa_files))], key="bub_st")
        if not sel_bub: st.warning("Select at least one station."); st.stop()
        df_r0b = load_csv(os.path.join(NASA_DIR, sel_bub[0]))
        param_bub = st.selectbox("Parameter", num_cols(df_r0b), key="bub_p")

        all_bub = []
        for i, fn in enumerate(sel_bub):
            try:
                tmp = load_csv(os.path.join(NASA_DIR, fn))
                tmp = add_season(tmp)
                tmp["Station"] = fn.replace(".csv","")
                tmp["StationIdx"] = i
                all_bub.append(tmp)
            except: pass

        if all_bub:
            df_bub = pd.concat(all_bub, ignore_index=True)
            bub_agg = df_bub.groupby(["Year","Station","StationIdx"])[param_bub].agg(
                value="mean", std_val="std"
            ).reset_index().dropna()
            bub_agg["Year"] = bub_agg["Year"].astype(int)
            bub_agg["std_val"] = bub_agg["std_val"].fillna(1)

            fig_bub = px.scatter(
                bub_agg, x="StationIdx", y="value",
                size="std_val", color="value",
                animation_frame="Year",
                text="Station",
                color_continuous_scale="turbo",
                size_max=55,
                title=f"{param_bub} — Multi-Station Bubble Evolution",
                hover_data={"StationIdx": False, "value": ":.3f", "std_val": ":.3f"}
            )
            fig_bub.update_traces(textposition="top center", textfont=dict(color="white", size=10))
            fig_bub.update_xaxes(showticklabels=False, title="Stations")
            fig_bub.update_yaxes(title=param_bub)
            fig_bub.update_layout(height=460, **PLOT_LAYOUT)
            fig_bub.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = ANIM_SPEED
            wrap_chart(fig_bub)

    # ── Tab 3: Wave Chart (animated rolling signal) ──
    with tab3:
        st.markdown('<div class="info-box">🌊 Animated wave — rolling mean sweeps across the signal, revealing how the smoothed climate signal evolves with different window sizes.</div>', unsafe_allow_html=True)
        c1w, c2w = st.columns(2)
        with c1w: station_w = st.selectbox("Station", nasa_files, key="wave_s")
        df_w = load_csv(os.path.join(NASA_DIR, station_w))
        with c2w: param_w = st.selectbox("Parameter", num_cols(df_w), key="wave_p")
        df_w = add_season(df_w)

        windows = list(range(7, 370, 14))  # 7d to 1 year in 14d steps
        wave_frames = []
        for w in windows:
            roll = df_w[param_w].rolling(w, center=True, min_periods=max(5,w//4)).mean()
            wave_frames.append(go.Frame(
                data=[
                    go.Scatter(x=df_w["Date"], y=df_w[param_w], mode="lines", name="Raw",
                               line=dict(color="rgba(56,189,248,0.2)", width=1)),
                    go.Scatter(x=df_w["Date"], y=roll, mode="lines", name=f"{w}d mean",
                               line=dict(color="#38bdf8", width=2.5),
                               fill="tozeroy", fillcolor="rgba(56,189,248,0.05)")
                ],
                name=str(w),
                layout=go.Layout(title_text=f"{param_w} — Rolling Mean (window = {w} days)")
            ))

        fig_wave = go.Figure(data=wave_frames[0].data, frames=wave_frames,
            layout=go.Layout(
                height=420, title=f"{param_w} — Wave Chart",
                updatemenus=[dict(
                    type="buttons", showactive=False,
                    bgcolor="rgba(10,17,30,0.9)", bordercolor="rgba(56,189,248,0.2)",
                    font=dict(color="#e2e8f0"), x=0.12, y=1.12, xanchor="right",
                    buttons=[
                        dict(label="▶ Play", method="animate",
                             args=[None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True}]),
                        dict(label="⏸ Pause", method="animate",
                             args=[[None], {"mode": "immediate", "frame": {"duration": 0}}])
                    ]
                )],
                sliders=[dict(
                    currentvalue=dict(prefix="Window: ", suffix="d", font=dict(color="#94a3b8", size=11)),
                    bgcolor="#0f172a", bordercolor="#1e3a5f", activebgcolor="#38bdf8",
                    font=dict(color="#64748b", size=9),
                    steps=[dict(args=[[f.name], {"frame": {"duration": 180}, "mode": "immediate"}],
                                method="animate", label=f.name) for f in wave_frames]
                )]
            )
        )
        fig_wave.update_layout(**PLOT_LAYOUT)
        wrap_chart(fig_wave)

    # ── Tab 4: Multi-Station Parameter Sweep ──
    with tab4:
        st.markdown('<div class="info-box">⚡ All stations side-by-side on the same parameter, animated by year — compare spatial variability across time.</div>', unsafe_allow_html=True)
        sel_sweep = st.multiselect("Stations for sweep", nasa_files, default=nasa_files[:min(6, len(nasa_files))], key="sw_st")
        if not sel_sweep: st.warning("Select stations."); st.stop()
        df_sw0 = load_csv(os.path.join(NASA_DIR, sel_sweep[0]))
        param_sw = st.selectbox("Parameter", num_cols(df_sw0), key="sw_p")

        all_sw = []
        for fn in sel_sweep:
            try:
                tmp = load_csv(os.path.join(NASA_DIR, fn))
                tmp = add_season(tmp)
                tmp["Station"] = fn.replace(".csv","")
                all_sw.append(tmp)
            except: pass

        if all_sw:
            df_sw = pd.concat(all_sw, ignore_index=True)
            sw_agg = df_sw.groupby(["Year","Month","Station"])[param_sw].mean().reset_index().dropna()
            sw_agg["Year"] = sw_agg["Year"].astype(int)
            sw_agg["Month_name"] = sw_agg["Month"].apply(lambda x: MONTHS[x-1])
            sw_pivot = sw_agg.groupby(["Year","Station"])[param_sw].mean().reset_index()

            sw_years = sorted(sw_pivot["Year"].unique())
            sw_stations = sorted(sw_pivot["Station"].unique())
            sw_colors = [C_PALETTE[i%len(C_PALETTE)] for i in range(len(sw_stations))]

            sw_frames = []
            for yr in sw_years:
                sub = sw_pivot[sw_pivot["Year"]==yr]
                sw_frames.append(go.Frame(
                    data=[go.Bar(
                        x=sub["Station"], y=sub[param_sw],
                        marker=dict(color=sw_colors[:len(sub)], opacity=0.88,
                                    line=dict(color="rgba(0,0,0,0)")),
                        text=sub[param_sw].round(3), textposition="outside",
                        textfont=dict(color="white", size=10)
                    )],
                    name=str(yr),
                    layout=go.Layout(title_text=f"{param_sw} across stations · Year {yr}")
                ))

            fig_sw = go.Figure(data=sw_frames[0].data, frames=sw_frames,
                layout=go.Layout(
                    height=430,
                    updatemenus=[dict(
                        type="buttons", showactive=False,
                        bgcolor="rgba(10,17,30,0.9)", bordercolor="rgba(56,189,248,0.2)",
                        font=dict(color="#e2e8f0"), x=0.12, y=1.12, xanchor="right",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": ANIM_SPEED, "redraw": True}, "fromcurrent": True}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"mode": "immediate"}])
                        ]
                    )],
                    sliders=[dict(
                        currentvalue=dict(prefix="Year: ", font=dict(color="#94a3b8", size=12)),
                        bgcolor="#0f172a", bordercolor="#1e3a5f", activebgcolor="#38bdf8",
                        font=dict(color="#64748b", size=10),
                        steps=[dict(args=[[f.name], {"frame": {"duration": 300}, "mode": "immediate"}],
                                    method="animate", label=f.name) for f in sw_frames]
                    )]
                )
            )
            fig_sw.update_layout(**PLOT_LAYOUT)
            wrap_chart(fig_sw)

    # ── Tab 5: Radial/Polar Animation ──
    with tab5:
        st.markdown('<div class="info-box">🎡 Animated polar chart — watch how the seasonal fingerprint of a station evolves year by year in a radial view.</div>', unsafe_allow_html=True)
        c1rd, c2rd = st.columns(2)
        with c1rd: station_rd = st.selectbox("Station", nasa_files, key="rd_s")
        df_rd = load_csv(os.path.join(NASA_DIR, station_rd))
        with c2rd: param_rd = st.selectbox("Parameter", num_cols(df_rd), key="rd_p")
        df_rd = add_season(df_rd)

        rd_agg = df_rd.groupby(["Year","Month"])[param_rd].mean().reset_index().dropna()
        rd_agg["Year"] = rd_agg["Year"].astype(int)
        rd_agg["Month_name"] = rd_agg["Month"].apply(lambda x: MONTHS[x-1])
        rd_years = sorted(rd_agg["Year"].unique())

        if len(rd_years) > 1:
            import plotly.colors as pc
            rd_colors = pc.sample_colorscale("Turbo", [i/(len(rd_years)-1) for i in range(len(rd_years))])
            rd_frames = []
            for i, yr in enumerate(rd_years):
                sub = rd_agg[rd_agg["Year"] == yr].sort_values("Month")
                r_vals = list(sub[param_rd]) + [sub[param_rd].iloc[0]] if len(sub) == 12 else list(sub[param_rd])
                theta_v = [MONTHS[m-1] for m in sub["Month"]] + [MONTHS[sub["Month"].iloc[0]-1]] if len(sub)==12 else [MONTHS[m-1] for m in sub["Month"]]
                rd_frames.append(go.Frame(
                    data=[go.Scatterpolar(
                        r=r_vals, theta=theta_v,
                        mode="lines+markers", fill="toself",
                        fillcolor=f"rgba{tuple(int(rd_colors[i].lstrip('rgb(').rstrip(')').split(',')[j].strip()) for j in range(3))+(0.12,)}" if rd_colors[i].startswith("rgb") else "rgba(56,189,248,0.1)",
                        line=dict(color=rd_colors[i], width=2.5),
                        marker=dict(size=7, color=rd_colors[i])
                    )],
                    name=str(yr),
                    layout=go.Layout(title_text=f"{param_rd} — Radial Seasonal · Year {yr}")
                ))

            fig_rd = go.Figure(data=rd_frames[0].data, frames=rd_frames,
                layout=go.Layout(
                    height=500,
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#475569", size=9)),
                        angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=10),
                                         direction="clockwise")
                    ),
                    updatemenus=[dict(
                        type="buttons", showactive=False,
                        bgcolor="rgba(10,17,30,0.9)", bordercolor="rgba(56,189,248,0.2)",
                        font=dict(color="#e2e8f0"), x=0.12, y=1.09, xanchor="right",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": ANIM_SPEED, "redraw": True}, "fromcurrent": True}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"mode": "immediate"}])
                        ]
                    )],
                    sliders=[dict(
                        currentvalue=dict(prefix="Year: ", font=dict(color="#94a3b8", size=12)),
                        bgcolor="#0f172a", bordercolor="#1e3a5f", activebgcolor="#38bdf8",
                        font=dict(color="#64748b", size=10),
                        steps=[dict(args=[[f.name], {"frame": {"duration": 300}, "mode": "immediate"}],
                                    method="animate", label=f.name) for f in rd_frames]
                    )]
                )
            )
            fig_rd.update_layout(**PLOT_LAYOUT)
            wrap_chart(fig_rd)


elif PAGE == "Climate Trends":
    section("🌡️","Climate Trends & Animations","Statistical tests · Animated evolution · Anomalies")

    nasa_files=sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    if not nasa_files: st.warning("No NASA CSV files found."); st.stop()

    c1,c2=st.columns(2)
    with c1: station=st.selectbox("Station",nasa_files,key="ct_s")
    df=load_csv(os.path.join(NASA_DIR,station)); df=add_season(df)
    with c2: param=st.selectbox("Parameter",num_cols(df),key="ct_p")

    df=add_trend(df,param)
    ann=df.groupby("Year")[param].mean().reset_index().dropna()
    z_mk,p_mk,tr_mk=mann_kendall(ann[param].values)
    baseline=ann[param].mean()
    ann["Anomaly"]=ann[param]-baseline
    ann["AnomalyColor"]=ann["Anomaly"].apply(lambda x:"#f87171" if x>0 else "#38bdf8")

    kpi_row([
        ("Trend",tr_mk,"",None,z_mk>=0,"📊"),
        ("MK Z-stat",f"{z_mk:.3f}","",None,z_mk>=0,"🔢"),
        ("p-value",f"{p_mk:.4f}","",None,p_mk<0.05,"🎯"),
        ("Baseline",f"{baseline:.3f}","",None,True,"📏"),
        ("Period",f"{int(ann['Year'].min())}–{int(ann['Year'].max())}","",None,True,"📅"),
    ])

    tab1,tab2,tab3,tab4=st.tabs(["📊 Anomaly Chart","🎬 Animated Scatter","🌡️ Decade Analysis","⚡ Extreme Events"])

    with tab1:
        fig_an=go.Figure()
        fig_an.add_hline(y=0,line_color="rgba(255,255,255,0.15)",line_width=1)
        fig_an.add_trace(go.Bar(x=ann["Year"],y=ann["Anomaly"],name="Anomaly",
            marker_color=ann["AnomalyColor"],
            marker_line_color="rgba(0,0,0,0)",marker_opacity=0.85))
        sl,ic=np.polyfit(ann["Year"],ann["Anomaly"],1)
        fig_an.add_trace(go.Scatter(x=ann["Year"],y=sl*ann["Year"]+ic,mode="lines",
            name=f"Linear trend ({sl:+.4f}/yr)",line=dict(color="#fbbf24",width=2.5,dash="dot")))
        fig_an.update_layout(height=380,title=f"{param} — Annual Anomaly from Baseline ({baseline:.2f})",**PLOT_LAYOUT)
        fig_an.update_yaxes(title_text=f"Anomaly ({param})")
        fig_an.update_xaxes(title_text="Year")
        wrap_chart(fig_an)
        st.markdown(f"**Mann-Kendall Result:** {trend_badge(z_mk,p_mk)} &nbsp; Rate: **{sl:+.5f} units/year**",unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="info-box">🎬 Each bubble is one year. Watch how the annual mean migrates over time.</div>',unsafe_allow_html=True)
        ann2=ann.copy(); ann2["Size"]=np.abs(ann2["Anomaly"])*30+10
        fig_ab=px.scatter(ann2,x="Year",y=param,size="Size",color="Anomaly",
            color_continuous_scale="RdBu_r",animation_frame="Year",
            title=f"{param} — Animated Annual Bubble",
            hover_data={"Size":False,"Anomaly":":.3f",param:":.3f"})
        fig_ab.update_layout(height=380,**PLOT_LAYOUT)
        fig_ab.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"]=ANIM_SPEED
        wrap_chart(fig_ab)

    with tab3:
        df["Decade"]=(df["Year"]//10*10).astype(str)+"s"
        dec=df.groupby("Decade")[param].agg(["mean","std","min","max"]).reset_index()
        fig_dec=go.Figure()
        fig_dec.add_trace(go.Bar(x=dec["Decade"],y=dec["mean"],name="Decadal mean",
            marker_color=C_PALETTE[:len(dec)],text=dec["mean"].round(2),textposition="outside",
            error_y=dict(type="data",array=dec["std"],color="rgba(255,255,255,0.2)")))
        fig_dec.update_layout(height=340,title=f"{param} — Decadal Analysis",**PLOT_LAYOUT)
        wrap_chart(fig_dec)

        fig_box=go.Figure()
        for i,decade in enumerate(sorted(df["Decade"].unique())):
            sg=df[df["Decade"]==decade][param].dropna()
            fig_box.add_trace(go.Box(y=sg,name=decade,marker_color=C_PALETTE[i%len(C_PALETTE)],
                boxmean="sd",showlegend=False))
        fig_box.update_layout(height=300,title="Decadal Distribution",**PLOT_LAYOUT)
        wrap_chart(fig_box)

    with tab4:
        pct_lo=st.slider("Lower percentile",1,20,5)
        pct_hi=st.slider("Upper percentile",80,99,95)
        lo=np.nanpercentile(df[param],pct_lo)
        hi=np.nanpercentile(df[param],pct_hi)
        df_ext=df.copy()
        df_ext["Category"]=np.where(df_ext[param]>=hi,"Extreme High",
                            np.where(df_ext[param]<=lo,"Extreme Low","Normal"))
        fig_ext=go.Figure()
        col_map={"Normal":"rgba(56,189,248,0.4)","Extreme High":"rgba(248,113,113,0.85)","Extreme Low":"rgba(129,140,248,0.85)"}
        for cat,col in col_map.items():
            sub=df_ext[df_ext["Category"]==cat]
            fig_ext.add_trace(go.Scatter(x=sub["Date"],y=sub[param],mode="markers",name=cat,
                marker=dict(color=col,size=3 if cat=="Normal" else 6),opacity=ALPHA))
        fig_ext.add_hline(y=hi,line_color="#f87171",line_dash="dot",line_width=1.2,
            annotation_text=f"P{pct_hi}",annotation_position="right")
        fig_ext.add_hline(y=lo,line_color="#818cf8",line_dash="dot",line_width=1.2,
            annotation_text=f"P{pct_lo}",annotation_position="right")
        fig_ext.update_layout(height=400,title=f"{param} — Extreme Events Detection",**PLOT_LAYOUT)
        wrap_chart(fig_ext)
        n_hi=(df_ext["Category"]=="Extreme High").sum()
        n_lo=(df_ext["Category"]=="Extreme Low").sum()
        kpi_row([("Extreme High Days",str(n_hi),"",None,False,"🔴"),
                 ("Extreme Low Days", str(n_lo),"",None,True, "🔵"),
                 ("Normal Days",str(len(df_ext)-n_hi-n_lo),"",None,True,"🟢"),
                 (f"P{pct_hi} threshold",f"{hi:.3f}","",None,False,"⬆️"),
                 (f"P{pct_lo} threshold",f"{lo:.3f}","",None,True, "⬇️")])

# ╔═══════════════════════════════════════════════════════╗
# ║  🗺️ PREDICTION MAPPING                               ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "Prediction Mapping":
    if not _ok: st.stop()
    import io as _io, base64 as _b64
    section("","Climate Prediction Mapping","Interactive WebGIS · IDW · Zoom · Opacity · Basemaps")

    lat_col=next((c for c in pred_df.columns if c.lower() in ("lat","latitude")),None)
    lon_col=next((c for c in pred_df.columns if c.lower() in ("lon","longitude","lng")),None)
    if not lat_col or not lon_col:
        st.error("Latitude/longitude columns not found."); st.stop()

    params=[c for c in num_cols(pred_df,exclude={lat_col,lon_col})]
    PBASEMAPS={
        "CartoDB Dark Matter":("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png","&copy; OSM &copy; CARTO"),
        "CartoDB Positron":   ("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png","&copy; OSM &copy; CARTO"),
        "OpenStreetMap":      ("https://tile.openstreetmap.org/{z}/{x}/{y}.png","&copy; OpenStreetMap"),
        "OpenTopoMap":        ("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png","&copy; OpenTopoMap"),
        "Esri Satellite":     ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}","&copy; Esri"),
    }
    c1,c2,c3,c4,c5,c6=st.columns([2,2,1.5,1,1,1])
    with c1: param=st.selectbox("Variable",[""] + params,key="pm_var")
    with c2: cmap_choice=st.selectbox("Colour map",["RdYlBu_r","viridis","plasma","coolwarm","YlOrRd","Blues","RdBu_r","Spectral_r"],key="pm_cm")
    with c3: bmap_ch=st.selectbox("Basemap",list(PBASEMAPS.keys()),key="pm_bmap")
    with c4: resolution=st.slider("Resolution",60,200,120,10,key="pm_res")
    with c5: overlay_opacity=st.slider("Opacity",0.1,1.0,0.72,0.05,key="pm_op")
    with c6: view_mode=st.radio("View",["Interactive","3D Surface"],key="pm_view")
    if not param: st.info("Select a variable to display the map."); st.stop()

    df=pred_df[[lat_col,lon_col,param]].dropna()
    gdf=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df[lon_col],df[lat_col]),crs="EPSG:4326")
    tun4=tunisia.to_crs(epsg=4326)
    tpoly=tun4.geometry.union_all() if hasattr(tun4.geometry,"union_all") else tun4.geometry.unary_union
    gdf_c=gdf[gdf.geometry.within(tpoly)]
    if gdf_c.empty: st.warning("No stations inside Tunisia boundary."); st.stop()
    x,y,z=gdf_c.geometry.x.values,gdf_c.geometry.y.values,gdf_c[param].values
    mn_lon,mn_lat,mx_lon,mx_lat=tun4.total_bounds
    glon,glat=np.mgrid[mn_lon:mx_lon:complex(0,resolution),mn_lat:mx_lat:complex(0,resolution)]
    xi,yi=glon.ravel(),glat.ravel()
    with st.spinner("Interpolating spatial grid..."):
        grid_z=idw_fast(x,y,z,xi,yi).reshape(glon.shape)
    pts4=gpd.GeoSeries(gpd.points_from_xy(xi,yi),crs="EPSG:4326")
    inside=pts4.within(tpoly).values.reshape(glon.shape)
    grid_z=np.where(inside,grid_z,np.nan)
    valid=grid_z[~np.isnan(grid_z)]

    if "3D" in view_mode:
        fig_3d=go.Figure(go.Surface(
            z=grid_z.T,x=np.linspace(mn_lon,mx_lon,resolution),y=np.linspace(mn_lat,mx_lat,resolution),
            colorscale=cmap_choice.lower(),opacity=overlay_opacity,
            contours=dict(z=dict(show=True,usecolormap=True,highlightcolor="white",project_z=True)),
            lighting=dict(ambient=0.7,diffuse=0.8,specular=0.3,roughness=0.5)))
        fig_3d.update_layout(height=580,title=f"{param} — 3D Climate Surface",
            scene=dict(xaxis_title="Lon",yaxis_title="Lat",zaxis_title=param,
                bgcolor="rgba(0,0,0,0)",
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)",gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)",gridcolor="rgba(255,255,255,0.05)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)",gridcolor="rgba(255,255,255,0.05)")),**PLOT_LAYOUT)
        wrap_chart(fig_3d)
    else:
        cmap_mpl=plt.get_cmap(cmap_choice)
        norm_mpl=mcolors.Normalize(vmin=np.nanmin(valid),vmax=np.nanmax(valid))
        rgba=cmap_mpl(norm_mpl(grid_z.T))
        rgba[np.isnan(grid_z.T),3]=0
        buf_img=_io.BytesIO()
        plt.imsave(buf_img,rgba,format="png",origin="lower"); buf_img.seek(0)
        img_b64="data:image/png;base64,"+_b64.b64encode(buf_img.read()).decode()
        plt.close("all")

        turl,tattr=PBASEMAPS[bmap_ch]
        center=[(mn_lat+mx_lat)/2,(mn_lon+mx_lon)/2]
        m=folium.Map(location=center,tiles=turl,attr=tattr,control_scale=True,zoom_start=6,prefer_canvas=True)

        folium.raster_layers.ImageOverlay(
            image=img_b64,
            bounds=[[mn_lat,mn_lon],[mx_lat,mx_lon]],
            opacity=overlay_opacity,zindex=1,name=f"{param} IDW"
        ).add_to(m)

        folium.GeoJson(tun4.to_json(),
            style_function=lambda x: {"color":"#38bdf8","weight":1.8,"fillOpacity":0},
            name="Tunisia boundary").add_to(m)
        if basins is not None:
            folium.GeoJson(basins.to_crs(epsg=4326).to_json(),
                style_function=lambda x: {"color":"#818cf8","weight":0.8,"fillOpacity":0,"dashArray":"4 3"},
                name="Basins").add_to(m)

        for _, row in gdf_c.iterrows():
            lat_s,lon_s=row.geometry.y,row.geometry.x
            val_s=row[param]
            vs=f"{val_s:.3f}" if pd.notna(val_s) else "N/A"
            nv=float((val_s-np.nanmin(valid))/(np.nanmax(valid)-np.nanmin(valid)+1e-9))
            rc2,gc2,bc2=tuple(int(255*cv) for cv in cmap_mpl(nv)[:3])
            dc=f"#{rc2:02x}{gc2:02x}{bc2:02x}"
            popup_lines = [
                '<div style="background:#0f172a;border:1px solid rgba(56,189,248,0.3);',
                'border-radius:12px;padding:14px 16px;min-width:180px;font-family:Inter,sans-serif;">',
                '<div style="font-size:13px;font-weight:800;color:#38bdf8;',
                'border-bottom:1px solid rgba(56,189,248,0.15);padding-bottom:7px;margin-bottom:9px">',
                '&#128205; Station</div>',
                '<div style="background:rgba(56,189,248,0.07);border:1px solid rgba(56,189,248,0.12);',
                'border-radius:8px;padding:8px 10px;">',
                f'<div style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:1px">{param}</div>',
                f'<div style="font-size:22px;font-weight:800;color:#f1f5f9">{vs}</div>',
                '</div>',
                f'<div style="font-size:10px;color:#475569;margin-top:8px">Lat: {lat_s:.4f} | Lon: {lon_s:.4f}</div>',
                '</div>',
            ]
            ph = "".join(popup_lines)
            folium.CircleMarker(location=[lat_s,lon_s],radius=7,
                color="white",weight=1.5,fill=True,fill_color=dc,fill_opacity=0.95,
                popup=folium.Popup(folium.IFrame(ph,width=210,height=155),max_width=220),
                tooltip=f"{param}: {vs}").add_to(m)

        MeasureControl(position="bottomleft",primary_length_unit="kilometers").add_to(m)
        Fullscreen(position="topright").add_to(m)
        MousePosition(position="bottomright").add_to(m)
        folium.LayerControl(position="topright",collapsed=False).add_to(m)
        # Inject CSS to hide the "Made with Folium" link & leaflet attribution link
        hide_link_css = """
        <style>
        .leaflet-control-attribution a { display: none !important; }
        .leaflet-control-attribution { font-size: 9px !important; color: rgba(100,116,139,0.6) !important;
            background: rgba(10,17,30,0.7) !important; border-radius: 4px; }
        </style>"""
        m.get_root().html.add_child(folium.Element(hide_link_css))

        _,cm_col,_=st.columns([0.2,9.6,0.2])
        # Inject CSS to hide the Folium attribution/link white box
        st.markdown("""
        <style>
        .folium-map a, .leaflet-control-attribution,
        .stIFrame + div, iframe + div,
        div[data-testid="stIFrame"] ~ div,
        div[data-testid="stIFrame"] + div { display: none !important; height: 0 !important; }
        </style>""", unsafe_allow_html=True)
        with cm_col:
            st_folium(m, width=None, height=560, use_container_width=True, returned_objects=[])


    st.markdown("### Spatial Statistics")
    kpi_row([(f"Mean",f"{np.nanmean(grid_z):.3f}","",None,True,"📊"),
             (f"Max", f"{np.nanmax(grid_z):.3f}","",None,True,"⬆️"),
             (f"Min", f"{np.nanmin(grid_z):.3f}","",None,False,"⬇️"),
             (f"Std", f"{np.nanstd(grid_z):.3f}","",None,True,"📉"),
             (f"Range",f"{np.nanmax(grid_z)-np.nanmin(grid_z):.3f}","",None,True,"↔️")])
    c_h,c_b=st.columns(2)
    with c_h:
        fh=go.Figure(go.Histogram(x=valid,nbinsx=50,marker=dict(color="#38bdf8",opacity=0.8)))
        fh.update_layout(height=240,title=f"Distribution of {param}",**PLOT_LAYOUT); wrap_chart(fh)
    with c_b:
        fb=go.Figure(go.Box(y=valid,name=param,marker_color="#818cf8",
            boxmean="sd",line_color="#818cf8",fillcolor="rgba(129,140,248,0.12)"))
        fb.update_layout(height=240,title=f"{param} - Box & Whisker",**PLOT_LAYOUT); wrap_chart(fb)

# ╔═══════════════════════════════════════════════════════╗
# ║  🌊 BASINS MAPPING                                    ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "Basins Mapping":
    if not _ok: st.stop()
    section("🌊","Basins Spatial Mapping","Interactive WebGIS · Rich popup cards")

    bmap=basins.to_crs(epsg=4326) if basins.crs!="EPSG:4326" else basins.copy()
    smap=study_zone.to_crs(epsg=4326) if study_zone.crs!="EPSG:4326" else study_zone.copy()
    bmap=bmap[bmap.geometry.notnull()].copy(); bmap["geometry"]=bmap.buffer(0)
    nc=bmap.select_dtypes(include="number").columns.tolist()

    BASEMAPS={"CartoDB Dark Matter":("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png","&copy; OSM &copy; CARTO"),
              "CartoDB Positron":("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png","&copy; OSM &copy; CARTO"),
              "OpenStreetMap":("https://tile.openstreetmap.org/{z}/{x}/{y}.png","&copy; OpenStreetMap"),
              "OpenTopoMap":("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png","&copy; OpenTopoMap")}

    c1,c2,c3=st.columns([2,2,1])
    with c1: param=st.selectbox("Basin Variable",nc)
    with c2: basemap_sel=st.selectbox("Basemap",list(BASEMAPS.keys()))
    with c3: opacity=st.slider("Opacity",0.3,1.0,0.8,0.05)

    mn,mx=bmap[param].min(),bmap[param].max()
    turl,tattr=BASEMAPS[basemap_sel]
    m=folium.Map(tiles=turl,attr=tattr,control_scale=True)

    def sty(ft,_p=param,_mn=mn,_mx=mx,_op=opacity):
        v=ft["properties"].get(_p,_mn); nr=(v-_mn)/(_mx-_mn+1e-9)
        return {"fillColor":mcolors.to_hex(plt.cm.YlGnBu(nr)),"color":"#1e3a5f","weight":1.2,"fillOpacity":_op}
    def hl(ft): return {"fillColor":"#38bdf8","color":"#0f172a","weight":2.5,"fillOpacity":0.9}

    fav=[f for f in ["Name",param] if f in bmap.columns]
    extra=[c for c in bmap.select_dtypes(include="number").columns if c!=param][:8]

    folium.GeoJson(bmap.to_json(),style_function=sty,highlight_function=hl,
        tooltip=folium.GeoJsonTooltip(fields=fav,aliases=[f.capitalize() for f in fav],sticky=False,
            style="background:#0f172a;color:#e2e8f0;border:1px solid rgba(56,189,248,0.3);border-radius:10px;padding:10px;font-size:13px;")
    ).add_to(m)
    folium.GeoJson(smap.to_json(),style_function=lambda x:{"color":"#f87171","weight":2.2,"fillOpacity":0,"dashArray":"5 4"}).add_to(m)

    for _,row in bmap.iterrows():
        try:
            cent=row.geometry.centroid; name=row.get("Name","Basin"); val=row.get(param,"N/A")
            vstr=f"{val:.3f}" if isinstance(val,(int,float)) else str(val)
            rows_html="".join(f'<tr><td style="color:#64748b;padding:2px 8px 2px 0;font-size:11px">{c}</td><td style="color:#e2e8f0;font-weight:700;font-size:11px">{row.get(c,""):.3f}</td></tr>' for c in extra if isinstance(row.get(c),float))
            html=f"""<div style="background:#0f172a;border:1px solid rgba(56,189,248,0.3);border-radius:14px;padding:16px;min-width:200px;font-family:Inter,sans-serif;box-shadow:0 8px 32px rgba(0,0,0,0.5)">
              <div style="font-size:15px;font-weight:800;color:#38bdf8;border-bottom:1px solid rgba(56,189,248,0.15);padding-bottom:8px;margin-bottom:10px">🌊 {name}</div>
              <div style="background:rgba(56,189,248,0.07);border:1px solid rgba(56,189,248,0.12);border-radius:8px;padding:8px 10px;margin-bottom:10px">
                <div style="font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:1px">{param}</div>
                <div style="font-size:22px;font-weight:800;color:#f1f5f9">{vstr}</div>
              </div>
              <table style="width:100%;border-collapse:collapse">{rows_html}</table>
            </div>"""
            folium.Marker([cent.y,cent.x],
                popup=folium.Popup(folium.IFrame(html,width=230,height=min(280,120+len(extra)*20)),max_width=250),
                icon=folium.DivIcon(html='<div style="width:9px;height:9px;border-radius:50%;background:#38bdf8;border:2px solid white;box-shadow:0 0 8px rgba(56,189,248,0.8)"></div>',
                    icon_size=(9,9),icon_anchor=(4,4))).add_to(m)
        except: pass

    colormap=bcm.LinearColormap(colors=["#ffffcc","#a1dab4","#41b6c4","#2c7fb8","#253494"],vmin=mn,vmax=mx,caption=param)
    colormap.add_to(m); MeasureControl(position="bottomleft",primary_length_unit="kilometers").add_to(m)
    Fullscreen(position="topright").add_to(m); MousePosition(position="bottomright").add_to(m)
    bnd=bmap.total_bounds; pad=[(bnd[3]-bnd[1])*0.03,(bnd[2]-bnd[0])*0.03]
    m.fit_bounds([[bnd[1]-pad[0],bnd[0]-pad[1]],[bnd[3]+pad[0],bnd[2]+pad[1]]])
    _,cm,_=st.columns([0.3,9.4,0.3])
    with cm: st_folium(m,width=None,height=520,use_container_width=True)
    if "Name" in bmap.columns:
        tbl=bmap[["Name",param]].sort_values(param,ascending=False)
        st.dataframe(tbl.rename(columns={"Name":"Basin"}),use_container_width=True,height=220)

# ╔═══════════════════════════════════════════════════════╗
# ║  🏔️ MORPHO-HYDROLOGY                                  ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "Morpho-Hydrology":
    if not _ok: st.stop()
    section("🏔️","Basin Morpho-Hydrological Analysis","Profiles · Risk · Shape · Radar · Correlation")

    bdf=basins.copy()
    nb=[c for c in bdf.select_dtypes(include="number").columns if c not in ("OBJECTID","Id","gridcode","FID")]
    _r=lambda c: rc(bdf,c)
    name_col=_r("Name")
    C_HMAX=_r("H_max_m"); C_HMIN=_r("H_min_m"); C_PENTE=_r("Pente")
    C_DD=_r("Drainage_density"); C_TC=_r("Tc_Tixeront"); C_DEBIT=_r("Debit_de_pointe")
    C_RELREL=_r("Relative_relief"); C_KN=_r("Compaction_Index"); C_ER=_r("Elongation_Ratio")
    C_HI=_r("Hypsometric_Integral"); C_CM=_r("Constant_Channel_maintenance")
    C_AREA=_r("Area_km2"); C_RR=_r("Relief_Ratio"); C_CIRC=_r("Circularity")
    MORPHO=[c for c in [_r("Area_km2"),_r("Perimetre_km"),C_KN,C_RR,C_ER,C_CIRC,C_HI] if c]
    HYDRO =[c for c in [C_DD,_r("Stream_frequency"),C_TC,C_DEBIT,_r("Drainage_texture"),C_CM] if c]
    RELIEF=[c for c in [C_HMAX,C_HMIN,C_PENTE,C_RELREL,_r("Ruggedness_number"),C_RR] if c]
    bdf=compute_risk(bdf)

    tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs([
        "📊 Profiles","🏔️ Relief","🔴 Risk & Gauges","📐 Shape","🕸️ Radar","🔗 Correlation","📈 Regression"])

    with tab1:
        c1,c2=st.columns(2)
        with c1: bar_p=st.selectbox("Bar parameter",nb,key="bp")
        with c2: line_p=st.selectbox("Line parameter",nb,index=min(1,len(nb)-1),key="lp")
        xv=bdf[name_col].tolist() if name_col else list(range(len(bdf)))
        fig_d=make_subplots(specs=[[{"secondary_y":True}]])
        fig_d.add_trace(go.Bar(x=xv,y=bdf[bar_p],name=bar_p,
            marker=dict(color=[f"rgba(56,189,248,{0.4+0.5*(v-bdf[bar_p].min())/(bdf[bar_p].max()-bdf[bar_p].min()+1e-9)})" for v in bdf[bar_p]],
                        line=dict(color="rgba(56,189,248,0.3)",width=0.5))),secondary_y=False)
        fig_d.add_trace(go.Scatter(x=xv,y=bdf[line_p],mode="lines+markers",name=line_p,
            line=dict(color="#f87171",width=2.2),marker=dict(size=7,color="#f87171",
            symbol="diamond",line=dict(color="white",width=1))),secondary_y=True)
        fig_d.update_layout(height=420,title=f"{bar_p} (bars) · {line_p} (line)",xaxis_tickangle=-50,**PLOT_LAYOUT)
        fig_d.update_yaxes(title_text=bar_p,secondary_y=False)
        fig_d.update_yaxes(title_text=line_p,secondary_y=True,showgrid=False)
        wrap_chart(fig_d)
        explain("dual_profile")
        st.caption('📐 **Dual-axis profile** — bars show absolute values (left axis); line overlays a second parameter (right axis). Useful for spotting whether larger basins (Area) also have longer concentration times (Tc).')
        sel_st=st.multiselect("Stats columns",nb,default=nb[:min(6,len(nb))])
        if sel_st: st.dataframe(bdf[sel_st].describe(percentiles=[.1,.25,.5,.75,.9]).round(3),use_container_width=True)

    with tab2:
        if C_HMAX and C_HMIN:
            bds=bdf.sort_values(C_HMAX,ascending=False)
            xr=bds[name_col].tolist() if name_col else list(range(len(bds)))
            fig_alt=go.Figure()
            fig_alt.add_trace(go.Scatter(x=xr+xr[::-1],y=list(bds[C_HMAX])+list(bds[C_HMIN][::-1]),
                fill="toself",fillcolor="rgba(56,189,248,0.1)",line=dict(color="rgba(0,0,0,0)"),
                hoverinfo="skip",name="Elevation band"))
            fig_alt.add_trace(go.Scatter(x=xr,y=bds[C_HMAX],mode="lines+markers",name=C_HMAX,
                line=dict(color="#38bdf8",width=2.2),marker=dict(size=6)))
            fig_alt.add_trace(go.Scatter(x=xr,y=bds[C_HMIN],mode="lines+markers",name=C_HMIN,
                line=dict(color="#34d399",width=2.2),marker=dict(size=6)))
            fig_alt.update_layout(height=380,title=f"Altitudinal Profile: {C_HMAX} vs {C_HMIN}",xaxis_tickangle=-50,**PLOT_LAYOUT)
            fig_alt.update_yaxes(title_text="Elevation (m)")
            wrap_chart(fig_alt)
            explain("altitudinal")
            st.caption('🏔️ **Altitudinal profile** — blue band = elevation range (H_max − H_min) per basin, sorted by H_max. Tall narrow bands indicate high relief; wide flat bands indicate gentle terrain. Relief directly drives runoff velocity.')
        else: st.warning(f"Elevation columns not found. Available: {', '.join(nb)}")
        if C_RELREL:
            xr2=bdf[name_col].tolist() if name_col else list(range(len(bdf)))
            fig_rr=go.Figure(go.Scatter(x=xr2,y=bdf[C_RELREL],fill="tozeroy",
                fillcolor="rgba(248,113,113,0.1)",mode="lines+markers",name=C_RELREL,
                line=dict(color="#f87171",width=2),marker=dict(symbol="square",size=7)))
            fig_rr.update_layout(height=280,title="Relative Relief Profile",xaxis_tickangle=-50,**PLOT_LAYOUT)
            wrap_chart(fig_rr)
            explain("relative_relief")
            st.caption('📏 **Relative relief** = (H_max − H_min) / Perimeter (m/km). High values mean steep catchments with fast storm response and high erosion potential. Basins above 30 m/km are typically classified as high-energy.')
        if C_HI:
            bh=bdf.sort_values(C_HI,ascending=False)
            xh=bh[name_col].tolist() if name_col else list(range(len(bh)))
            ch=["#34d399" if v>0.6 else "#fbbf24" if v>0.35 else "#fb923c" for v in bh[C_HI]]
            fig_hi=go.Figure(go.Bar(x=xh,y=bh[C_HI],marker_color=ch,
                text=bh[C_HI].round(3),textposition="outside",
                marker_line_color="rgba(255,255,255,0.05)",marker_line_width=0.5))
            fig_hi.add_hline(y=0.6,line_dash="dash",line_color="#f87171",annotation_text="Youth (0.6)")
            fig_hi.add_hline(y=0.35,line_dash="dash",line_color="#818cf8",annotation_text="Equilibrium (0.35)")
            fig_hi.update_layout(height=340,title="Hypsometric Integral — Geomorphological Maturity",xaxis_tickangle=-55,**PLOT_LAYOUT)
            wrap_chart(fig_hi)
            explain("hypsometric")
            st.caption('⚖️ **Hypsometric Integral (HI)** measures the geomorphological maturity of a basin. HI > 0.60 = Youthful (active erosion, high sediment load). 0.35–0.60 = Equilibrium (mature). < 0.35 = Monadnock (old, stable). Calculated as HI = (mean_elevation − H_min) / (H_max − H_min).')

    with tab3:
        if bdf["Risk_Score"].isna().all():
            st.warning(f"Risk score needs slope/drainage/TC. Available: {', '.join(nb[:12])}")
        else:
            bdr=bdf.sort_values("Risk_Score",ascending=False).reset_index(drop=True)
            xr=bdr[name_col].tolist() if name_col else list(range(len(bdr)))
            rc_colors=["#f87171" if v>0.7 else "#fbbf24" if v>0.4 else "#34d399" for v in bdr["Risk_Score"]]

            # Gauge row for top 4 basins
            g_basins=bdr.head(4)
            gcols=st.columns(4)
            for i,(gcol,(_,grow)) in enumerate(zip(gcols,g_basins.iterrows())):
                with gcol:
                    bn=grow.get(name_col,f"Basin {i+1}") if name_col else f"Basin {i+1}"
                    rs=grow["Risk_Score"]*100
                    fig_g=go.Figure(go.Indicator(
                        mode="gauge+number",value=round(rs,1),
                        title=dict(text=str(bn)[:15],font=dict(color="#94a3b8",size=11)),
                        number=dict(font=dict(color="#f87171" if rs>70 else "#fbbf24" if rs>40 else "#34d399",size=22),suffix="%"),
                        gauge=dict(axis=dict(range=[0,100],tickfont=dict(color="#334155")),
                            bar=dict(color="#f87171" if rs>70 else "#fbbf24" if rs>40 else "#34d399",thickness=0.28),
                            bgcolor="rgba(0,0,0,0)",bordercolor="rgba(56,189,248,0.08)",
                            steps=[dict(range=[0,40],color="rgba(52,211,153,0.08)"),
                                   dict(range=[40,70],color="rgba(251,191,36,0.08)"),
                                   dict(range=[70,100],color="rgba(248,113,113,0.1)")],
                            threshold=dict(line=dict(color="#f87171",width=3),thickness=0.75,value=70))))
                    fig_g.update_layout(height=200,**PLOT_LAYOUT)
                    fig_g.update_layout(margin=dict(l=10,r=10,t=50,b=5))
                    wrap_chart(fig_g)

            fig_risk=go.Figure(go.Bar(x=xr,y=bdr["Risk_Score"],marker_color=rc_colors,
                text=bdr["Risk_Score"].round(3),textposition="outside",
                marker_line_color="rgba(255,255,255,0.05)",marker_line_width=0.5))
            fig_risk.update_layout(height=360,title="Hydrological Risk Ranking",xaxis_tickangle=-55,**PLOT_LAYOUT)
            fig_risk.update_yaxes(title_text="Risk Score (0–1)")
            wrap_chart(fig_risk)
            explain("risk_ranking")
            st.caption('🔴 **Risk Score** = normalised composite of slope (Pente), drainage density (Dd), peak discharge (Qmax) and concentration time (Tc, inverse contribution). Score 0–1: red > 0.7 = High, yellow 0.4–0.7 = Medium, green < 0.4 = Low. Each component is min-max normalised before summing.')

            sc=[name_col]+[c for c in [C_AREA,C_PENTE,C_TC,C_DD,C_DEBIT,"Risk_Score"] if c] if name_col else [c for c in [C_PENTE,C_TC,C_DD,C_DEBIT,"Risk_Score"] if c]
            top5=bdr[[c for c in sc if c in bdr.columns]].head(5).reset_index(drop=True)
            st.markdown("##### 🔴 Top 5 High-Risk Basins")
            st.dataframe(top5.style.background_gradient(subset=["Risk_Score"],cmap="RdYlGn_r"),use_container_width=True)

            if C_PENTE and C_DEBIT:
                sz=bdf[C_AREA] if C_AREA else pd.Series([10]*len(bdf))
                szn=(sz-sz.min())/(sz.max()-sz.min()+1e-9)*35+8
                hue=bdf[C_RR] if C_RR else bdf["Risk_Score"]
                fig_cr=go.Figure(go.Scatter(x=bdf[C_PENTE],y=bdf[C_DEBIT],mode="markers",
                    text=bdf[name_col] if name_col else None,
                    marker=dict(size=szn,color=hue,colorscale="ylorrd",showscale=True,
                        colorbar=dict(title=C_RR or "Risk",thickness=12),
                        line=dict(color="white",width=0.5),opacity=0.88)))
                fig_cr.update_layout(height=400,title=f"Critical Basins: {C_PENTE} vs {C_DEBIT}",**PLOT_LAYOUT)
                fig_cr.update_xaxes(title_text=C_PENTE); fig_cr.update_yaxes(title_text=C_DEBIT)
                wrap_chart(fig_cr)
                explain("critical_scatter")
                st.caption('⚡ **Critical basin identification** — X = slope (%), Y = peak discharge (Qmax). Bubble size = basin area; colour = relief ratio. Top-right quadrant = steep + high peak flow = highest flood risk. Use to prioritise retention infrastructure.')

    with tab4:
        st.markdown("#### Basin Shape Analysis")

        # ── Fallback pickers if canonical columns not resolved ──
        _C_KN   = C_KN   or st.selectbox("Compaction / Gravelius index column", [None]+nb, key="pick_kn")
        _C_ER   = C_ER   or st.selectbox("Elongation Ratio column",              [None]+nb, key="pick_er")
        _C_AREA = C_AREA or st.selectbox("Area column",                           [None]+nb, key="pick_ar")
        _C_TC   = C_TC   or st.selectbox("Concentration Time column",             [None]+nb, key="pick_tc")
        _C_DD   = C_DD   or st.selectbox("Drainage Density column",               [None]+nb, key="pick_dd")
        _C_CM   = C_CM   or st.selectbox("Channel Maintenance column",            [None]+nb, key="pick_cm")

        if _C_KN and _C_AREA:
            tc_c = _C_TC or (nb[0] if nb else None)
            if tc_c:
                sz_ci=bdf[_C_KN]; szn=(sz_ci-sz_ci.min())/(sz_ci.max()-sz_ci.min()+1e-9)*30+8
                fig_atc=go.Figure(go.Scatter(x=bdf[_C_AREA],y=bdf[tc_c],mode="markers",
                    text=bdf[name_col] if name_col else None,
                    marker=dict(size=szn,color="#818cf8",opacity=0.85,line=dict(color="white",width=0.5))))
                fig_atc.update_layout(height=360,title=f"{_C_AREA} vs {tc_c} (size={_C_KN})",**PLOT_LAYOUT)
                fig_atc.update_xaxes(title_text=_C_AREA); fig_atc.update_yaxes(title_text=tc_c)
                wrap_chart(fig_atc)
                explain("area_tc")
                st.caption('🔵 **Area vs Concentration Time** — bubble size = Gravelius Compaction Index (Kc). Tc is the time for runoff to travel from the furthest point to the outlet (Tixeront formula: Tc = 0.5 × L^0.76 / S^0.19). Compact basins (Kc near 1) tend to have shorter Tc and higher flood peaks.')
        else:
            st.info(f"Select Compaction Index and Area columns above. Available: {', '.join(nb[:12])}")

        if _C_KN and _C_ER:
            sz_a=(bdf[_C_AREA]/bdf[_C_AREA].max()*30+8) if _C_AREA else 10
            tc_hue=bdf[_C_TC] if _C_TC else None
            fig_sh=go.Figure(go.Scatter(x=bdf[_C_KN],y=bdf[_C_ER],mode="markers",
                text=bdf[name_col] if name_col else None,
                marker=dict(size=sz_a,color=tc_hue if tc_hue is not None else "#818cf8",
                    colorscale="rdbu",showscale=(tc_hue is not None),
                    colorbar=dict(title=_C_TC) if tc_hue is not None else None,
                    opacity=0.88,line=dict(color="white",width=0.5))))
            fig_sh.add_vline(x=1.0,line_dash="dash",line_color="#f87171",annotation_text="Circle (Kc=1)")
            fig_sh.update_layout(height=380,title=f"Shape: {_C_KN} vs {_C_ER}",**PLOT_LAYOUT)
            fig_sh.update_xaxes(title_text=_C_KN); fig_sh.update_yaxes(title_text=_C_ER)
            wrap_chart(fig_sh)
            explain("shape_scatter")
            st.caption('🔶 **Shape analysis** — Gravelius Index Kc = Perimeter / (2√(π·Area)). Kc = 1 = perfect circle (highest flood risk). Elongation Ratio Re = diameter of equivalent circle / max length. Re near 1 = circular; Re < 0.5 = very elongated (low peak, long response). Colour = concentration time.')

        if _C_DD and _C_CM:
            fig_dl=go.Figure()
            fig_dl.add_trace(go.Scatter(x=bdf[_C_DD],y=bdf[_C_CM],mode="markers",
                text=bdf[name_col] if name_col else None,
                marker=dict(color="#38bdf8",size=9,opacity=0.85,line=dict(color="white",width=0.5))))
            xy=pd.DataFrame({"x":bdf[_C_DD],"y":bdf[_C_CM]}).dropna()
            if len(xy)>2:
                sl,ic,*_=stats.linregress(xy["x"],xy["y"]); xl=np.linspace(xy["x"].min(),xy["x"].max(),80)
                fig_dl.add_trace(go.Scatter(x=xl,y=sl*xl+ic,mode="lines",
                    line=dict(color="#f87171",width=2),name="Regression"))
            fig_dl.update_layout(height=360,title=f"Drainage Law: {_C_DD} vs {_C_CM}",**PLOT_LAYOUT)
            fig_dl.update_xaxes(title_text=_C_DD); fig_dl.update_yaxes(title_text=_C_CM)
            wrap_chart(fig_dl)
            explain("drainage_law")

    with tab5:
        st.markdown("#### 🕸️ Basin Radar / Spider Chart")
        st.markdown('<div class="info-box">📌 Each polygon = one basin. Axes normalised 0–1 for direct comparison. If canonical columns were not auto-detected, select them manually below.</div>', unsafe_allow_html=True)
        radar_pool = list(dict.fromkeys([c for c in MORPHO+HYDRO+RELIEF if c] + nb))
        radar_default = radar_pool[:min(6, len(radar_pool))]
        radar_cols = st.multiselect("Radar axes (select 3–8)", nb, default=[c for c in radar_default if c in nb], key="rad_axes")
        name_sel   = st.selectbox("Basin name column", [None]+list(bdf.select_dtypes(include="object").columns), key="rad_nm")
        actual_name = name_sel or name_col

        if len(radar_cols) >= 3:
            norm_bdf = bdf.copy()
            for c in radar_cols:
                rng = norm_bdf[c].max() - norm_bdf[c].min()
                norm_bdf[c] = (norm_bdf[c] - norm_bdf[c].min()) / (rng + 1e-9)
            fig_rad = go.Figure()
            for i, (_, row) in enumerate(norm_bdf.iterrows()):
                nm = str(row[actual_name])[:20] if actual_name and actual_name in row else f"Basin {i+1}"
                vals = [row[c] for c in radar_cols] + [row[radar_cols[0]]]
                cats = radar_cols + [radar_cols[0]]
                r, g, b = tuple(int(C_PALETTE[i%len(C_PALETTE)].lstrip("#")[j:j+2], 16) for j in (0,2,4))
                fig_rad.add_trace(go.Scatterpolar(
                    r=vals, theta=cats, fill="toself", name=nm,
                    line=dict(color=C_PALETTE[i%len(C_PALETTE)], width=1.8),
                    fillcolor=f"rgba({r},{g},{b},0.07)"
                ))
            fig_rad.update_layout(height=520, title="Multi-Basin Radar Comparison",
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,1], gridcolor="rgba(255,255,255,0.06)",
                        tickfont=dict(color="#475569", size=9)),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=11)),
                    bgcolor="rgba(0,0,0,0)"
                ), **PLOT_LAYOUT)
            wrap_chart(fig_rad)
            explain("radar")
            st.caption('🕸️ **Radar / Spider chart** — each polygon represents one basin; axes are min-max normalised to [0–1] for fair comparison. Larger polygon area = more extreme values across all parameters. Useful for visually clustering basins by morpho-hydrological signature.')
        else:
            st.info("Select at least 3 axes from the multiselect above to render the radar chart.")

    with tab6:
        kcands = list(dict.fromkeys([c for c in MORPHO+HYDRO+RELIEF if c]))
        avail  = [c for c in kcands if c in bdf.columns and bdf[c].notna().sum() > 2]
        if not avail:
            avail = [c for c in nb if bdf[c].notna().sum() > 2]
        sel_corr = st.multiselect("Parameters for correlation", avail or nb,
                                   default=(avail or nb)[:min(10, len(avail or nb))], key="corr_sel")
        if len(sel_corr)>=2:
            cm=bdf[sel_corr].corr().round(3)
            mask=np.triu(np.ones_like(cm,dtype=bool),k=1)
            cd=cm.copy(); cd[mask]=np.nan
            fig_cor=go.Figure(go.Heatmap(
                z=cd.values,x=cd.columns.tolist(),y=cd.index.tolist(),
                colorscale="rdbu",zmid=0,zmin=-1,zmax=1,
                text=np.where(mask,"",cd.round(2).astype(str).values),texttemplate="%{text}",
                colorbar=dict(title="r",thickness=14,len=0.85),hoverongaps=False))
            fig_cor.update_layout(height=max(380,len(sel_corr)*40),title="Morpho-Hydrological Correlation Matrix",**PLOT_LAYOUT)
            wrap_chart(fig_cor)
            explain("correlation")
            st.caption('🔗 **Pearson correlation matrix** (lower triangle). r > 0.7 = strong positive (red). r < −0.7 = strong negative (blue). Near zero = no linear relationship. Note: correlation ≠ causation. Check scatter plots in the Regression tab to confirm direction and linearity.')
            strong=[(sel_corr[i],sel_corr[j],round(cm.iloc[i,j],3))
                    for i in range(len(sel_corr)) for j in range(i+1,len(sel_corr)) if abs(cm.iloc[i,j])>0.7]
            if strong:
                st.markdown("**Strong correlations |r| > 0.7:**")
                st.dataframe(pd.DataFrame(strong,columns=["Param A","Param B","r"]).sort_values("r",key=abs,ascending=False),use_container_width=True)
        else: st.info("Select at least 2 parameters.")

    with tab7:
        c1,c2=st.columns(2)
        with c1: xr=st.selectbox("X",nb,key="rx")
        with c2: yr=st.selectbox("Y",nb,index=min(1,len(nb)-1),key="ry")
        sz_r=(bdf[C_AREA]/bdf[C_AREA].max()*30+8) if C_AREA else 10
        fig_reg=go.Figure()
        fig_reg.add_trace(go.Scatter(x=bdf[xr],y=bdf[yr],mode="markers",
            text=bdf[name_col] if name_col else None,
            marker=dict(size=sz_r,color="#818cf8",opacity=0.85,line=dict(color="white",width=0.5))))
        xy2=pd.DataFrame({"x":bdf[xr],"y":bdf[yr]}).dropna()
        if len(xy2)>2:
            sl,ic,r,pv,_=stats.linregress(xy2["x"],xy2["y"])
            xl=np.linspace(xy2["x"].min(),xy2["x"].max(),100)
            fig_reg.add_trace(go.Scatter(x=xl,y=sl*xl+ic,mode="lines",
                line=dict(color="#34d399",width=2.2),name=f"R²={r**2:.3f}"))
            st.markdown(f"**y = {sl:.4f}·x + {ic:.4f}** &nbsp;|&nbsp; **R² = {r**2:.4f}** &nbsp;|&nbsp; **p = {pv:.4e}**")
        fig_reg.update_layout(height=440,title=f"Regression: {yr} ~ {xr}",**PLOT_LAYOUT)
        fig_reg.update_xaxes(title_text=xr); fig_reg.update_yaxes(title_text=yr)
        wrap_chart(fig_reg)

# ╔═══════════════════════════════════════════════════════╗
# ║  🔬 MULTIVARIATE ANALYSIS                             ║
# ╚═══════════════════════════════════════════════════════╝
# ╔═══════════════════════════════════════════════════════╗
# ║  📊 NASA vs PREDICTION                                ║
# ╚═══════════════════════════════════════════════════════╝
elif PAGE == "NASA vs Prediction":
    section("📊","NASA vs Prediction Comparison","Overlay · Scatter · Seasonal · Animated divergence")

    nasa_files=sorted([f for f in os.listdir(NASA_DIR) if f.endswith(".csv")]) if os.path.isdir(NASA_DIR) else []
    pred_files=sorted([f for f in os.listdir(PRED_DIR) if f.endswith(".csv")]) if os.path.isdir(PRED_DIR) else []
    if not nasa_files or not pred_files: st.warning("Need both NASA and prediction folders."); st.stop()

    c1,c2,c3=st.columns(3)
    with c1: n=st.selectbox("NASA dataset",nasa_files)
    with c2: p=st.selectbox("Prediction dataset",pred_files)
    df_n=load_csv(os.path.join(NASA_DIR,n)); df_p=load_csv(os.path.join(PRED_DIR,p))
    common=sorted(set(num_cols(df_n))&set(num_cols(df_p)))
    if not common: st.error("No common numeric columns."); st.stop()
    with c3: param=st.selectbox("Parameter",common)

    # Date merge
    _dn=df_n[["Date",param]].copy(); _dp=df_p[["Date",param]].copy()
    _dn["_d"]=pd.to_datetime(_dn["Date"]).dt.normalize()
    _dp["_d"]=pd.to_datetime(_dp["Date"]).dt.normalize()
    merged=pd.merge(_dn[["_d",param]].rename(columns={param:"NASA"}),
                    _dp[["_d",param]].rename(columns={param:"Pred"}),on="_d",how="inner").dropna()
    if merged.empty:
        n_pts=min(len(df_n),len(df_p))
        if n_pts>10:
            merged=pd.DataFrame({"_d":range(n_pts),"NASA":df_n[param].iloc[:n_pts].values,
                                  "Pred":df_p[param].iloc[:n_pts].values}).dropna()

    if not merged.empty:
        res=scatter_stats(merged["NASA"].values,merged["Pred"].values)
        if res:
            sl,ic,r2,rmse=res; bias=float((merged["Pred"]-merged["NASA"]).mean())
            mae=float((merged["Pred"]-merged["NASA"]).abs().mean())
            kpi_row([("R²",f"{r2:.4f}","",None,r2>0.7,"🎯"),
                     ("RMSE",f"{rmse:.4f}","",None,rmse<1,"📉"),
                     ("MAE",f"{mae:.4f}","",None,mae<1,"📊"),
                     ("Bias",f"{bias:+.4f}","",None,bias>=0,"↔️"),
                     ("N points",str(len(merged)),"",None,True,"🔢")])

    tab1,tab2,tab3,tab4,tab5,tab6=st.tabs(["📈 Overlay","📊 Distributions","🔵 Scatter","📅 Seasonal","🎬 Animated Divergence","Δ Difference"])

    with tab1:
        fig_ov=go.Figure()
        fig_ov.add_trace(go.Scatter(x=df_n["Date"],y=df_n[param],mode="lines",name="NASA",
            line=dict(color="#38bdf8",width=1.8)))
        fig_ov.add_trace(go.Scatter(x=df_p["Date"],y=df_p[param],mode="lines",name="Prediction",
            line=dict(color="#34d399",width=2,dash="dot")))
        fig_ov.update_layout(height=400,title=f"{param}: NASA vs Prediction",**PLOT_LAYOUT)
        wrap_chart(fig_ov)

    with tab2:
        c1,c2=st.columns(2)
        with c1:
            fig_hist=go.Figure()
            fig_hist.add_trace(go.Histogram(x=df_n[param],name="NASA",opacity=0.7,marker_color="#38bdf8",nbinsx=45))
            fig_hist.add_trace(go.Histogram(x=df_p[param],name="Prediction",opacity=0.7,marker_color="#34d399",nbinsx=45))
            fig_hist.update_layout(barmode="overlay",height=320,title="Overlapping Histograms",**PLOT_LAYOUT)
            wrap_chart(fig_hist)
        with c2:
            fig_vio=go.Figure()
            fig_vio.add_trace(go.Violin(y=df_n[param],name="NASA",line_color="#38bdf8",
                fillcolor="rgba(56,189,248,0.1)",box_visible=True,meanline_visible=True,points=False))
            fig_vio.add_trace(go.Violin(y=df_p[param],name="Prediction",line_color="#34d399",
                fillcolor="rgba(52,211,153,0.1)",box_visible=True,meanline_visible=True,points=False))
            fig_vio.update_layout(height=320,title="Violin Comparison",**PLOT_LAYOUT)
            wrap_chart(fig_vio)

    with tab3:
        if not merged.empty and res:
            sl,ic,r2,rmse=res; mn2=min(merged["NASA"].min(),merged["Pred"].min()); mx2=max(merged["NASA"].max(),merged["Pred"].max())
            fig_sc=go.Figure()
            fig_sc.add_trace(go.Scatter(x=merged["NASA"],y=merged["Pred"],mode="markers",
                marker=dict(color="#818cf8",size=4,opacity=0.55),name="Data points"))
            fig_sc.add_trace(go.Scatter(x=np.linspace(mn2,mx2,100),y=sl*np.linspace(mn2,mx2,100)+ic,
                mode="lines",line=dict(color="#f472b6",width=2.2),name=f"Fit  R²={r2:.3f}"))
            fig_sc.add_trace(go.Scatter(x=[mn2,mx2],y=[mn2,mx2],mode="lines",
                line=dict(color="rgba(255,255,255,0.2)",dash="dash",width=1.5),name="1:1"))
            fig_sc.update_layout(height=420,title="Scatter & Regression",**PLOT_LAYOUT)
            fig_sc.update_xaxes(title_text="NASA"); fig_sc.update_yaxes(title_text="Prediction")
            wrap_chart(fig_sc)
        else: st.info("No overlapping dates found for scatter plot.")

    with tab4:
        df_ns=add_season(df_n); df_ps=add_season(df_p)
        sn=df_ns.groupby("Season")[param].mean().reindex(["Winter","Spring","Summer","Autumn"])
        sp=df_ps.groupby("Season")[param].mean().reindex(["Winter","Spring","Summer","Autumn"])
        c1,c2=st.columns(2)
        with c1:
            fig_sb=go.Figure()
            fig_sb.add_trace(go.Bar(x=sn.index,y=sn.values,name="NASA",marker_color="rgba(56,189,248,0.75)"))
            fig_sb.add_trace(go.Bar(x=sp.index,y=sp.values,name="Prediction",marker_color="rgba(52,211,153,0.75)"))
            fig_sb.update_layout(barmode="group",height=340,title="Seasonal Mean Comparison",**PLOT_LAYOUT)
            wrap_chart(fig_sb)
        with c2:
            cn=monthly_clim(df_n.copy(),param); cp=monthly_clim(df_p.copy(),param)
            fig_mc=go.Figure()
            fig_mc.add_trace(go.Scatter(x=cn["month"],y=cn["mean"],mode="lines+markers",name="NASA",
                line=dict(color="#38bdf8",width=2.2),marker=dict(size=7)))
            fig_mc.add_trace(go.Scatter(x=cp["month"],y=cp["mean"],mode="lines+markers",name="Prediction",
                line=dict(color="#34d399",width=2.2,dash="dot"),marker=dict(size=7,symbol="square")))
            fig_mc.update_layout(height=340,title="Monthly Climatology",**PLOT_LAYOUT)
            fig_mc.update_xaxes(tickmode="array",tickvals=list(range(1,13)),ticktext=MONTHS)
            wrap_chart(fig_mc)

    with tab5:
        st.markdown('<div class="info-box">🎬 Animated annual divergence — bars show NASA vs Prediction side by side, evolving year by year.</div>',unsafe_allow_html=True)
        df_ns2=add_season(df_n); df_ps2=add_season(df_p)
        ann_n=df_ns2.groupby(["Year","Month"])[param].mean().reset_index().rename(columns={param:"NASA"})
        ann_p=df_ps2.groupby(["Year","Month"])[param].mean().reset_index().rename(columns={param:"Pred"})
        ann_m=pd.merge(ann_n,ann_p,on=["Year","Month"],how="inner")
        if not ann_m.empty:
            ann_m["Year"]=ann_m["Year"].astype(int).astype(str)
            ann_m["Month_name"]=ann_m["Month"].apply(lambda x: MONTHS[x-1])
            ann_long=ann_m.melt(id_vars=["Year","Month","Month_name"],value_vars=["NASA","Pred"],var_name="Source",value_name=param)
            fig_anim=px.bar(ann_long,x="Month_name",y=param,color="Source",barmode="group",
                animation_frame="Year",color_discrete_map={"NASA":"#38bdf8","Pred":"#34d399"},
                title=f"{param} — NASA vs Prediction Monthly (Animated)",
                category_orders={"Month_name":MONTHS})
            fig_anim.update_layout(height=400,**PLOT_LAYOUT)
            fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"]=ANIM_SPEED
            wrap_chart(fig_anim)
        else: st.info("No overlapping data for animation.")

    with tab6:
        st.markdown('<div class="info-box">Δ Difference map — Prediction minus NASA, by month and year. Positive = model predicts more than observed. Animated frame-by-frame.</div>', unsafe_allow_html=True)
        if not merged.empty:
            merged_idx = merged.copy()
            merged_idx["delta"] = merged_idx["Pred"] - merged_idx["NASA"]
            merged_idx["delta_color"] = np.where(merged_idx["delta"] > 0, "#f87171", "#38bdf8")

            # Delta time series with animated envelope
            fig_delta = go.Figure()
            fig_delta.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_width=1)
            fig_delta.add_trace(go.Scatter(
                x=merged_idx["_d"], y=merged_idx["delta"],
                mode="lines", name="Δ (Pred − NASA)",
                line=dict(color="#818cf8", width=1.5),
                fill="tozeroy",
                fillcolor=f"rgba(129,140,248,0.08)"
            ))
            roll_d = merged_idx["delta"].rolling(90, center=True, min_periods=20).mean()
            fig_delta.add_trace(go.Scatter(
                x=merged_idx["_d"], y=roll_d,
                mode="lines", name="90d smoothed Δ",
                line=dict(color="#fbbf24", width=2.5)
            ))
            fig_delta.update_layout(height=380, title=f"{param} — Prediction minus NASA (Δ)", **PLOT_LAYOUT)
            fig_delta.update_yaxes(title_text=f"Δ {param}")
            wrap_chart(fig_delta)

            # Monthly delta heatmap
            if "_d" in merged_idx.columns:
                merged_idx["Year2"] = pd.to_datetime(merged_idx["_d"]).dt.year
                merged_idx["Month2"] = pd.to_datetime(merged_idx["_d"]).dt.month
            else:
                merged_idx["Year2"] = merged_idx.index
                merged_idx["Month2"] = 1
            pivot_d = merged_idx.groupby(["Year2","Month2"])["delta"].mean().unstack(fill_value=np.nan)
            pivot_d.columns = MONTHS[:len(pivot_d.columns)]
            fig_dh = go.Figure(go.Heatmap(
                z=pivot_d.values, x=pivot_d.columns.tolist(), y=pivot_d.index.tolist(),
                colorscale="rdbu", zmid=0,
                text=np.round(pivot_d.values, 3), texttemplate="%{text}",
                colorbar=dict(title=f"Δ {param}", thickness=12)
            ))
            fig_dh.update_layout(height=350, title=f"{param} — Bias Heatmap (Year × Month)", **PLOT_LAYOUT)
            wrap_chart(fig_dh)

            bias = merged_idx["delta"].mean()
            mae_d = merged_idx["delta"].abs().mean()
            kpi_row([
                ("Mean Bias",   f"{bias:+.4f}", "", None, bias>=0, "📊"),
                ("MAE",         f"{mae_d:.4f}",  "", None, True,   "🎯"),
                ("Max Δ",       f"{merged_idx['delta'].max():+.4f}", "", None, True, "⬆️"),
                ("Min Δ",       f"{merged_idx['delta'].min():+.4f}", "", None, False,"⬇️"),
                ("N points",    str(len(merged_idx)), "", None, True, "🔢"),
            ])
        else:
            st.info("No overlapping data to compute differences.")

