<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=greensock&logoColor=white" />
</p>

<h1 align="center">🎮 Esports Integrity Command Center</h1>

<p align="center">
  <b>AI-Powered Anti-Cheat System for Competitive Gaming</b><br>
  <sub>Real-time bot behaviour detection using Isolation Forest anomaly detection</sub>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-ml-pipeline">ML Pipeline</a> •
  <a href="#-dashboard">Dashboard</a> •
  <a href="#-website">Website</a> •
  <a href="#-tech-stack">Tech Stack</a>
</p>

---

## 📖 About The Project

The **Esports Integrity Command Center** is a full-stack AI-driven analytics platform designed to detect cheating and bot behaviour in competitive gaming environments. It combines a robust **machine learning pipeline** built on scikit-learn's Isolation Forest algorithm with two stunning front-end interfaces — an interactive **Streamlit dashboard** for analysts and a public-facing **static website** for showcasing threat intelligence.

The system processes thousands of player session records, extracts behavioural features such as kill/death ratios, aim accuracy patterns, and session consistency metrics, then uses unsupervised anomaly detection to flag players exhibiting inhuman performance patterns. Every player receives an **integrity score** and **confidence rating**, enabling tiered threat classification from 🏆 Elite to 💀 Critical.

---

## ✨ Features

### 🧠 Machine Learning Engine
- **Isolation Forest** anomaly detection with 200 estimators and 10% contamination rate
- Synthetic dataset generation with configurable player counts and cheater ratios
- Multi-dimensional feature engineering (K/D ratio, accuracy variance, composite performance scores)
- Normalised anomaly scoring with MinMaxScaler for interpretable 0–1 outputs
- Confidence-weighted classification for model certainty measurement

### 📊 Interactive Streamlit Dashboard
- **Cinematic intro animation** with zoom-blur and scan-pulse effects
- **Floating metric cards** — Players scanned, threats found, clean rate, average integrity
- **Leaderboard tab** — Colour-gradient sortable table with RdYlGn heatmapping
- **Threat Intel tab** — Individual player cards with SVG confidence rings, integrity bars, and risk badges
- **Scatter Ops tab** — Interactive Plotly scatter with density heatmaps, quadrant analysis, and top-5 risk highlighting
- **Simulate New Match** button — Re-runs the entire ML pipeline with different seeds for live demo
- **Filter system** — View All / Clean Only / Suspicious Only / High Risk Only

### 🌐 Static Website
- **GSAP + ScrollTrigger** powered scroll animations with parallax orbs
- **Lenis** smooth scrolling for buttery-smooth navigation
- **Canvas scatter plot** with hover tooltips and real-time data rendering
- **Animated stat bars** with counter animations driven by Intersection Observer
- **Leaderboard table** with expandable hover rows and status badges
- **Suspect cards** with filterable risk levels (High / Medium / Low)
- **Risk assessment** section with tiered threat classification cards
- **Responsive design** optimised for desktop and mobile viewports

### 🎨 Design System
- **Dark mode first** — Deep navy background (`#0b0f19`) with glassmorphism panels
- **Neon accent palette** — Cyan (`#00f5ff`), Purple (`#8b5cf6`), Pink (`#ff2e88`)
- **Custom typography** — Orbitron (headings), JetBrains Mono (data), Inter (body)
- **Micro-interactions** — Hover-lift cards, pulsing threat badges, animated progress bars
- **Backdrop blur** panels with CSS `backdrop-filter` for frosted glass effects

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                       DATA PIPELINE                                │
│                                                                    │
│   ┌──────────────────┐    ┌───────────────────┐    ┌────────────┐ │
│   │  generate_dataset │───►│ engineer_features │───►│  detect    │ │
│   │                  │    │                   │    │  anomalies │ │
│   │  • 1,000 sessions│    │  • kd_ratio       │    │            │ │
│   │  • kills/deaths  │    │  • avg_accuracy   │    │  • 200     │ │
│   │  • aim_accuracy  │    │  • accuracy_std   │    │    trees   │ │
│   │  • timestamps    │    │  • kill_std       │    │  • 10%     │ │
│   │  • is_cheater    │    │  • session_count  │    │    contam. │ │
│   │                  │    │  • performance    │    │  • MinMax  │ │
│   │                  │    │    _score         │    │    scaling │ │
│   └──────────────────┘    └───────────────────┘    └─────┬──────┘ │
│                                                          │        │
│                                                ┌─────────▼──────┐ │
│                                                │ build          │ │
│                                                │ _leaderboard   │ │
│                                                │                │ │
│                                                │ integrity =    │ │
│                                                │ 1 - anomaly    │ │
│                                                └────────┬───────┘ │
└─────────────────────────────────────────────────────────┼─────────┘
                                                          │
                          ┌───────────────────────────────┼──────────────────┐
                          │                               │                  │
                   ┌──────▼──────────┐         ┌─────────▼────────┐  ┌──────▼──────┐
                   │   Streamlit     │         │  Static Website  │  │    CLI      │
                   │   Dashboard     │         │                  │  │    Output   │
                   │                 │         │  • HTML/CSS/JS   │  │             │
                   │  • Plotly       │         │  • GSAP anims    │  │  • Top 10   │
                   │    charts       │         │  • Canvas plots  │  │    table    │
                   │  • Live metric  │         │  • Leaderboard   │  │  • Stats    │
                   │    cards        │         │  • Threat cards  │  │    summary  │
                   │  • Threat intel │         │  • Risk map      │  │             │
                   │  • Scatter ops  │         │                  │  │             │
                   └─────────────────┘         └──────────────────┘  └─────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.9+    |
