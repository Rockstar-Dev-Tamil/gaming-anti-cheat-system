# Gaming Bot Behaviour Analyzer — Walkthrough

## What Was Built

A complete esports anti-cheat analytics pipeline with an interactive Streamlit dashboard.

### Files Created

| File | Purpose |
|------|---------|
| [bot_analyzer.py](file:///c:/Hackathon/bot_analyzer.py) | Core analysis: data gen, feature engineering, Isolation Forest, leaderboard |
| [app.py](file:///c:/Hackathon/app.py) | Streamlit dashboard with dark theme, 3 tabs |
| [requirements.txt](file:///c:/Hackathon/requirements.txt) | Python dependencies |

---

## Pipeline Results

The pipeline processes **1000 session records** → aggregates to **440 unique players** → flags **44 suspicious** (10% contamination).

| Metric | Value |
|--------|-------|
| Total Players | 440 |
| Suspicious Flagged | 44 |
| Clean Rate | 90.0% |
| Avg Integrity Score | 0.81 |

---

## Dashboard

![Dashboard with metric cards the three tabs](C:/Users/Rockstar/.gemini/antigravity/brain/2f92280a-fc2c-430e-89d1-ce4871722add/dashboard_screenshot.png)

**Three tabs verified working:**
- **🏆 Leaderboard** — All players ranked by integrity score with color gradients
- **🚨 Suspicious Players** — Filtered table of flagged players with anomaly/confidence scores
- **📊 Scatter Analysis** — Plotly scatter of Aim Accuracy vs K/D Ratio, color-coded by flag

---

## How to Run

```powershell
# Start the dashboard
& "C:\Users\Rockstar\miniconda3\Scripts\streamlit.exe" run "c:\Hackathon\app.py"

# Or run pipeline standalone
& "C:\Users\Rockstar\miniconda3\python.exe" "c:\Hackathon\bot_analyzer.py"
```
