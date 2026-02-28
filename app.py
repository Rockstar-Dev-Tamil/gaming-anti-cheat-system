"""
Esports Integrity Command Center — Streamlit Dashboard
========================================================
Launch:  streamlit run app.py
Checkpoint: app_checkpoint.py (previous Cyber Command Center UI)
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
    page_title="🎮 Esports Integrity Command Center",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
# MASSIVE CSS INJECTION — Playful, colourful, tactile
# ═══════════════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── ROOT ───────────────────────────────────────────────── */
:root{
  --deep:#0b0f19; --panel:rgba(15,23,42,.6);
  --glass-border:rgba(0,245,255,.12);
  --cyan:#00f5ff; --purple:#8b5cf6; --pink:#ff2e88;
  --red:#ff3b3b; --orange:#f97316; --green:#10b981;
  --txt:#e2e8f0; --txt2:#94a3b8;
  --r:18px;
}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}

/* ── ANIMATED GRADIENT BG ───────────────────────────────── */
.stApp{
  background:var(--deep);
  background-image:
    radial-gradient(ellipse 90% 70% at 15% 5%,rgba(139,92,246,.09) 0%,transparent 55%),
    radial-gradient(ellipse 70% 60% at 85% 85%,rgba(0,245,255,.07) 0%,transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 50%,rgba(255,46,136,.04) 0%,transparent 55%);
  animation:bgShift 25s ease-in-out infinite alternate;
}
@keyframes bgShift{
  0%{background-position:0% 0%,100% 100%,50% 50%;}
  100%{background-position:30% 20%,70% 80%,40% 60%;}
}

/* ── CINEMATIC INTRO ────────────────────────────────────── */
@keyframes introZoom{0%{opacity:0;transform:scale(1.15) translateY(10px);filter:blur(18px);}100%{opacity:1;transform:scale(1) translateY(0);filter:blur(0);}}
@keyframes scanPulse{0%{top:-8%;}100%{top:108%;}}
@keyframes typeReveal{0%{width:0;opacity:0;}10%{opacity:1;}100%{width:100%;opacity:1;}}
@keyframes introOut{0%{opacity:1;}100%{opacity:0;visibility:hidden;pointer-events:none;}}

.cin-overlay{
  position:fixed;inset:0;z-index:9999;background:var(--deep);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  animation:introZoom .9s ease-out forwards,introOut .6s 2.6s forwards;
  overflow:hidden;pointer-events:none;
}
.cin-overlay::after{
  content:'';position:absolute;left:0;width:100%;height:2px;
  background:linear-gradient(90deg,transparent,var(--cyan),var(--pink),transparent);
  animation:scanPulse 1.8s linear infinite;opacity:.35;
}
.cin-title{
  font-family:'Orbitron',monospace;font-size:3rem;font-weight:900;
  background:linear-gradient(135deg,var(--cyan),var(--purple),var(--pink));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-transform:uppercase;letter-spacing:.1em;
}
.cin-sub{
  font-family:'JetBrains Mono',monospace;font-size:.85rem;color:var(--cyan);
  letter-spacing:.3em;text-transform:uppercase;margin-top:.6rem;
  overflow:hidden;white-space:nowrap;
  animation:typeReveal 2s .8s steps(40) both;
}

/* ── HERO ───────────────────────────────────────────────── */
@keyframes heroIn{0%{opacity:0;transform:translateY(25px);}100%{opacity:1;transform:translateY(0);}}
.hero{text-align:center;padding:1.6rem 0 .3rem;animation:heroIn .8s .15s both;}
.hero h1{
  font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:800;
  background:linear-gradient(135deg,var(--cyan) 0%,var(--purple) 45%,var(--pink) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:.25rem;
}
.hero p{color:var(--txt2);font-size:.92rem;font-family:'JetBrains Mono',monospace;letter-spacing:.03em;}

/* ── METRIC CARDS ───────────────────────────────────────── */
@keyframes cardPop{0%{opacity:0;transform:scale(.85) translateY(20px);}100%{opacity:1;transform:scale(1) translateY(0);}}
@keyframes floatY{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}

.mgrid{display:flex;justify-content:center;gap:1.3rem;flex-wrap:wrap;margin:1.2rem auto 1.8rem;max-width:1100px;}
.mcard{
  background:var(--panel);border:1px solid var(--glass-border);border-radius:var(--r);
  padding:1.3rem 1.8rem;min-width:200px;text-align:center;position:relative;
  backdrop-filter:blur(16px);overflow:hidden;cursor:default;
  animation:cardPop .6s both,floatY 7s ease-in-out infinite;
  transition:transform .22s cubic-bezier(.34,1.56,.64,1),box-shadow .3s,border-color .3s;
}
.mcard:nth-child(1){animation-delay:.1s,.1s;}
.mcard:nth-child(2){animation-delay:.2s,.9s;}
.mcard:nth-child(3){animation-delay:.3s,1.7s;}
.mcard:nth-child(4){animation-delay:.4s,2.5s;}

.mcard::before{
  content:'';position:absolute;inset:-1px;border-radius:var(--r);
  background:linear-gradient(135deg,var(--cyan),var(--purple),var(--pink));
  opacity:0;transition:opacity .35s;z-index:-1;
}
.mcard:hover{transform:translateY(-10px) scale(1.04);box-shadow:0 12px 40px rgba(0,245,255,.15);}
.mcard:hover::before{opacity:.15;}
.mcard:active{transform:translateY(-5px) scale(.97);}

.micon{font-size:1.5rem;margin-bottom:.2rem;}
.mval{font-family:'Orbitron',monospace;font-size:2rem;font-weight:800;}
.mlbl{color:var(--txt2);font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-top:.2rem;}

.v-cyan{color:var(--cyan);text-shadow:0 0 25px rgba(0,245,255,.45);}
.v-red{color:var(--red);text-shadow:0 0 25px rgba(255,59,59,.45);}
.v-green{color:var(--green);text-shadow:0 0 25px rgba(16,185,129,.45);}
.v-purple{color:var(--purple);text-shadow:0 0 25px rgba(139,92,246,.45);}

/* ── GLASS PANELS ───────────────────────────────────────── */
.gpanel{background:var(--panel);border:1px solid var(--glass-border);border-radius:var(--r);padding:1.4rem;backdrop-filter:blur(14px);margin:.6rem 0;}

/* ── TABS ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{gap:.4rem;justify-content:center;border-bottom:1px solid rgba(0,245,255,.1);padding-bottom:3px;}
.stTabs [data-baseweb="tab"]{
  background:transparent;border:1px solid transparent;border-radius:14px 14px 0 0;
  color:var(--txt2);font-family:'Orbitron',monospace;font-weight:600;font-size:.82rem;
  padding:.6rem 1.6rem;transition:all .3s;position:relative;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--cyan);background:rgba(0,245,255,.05);}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(0,245,255,.12),rgba(139,92,246,.1)) !important;
  color:var(--cyan) !important;border-color:rgba(0,245,255,.3) !important;
  border-bottom-color:transparent !important;
  box-shadow:0 -3px 18px rgba(0,245,255,.12);
}
.stTabs [data-baseweb="tab-panel"]{animation:tabReveal .35s ease-out;}
@keyframes tabReveal{0%{opacity:0;transform:translateY(12px);}100%{opacity:1;transform:translateY(0);}}

/* ── RISK BADGES ────────────────────────────────────────── */
@keyframes pulseGlow{0%,100%{box-shadow:0 0 4px currentColor;}50%{box-shadow:0 0 18px currentColor;}}
.badge{
  display:inline-flex;align-items:center;gap:.35rem;
  padding:.25rem .75rem;border-radius:20px;
  font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:700;
  text-transform:uppercase;letter-spacing:.05em;
}
.badge-critical{background:rgba(255,59,59,.14);border:1px solid rgba(255,59,59,.4);color:var(--red);animation:pulseGlow 2s ease-in-out infinite;}
.badge-risky{background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.35);color:var(--orange);}
.badge-stable{background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.3);color:var(--purple);}
.badge-elite{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);color:var(--green);}

/* ── INTEGRITY BAR ──────────────────────────────────────── */
@keyframes barGrow{0%{width:0;}}
.ibar-bg{width:100%;height:7px;border-radius:4px;background:rgba(255,255,255,.06);overflow:hidden;}
.ibar-fill{height:100%;border-radius:4px;animation:barGrow 1s cubic-bezier(.25,.46,.45,.94) forwards;box-shadow:0 0 10px currentColor;}

/* ── CONFIDENCE RING SVG ────────────────────────────────── */
.cring{display:inline-flex;align-items:center;justify-content:center;position:relative;width:52px;height:52px;}
.cring svg{transform:rotate(-90deg);}
.cring-lbl{position:absolute;font-family:'Orbitron',monospace;font-size:.62rem;font-weight:700;color:var(--txt);}

/* ── PLAYER CARDS ───────────────────────────────────────── */
@keyframes shimmerBorder{0%,100%{border-color:rgba(255,59,59,.2);}50%{border-color:rgba(255,46,136,.5);}}
.pcard{
  background:var(--panel);border:1px solid var(--glass-border);border-radius:var(--r);
  padding:1.1rem 1.4rem;margin-bottom:.7rem;backdrop-filter:blur(12px);
  display:flex;align-items:center;gap:1.1rem;
  transition:all .25s cubic-bezier(.34,1.56,.64,1);
}
.pcard:hover{transform:translateY(-4px) scale(1.01);box-shadow:0 8px 30px rgba(139,92,246,.12);}
.pcard:active{transform:scale(.98);}
.pcard.threat{border-color:rgba(255,59,59,.25);animation:shimmerBorder 3s ease-in-out infinite;}
.pcard.threat:hover{box-shadow:0 8px 30px rgba(255,59,59,.15);}

.pid{font-family:'Orbitron',monospace;font-size:.95rem;font-weight:700;color:var(--txt);}
.pstats{display:flex;gap:1rem;margin-top:.35rem;font-size:.78rem;color:var(--txt2);font-family:'JetBrains Mono',monospace;}
.pstats b{color:var(--cyan);}

/* ── SECTION HEADERS ────────────────────────────────────── */
.shdr{
  font-family:'Orbitron',monospace;font-size:1rem;font-weight:700;
  color:var(--cyan);margin:.8rem 0;padding-bottom:.35rem;
  border-bottom:1px solid rgba(0,245,255,.12);letter-spacing:.04em;
}

/* ── BUTTONS ────────────────────────────────────────────── */
.stButton > button{
  font-family:'Orbitron',monospace !important;font-weight:600 !important;font-size:.85rem !important;
  border:1px solid var(--cyan) !important;color:var(--cyan) !important;
  background:rgba(0,245,255,.05) !important;border-radius:14px !important;
  padding:.55rem 1.6rem !important;transition:all .25s !important;letter-spacing:.04em !important;
  position:relative !important;overflow:hidden !important;
}
.stButton > button:hover{
  background:rgba(0,245,255,.12) !important;box-shadow:0 0 25px rgba(0,245,255,.2) !important;
  transform:translateY(-2px) !important;
}
.stButton > button:active{transform:scale(.96) !important;box-shadow:none !important;}

/* ── SELECTBOX ──────────────────────────────────────────── */
.stSelectbox > div > div{
  background:var(--panel) !important;border:1px solid var(--glass-border) !important;
  border-radius:12px !important;color:var(--txt) !important;
  font-family:'JetBrains Mono',monospace !important;
}

/* ── TOGGLE ─────────────────────────────────────────────── */
.stToggle label span{font-family:'JetBrains Mono',monospace;font-size:.82rem;}

/* ── EXPANDER ───────────────────────────────────────────── */
.streamlit-expanderHeader{
  font-family:'Orbitron',monospace !important;color:var(--cyan) !important;
  font-size:.88rem !important;background:var(--panel) !important;
  border:1px solid var(--glass-border) !important;border-radius:var(--r) !important;
}

/* ── DATAFRAME ──────────────────────────────────────────── */
.stDataFrame{border-radius:14px;overflow:hidden;}

/* ── HOW-IT-WORKS ───────────────────────────────────────── */
.hiw{background:var(--panel);border:1px solid var(--glass-border);border-radius:var(--r);padding:1.4rem;backdrop-filter:blur(12px);margin-top:1rem;}
.hiw h4{font-family:'Orbitron',monospace;color:var(--cyan);font-size:.9rem;margin-bottom:.6rem;}
.hiw p,.hiw li{color:var(--txt2);font-size:.83rem;line-height:1.65;}
.hiw b{color:var(--cyan);}

/* ── FOOTER ─────────────────────────────────────────────── */
.foot{text-align:center;padding:2rem 0 1rem;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#334155;letter-spacing:.05em;}
</style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# CINEMATIC INTRO
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="cin-overlay">
    <div class="cin-title">Integrity Command</div>
    <div class="cin-sub">▸ scanning player sessions ▸ detecting anomalies ▸ building threat map</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# DATA PIPELINE
# ═══════════════════════════════════════════════════════════════════
def run_pipeline(seed_offset=0):
    raw = generate_dataset(n=1000, cheater_ratio=0.08, seed=42 + seed_offset)
    feat = engineer_features(raw)
    scored = detect_anomalies(feat)
    return build_leaderboard(scored)

if "sim" not in st.session_state:
    st.session_state.sim = 0

lb = run_pipeline(st.session_state.sim)
suspicious = lb[lb["suspicious_flag"] == True].copy()
clean_df = lb[lb["suspicious_flag"] == False].copy()


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════
def integrity_level(score):
    if score >= 0.85:
        return '<span class="badge badge-elite">🏆 Elite</span>'
    elif score >= 0.6:
        return '<span class="badge badge-stable">🛡️ Stable</span>'
    elif score >= 0.35:
        return '<span class="badge badge-risky">⚡ Risky</span>'
    else:
        return '<span class="badge badge-critical">💀 Critical</span>'

def conf_ring(val, sz=52, sw=5):
    r = (sz - sw) / 2
    c = 2 * 3.14159 * r
    off = c * (1 - val)
    col = "var(--red)" if val > .8 else "var(--orange)" if val > .5 else "var(--green)"
    return f'''<div class="cring"><svg width="{sz}" height="{sz}">
      <circle cx="{sz/2}" cy="{sz/2}" r="{r}" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="{sw}"/>
      <circle cx="{sz/2}" cy="{sz/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}"
        stroke-dasharray="{c}" stroke-dashoffset="{off}" stroke-linecap="round"/>
    </svg><span class="cring-lbl">{val:.0%}</span></div>'''

def ibar(score):
    pct = max(0, min(100, score * 100))
    col = "var(--green)" if score > .7 else "var(--orange)" if score > .4 else "var(--red)"
    return f'<div class="ibar-bg"><div class="ibar-fill" style="width:{pct}%;background:{col};color:{col};"></div></div>'


# ═══════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>🎮 Esports Integrity Command Center</h1>
    <p>AI-driven Isolation Forest scanning 1,000 sessions · detecting bot behaviour · scoring player integrity</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# FILTER ROW + SIMULATE BUTTON
# ═══════════════════════════════════════════════════════════════════
f1, f2, f3 = st.columns([2, 2, 1.5])
with f1:
    view_filter = st.selectbox("Player View", ["All Players", "Clean Only", "Suspicious Only", "High Risk Only"], key="vf")
with f2:
    st.write("")  # spacer
with f3:
    if st.button("🎮  Simulate New Match", use_container_width=True):
        st.session_state.sim += 1
        st.rerun()

# Apply filter
if view_filter == "Clean Only":
    view_df = clean_df
elif view_filter == "Suspicious Only":
    view_df = suspicious
elif view_filter == "High Risk Only":
    view_df = suspicious[suspicious["confidence"] > 0.8] if len(suspicious) > 0 else suspicious
else:
    view_df = lb


# ═══════════════════════════════════════════════════════════════════
# METRIC CARDS
# ═══════════════════════════════════════════════════════════════════
total = len(lb)
threats = len(suspicious)
cleanpct = len(clean_df) / total * 100
avgint = lb["integrity_score"].mean()

st.markdown(f"""
<div class="mgrid">
  <div class="mcard"><div class="micon">👥</div><div class="mval v-cyan">{total}</div><div class="mlbl">Players Scanned</div></div>
  <div class="mcard"><div class="micon">🚨</div><div class="mval v-red">{threats}</div><div class="mlbl">Threats Found</div></div>
  <div class="mcard"><div class="micon">🛡️</div><div class="mval v-green">{cleanpct:.1f}%</div><div class="mlbl">Clean Rate</div></div>
  <div class="mcard"><div class="micon">⚡</div><div class="mval v-purple">{avgint:.2f}</div><div class="mlbl">Avg Integrity</div></div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🏆 LEADERBOARD", "🚨 THREAT INTEL", "📊 SCATTER OPS"])


