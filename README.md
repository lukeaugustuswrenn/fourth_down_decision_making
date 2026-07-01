# Modeling Fourth-Down Decision-Making in College Football

## Live Dashboard

[Open the Streamlit dashboard](https://lukeaugustuswrenn-fourth-down-decision-making-app-qom12a.streamlit.app/)


## Project Overview

This project analyzes fourth-down decision-making in college football using FBS play-by-play data from the 2023-2025 seasons.

The goal is to understand when teams choose aggression on fourth down, how Notre Dame compares to the national average, and which FBS programs are most aggressive or conservative relative to situation.

## Dashboard

This project includes a Streamlit dashboard that allows users to:

- Select any FBS team
- View fourth-down decisions by distance
- View fourth-down decisions by field position
- Compare team go-for-it rates to national averages
- View Aggressiveness Index rankings
- Explore selected-team fourth-down plays
- Download the accompanying PowerPoint deck

To run the dashboard locally:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## Key Findings

- Teams go for it 74.6% of the time on 4th & 1.
- Teams go for it only 30.7% of the time on 4th & 3-4.
- Midfield is the most conservative decision zone, with teams punting 72.7% of the time.
- Notre Dame is more aggressive than the national average in short-yardage and midfield situations.
- Notre Dame ranks 36th nationally in the Version 1 Aggressiveness Index.
- Baylor, Florida Atlantic, Army, and North Texas are among the most aggressive FBS teams.
- Iowa, Minnesota, Louisville, Texas A&M, and Michigan are among the most conservative FBS teams.

## Methodology

Fourth-down plays were classified into three decision types:

- Punt
- Field goal
- Go for it

Non-decision plays, including timeouts and penalties, were removed.

The Version 1 Aggressiveness Index is calculated as:

```text
Actual Go Rate - Expected Go Rate
```

Expected go rate is based on national FBS behavior in similar situations, controlling for distance bucket and field zone.

## Project Structure

- app.py
- README.md
- requirements.txt
- data/
- charts/
- deck/
- notebooks/

## Version 1 Scope

This version is intentionally descriptive and presentation-ready.

It focuses on data cleaning, fourth-down classification, national trend analysis, Notre Dame comparison, a simple context-adjusted Aggressiveness Index, a dashboard, and a presentation deck.

## Future Work

Future versions could add expected value modeling, logistic regression, random forest or XGBoost models, coach-level rankings, similar-play search, win probability integration, and an interactive fourth-down recommendation engine.

## Author

Luke Wrenn
