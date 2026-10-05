# Network ML Lab

An educational Python project for learning the practical machine learning workflow
through network traffic analysis. This is preparation for a future Final Year
Project, **not the FYP itself**, and it makes no claim of reliable real-world
cyberattack detection.

Network traffic offers useful practice with mixed numeric/categorical features,
imbalanced classes, noisy observations, and generalization. Future research
interests include TLS 1.3 and post-quantum cryptography; this dataset does not
establish performance on those protocols or configurations.

## Current progress — Phase 1

- Project structure, dependency list, and Git exclusions.
- Manual UNSW-NB15 setup and a validated CSV loader.
- Training-data EDA: shape, columns, types, missingness, duplicates, class balance,
  numeric summaries, and plots.
- Small loader test foundation and a findings journal.

No cleaning transformations or models have been implemented yet.

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
│   └── 01_data_exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── utils.py
├── results/
│   ├── figures/             # Generated outputs; ignored by Git
│   └── metrics/
├── tests/
│   └── test_data_loader.py
└── docs/
    └── findings.md
```

Add preprocessing/evaluation modules and later notebooks when their phases begin,
so every file represents understandable work rather than an empty implementation.

## Learning roadmap

1. **EDA (current):** pandas/NumPy, feature types, quality checks, distributions,
   class imbalance, and leakage risks.
2. **Cleaning and preprocessing:** inspect anomalies, define feature/target
   separation, reserve validation data, and use training-fitted transformations.
3. **Logistic Regression:** a baseline, confusion matrix, precision, recall,
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
[docs/findings.md](docs/findings.md). Dataset-dependent findings remain unfilled
until the notebook is run on actual data.

Before committing an executed notebook, clear its outputs so raw traffic records
and bulky plots do not enter Git. Keep source cells and meaningful observations.