| pip         | Latest  |

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd gaming-anti-cheat-system
   ```

2. **Create a virtual environment** *(recommended)*

   ```bash
   python -m venv .venv
   ```

   Activate it:

   ```bash
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # Windows (CMD)
   .venv\Scripts\activate.bat

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   | Package       | Purpose                              |
   |---------------|--------------------------------------|
   | `pandas`      | DataFrame operations & aggregation   |
   | `numpy`       | Numerical computations               |
   | `scikit-learn`| Isolation Forest & MinMaxScaler      |
   | `streamlit`   | Interactive web dashboard            |
   | `plotly`      | Interactive scatter & heatmap charts |
   | `matplotlib`  | Supplementary plotting utilities     |

---

## 🖥️ Usage

### 1. Streamlit Dashboard (Primary Interface)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` with the full command center:

| Tab | Description |
|-----|-------------|
| 🏆 **Leaderboard** | Sortable player table with colour-graded integrity & anomaly scores |
| 🚨 **Threat Intel** | Detailed threat cards with confidence rings, integrity bars, & risk badges |
| 📊 **Scatter Ops** | Interactive scatter plot with density heatmaps, quadrant overlays, & top-5 highlights |

**Controls:**
- **Player View** dropdown — Filter between All / Clean / Suspicious / High Risk players
- **Simulate New Match** — Re-seeds and re-runs the full ML pipeline
- **Density Heatmap** toggle — Overlays 2D contour density on the scatter plot
- **Top 5 Risks** toggle — Highlights the 5 most anomalous players with pink markers

### 2. Bot Analyzer CLI

Run the ML pipeline directly with terminal output:

```bash
python bot_analyzer.py
```

**Sample output:**
```
=== TOP 10 LEADERBOARD ===
   player_id  avg_accuracy  avg_kills  ...  anomaly_score  suspicious_flag  confidence  integrity_score
1      P0234         38.21       11.2  ...         0.0012            False      0.9821           0.9988
2      P0891         41.56       12.8  ...         0.0015            False      0.9798           0.9985
...

Total players  : 680
Suspicious     : 68
Avg integrity  : 0.8542
```

### 3. Static Website

**Step 1:** Generate the data file (exports 5,000 records):

```bash
python website/generate_data.py
```

**Step 2:** Serve locally:

```bash
cd website
python -m http.server 8000
```

**Step 3:** Visit `http://localhost:8000` in your browser.

**Website sections:**
| Section | Description |
|---------|-------------|
| **Hero** | Cinematic landing with parallax orbs and scan-line animation |
| **Metrics Banner** | Animated counter cards (players, threats, clean rate, integrity) |
| **Pattern Recognition** | Side-by-side stat bars comparing Normal vs Cheater behaviour |
| **Threat Visualization** | Canvas scatter plot with hover tooltips and quadrant labels |
| **Player Leaderboard** | Full ranked table with expandable hover rows |
| **Flagged Players** | Suspect cards filterable by risk level (High / Medium / Low) |
| **Risk Assessment** | Tiered threat classification breakdown |
| **CTA** | Call-to-action footer with gradient title |

---

## 📂 Project Structure