# ─── TAB 1: LEADERBOARD ──────────────────────────────────────────
with tab1:
    st.markdown('<div class="shdr">Player Integrity Leaderboard</div>', unsafe_allow_html=True)
    cols = ["player_id", "integrity_score", "anomaly_score", "confidence",
            "avg_accuracy", "avg_kills", "avg_deaths", "avg_kd",
            "session_count", "suspicious_flag"]
    st.dataframe(
        view_df[cols].style.format({
            "integrity_score": "{:.4f}", "anomaly_score": "{:.4f}",
            "confidence": "{:.4f}", "avg_accuracy": "{:.2f}",
            "avg_kills": "{:.1f}", "avg_deaths": "{:.1f}", "avg_kd": "{:.2f}",
        }).background_gradient(subset=["integrity_score"], cmap="RdYlGn")
         .background_gradient(subset=["anomaly_score"], cmap="RdYlGn_r"),
        use_container_width=True, height=540,
    )
    with st.expander("ℹ️  Score Definitions"):
        st.markdown("""
        - **Anomaly Score** — Isolation Forest deviation measure (0 = normal, 1 = extreme outlier)
        - **Integrity Score** — `1 - anomaly_score` (higher = cleaner)
        - **Confidence** — Model certainty about classification (0–1)
        """)


