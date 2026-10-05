# Dataset setup

Use the headered **UNSW-NB15 training and testing partitions** from the
[official UNSW dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
Follow its download link and retain the original filenames:

```text
data/raw/
├── UNSW_NB15_training-set.csv
└── UNSW_NB15_testing-set.csv
```

The official page describes 175,341 training records and 82,332 testing records.
Avoid the original `UNSW-NB15_1.csv` through `UNSW-NB15_4.csv` shards: they use a
different layout and are outside this beginner workflow. Extract downloaded
archives locally; do not place an archive where a CSV is expected.

`label` is the binary target: 0 = normal, 1 = attack. `attack_cat` describes the
attack category and must not become an input feature for binary prediction: it
reveals the outcome. `id` is a record identifier, not a meaningful traffic feature.

Phase 1 explores **only the training partition**. You can begin with just that
file. Keep the testing partition untouched until final evaluation; do not combine
the partitions. Later, create a validation split within training data and fit
imputation, encoders, scaling, and feature selection only on the training subset.
Apply those fitted transformations to validation/test data.

The loader preserves raw data, including missing values and duplicates. An
identifier can make exact full-row duplicate counts look artificially low, so the
EDA also inspects duplicate traffic feature rows excluding `id`, `label`, and
`attack_cat`. These are observations, not automatic instructions to delete rows.

Raw and processed data are ignored by Git. `data/processed/` is reserved for later
work; Phase 1 does not write cleaned datasets. Record source, download date, and
SHA-256 checksums in `docs/findings.md` locally for reproducible experiments.
Respect the source's usage terms and cite its papers when using the dataset:

- Moustafa, N. and Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set).* MilCIS.

Consult the official page for the complete requested citations and dataset details.
