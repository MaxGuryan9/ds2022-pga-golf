# src/app.py

from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="../templates")

DATA_PATH = Path("data/processed/master_player_seasons.csv")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_PATH}. "
        "Run build_master.py to generate it before starting the app."
    )

# Load data once at startup
df = pd.read_csv(DATA_PATH)

# If sg_tee_to_green is missing (older build), compute it
if "sg_tee_to_green" not in df.columns:
    if all(c in df.columns for c in ["sg_off_the_tee", "sg_approach", "sg_around_green"]):
        df["sg_tee_to_green"] = (
            df["sg_off_the_tee"]
            + df["sg_approach"]
            + df["sg_around_green"]
        )

# Define which stats we want to show leaders for
# higher_is_better = False means we take the minimum (e.g., scoring average, rank)
STAT_DEFS = [
    {"col": "money_earned",      "label": "Money Earned",                         "higher_is_better": True},
    {"col": "sg_total",          "label": "Strokes Gained: Total",                "higher_is_better": True},
    {"col": "sg_off_the_tee",    "label": "Strokes Gained: Off the Tee",          "higher_is_better": True},
    {"col": "sg_tee_to_green",   "label": "Strokes Gained: Tee to Green",         "higher_is_better": True},
    {"col": "sg_putting",        "label": "Strokes Gained: Putting",              "higher_is_better": True},
    {"col": "driving_accuracy",  "label": "Driving Accuracy (%)",                 "higher_is_better": True},
    {"col": "driving_distance",  "label": "Driving Distance (yards)",             "higher_is_better": True},
    {"col": "greens_in_regulation", "label": "Greens in Regulation (%)",          "higher_is_better": True},
    {"col": "scoring_average",   "label": "Scoring Average (lower is better)",    "higher_is_better": False},
    # optional: show “best” FedEx rank (1 is best)
    {"col": "final_season_rank", "label": "Season Rank (1 is best)",              "higher_is_better": False},
]


@app.route("/")
def index():
    # default to most recent year in the data
    default_year = int(df["year"].max())
    year = request.args.get("year", default=default_year, type=int)

    subset = df[df["year"] == year]
    if subset.empty:
        return f"No data available for year {year}", 404

    leaders = []

    for stat in STAT_DEFS:
        col = stat["col"]
        label = stat["label"]
        higher_is_better = stat["higher_is_better"]

        if col not in subset.columns:
            # Skip stats that aren't available in this dataset
            continue

        series = subset[col]

        # Drop rows where this stat is missing
        series = series.dropna()
        if series.empty:
            continue

        if higher_is_better:
            idx = series.idxmax()
        else:
            idx = series.idxmin()

        row = subset.loc[idx]
        
        # Format the value for display
        value = row[col]
        if col == "money_earned" and pd.notna(value):
            # Format money with dollar sign and commas
            value = f"${value:,.0f}"
        elif pd.notna(value):
            # Keep numeric values as-is for template formatting
            value = float(value) if isinstance(value, (int, float)) else value
        else:
            value = "N/A"

        leaders.append(
            {
                "stat_label": label,
                "player_name": row["player_name"],
                "value": value,
            }
        )

    years_available = sorted(df["year"].unique())

    return render_template(
        "index.html",
        year=year,
        years=years_available,
        leaders=leaders,
    )

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # For local dev; Docker will also bind to 0.0.0.0:8000
    app.run(host="0.0.0.0", port=8000, debug=False)