# ─── TAB 2: THREAT INTEL ─────────────────────────────────────────
with tab2:
    st.markdown('<div class="shdr">Threat Intelligence — Flagged Players</div>', unsafe_allow_html=True)

    if len(suspicious) == 0:
        st.success("✅ No threats detected in this session.")
    else:
        risk_pick = st.selectbox("Risk Level Filter",
            ["All Threats", "💀 Critical Only", "⚡ Risky Only", "🛡️ Stable Only"], key="rf")

        filt = suspicious.copy()
        if "Critical" in risk_pick:
            filt = filt[filt["integrity_score"] < 0.35]
        elif "Risky" in risk_pick:
            filt = filt[(filt["integrity_score"] >= 0.35) & (filt["integrity_score"] < 0.6)]
        elif "Stable" in risk_pick:
            filt = filt[filt["integrity_score"] >= 0.6]

        st.caption(f"Showing **{len(filt)}** of **{len(suspicious)}** flagged players")

        for _, r in filt.iterrows():
            lvl = integrity_level(r["integrity_score"])
            ring = conf_ring(r["confidence"])
            bar = ibar(r["integrity_score"])
            cls = "threat" if r["confidence"] > 0.5 else ""

            st.markdown(f"""
            <div class="pcard {cls}">
              <div style="flex-shrink:0;">{ring}</div>
              <div style="flex:1;">
                <div style="display:flex;align-items:center;gap:.7rem;">
                  <span class="pid">{r["player_id"]}</span>{lvl}
                </div>
                <div class="pstats">
                  <span>K/D <b>{r["avg_kd"]:.2f}</b></span>
                  <span>Acc <b>{r["avg_accuracy"]:.1f}%</b></span>
                  <span>Kills <b>{r["avg_kills"]:.1f}</b></span>
                  <span>Deaths <b>{r["avg_deaths"]:.1f}</b></span>
                  <span>Sessions <b>{int(r["session_count"])}</b></span>
                </div>
                <div style="margin-top:.45rem;max-width:240px;">
                  <div style="display:flex;justify-content:space-between;font-size:.68rem;color:var(--txt2);margin-bottom:2px;">
                    <span>Integrity</span>
                    <span style="color:var(--txt);font-weight:600;">{r["integrity_score"]:.2%}</span>
                  </div>
                  {bar}
                </div>
              </div>
              <div style="text-align:right;flex-shrink:0;">
                <div style="font-family:'JetBrains Mono';font-size:.68rem;color:var(--txt2);">ANOMALY</div>
                <div style="font-family:'Orbitron';font-size:1.2rem;font-weight:800;color:var(--red);">{r["anomaly_score"]:.4f}</div>
              </div>
            </div>""", unsafe_allow_html=True)


