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
#### Flowchart
![Flowchart](assets/flowchart.png)
#### Data Sources
All PGA Data came from the PGA's official CSV API:
https://www.pgatour.com/api/stats-download?timePeriod=THROUGH_EVENT&tourCode=R&statsId=<ID>&year=<YEAR>

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