```
gaming-anti-cheat-system/
│
├── 📄 app.py                   # Streamlit dashboard — main application
│                                #   • CSS injection (240+ lines of custom styles)
│                                #   • Cinematic intro overlay animation
│                                #   • Data pipeline execution & session state
│                                #   • Metric cards, leaderboard, threat intel, scatter ops
│                                #   • Helper functions: integrity_level(), conf_ring(), ibar()
│
├── 📄 app_checkpoint.py        # Previous UI checkpoint (Cyber Command Center version)
│
├── 📄 bot_analyzer.py          # Core ML pipeline module
│                                #   • generate_dataset()    — Synthetic data generation
│                                #   • engineer_features()   — Per-player feature aggregation
│                                #   • detect_anomalies()    — Isolation Forest detection
│                                #   • build_leaderboard()   — Integrity scoring & ranking
│                                #   • run_pipeline()        — Convenience full pipeline
│
├── 📄 requirements.txt         # Python dependencies (6 packages)
├── 📄 README.md                # This documentation file
│
└── 📁 website/                 # Static website (HTML/CSS/JS)
    ├── 📄 index.html           # Landing page with 7 animated sections
    │                            #   • Nav, Hero, Metrics, Behaviour, Scatter,
    │                            #   • Leaderboard, Suspects, Risk, CTA, Footer
    ├── 📄 style.css            # Full design system (~30KB)
    │                            #   • CSS custom properties, glassmorphism
    │                            #   • Keyframe animations, responsive breakpoints
    ├── 📄 main.js              # Client-side logic (~25KB)
    │                            #   • GSAP + ScrollTrigger animations
    │                            #   • Canvas scatter plot renderer
    │                            #   • Counter animations, smooth scroll (Lenis)
    │                            #   • Data loading, table rendering, filtering
    ├── 📄 generate_data.py     # Script to export pipeline data to JSON
    └── 📄 data.json            # Pre-generated dataset (5,000 player records)
```

---

## 🧪 ML Pipeline Deep Dive

### Stage 1: Synthetic Data Generation

`generate_dataset(n=1000, cheater_ratio=0.08, seed=42)`

Generates realistic player-session records with distinct statistical profiles for legitimate and cheating players:

| Metric         | Normal Players     | Cheaters (Bots)     | Purpose                         |
|----------------|--------------------|---------------------|----------------------------------|
| **Kills**      | 0 – 24             | 25 – 50             | Abnormally high kill counts      |
| **Deaths**     | 1 – 19             | 0 – 3               | Suspiciously low death counts    |
| **Aim Accuracy** | 15.0% – 65.0%   | 85.0% – 99.5%       | Inhuman accuracy levels          |
| **Timestamps** | Random across 30 days | Random across 30 days | Session timing analysis       |
| **Player IDs** | `P0001` – `P1000`  | `P1001` – `P1080`   | 80 unique cheater identities     |

### Stage 2: Feature Engineering

`engineer_features(df)`

Aggregates raw session data into per-player behavioural features:

```
Per-row:
  kd_ratio = kills / (deaths + 1)

Per-player aggregates:
  avg_accuracy    = mean(aim_accuracy)
  avg_kills       = mean(kills)
  avg_deaths      = mean(deaths)
  accuracy_std    = std(aim_accuracy)       ← low variance = suspicious
  kill_std        = std(kills)
  session_count   = count(sessions)
  avg_kd          = mean(kd_ratio)

Composite score:
  performance_score = 0.4 × avg_kd
                    + 0.4 × (avg_accuracy / 100)
                    + 0.2 × (1 / (accuracy_std + 1))
```

> **Key Insight:** Cheaters exhibit both extremely high performance *and* suspiciously low variance — they perform consistently at inhuman levels, unlike legitimate players whose accuracy naturally fluctuates.

### Stage 3: Isolation Forest Anomaly Detection

`detect_anomalies(agg, contamination=0.10, seed=42)`

| Parameter       | Value | Description                                      |
|-----------------|-------|--------------------------------------------------|
| `n_estimators`  | 200   | Number of isolation trees in the ensemble         |
| `contamination` | 0.10  | Expected proportion of anomalies in the dataset   |
| `random_state`  | 42    | Seed for reproducibility                          |

**Feature columns used:**
```
avg_accuracy, avg_kills, avg_deaths, accuracy_std, avg_kd, performance_score
```

