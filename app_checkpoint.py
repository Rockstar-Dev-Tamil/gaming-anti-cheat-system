"""
Gaming Bot Behaviour Analyzer — Cyber Command Center Dashboard
================================================================
Launch:  streamlit run app.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from bot_analyzer import generate_dataset, engineer_features, detect_anomalies, build_leaderboard

# ═══════════════════════════════════════════════════════════════════
# Page Config
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=" Anti-Cheat Command Center",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
# CSS — Cyber Command Center Theme
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ══════════ ROOT VARIABLES ══════════ */
:root {
    --bg-deep: #0b0f19;
    --bg-panel: rgba(15, 23, 42, 0.65);
    --border-glass: rgba(0, 245, 255, 0.12);
    --cyan: #00f5ff;
    --purple: #8b5cf6;
    --pink: #ec4899;
    --red: #ff3b3b;
    --orange: #f97316;
    --green: #10b981;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --glow-cyan: 0 0 20px rgba(0,245,255,.25);
    --glow-purple: 0 0 20px rgba(139,92,246,.25);
    --glow-red: 0 0 20px rgba(255,59,59,.3);
    --radius: 18px;
}

/* ══════════ GLOBAL ══════════ */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: var(--bg-deep);
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(139,92,246,.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(0,245,255,.06) 0%, transparent 60%);
    animation: bgDrift 20s ease-in-out infinite alternate;
}
@keyframes bgDrift {
    0%   { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ══════════ CINEMATIC INTRO ══════════ */
@keyframes introFadeIn {
    0%   { opacity: 0; transform: scale(1.1); filter: blur(15px); }
    100% { opacity: 1; transform: scale(1);   filter: blur(0); }
}
@keyframes introSlideUp {
    0%   { opacity: 0; transform: translateY(40px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes scanline {
    0%   { top: -5%; }
    100% { top: 105%; }
}
@keyframes glitchFlicker {
    0%, 90%, 100% { opacity: 1; }
    92% { opacity: 0.7; transform: translateX(-2px); }
    94% { opacity: 1; transform: translateX(2px); }
    96% { opacity: 0.8; transform: translateX(0); }
}

.intro-overlay {
    position: fixed; inset: 0; z-index: 9999;
    background: var(--bg-deep);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: introFadeIn .8s ease-out forwards;
    pointer-events: none;
    overflow: hidden;
}
.intro-overlay::after {
    content: ''; position: absolute; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    animation: scanline 2s linear infinite;
    opacity: .4;
}
.intro-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.4rem; font-weight: 900;
    background: linear-gradient(135deg, var(--cyan), var(--purple), var(--pink));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-transform: uppercase; letter-spacing: .12em;
    animation: glitchFlicker 3s ease-in-out infinite, introSlideUp 1s .3s both;
    text-shadow: 0 0 40px rgba(0,245,255,.3);
}
.intro-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem; color: var(--cyan); letter-spacing: .25em;
    text-transform: uppercase; margin-top: .8rem;
    animation: introSlideUp 1s .6s both;
    opacity: .8;
}
.intro-fade {
    animation: fadeOutIntro 1s 2.8s forwards;
}
@keyframes fadeOutIntro {
    0%   { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}

/* ══════════ HERO ══════════ */
@keyframes heroReveal {
    0%   { opacity: 0; transform: translateY(30px); filter: blur(8px); }
    100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.hero { text-align: center; padding: 1.8rem 0 .5rem; animation: heroReveal 1s .2s both; }
.hero h1 {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 50%, var(--pink) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: .3rem;
    text-shadow: 0 0 60px rgba(0,245,255,.15);
}
.hero p {
    color: var(--text-secondary); font-size: 1rem;
    font-family: 'JetBrains Mono', monospace; letter-spacing: .04em;
}

/* ══════════ METRIC CARDS ══════════ */
@keyframes cardFloat {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}
@keyframes countBounce {
    0%   { transform: scale(0.6); opacity: 0; }
    60%  { transform: scale(1.08); }
    100% { transform: scale(1); opacity: 1; }
}

.metrics-grid {
    display: flex; justify-content: center; gap: 1.4rem;
    flex-wrap: wrap; margin: 1.5rem auto 2rem; max-width: 1100px;
}
.metric-card {
    background: var(--bg-panel);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius);
    padding: 1.5rem 2rem; min-width: 210px;
    text-align: center; position: relative;
    backdrop-filter: blur(16px);
    transition: transform .25s cubic-bezier(.34,1.56,.64,1), box-shadow .3s;
    animation: cardFloat 6s ease-in-out infinite;
    cursor: default;
    overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; inset: 0;
    border-radius: var(--radius);
    background: linear-gradient(135deg, rgba(0,245,255,.04), rgba(139,92,246,.04));
    opacity: 0; transition: opacity .3s;
}
.metric-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: var(--glow-cyan);
}
.metric-card:hover::before { opacity: 1; }
.metric-card:active { transform: translateY(-4px) scale(0.98); }

.metric-card:nth-child(2) { animation-delay: .8s; }
.metric-card:nth-child(3) { animation-delay: 1.6s; }
.metric-card:nth-child(4) { animation-delay: 2.4s; }

.metric-icon { font-size: 1.6rem; margin-bottom: .3rem; }
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem; font-weight: 800;
    animation: countBounce .7s .5s both;
}
.metric-label {
    color: var(--text-secondary); font-size: .8rem;
    font-weight: 600; text-transform: uppercase;
    letter-spacing: .08em; margin-top: .25rem;
}

.val-cyan    { color: var(--cyan); text-shadow: 0 0 20px rgba(0,245,255,.4); }
.val-red     { color: var(--red);  text-shadow: 0 0 20px rgba(255,59,59,.4); }
.val-green   { color: var(--green); text-shadow: 0 0 20px rgba(16,185,129,.4); }
.val-purple  { color: var(--purple); text-shadow: 0 0 20px rgba(139,92,246,.4); }

/* ══════════ GLASS PANEL ══════════ */
.glass-panel {
    background: var(--bg-panel);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius);
    padding: 1.5rem; margin: .8rem 0;
    backdrop-filter: blur(16px);
}

/* ══════════ TABS ══════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: .5rem; justify-content: center;
    border-bottom: 1px solid rgba(0,245,255,.1);
    padding-bottom: 2px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 12px 12px 0 0;
    color: var(--text-secondary);
    font-family: 'Orbitron', monospace;
    font-weight: 600; font-size: .85rem;
    padding: .65rem 1.8rem;
    transition: all .3s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--cyan);
    background: rgba(0,245,255,.06);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,245,255,.15), rgba(139,92,246,.12)) !important;
    color: var(--cyan) !important;
    border-color: var(--cyan) !important;
    border-bottom-color: transparent !important;
    box-shadow: 0 -2px 15px rgba(0,245,255,.15);
}

/* Tab content fade-in */
.stTabs [data-baseweb="tab-panel"] {
    animation: tabSlide .4s ease-out;
}
@keyframes tabSlide {
    0%   { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* ══════════ RISK BADGES ══════════ */
@keyframes pulseRed {
    0%, 100% { box-shadow: 0 0 5px rgba(255,59,59,.3); }
    50%      { box-shadow: 0 0 20px rgba(255,59,59,.6); }
}
.risk-badge {
    display: inline-flex; align-items: center; gap: .4rem;
    padding: .3rem .8rem; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .06em;
}
.risk-high {
    background: rgba(255,59,59,.15);
    border: 1px solid rgba(255,59,59,.4);
    color: var(--red);
    animation: pulseRed 2s ease-in-out infinite;
}
.risk-medium {
    background: rgba(249,115,22,.12);
    border: 1px solid rgba(249,115,22,.35);
    color: var(--orange);
}
.risk-low {
    background: rgba(16,185,129,.1);
    border: 1px solid rgba(16,185,129,.3);
    color: var(--green);
}

/* ══════════ INTEGRITY BAR ══════════ */
@keyframes barFill {
    0%   { width: 0%; }
}
.integrity-bar-bg {
    width: 100%; height: 8px; border-radius: 4px;
    background: rgba(255,255,255,.06);
    overflow: hidden; position: relative;
}
.integrity-bar-fill {
    height: 100%; border-radius: 4px;
    animation: barFill 1.2s cubic-bezier(.25,.46,.45,.94) forwards;
    box-shadow: 0 0 12px currentColor;
}

/* ══════════ CONFIDENCE RING ══════════ */
.conf-ring-container {
    display: inline-flex; align-items: center;
    justify-content: center; position: relative;
    width: 54px; height: 54px;
}
.conf-ring-container svg { transform: rotate(-90deg); }
.conf-ring-label {
    position: absolute;
    font-family: 'Orbitron', monospace;
    font-size: .65rem; font-weight: 700;
    color: var(--text-primary);
}

/* ══════════ PLAYER CARD ══════════ */
@keyframes neonShimmer {
    0%, 100% { border-color: rgba(255,59,59,.25); }
    50%      { border-color: rgba(255,59,59,.55); }
}
.player-card {
    background: var(--bg-panel);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem; margin-bottom: .8rem;
    backdrop-filter: blur(12px);
    transition: transform .2s, box-shadow .3s;
    display: flex; align-items: center; gap: 1.2rem;
}
.player-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--glow-purple);
}
.player-card.suspicious {
    border-color: rgba(255,59,59,.3);
    animation: neonShimmer 3s ease-in-out infinite;
}
.player-card.suspicious:hover {
    box-shadow: var(--glow-red);
}
.player-info { flex: 1; }
.player-id {
    font-family: 'Orbitron', monospace;
    font-size: 1rem; font-weight: 700;
    color: var(--text-primary);
}
.player-stats {
    display: flex; gap: 1.2rem; margin-top: .4rem;
    font-size: .8rem; color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}
.player-stats span b { color: var(--cyan); }

/* ══════════ SECTION HEADERS ══════════ */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.05rem; font-weight: 700;
    color: var(--cyan); margin: 1rem 0 .8rem;
    padding-bottom: .4rem;
    border-bottom: 1px solid rgba(0,245,255,.15);
    letter-spacing: .05em;
}

/* ══════════ HOW-IT-WORKS ══════════ */
.how-it-works {
    background: var(--bg-panel);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius);
    padding: 1.5rem; margin-top: 1.5rem;
    backdrop-filter: blur(12px);
}
.how-it-works h4 {
    font-family: 'Orbitron', monospace;
    color: var(--cyan); font-size: .95rem; margin-bottom: .8rem;
}
.how-it-works p, .how-it-works li {
    color: var(--text-secondary); font-size: .85rem;
    line-height: 1.6;
}

/* ══════════ REFRESH BTN ══════════ */
.stButton > button {
    font-family: 'Orbitron', monospace !important;
    font-weight: 600 !important;
    border: 1px solid var(--cyan) !important;
    color: var(--cyan) !important;
    background: rgba(0,245,255,.06) !important;
    border-radius: 12px !important;
    padding: .5rem 1.5rem !important;
    transition: all .25s !important;
    letter-spacing: .04em !important;
}
.stButton > button:hover {
    background: rgba(0,245,255,.15) !important;
    box-shadow: var(--glow-cyan) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: scale(.96) !important;
}

/* ══════════ DATAFRAME ══════════ */
.stDataFrame { border-radius: 14px; overflow: hidden; }

/* ══════════ FOOTER ══════════ */
.footer {
    text-align: center; padding: 2.5rem 0 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem; color: #334155;
    letter-spacing: .05em;
}

/* ══════════ SELECTBOX/TOGGLE ══════════ */
.stSelectbox > div > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}
.stToggle label span { font-family: 'JetBrains Mono', monospace; font-size: .85rem; }

/* ══════════ EXPANDER ══════════ */
.streamlit-expanderHeader {
    font-family: 'Orbitron', monospace !important;
    color: var(--cyan) !important;
    font-size: .9rem !important;
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius) !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# CINEMATIC INTRO
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="intro-overlay intro-fade">
    <div class="intro-title">Anti-Cheat Command Center</div>
    <div class="intro-sub">▸ Initializing threat analysis ▸ Loading player data ▸ Scanning anomalies</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# DATA PIPELINE (Cached)
# ═══════════════════════════════════════════════════════════════════
def run_full_pipeline(seed_offset=0):
    raw = generate_dataset(n=1000, cheater_ratio=0.08, seed=42 + seed_offset)
    features = engineer_features(raw)
    scored = detect_anomalies(features)
    leaderboard = build_leaderboard(scored)
    return raw, leaderboard

if "sim_count" not in st.session_state:
    st.session_state.sim_count = 0

raw_df, lb = run_full_pipeline(st.session_state.sim_count)
suspicious = lb[lb["suspicious_flag"] == True].copy()
clean = lb[lb["suspicious_flag"] == False].copy()


# ═══════════════════════════════════════════════════════════════════
# HELPER: Risk badge HTML
# ═══════════════════════════════════════════════════════════════════
def risk_badge(confidence):
    if confidence > 0.8:
        return '<span class="risk-badge risk-high">🔴 HIGH RISK</span>'
    elif confidence > 0.5:
        return '<span class="risk-badge risk-medium">🟠 MEDIUM RISK</span>'
    else:
        return '<span class="risk-badge risk-low">🟢 LOW RISK</span>'


# ═══════════════════════════════════════════════════════════════════
# HELPER: SVG Confidence Ring
# ═══════════════════════════════════════════════════════════════════
def confidence_ring(value, size=54, stroke=5):
    r = (size - stroke) / 2
    circ = 2 * np.pi * r
    offset = circ * (1 - value)
    if value > 0.8:
        color = "var(--red)"
    elif value > 0.5:
        color = "var(--orange)"
    else:
        color = "var(--green)"
    return f"""
    <div class="conf-ring-container">
        <svg width="{size}" height="{size}">
            <circle cx="{size/2}" cy="{size/2}" r="{r}"
                fill="none" stroke="rgba(255,255,255,.08)" stroke-width="{stroke}"/>
            <circle cx="{size/2}" cy="{size/2}" r="{r}"
                fill="none" stroke="{color}" stroke-width="{stroke}"
                stroke-dasharray="{circ}" stroke-dashoffset="{offset}"
                stroke-linecap="round"
                style="transition: stroke-dashoffset 1.2s ease-out;"/>
        </svg>
        <span class="conf-ring-label">{value:.0%}</span>
    </div>"""


# ═══════════════════════════════════════════════════════════════════
# HELPER: Integrity Bar
# ═══════════════════════════════════════════════════════════════════
def integrity_bar(score):
    pct = max(0, min(100, score * 100))
    if score > 0.7:
        color = "var(--green)"
    elif score > 0.4:
        color = "var(--orange)"
    else:
        color = "var(--red)"
    return f"""
    <div class="integrity-bar-bg">
        <div class="integrity-bar-fill" style="width:{pct}%;background:{color};color:{color};"></div>
    </div>"""


# ═══════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>🎮 Anti-Cheat Command Center</h1>
    <p>AI-powered Isolation Forest model scanning 1,000 player sessions for anomalous behaviour patterns</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# CONTROLS ROW
# ═══════════════════════════════════════════════════════════════════
ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 1])
with ctrl2:
    if st.button("⟳  Simulate New Session Data", use_container_width=True):
        st.session_state.sim_count += 1
        st.rerun()


# ═══════════════════════════════════════════════════════════════════
# METRIC CARDS
# ═══════════════════════════════════════════════════════════════════
total_players = len(lb)
flagged = len(suspicious)
clean_pct = len(clean) / total_players * 100
avg_integrity = lb["integrity_score"].mean()

st.markdown(f"""
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-icon">👥</div>
        <div class="metric-value val-cyan">{total_players}</div>
        <div class="metric-label">Total Players</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🚨</div>
        <div class="metric-value val-red">{flagged}</div>
        <div class="metric-label">Threats Detected</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🛡️</div>
        <div class="metric-value val-green">{clean_pct:.1f}%</div>
        <div class="metric-label">Clean Rate</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value val-purple">{avg_integrity:.2f}</div>
        <div class="metric-label">Avg Integrity</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🏆 LEADERBOARD", "🚨 THREAT INTEL", "📊 SCATTER OPS"])

