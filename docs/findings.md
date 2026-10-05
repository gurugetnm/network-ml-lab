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

## Phase 2 — Preprocessing and Baseline Classification

Executed on 2026-10-06 using only `UNSW_NB15_training-set.csv`. The official
`UNSW_NB15_testing-set.csv` was not read or used for decisions or evaluation.
The internal held-out subset is validation, not the official final test.

### Dataset audit and choices

- Raw shape: 175,341 rows × 45 columns.
- `label`: 0 = normal (56,000), 1 = attack (119,341; 68.06%). This is moderate
  attack-majority imbalance, not an extreme rare-attack population.
- Exclude `id` (record identifier) and `attack_cat` (reveals the target).
- Keep 42 traffic inputs: 39 numerical, three categorical (`proto`, `service`,
  `state`). Numeric flags/counts remain numeric for this simple baseline.
- Numeric columns: `dur`, `spkts`, `dpkts`, `sbytes`, `dbytes`, `rate`, `sttl`,
  `dttl`, `sload`, `dload`, `sloss`, `dloss`, `sinpkt`, `dinpkt`, `sjit`, `djit`,
  `swin`, `stcpb`, `dtcpb`, `dwin`, `tcprtt`, `synack`, `ackdat`, `smean`,
  `dmean`, `trans_depth`, `response_body_len`, `ct_srv_src`, `ct_state_ttl`,
  `ct_dst_ltm`, `ct_src_dport_ltm`, `ct_dst_sport_ltm`, `ct_dst_src_ltm`,
  `is_ftp_login`, `ct_ftp_cmd`, `ct_flw_http_mthd`, `ct_src_ltm`, `ct_srv_dst`,
  `is_sm_ips_ports`.
- No missing values, numeric infinities, or exact full-row duplicates.
- 74,301 repeated feature rows after excluding ID and labels. Unique IDs hide
  these in full-row duplicate checks. Zero is not automatically invalid.
- Preserve `service='-'` (94,168 raw rows): no identified service is a category,
  not an instruction to delete rows or impute a known service.
- Exclude all 940 observations in feature groups with conflicting labels. Then
  remove 73,590 duplicate observations, retaining one per unambiguous input.
  No majority-label relabeling is performed.
- Result: 100,811 unique unambiguous observations: normal 51,661 (51.24%),
  attack 49,150 (48.76%). **This changes the evaluation population and discards
  traffic frequency.** Repeated inputs may be legitimate traffic. A later
  grouped-split experiment could retain them without exact overlap.

### Training workflow

Deterministic cleaning precedes splitting. Seed-42 stratified 80/20 split:

| Subset | Normal | Attack | Total |
|---|---:|---:|---:|
| Training | 41,328 | 39,320 | 80,648 |
| Held-out validation | 10,333 | 9,830 | 20,163 |

Fit median imputation and StandardScaler on training numerical columns only;
fit most-frequent imputation and unknown-safe one-hot encoding on training
categorical columns only. Combine these in a ColumnTransformer and Pipeline
with LogisticRegression(random_state=42, max_iter=2000). No class weighting,
feature selection, tuning, or threshold optimization. Converged after 226
iterations. Default prediction threshold: 0.5.

### Measured baseline

| Metric (attack positive) | Value |
|---|---:|
| Accuracy | 0.900709 |
| Precision | 0.844542 |
| Recall | 0.975992 |
| F1 | 0.905521 |
| ROC-AUC | 0.968241 |

Confusion matrix: rows = true class, columns = predicted class.

| | Predicted normal | Predicted attack |
|---|---:|---:|
| Actual normal | 8,567 | 1,766 |
| Actual attack | 236 | 9,594 |

The model detected 9,594 attacks and missed 236 (2.40% of attacks). It falsely
flagged 1,766 normal rows (17.09% of normals). High recall is accompanied by a
meaningful false-alarm burden. Normal recall is about 82.91%; the saved report
shows both classes. The cleaned-population majority baseline is about 51.24%.

### Leakage and generalization limits

Known target leakage (`attack_cat`) and ID inputs are excluded; preprocessing
learns only from training; identical feature rows cannot span the split. No
near-perfect result suggests an obvious remaining label shortcut, but a score
alone cannot rule out leakage. Related flows/capture conditions may occur on
both sides of a random row split; temporal/session independence is unverified.
Strong accuracy and ROC-AUC do **not** automatically mean the model generalizes
well. These are internal results on unique unambiguous observations, not the
original traffic mix or the official testing population. Do not generalize to
live networks, TLS 1.3, or post-quantum traffic. Repeatedly tuning against this
validation subset would also make its reported score optimistic.

### Reproduction and artifacts

- Python 3.12.14; scikit-learn 1.9.1; pandas 2.3.3.
- Training SHA-256:
  `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`.
- Existing local dataset; original download date/source provenance has not been
  independently verified. See `data/README.md` for the intended official source.
- Run `python -m src.train_baseline`; outputs are ignored by Git.
- Metrics CSV, run audit JSON (including feature lists/counts/versions),
  classification report, confusion-matrix PNG, complete joblib pipeline.
- Six new synthetic tests cover target separation/validation, deduplication and
  conflicting labels, invalid values, reproducible/disjoint stratification,
  unseen categories and training-only statistics, and metric calculations.
  Together with the four loader tests, all 10 pass.
- Notebook executed successfully; source notebook retained without outputs.
  Its optimizer took 223 iterations and predicted one fewer false positive
  (1,765 versus the CLI reference 1,766); small numerical optimization
  differences affect borderline probabilities. The CLI run is the numerical
  reference reported above, not an exact cross-runtime guarantee.

Learning glossary is at the end of the Phase 2 notebook. Before proceeding,
explain leakage, fitted transformations, stratification, the confusion matrix,
and the population change caused by cleaning. Phase 3 recommendation: compare
one Random Forest baseline on the same prepared split; inspect overfitting and
errors without tuning against validation repeatedly. No Phase 3 model has been
implemented.
