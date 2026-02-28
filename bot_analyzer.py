"""
Gaming Bot Behaviour Analyzer
==============================
Synthetic data generation, feature engineering, and Isolation Forest
anomaly detection for esports anti-cheat analytics.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler


# ---------------------------------------------------------------------------
# 1. Synthetic Dataset Generation
# ---------------------------------------------------------------------------

def generate_dataset(n: int = 1000, cheater_ratio: float = 0.08, seed: int = 42) -> pd.DataFrame:
    """
    Generate *n* synthetic player-session records.

    Parameters
    ----------
    n : int
        Total number of session records.
    cheater_ratio : float
        Fraction of records that exhibit cheating patterns.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Columns: player_id, kills, deaths, aim_accuracy, timestamp, is_cheater
    """
    rng = np.random.default_rng(seed)
    n_cheaters = int(n * cheater_ratio)
    n_legit = n - n_cheaters

    # --- Legitimate players ---------------------------------------------------
    legit_player_ids = [f"P{str(i).zfill(4)}" for i in rng.choice(range(1, 501), size=n_legit)]
    legit_kills = rng.integers(0, 25, size=n_legit)
    legit_deaths = rng.integers(1, 20, size=n_legit)
    legit_accuracy = rng.uniform(15.0, 65.0, size=n_legit).round(2)

    # --- Cheating players (distinctive patterns) ------------------------------
    cheater_pool = [f"P{str(i).zfill(4)}" for i in range(901, 921)]  # 20 unique cheater IDs
    cheater_player_ids = rng.choice(cheater_pool, size=n_cheaters)
    cheater_kills = rng.integers(25, 51, size=n_cheaters)            # very high kills
    cheater_deaths = rng.integers(0, 4, size=n_cheaters)             # very low deaths
    cheater_accuracy = rng.uniform(85.0, 99.5, size=n_cheaters).round(2)  # suspiciously high

    # --- Timestamps over the last 30 days ------------------------------------
    base_ts = pd.Timestamp("2026-02-01")
    legit_ts = base_ts + pd.to_timedelta(rng.integers(0, 30 * 24 * 3600, size=n_legit), unit="s")
    cheater_ts = base_ts + pd.to_timedelta(rng.integers(0, 30 * 24 * 3600, size=n_cheaters), unit="s")

    # --- Assemble -------------------------------------------------------------
    df_legit = pd.DataFrame({
        "player_id": legit_player_ids,
        "kills": legit_kills,
        "deaths": legit_deaths,
        "aim_accuracy": legit_accuracy,
        "timestamp": legit_ts,
        "is_cheater": False,
    })

    df_cheat = pd.DataFrame({
        "player_id": cheater_player_ids,
        "kills": cheater_kills,
        "deaths": cheater_deaths,
        "aim_accuracy": cheater_accuracy,
        "timestamp": cheater_ts,
        "is_cheater": True,
    })

    df = pd.concat([df_legit, df_cheat], ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# 2. Feature Engineering
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive per-player aggregate features useful for anomaly detection.

    New columns (per player):
        kd_ratio, avg_accuracy, avg_kills, avg_deaths,
        accuracy_std, kill_std, session_count, performance_score
    """
    df = df.copy()

    # Per-row K/D ratio
    df["kd_ratio"] = (df["kills"] / (df["deaths"] + 1)).round(3)

    # Per-player aggregates
    agg = df.groupby("player_id").agg(
        avg_accuracy=("aim_accuracy", "mean"),
        avg_kills=("kills", "mean"),
        avg_deaths=("deaths", "mean"),
        accuracy_std=("aim_accuracy", "std"),
        kill_std=("kills", "std"),
        session_count=("player_id", "count"),
        avg_kd=("kd_ratio", "mean"),
    ).reset_index()

    # Fill NaN std (players with 1 session)
    agg["accuracy_std"] = agg["accuracy_std"].fillna(0)
    agg["kill_std"] = agg["kill_std"].fillna(0)

    # Composite performance score (higher → more suspicious)
    agg["performance_score"] = (
        agg["avg_kd"] * 0.4
        + agg["avg_accuracy"] / 100 * 0.4
        + (1 / (agg["accuracy_std"] + 1)) * 0.2   # low variance → suspicious
    ).round(4)

    return agg


# ---------------------------------------------------------------------------
# 3. Isolation Forest Anomaly Detection
# ---------------------------------------------------------------------------

def detect_anomalies(agg: pd.DataFrame, contamination: float = 0.10, seed: int = 42) -> pd.DataFrame:
    """
    Run Isolation Forest on the engineered features and return the dataframe
    enriched with anomaly_score, suspicious_flag, and confidence.
    """
    agg = agg.copy()

    feature_cols = [
        "avg_accuracy", "avg_kills", "avg_deaths",
        "accuracy_std", "avg_kd", "performance_score",
    ]

    X = agg[feature_cols].values

    # Fit Isolation Forest
    iso = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=seed,
    )
    iso.fit(X)

    # Raw scores: lower (more negative) = more anomalous
    raw_scores = iso.decision_function(X)
    labels = iso.predict(X)  # 1 = normal, -1 = anomaly

    # Normalise raw_scores to 0-1 anomaly_score (1 = most anomalous)
    scaler = MinMaxScaler()
    norm = scaler.fit_transform(-raw_scores.reshape(-1, 1)).flatten()

    agg["anomaly_score"] = norm.round(4)
    agg["suspicious_flag"] = labels == -1
    agg["confidence"] = np.clip(np.abs(raw_scores) / np.abs(raw_scores).max(), 0, 1).round(4)

    return agg


# ---------------------------------------------------------------------------
# 4. Leaderboard Builder
# ---------------------------------------------------------------------------

def build_leaderboard(agg: pd.DataFrame) -> pd.DataFrame:
    """
    Build a final leaderboard sorted by integrity_score (1 - anomaly_score).
    """
    lb = agg.copy()
    lb["integrity_score"] = (1 - lb["anomaly_score"]).round(4)
    lb = lb.sort_values("integrity_score", ascending=False).reset_index(drop=True)
    lb.index += 1  # 1-based rank
    lb.index.name = "rank"
    return lb


# ---------------------------------------------------------------------------
# Convenience: run full pipeline
# ---------------------------------------------------------------------------

def run_pipeline(n: int = 1000, cheater_ratio: float = 0.08) -> pd.DataFrame:
    """Execute the full pipeline and return the leaderboard dataframe."""
    raw = generate_dataset(n=n, cheater_ratio=cheater_ratio)
    features = engineer_features(raw)
    scored = detect_anomalies(features)
    leaderboard = build_leaderboard(scored)
    return leaderboard


if __name__ == "__main__":
    lb = run_pipeline()
    print("\n=== TOP 10 LEADERBOARD ===")
    print(lb.head(10).to_string())
    print(f"\nTotal players  : {len(lb)}")
    print(f"Suspicious     : {lb['suspicious_flag'].sum()}")
    print(f"Avg integrity  : {lb['integrity_score'].mean():.4f}")
