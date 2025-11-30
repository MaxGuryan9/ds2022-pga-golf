# PGA TOUR Stats Pipeline & Flask Dashboard

## 1. Executive Summary
### Problem
The PGA Tour collects statistical data (strokes gained, driving distance, scoring, ranking, etc.), which is displayed on the PGA Tour website. Many analysts and fans want to compare player performance throughout a season, across different seasons, or view category leaders, which is displayed on their website. However, the data, which is publicly available, is spread across multiple separate CSV endpoints, making it hard to obtain a complete dataset of all stats collected on the PGA Tour for a given season or range of seasons.
### Solution
This project builds a fully containerized data pipeline and Flask dashboard. Through this pipeline, raw CSV files are downloaded, the data is cleaned and normalized, and then merged into two different master datasets. One is a dataset with all statistical categories during a given season, and the other is a dataset with all statistical categories over a range of seasons. This data is displayed through a dashboard, allowing a fan or analyst to toggle between seasons and see which player leads in each category during that specific season. Despite the dashboards simplicity, it is for proof of concept, showing that we now have all the data in one place. This entire containerized system can be run with a single pipeline command `./run.sh`.

## 2. System Overview

### Concept(s)/Tool(s) Used:
- Data pipelines
- Flask API
- Docker Containerization
- Smoke Testing and Health Checks

### Architecture Diagrams

#### Pipeline
![Pipeline Diagram](assets/pipeline.png)
This pipeline shows the steps taken through the Dockerfile when you run the `./run.sh` command. 

#### Flowchart
![Flowchart](assets/flowchart.png)
This flowchart represents how each datapoint is represented on the dashboard based on the users input.

#### Project Folder Tree
ds2022-pga-golf/
│
├── Dockerfile                   # Defines build-run environment; runs the pipeline
├── run.sh                       # One-command build + run (no cache)
├── requirements.txt             # Python dependencies
├── README.md                    # Full project write-up
├── LICENSE                      # MIT license
├── .gitignore                   # Excludes local env + data dirs
├── .env.example                 # Example environment variables (no secrets)
│
├── assets/                      # Static documentation assets
│   ├── pipeline.png             # Pipeline diagram
│   ├── flowchart.png            # App flowchart
│   └── dashboard.png            # Screenshot of dashboard
│
├── src/                         # All application + pipeline code
│   ├── app.py                   # Flask server
│   ├── download_stats.py        # Download raw PGA stats
│   ├── parse_stats.py           # Normalize + clean data
│   ├── build_master.py          # Merge into master dataset
│
├── templates/
│   └── index.html               # Dashboard page template (Jinja2)
│
├── tests/                       # Smoke tests (pytest)
│   ├── test_data.py             # Dataset validation tests
│   └── test_app.py              # Flask app tests
│
└── data/                        # Created only inside Docker container
    ├── raw/                     # Raw CSVs from PGA API
    ├── intermediate/            # Cleaned intermediate CSVs
    └── processed/               # Final master_player_seasons.csv

#### Data Sources
All PGA Data came from the PGA's official CSV API:
"https://www.pgatour.com/api/stats-download?timePeriod=THROUGH_EVENT&tourCode=R&statsId=<ID>&year=<YEAR>"

#### Stats Included
- Strokes Gained (Total, OTT, Approach, ARG, Putting)
- Driving Distance
- Driving Accuracy
- Greens in Regulation
- Scoring Average
- Money Earned
- FedEx-style Season Rank
- Derived: Strokes Gained Tee-to-Green (Strokes Gained Total excluding Putting)
#### Data Credits
This project uses publicly available PGA TOUR data exclusively for educational and non-commercial use.
All PGA data is © PGA TOUR

## 3. How to Run with Docker (Local)
In your terminal:
```
./run.sh
```
This runs:

```python
#!/usr/bin/env bash
docker build -t pga-stats:latest .

docker run --rm -p 8000:8000 pga-stats:latest

curl http://localhost:8000/health

```
