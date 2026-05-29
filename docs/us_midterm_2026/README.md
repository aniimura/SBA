# 2026 U.S. Midterm Elections — Forecast Dossier

A self-contained research and analysis package for forecasting the November 3,
2026 U.S. midterm elections (U.S. House, U.S. Senate, and the cycle's notable
specials and governorships).

## Contents

| File | Purpose |
|------|---------|
| `01_landscape_and_stakes.md` | Starting conditions, what is on the ballot, what control requires |
| `02_senate_2026.md` | Seat-by-seat Senate map (Class 2 + 2026 specials) with ratings |
| `03_house_2026.md` | House math, the 2025-26 mid-decade redistricting war, generic ballot |
| `04_fundamentals_base_rates.md` | Presidential approval, economy, historical midterm base rates |
| `05_situational_adequacy_assessment.md` | Evidence quality / analytic-confidence check before forecasting |
| `06_forecast.md` | The forecast: scenarios, probabilities, seat ranges, confidence |

## Methodology in brief

The forecast is built bottom-up (seat-by-seat ratings aggregated) and validated
top-down (national fundamentals + historical base rates). Where the two
disagree, the disagreement is treated as a measure of uncertainty rather than
smoothed away. An explicit adequacy assessment (file 05) gates the forecast:
the prediction is only stated at the confidence the evidence supports.

## IMPORTANT — data-source caveat (read before using)

This dossier was produced inside an execution environment whose network policy
**blocks all outbound internet access** (the repository's own `README.md`
documents the same restriction; live attempts via `WebSearch`, `WebFetch`, and
`curl` all failed during preparation on 2026-05-29).

Consequently the numbers and ratings here are **not** freshly scraped from live
trackers. They are reconstructed from:

1. The analyst's knowledge base, reliable through **January 2026**; and
2. Well-established, slow-moving historical base rates (which do not expire).

Named sources (Cook Political Report, Sabato's Crystal Ball, FiveThirtyEight,
RealClearPolitics, Wikipedia seat lists, etc.) are cited as the **verification
targets** the reader should consult to refresh any figure — not as pages that
were retrieved here. Treat every specific poll number, retirement, and primary
result as **"as of early 2026, verify against live sources before relying on
it."** Developments between January and May 2026 (late retirements, primary
outcomes, economic shocks) are, by construction, outside this dataset; file 05
quantifies how much that widens the uncertainty.

Prepared: 2026-05-29.
