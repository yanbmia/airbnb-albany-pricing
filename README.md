# Airbnb Albany — Occupancy & Price Prediction

Predicts the probability that an Airbnb listing in Albany, NY will be booked on a given day, and recommends a competitive nightly price. Built on 11 months of real Inside Airbnb data (1.66M calendar-day records, 478 listings).

## Problem

Short-term rental hosts set prices manually, with no visibility into demand for a specific date. The goal: given a listing's attributes and a target date, predict (1) the probability it gets booked and (2) a competitive nightly price, so hosts can price dynamically instead of guessing.

## Data

- Source: [Inside Airbnb](http://insideairbnb.com/), Albany NY
- 11 monthly snapshots, April 2025 – February 2026
- 1,664,765 raw calendar rows → 365,082 after merging calendar + listings + reviews
- 478 unique listings, 32.9% overall occupancy rate (imbalanced target)

## Approach

**Time-aware validation.** This is panel/time-series data, so train/test and cross-validation splits are chronological, not random — an 8-month train / 3-month test split (73/27), confirmed with a 5-fold expanding-window time-series CV (not k-fold) to check the split was representative.

**Leakage auditing.** Every feature was checked against the rule "a prediction for day *t* can only use information available before *t*":
- Lag features (bookings in the last 30/60 days, rolling occupancy) use `.shift(1)` so the current day is never included in its own input.
- A neighbourhood-occupancy feature originally leaked future test-period data into its encoding; replaced with K-fold target encoding fit only on training data.
- Removing all lag features as a diagnostic dropped LightGBM AUC from 0.928 → 0.894 (LR: 0.767 → 0.622) — a believable, non-suspicious drop, which is evidence the lag features add real signal rather than leak the label.

**Feature engineering.** Date/seasonality features, log-transformed price, K-fold target-encoded neighbourhood occupancy, rolling booking/occupancy lag features, and a KNN-engineered "competitor price" feature (haversine-distance nearest neighbors of the same room type, within 2km) used by the price model.

**Modeling.** Logistic regression baseline → LightGBM → weighted ensemble, selected on AUC (threshold-independent) then tuned to a decision threshold via the precision-recall curve.

## Results

**Occupancy model** (binary classification, test set AUC):

| Model | AUC |
|---|---|
| Logistic Regression (baseline) | 0.767 |
| LightGBM | 0.928 |
| Ensemble (weighted avg) | **0.937** |

LightGBM alone: 96% accuracy, 0.96 precision / 0.90 recall on the "booked" class.

**Price model** (LightGBM regression, log-price target):

| Metric | Value |
|---|---|
| MAE | $29.72 |
| R² | 0.35 |

## Tech stack

Python · pandas/numpy · scikit-learn · LightGBM · matplotlib/seaborn/plotly · U.S. Census ACS5 API · joblib

## Repo structure

```
airbnb_albany_portfolio.ipynb   # full analysis: EDA → feature engineering → modeling → evaluation
Group B6_Project Report.pdf     # original written report (methodology + deployment write-up)
README.md                       # this file
```

## How to run

1. Get the Albany, NY data from [Inside Airbnb](http://insideairbnb.com/get-the-data.html) (calendar, listings, reviews — multiple monthly snapshots).
2. Place the files in a local `data/` folder (see the Configuration cell in the notebook for the expected layout).
3. `pip install lightgbm scikit-learn pandas matplotlib seaborn plotly requests joblib`
4. Run the notebook top to bottom.

## Limitations & future work

- A census-income enrichment feature was attempted but never fully wired up: Albany listings are labeled by city ward, Census data is by tract, and there's no public ward↔tract lookup — a real fix needs a spatial join (`geopandas`), not a hand-typed name mapping. Documented honestly in the notebook rather than faked.
- Price model R² (0.35) suggests unobserved factors (photos, amenities, exact location) matter more for price than for occupancy.
- Single-market model (Albany only, 478 listings); would need retraining, not just re-scoring, for another city.

## Deployment design

Both models are serialized with `joblib` and intended to be served behind a thin REST API (e.g. FastAPI): a client sends listing attributes + target date, and the response includes a booking-probability, a price recommendation, and a demand tier — see the project report for the full design.
