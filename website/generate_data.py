"""Generate data.json from the bot_analyzer pipeline for the website."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_analyzer import generate_dataset, engineer_features, detect_anomalies, build_leaderboard

raw = generate_dataset(n=5000, cheater_ratio=0.08, seed=42)
feat = engineer_features(raw)
scored = detect_anomalies(feat)
lb = build_leaderboard(scored)

records = []
for _, r in lb.iterrows():
    records.append({
        "id": r["player_id"],
        "kd": round(r["avg_kd"], 3),
        "accuracy": round(r["avg_accuracy"], 2),
        "kills": round(r["avg_kills"], 1),
        "deaths": round(r["avg_deaths"], 1),
        "sessions": int(r["session_count"]),
        "accStd": round(r["accuracy_std"], 2),
        "anomaly": round(r["anomaly_score"], 4),
        "confidence": round(r["confidence"], 4),
        "integrity": round(r["integrity_score"], 4),
        "suspicious": bool(r["suspicious_flag"]),
    })

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
with open(out, "w") as f:
    json.dump(records, f)

print(f"Wrote {len(records)} players to {out}")
