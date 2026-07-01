
# Modeling Fourth-Down Decision-Making in College Football

## Project Overview

This project analyzes fourth-down decision-making in college football using play-by-play data from the 2023–2025 seasons.

The analysis focuses on:

- National fourth-down decision tendencies
- Go-for-it rates by distance and field position
- Conversion success rates
- Notre Dame's fourth-down profile
- FBS team aggressiveness rankings

## Key Findings

- Teams go for it 74.6% of the time on 4th & 1, but only 30.7% on 4th & 3–4.
- Midfield is the most conservative decision zone, with teams punting 72.7% of the time.
- Notre Dame is more aggressive than the national average in midfield and short-yardage situations.
- Notre Dame ranks 36th nationally in the Version 1 Aggressiveness Index.
- Baylor, Florida Atlantic, Army, and North Texas rank among the most aggressive FBS teams.

## Methodology

Fourth-down plays were classified into three categories:

- Punt
- Field goal
- Go for it

Non-decision plays, including timeouts and penalties, were removed.

The Aggressiveness Index is calculated as:

Actual Go Rate - Expected Go Rate

Expected go rate is based on national FBS behavior in similar situations, controlling for:

- Distance bucket
- Field zone

## Project Files

- `data/` — processed datasets
- `charts/` — final visualizations
- `deck/` — PowerPoint presentation with presenter notes
- `notebooks/` — analysis notebooks

## Future Work

Version 2 could expand this project with:

- Expected value modeling
- Logistic regression decision modeling
- Coach-level aggressiveness rankings
- Similar-play search
- Streamlit decision dashboard