# ─── LEADERBOARD ──────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Player Integrity Leaderboard</div>', unsafe_allow_html=True)

    display_cols = [
        "player_id", "integrity_score", "anomaly_score", "confidence",
        "avg_accuracy", "avg_kills", "avg_deaths", "avg_kd",
        "session_count", "suspicious_flag",
    ]
    st.dataframe(
        lb[display_cols].style
            .format({
                "integrity_score": "{:.4f}",
                "anomaly_score": "{:.4f}",
                "confidence": "{:.4f}",
                "avg_accuracy": "{:.2f}",
                "avg_kills": "{:.1f}",
                "avg_deaths": "{:.1f}",
                "avg_kd": "{:.2f}",
            })
            .background_gradient(subset=["integrity_score"], cmap="RdYlGn")
            .background_gradient(subset=["anomaly_score"], cmap="RdYlGn_r"),
        use_container_width=True,
        height=540,
    )

    # Tooltips
    with st.expander("ℹ️  Score Definitions"):
        st.markdown("""
        - **Anomaly Score** — How far a player deviates from normal behaviour (0 = normal, 1 = extreme outlier).
          Computed using Isolation Forest model across multiple engineered features.
        - **Integrity Score** — `1 - anomaly_score`. Higher is cleaner.
        - **Confidence** — How sure the model is about its classification, normalized 0–1.
        """)