# ─── TAB 3: SCATTER OPS ──────────────────────────────────────────
with tab3:
    st.markdown('<div class="shdr">Scatter Analysis — Accuracy vs K/D Ratio</div>', unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns([1.2, 1, 1])
    with sc1:
        scat_filt = st.selectbox("Filter", ["Show All", "Clean Only", "Suspicious Only"], key="sf")
    with sc2:
        show_heat = st.toggle("Density Heatmap", value=False, key="ht")
    with sc3:
        show_top5 = st.toggle("Highlight Top 5 Risks", value=False, key="t5")

    # Determine data
    pdata = clean_df if scat_filt == "Clean Only" else suspicious if scat_filt == "Suspicious Only" else lb

    # Build figure
    if show_heat:
        fig = go.Figure()
        fig.add_trace(go.Histogram2dContour(
            x=lb["avg_kd"], y=lb["avg_accuracy"],
            colorscale=[[0, "rgba(0,0,0,0)"], [.3, "rgba(0,245,255,.08)"],
                        [.6, "rgba(139,92,246,.16)"], [1, "rgba(255,46,136,.22)"]],
            showscale=False, ncontours=20, line=dict(width=0),
        ))
        for flag, col, nm in [(False, "#6366f1", "Clean"), (True, "#ff3b3b", "Suspicious")]:
            sub = pdata[pdata["suspicious_flag"] == flag]
            if len(sub):
                fig.add_trace(go.Scatter(
                    x=sub["avg_kd"], y=sub["avg_accuracy"], mode="markers", name=nm,
                    marker=dict(size=sub["anomaly_score"] * 20 + 5, color=col, opacity=.85,
                                line=dict(width=1, color="rgba(255,255,255,.15)")),
                    text=sub["player_id"],
                    customdata=np.stack([sub["integrity_score"], sub["confidence"],
                                        sub["session_count"], sub["anomaly_score"]], axis=-1),
                    hovertemplate="<b>%{text}</b><br>K/D: %{x:.2f}<br>Acc: %{y:.1f}%<br>"
                                 "Integrity: %{customdata[0]:.4f}<br>Confidence: %{customdata[1]:.4f}<extra></extra>",
                ))
    else:
        fig = px.scatter(
            pdata, x="avg_kd", y="avg_accuracy",
            color="suspicious_flag",
            color_discrete_map={True: "#ff3b3b", False: "#6366f1"},
            size="anomaly_score", size_max=20,
            hover_data={"player_id": True, "integrity_score": ":.4f",
                        "confidence": ":.4f", "session_count": True,
                        "suspicious_flag": True, "anomaly_score": ":.4f"},
            labels={"avg_kd": "Avg K/D Ratio", "avg_accuracy": "Avg Aim Accuracy (%)", "suspicious_flag": "Suspicious"},
        )

    # Top 5 risks highlight
    if show_top5 and len(suspicious) > 0:
        top5 = suspicious.nlargest(5, "anomaly_score")
        fig.add_trace(go.Scatter(
            x=top5["avg_kd"], y=top5["avg_accuracy"], mode="markers+text",
            name="Top 5 Risks",
            marker=dict(size=22, color="rgba(255,46,136,.3)", line=dict(width=2.5, color="#ff2e88")),
            text=top5["player_id"], textposition="top center",
            textfont=dict(size=10, color="#ff2e88", family="Orbitron"),
            hoverinfo="skip",
        ))

    # Quadrant overlays
    kd_mid = lb["avg_kd"].median()
    acc_mid = lb["avg_accuracy"].median()
    kd_max = lb["avg_kd"].max() * 1.1
    acc_max = lb["avg_accuracy"].max() * 1.05

    fig.add_shape(type="rect", x0=0, x1=kd_mid, y0=0, y1=acc_mid,
                  fillcolor="rgba(16,185,129,.04)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=kd_mid, x1=kd_max, y0=acc_mid, y1=acc_max,
                  fillcolor="rgba(255,59,59,.05)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=kd_mid, x1=kd_max, y0=0, y1=acc_mid,
                  fillcolor="rgba(139,92,246,.04)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=0, x1=kd_mid, y0=acc_mid, y1=acc_max,
                  fillcolor="rgba(255,46,136,.03)", line_width=0, layer="below")

    fig.add_annotation(x=kd_mid * .3, y=acc_mid * .5, text="Normal",
                       showarrow=False, font=dict(size=11, color="rgba(16,185,129,.45)"), bgcolor="rgba(0,0,0,.3)")
    fig.add_annotation(x=kd_max * .85, y=acc_max * .95, text="⚠ Suspicious Pattern",
                       showarrow=False, font=dict(size=11, color="rgba(255,59,59,.55)"), bgcolor="rgba(0,0,0,.35)")
    fig.add_annotation(x=kd_max * .85, y=acc_mid * .5, text="Skilled",
                       showarrow=False, font=dict(size=11, color="rgba(139,92,246,.45)"), bgcolor="rgba(0,0,0,.3)")
    fig.add_annotation(x=kd_mid * .3, y=acc_max * .95, text="Extreme Anomaly",
                       showarrow=False, font=dict(size=11, color="rgba(255,46,136,.45)"), bgcolor="rgba(0,0,0,.3)")

    fig.add_hline(y=acc_mid, line_dash="dot", line_color="rgba(0,245,255,.12)", line_width=1)
    fig.add_vline(x=kd_mid, line_dash="dot", line_color="rgba(0,245,255,.12)", line_width=1)

    fig.update_layout(
        template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#cbd5e1"),
        legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="center", x=.5, font=dict(size=12)),
        xaxis=dict(gridcolor="rgba(0,245,255,.05)", zeroline=False, title="Avg K/D Ratio"),
        yaxis=dict(gridcolor="rgba(0,245,255,.05)", zeroline=False, title="Avg Aim Accuracy (%)"),
        margin=dict(l=50, r=20, t=50, b=50), height=580,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparison stats
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="gpanel">', unsafe_allow_html=True)
        st.markdown("**🛡️ Clean Players**")
        st.metric("Avg Accuracy", f"{clean_df['avg_accuracy'].mean():.1f}%")
        st.metric("Avg K/D", f"{clean_df['avg_kd'].mean():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if len(suspicious) > 0:
            st.markdown('<div class="gpanel">', unsafe_allow_html=True)
            st.markdown("**🚨 Suspicious Players**")
            st.metric("Avg Accuracy", f"{suspicious['avg_accuracy'].mean():.1f}%")
            st.metric("Avg K/D", f"{suspicious['avg_kd'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# HOW AI DETECTS CHEATERS
# ═══════════════════════════════════════════════════════════════════
with st.expander("🔬 How AI Detects Cheaters"):
    st.markdown("""
    <div class="hiw">
        <h4>Isolation Forest Anti-Cheat Pipeline</h4>
        <ol>
            <li><b>Data Ingestion</b> — 1,000 session records: kills, deaths, aim accuracy, timestamps.</li>
            <li><b>Feature Engineering</b> — K/D ratio, accuracy deviation, session consistency, composite performance score.</li>
            <li><b>Anomaly Detection</b> — Isolation Forest (200 trees, 10% contamination) isolates behavioural outliers.</li>
            <li><b>Scoring</b> — Anomaly score (0–1, higher = suspicious), confidence (model certainty).</li>
            <li><b>Integrity Rating</b> — <code>integrity = 1 - anomaly_score</code>. Players ranked accordingly.</li>
        </ol>
        <p><b>Cheater signatures:</b> aim accuracy 85–99%, K/D > 10, near-zero deaths, very low variance across sessions.</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="foot">
  ESPORTS INTEGRITY COMMAND CENTER · SESSION #{st.session_state.sim + 1} ·
  {total} PLAYERS · {threats} THREATS · ISOLATION FOREST ENGINE
</div>
""", unsafe_allow_html=True)
