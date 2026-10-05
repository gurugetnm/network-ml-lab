# Learning journal

## Phase 1 — dataset inspection

Status: notebook prepared; observations await a run on the real training CSV.
No measured dataset findings or model performance are claimed yet.

Record after running:

- Dataset source URL, download date, filename, and SHA-256 checksum:
- Python and package versions:
- Row/column counts and feature types:
- Missing values and possible sentinel values (for example `-`):
- Exact duplicates versus repeated traffic features:
- Normal/attack counts and proportions:
- Skewed numeric features, infinities, and notable ranges:
- Questions to investigate before cleaning:

## Concepts to explain in your own words

- How does a feature differ from a target?
- Why does class imbalance make accuracy insufficient?
- Why might an ID hide duplicates? Are repeated feature rows always errors?
- Why is `attack_cat` a leakage risk when predicting `label`?
- Why should encoders, imputers, and scalers learn only from training data?
- Why does training-set EDA say little about performance on future traffic?

## Phase 2 proposal (not implemented)

Create a cleaning notebook. Define inputs and target, inspect suspect values,
choose cleaning rules with reasons, and create a reproducible validation split
within the official training partition. Fit preprocessing only on the training
subset and apply it to validation data. Keep the official testing partition
reserved. Add small, targeted tests for feature exclusion and split separation.
Model training starts in a subsequent phase.
