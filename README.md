# Network ML Lab

An educational Python project for learning the practical machine learning workflow
through network traffic analysis. This is preparation for a future Final Year
Project, **not the FYP itself**, and it makes no claim of reliable real-world
cyberattack detection.

Network traffic offers useful practice with mixed numeric/categorical features,
imbalanced classes, noisy observations, and generalization. Future research
interests include TLS 1.3 and post-quantum cryptography; this dataset does not
establish performance on those protocols or configurations.

## Current progress — Phase 2

- Project structure, dependency list, and Git exclusions.
- Manual UNSW-NB15 setup and a validated CSV loader.
- Training-data EDA: shape, columns, types, missingness, duplicates, class balance,
  numeric summaries, and plots.
- Small loader test foundation and a findings journal.

Phase 2 is complete: reusable cleaning, training-only preprocessing, a Logistic
Regression baseline, evaluation, model persistence, and lightweight tests.
The official test partition remains reserved; Phase 3 has not started.

## Setup (Python 3.12)

From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m jupyter lab
```

On Windows, create the environment with `py -3.12 -m venv .venv` and activate it
with `.venv\Scripts\Activate.ps1` in PowerShell.

Follow [data setup instructions](data/README.md), then open
`notebooks/01_data_exploration.ipynb`. Select the environment's Python kernel and
use **Restart Kernel and Run All Cells**. Start Jupyter from the repository root
as shown above; the notebook also supports its `notebooks/` working directory.
Missing data produces a helpful error rather than invented results.

Dependencies use compatible version ranges, not a locked environment. After a
successful run, record the Python/package versions and dataset checksums in the
findings journal. `python -m pip freeze` displays exact installed versions.
The shared random seed is `RANDOM_STATE = 42`; Phase 1 plots use all training rows
and do not need random sampling.

## Structure

```text
network-ml-lab/
├── README.md
├── requirements.txt
├── data/
│   ├── README.md
│   ├── raw/                 # Local CSVs; ignored by Git
│   └── processed/           # Reserved for later phases
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_preprocessing_and_logistic_regression.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── utils.py
│   ├── preprocessing.py
│   ├── evaluation.py
│   └── train_baseline.py
├── results/
│   ├── figures/             # Generated outputs; ignored by Git
│   └── metrics/
├── tests/
│   ├── test_data_loader.py
│   └── test_preprocessing.py
├── models/                 # Local fitted pipeline; ignored by Git
└── docs/
    └── findings.md
```

Generated datasets, metrics, figures, and model files stay local and are ignored
by Git. The findings journal records the measured baseline results.

## Learning roadmap

1. **EDA (complete):** pandas/NumPy, feature types, quality checks, distributions,
   class imbalance, and leakage risks.
2. **Cleaning and preprocessing (complete):** inspect anomalies, define feature/target
   separation, reserve validation data, and use training-fitted transformations.
3. **Logistic Regression (complete in Phase 2):** a baseline, confusion matrix, precision, recall,
   F1-score, and ROC-AUC.
4. **Random Forest**, then **XGBoost:** compare overfitting and generalization.
5. **Comparison and feature selection:** consistent splits, reproducible metrics,
   feature importance, and careful evaluation.
6. Optional later experiments: permutation importance, SHAP, tuning, and
   cross-scenario testing when suitable scenario data is available.

Use `RANDOM_STATE = 42` for later randomized splits and estimators. Keep the
provided test set reserved for final evaluation. Fit preprocessing and feature
selection only on training data, including within cross-validation folds.
Exclude `attack_cat` and `id` from predictive features. Accuracy alone can hide
poor minority-class performance; later phases will examine several metrics.

## Dataset and findings

[UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) is the selected
public network intrusion dataset. See [data/README.md](data/README.md) for source,
file placement, and citation guidance. Document observations and decisions in
[docs/findings.md](docs/findings.md). Phase 2 findings include an executed baseline on the local training CSV.

Before committing an executed notebook, clear its outputs so raw traffic records
and bulky plots do not enter Git. Keep source cells and meaningful observations.


## Phase 2 — Preprocessing and Baseline Classification

Open `notebooks/02_preprocessing_and_logistic_regression.ipynb` and run all cells.
The notebook explains features, targets, encoding, scaling, leakage, and the
intrusion-detection meaning of precision, recall, and false alarms.

Logistic Regression provides an understandable linear baseline before trying
more complex models. We use default settings with seed 42 and `max_iter=2000`;
there is no tuning, class weighting, or Random Forest/XGBoost implementation.

The workflow removes ambiguous feature groups with conflicting labels (940
rows), then duplicate traffic observations (73,590 rows). `id` and `attack_cat`
are excluded for their identifier and label-leakage roles. All 39 numeric and
three categorical traffic features remain. Numeric infinities become missing;
zero and the service category `-` remain valid.

Split the 100,811 remaining observations into 80,648 training and 20,163 held-out
validation rows using an 80/20 stratified split with seed 42. Stratification
keeps class proportions similar. The official testing CSV remains untouched.
**Never fit preprocessing on the full dataset:** medians, scales, and category
vocabularies learn only from training data through the combined pipeline.
Numerical features use median imputation and StandardScaler; categorical
features use most-frequent imputation and OneHotEncoder with unknown categories
ignored. Missing-value handling is reusable even though this CSV has none.

Attack-positive results: accuracy **90.07%**, precision **84.45%**, recall
**97.60%**, F1 **90.55%**, ROC-AUC **0.96824**. We also save a classification
report and confusion matrix. Accuracy alone hides missed attacks and false
alarms. Deduplication changes the original traffic distribution, and strong
internal scores do not automatically imply generalization to future traffic.
See [findings](docs/findings.md) for class counts, errors, checksums, and limits.

Run from the root after activating `.venv`:

```bash
python -m unittest discover -s tests -v
python -m src.train_baseline
python -m jupyter lab
```

The runner saves `results/metrics/logistic_regression_metrics.csv`, a JSON audit,
a classification report, `results/figures/logistic_regression_confusion_matrix.png`,
and `models/logistic_regression_pipeline.joblib`. Persist the complete pipeline
so prediction uses the fitted preprocessing. Load only trusted joblib files.
Package ranges can cause small numerical differences; the recorded run includes
versions. Notebook outputs should be cleared before Git commits.

Current status: Phase 2 completed and executed; 10 tests pass. Before Phase 3,
explain why splitting precedes fitting, why `attack_cat` leaks the answer, how
cleaning changes class balance, and what false positives/negatives mean.
Suggested Phase 3 scope: one Random Forest comparison using the same split,
features, and metrics, with train-versus-validation and error analysis. Begin
only after an explicit request; defer XGBoost, tuning, and SHAP.
