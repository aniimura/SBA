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
| `07_sources.md` | Source list (links) for the `[LIVE]` 2026-05-29 data |

## Methodology in brief

The forecast is built bottom-up (seat-by-seat ratings aggregated) and validated
top-down (national fundamentals + historical base rates). Where the two
disagree, the disagreement is treated as a measure of uncertainty rather than
smoothed away. An explicit adequacy assessment (file 05) gates the forecast:
the prediction is only stated at the confidence the evidence supports.

## Data sources and currency (read before using)

This dossier combines **two streams**, both dated **2026-05-29**:

1. **[LIVE] Aggregated web-search data** — `WebSearch` succeeded and returned
   current May-2026 figures, which **are incorporated and tagged `[LIVE]`**
   throughout (presidential approval, generic ballot, candidate recruitments,
   redistricting seat estimates, retirements). These reflect averages reported by
   Silver Bulletin, RealClearPolitics, FiftyPlusOne, US Polling Data, Sabato's
   Crystal Ball, Cook Political Report, Ballotpedia, NPR, and 270toWin.
2. **Historical base rates + structural facts** — timeless and do not expire.

**Caveats on the live stream:** `WebSearch` returns *summarized* results, and
**full-page fetches to several primary sources (Wikipedia, FiveThirtyEight) were
blocked (HTTP 403) and direct `curl` was host-allowlist-restricted** in this
environment. So `[LIVE]` figures are accurate to the **aggregator summaries as of
2026-05-29** but were not each independently cross-verified against the raw
source page. Anyone relying on a specific number should reconfirm it against the
named tracker. Anything **not** tagged `[LIVE]` reflects the analyst's knowledge
through January 2026 and should likewise be re-checked.

Prepared: 2026-05-29.