**Outputs:**
| Column            | Range | Description                                     |
|-------------------|-------|-------------------------------------------------|
| `anomaly_score`   | 0 – 1 | Normalised deviation (1 = most anomalous)       |
| `suspicious_flag` | bool  | `True` if the model labels the player as outlier |
| `confidence`      | 0 – 1 | Model certainty about the classification         |

### Stage 4: Leaderboard & Integrity Scoring

`build_leaderboard(agg)`

```
integrity_score = 1 - anomaly_score
```

Players are ranked by integrity score (highest first) and classified into tiers:

| Tier            | Integrity Score | Visual Badge        | Dashboard Color |
|-----------------|-----------------|---------------------|-----------------|
| 🏆 **Elite**    | ≥ 0.85          | `badge-elite`       | Green `#10b981` |
| 🛡️ **Stable**   | ≥ 0.60          | `badge-stable`      | Purple `#8b5cf6`|
| ⚡ **Risky**    | ≥ 0.35          | `badge-risky`       | Orange `#f97316`|
| 💀 **Critical** | < 0.35          | `badge-critical`    | Red `#ff3b3b`   |

---

## 🎨 Design & UI Details

### Color Palette

| Token          | Hex       | Usage                                |
|----------------|-----------|--------------------------------------|
| `--deep`       | `#0b0f19` | Page background                      |
| `--panel`      | `rgba(15,23,42,.6)` | Glass panel backgrounds     |
| `--cyan`       | `#00f5ff` | Primary accent, headings, highlights |
| `--purple`     | `#8b5cf6` | Secondary accent, stable badges      |
| `--pink`       | `#ff2e88` | Tertiary accent, extreme anomalies   |
| `--red`        | `#ff3b3b` | Danger, critical threats             |
| `--orange`     | `#f97316` | Warning, risky tier                  |
| `--green`      | `#10b981` | Success, elite tier, clean players   |
| `--txt`        | `#e2e8f0` | Primary text                         |
| `--txt2`       | `#94a3b8` | Secondary / muted text               |

### Typography

| Font            | Weight       | Usage                                   |
|-----------------|------------- |-----------------------------------------|
| **Orbitron**    | 400–900      | Headings, metric values, section titles |
| **JetBrains Mono** | 400–700  | Data labels, stats, monospace elements  |
| **Inter**       | 300–900      | Body text, descriptions, UI elements    |

### Key Animations

| Animation       | Effect                                    | Duration |
|-----------------|-------------------------------------------|----------|
| `introZoom`     | Scale + blur cinematic intro              | 0.9s     |
| `scanPulse`     | Horizontal scan line across intro         | 1.8s     |
| `typeReveal`    | Typewriter subtitle reveal                | 2.0s     |
| `cardPop`       | Scale-up entrance for metric cards        | 0.6s     |
| `floatY`        | Gentle vertical float on metric cards     | 7.0s     |
| `pulseGlow`     | Pulsing box-shadow on critical badges     | 2.0s     |
| `shimmerBorder` | Border color shimmer on threat cards      | 3.0s     |
| `barGrow`       | Integrity bar width animation             | 1.0s     |
| `tabReveal`     | Fade-up on tab content switch             | 0.35s    |

---

## 🛠️ Tech Stack

| Layer            | Technology                                                        |
|------------------|-------------------------------------------------------------------|
| **ML Engine**    | Python 3.9+, NumPy, pandas, scikit-learn (Isolation Forest)       |
| **Dashboard**    | Streamlit, Plotly Express, Plotly Graph Objects                    |
| **Website**      | Vanilla HTML5, CSS3, JavaScript (ES6+)                            |
| **Animations**   | GSAP 3 + ScrollTrigger, CSS Keyframes, Canvas API                 |
| **Smooth Scroll**| Lenis                                                             |
| **Typography**   | Google Fonts (Orbitron, Inter, JetBrains Mono)                    |
| **Data Format**  | JSON (website), pandas DataFrame (dashboard)                      |
| **Design**       | Glassmorphism, CSS Custom Properties, backdrop-filter              |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project was built for a hackathon. Feel free to use, modify, and distribute.

---

<p align="center">
  <br>
  <b>🎮 ESPORTS INTEGRITY COMMAND CENTER</b><br>
  <sub>Isolation Forest Engine · AI Anti-Cheat · Protecting Competitive Integrity</sub><br>
  <sub>Built with ❤️ for fair play</sub>
</p>