# ─── THREAT INTEL ─────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Threat Intelligence — Flagged Players</div>', unsafe_allow_html=True)

    if len(suspicious) == 0:
        st.info("✅ No threats detected in current session data.")
    else:
        # Risk filter
        risk_filter = st.selectbox(
            "Filter by Risk Level",
            ["All Threats", "🔴 High Risk Only", "🟠 Medium Risk Only", "🟢 Low Risk Only"],
            key="risk_filter",
        )

        filtered = suspicious.copy()
        if "High" in risk_filter:
            filtered = filtered[filtered["confidence"] > 0.8]
        elif "Medium" in risk_filter:
            filtered = filtered[(filtered["confidence"] > 0.5) & (filtered["confidence"] <= 0.8)]
        elif "Low" in risk_filter:
            filtered = filtered[filtered["confidence"] <= 0.5]

        st.caption(f"Showing **{len(filtered)}** of **{len(suspicious)}** flagged players")

        for _, row in filtered.iterrows():
            badge = risk_badge(row["confidence"])
            ring = confidence_ring(row["confidence"])
            ibar = integrity_bar(row["integrity_score"])
            is_susp_cls = "suspicious" if row["confidence"] > 0.5 else ""

            st.markdown(f"""
            <div class="player-card {is_susp_cls}">
                <div style="flex-shrink:0;">{ring}</div>
                <div class="player-info">
                    <div style="display:flex;align-items:center;gap:.8rem;">
                        <span class="player-id">{row["player_id"]}</span>
                        {badge}
                    </div>
                    <div class="player-stats">
                        <span>K/D <b>{row["avg_kd"]:.2f}</b></span>
                        <span>Acc <b>{row["avg_accuracy"]:.1f}%</b></span>
                        <span>Kills <b>{row["avg_kills"]:.1f}</b></span>
                        <span>Deaths <b>{row["avg_deaths"]:.1f}</b></span>
                        <span>Sessions <b>{int(row["session_count"])}</b></span>
                    </div>
                    <div style="margin-top:.5rem;max-width:260px;">
                        <div style="display:flex;justify-content:space-between;font-size:.7rem;color:var(--text-secondary);margin-bottom:2px;">
                            <span>Integrity</span>
                            <span style="color:var(--text-primary);font-weight:600;">{row["integrity_score"]:.2%}</span>
                        </div>
                        {ibar}
                    </div>
                </div>
                <div style="text-align:right;flex-shrink:0;">
                    <div style="font-family:'JetBrains Mono';font-size:.7rem;color:var(--text-secondary);">ANOMALY</div>
                    <div style="font-family:'Orbitron';font-size:1.3rem;font-weight:800;color:var(--red);">{row["anomaly_score"]:.4f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─── SCATTER OPS ──────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Scatter Analysis — Accuracy vs K/D Ratio</div>', unsafe_allow_html=True)

    # Controls
    sc1, sc2 = st.columns([1, 1])
    with sc1:
        scatter_filter = st.selectbox(
            "Player Filter",
            ["Show All", "Clean Only", "Suspicious Only"],
            key="scatter_filter",
        )
    with sc2:
        show_heatmap = st.toggle("Show Density Heatmap Overlay", value=False, key="heatmap_toggle")

    # Filter data
    if scatter_filter == "Clean Only":
        plot_df = clean
    elif scatter_filter == "Suspicious Only":
        plot_df = suspicious
    else:
        plot_df = lb

    # Build figure
    if show_heatmap:
        fig = go.Figure()
        fig.add_trace(go.Histogram2dContour(
            x=lb["avg_kd"], y=lb["avg_accuracy"],
            colorscale=[[0, "rgba(0,0,0,0)"], [0.3, "rgba(0,245,255,.1)"],
                        [0.6, "rgba(139,92,246,.2)"], [1, "rgba(236,72,153,.3)"]],
            showscale=False, ncontours=20,
            line=dict(width=0),
        ))
        for flag_val, color, name in [(False, "#6366f1", "Clean"), (True, "#ff3b3b", "Suspicious")]:
            subset = plot_df[plot_df["suspicious_flag"] == flag_val]
            if len(subset) > 0:
                fig.add_trace(go.Scatter(
                    x=subset["avg_kd"], y=subset["avg_accuracy"],
                    mode="markers", name=name,
                    marker=dict(
                        size=subset["anomaly_score"] * 18 + 5,
                        color=color, opacity=0.85,
                        line=dict(width=1, color="rgba(255,255,255,.2)"),
                    ),
                    text=subset["player_id"],
                    customdata=np.stack([
                        subset["integrity_score"], subset["confidence"],
                        subset["session_count"], subset["anomaly_score"]
                    ], axis=-1),
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "K/D: %{x:.2f}<br>"
                        "Accuracy: %{y:.1f}%<br>"
                        "Integrity: %{customdata[0]:.4f}<br>"
                        "Confidence: %{customdata[1]:.4f}<br>"
                        "Sessions: %{customdata[2]:.0f}<br>"
                        "<extra></extra>"
                    ),
                ))
    else:
        fig = px.scatter(
            plot_df, x="avg_kd", y="avg_accuracy",
            color="suspicious_flag",
            color_discrete_map={True: "#ff3b3b", False: "#6366f1"},
            size="anomaly_score", size_max=18,
            hover_data={
                "player_id": True, "integrity_score": ":.4f",
                "confidence": ":.4f", "session_count": True,
                "suspicious_flag": True, "anomaly_score": ":.4f",
            },
            labels={
                "avg_kd": "Average K/D Ratio",
                "avg_accuracy": "Average Aim Accuracy (%)",
                "suspicious_flag": "Suspicious",
            },
        )

    # Quadrant overlays
    kd_mid = lb["avg_kd"].median()
    acc_mid = lb["avg_accuracy"].median()

    fig.add_shape(type="rect", x0=0, x1=kd_mid, y0=0, y1=acc_mid,
                  fillcolor="rgba(16,185,129,.04)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=kd_mid, x1=lb["avg_kd"].max()*1.1, y0=acc_mid,
                  y1=lb["avg_accuracy"].max()*1.05,
                  fillcolor="rgba(255,59,59,.06)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=kd_mid, x1=lb["avg_kd"].max()*1.1, y0=0, y1=acc_mid,
                  fillcolor="rgba(139,92,246,.04)", line_width=0, layer="below")

    # Quadrant labels
    fig.add_annotation(x=kd_mid*0.3, y=acc_mid*0.5, text="Normal Zone",
                       showarrow=False, font=dict(size=11, color="rgba(16,185,129,.5)"),
                       bgcolor="rgba(0,0,0,.3)")
    fig.add_annotation(x=lb["avg_kd"].max()*0.85, y=lb["avg_accuracy"].max()*0.95,
                       text="⚠ Suspicious Zone",
                       showarrow=False, font=dict(size=11, color="rgba(255,59,59,.6)"),
                       bgcolor="rgba(0,0,0,.4)")
    fig.add_annotation(x=lb["avg_kd"].max()*0.85, y=acc_mid*0.5, text="High Skill",
                       showarrow=False, font=dict(size=11, color="rgba(139,92,246,.5)"),
                       bgcolor="rgba(0,0,0,.3)")

    # Divider lines
    fig.add_hline(y=acc_mid, line_dash="dot", line_color="rgba(0,245,255,.15)", line_width=1)
    fig.add_vline(x=kd_mid, line_dash="dot", line_color="rgba(0,245,255,.15)", line_width=1)

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#cbd5e1"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.06,
            xanchor="center", x=0.5, font=dict(size=12),
        ),
        xaxis=dict(gridcolor="rgba(0,245,255,.06)", zeroline=False, title="Average K/D Ratio"),
        yaxis=dict(gridcolor="rgba(0,245,255,.06)", zeroline=False, title="Average Aim Accuracy (%)"),
        margin=dict(l=50, r=20, t=50, b=50),
        height=580,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Stats comparison
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("**🛡️ Clean Players**")
        st.metric("Avg Accuracy", f"{clean['avg_accuracy'].mean():.1f}%")
        st.metric("Avg K/D", f"{clean['avg_kd'].mean():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if len(suspicious) > 0:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("**🚨 Suspicious Players**")
            st.metric("Avg Accuracy", f"{suspicious['avg_accuracy'].mean():.1f}%")
            st.metric("Avg K/D", f"{suspicious['avg_kd'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# HOW DETECTION WORKS
# ═══════════════════════════════════════════════════════════════════
with st.expander("🔬 How Detection Works"):
    st.markdown("""
    <div class="how-it-works">
        <h4>Isolation Forest Anti-Cheat Pipeline</h4>
        <p>The system analyses each player session across multiple behavioural dimensions:</p>
        <ol>
            <li><b>Data Ingestion</b> — 1,000 player sessions with kills, deaths, aim accuracy, and timestamps.</li>
            <li><b>Feature Engineering</b> — Computes K/D ratio, accuracy deviation, session consistency,
                and a composite performance score for each unique player.</li>
            <li><b>Anomaly Detection</b> — An Isolation Forest model (200 estimators, 10% contamination)
                isolates players whose feature profiles diverge significantly from the population.</li>
            <li><b>Scoring</b> — Each player receives an <b>anomaly score</b> (0–1, higher = more suspicious)
                and a <b>confidence score</b> reflecting model certainty.</li>
            <li><b>Integrity Rating</b> — <code>integrity_score = 1 - anomaly_score</code>. Used for leaderboard ranking.</li>
        </ol>
        <p style="margin-top:.8rem;color:var(--cyan);font-weight:600;">
            Cheater patterns detected: abnormally high accuracy (85–99%), extreme K/D ratios,
            near-zero deaths, and suspiciously low variance across sessions.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    ANTI-CHEAT COMMAND CENTER · ISOLATION FOREST ENGINE · BUILT WITH STREAMLIT & PLOTLY<br>
    Session #{session} · {players} players scanned · {threats} threats identified
</div>
""".format(
    session=st.session_state.sim_count + 1,
    players=total_players,
    threats=flagged,
), unsafe_allow_html=True)
