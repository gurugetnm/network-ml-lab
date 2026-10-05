"""Small, leakage-safe preparation helpers for the binary UNSW-NB15 task."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils import RANDOM_STATE


def remove_duplicate_rows(data, subset=None):
    """Keep the first exact observation; optionally ignore identifier columns."""
    return data.drop_duplicates(subset=subset).copy()


def separate_features_target(data):
    """Exclude label leakage and the record ID, retaining all traffic features."""
    if 'label' not in data or data['label'].isna().any() or not data['label'].isin([0, 1]).all():
        raise ValueError('label must contain only 0 (normal) and 1 (attack).')
    return data.drop(columns=['label', 'attack_cat', 'id'], errors='ignore').copy(), data['label'].astype(int).copy()


def identify_feature_types(features):
    numeric = features.select_dtypes(include='number').columns.tolist()
    categorical = features.columns.difference(numeric, sort=False).tolist()
    return numeric, categorical


def handle_invalid_values(features):
    """Replace numeric infinities with missing values; never invent numeric ranges.

    Zero is often a valid traffic measurement. The service '-' category is kept:
    it denotes no identified service, and is useful categorical information.
    """
    cleaned = features.copy()
    numeric, categorical = identify_feature_types(cleaned)
    cleaned[numeric] = cleaned[numeric].replace([np.inf, -np.inf], np.nan)
    for column in categorical:
        cleaned[column] = cleaned[column].where(cleaned[column].notna(), np.nan)
    return cleaned


def clean_observations(data):
    """Remove contradictory labels and repeated traffic observations before splitting.

    IDs hide repeated observations. Rows with identical inputs but conflicting
    targets are ambiguous; exclude the whole group rather than choose a label.
    This changes the evaluation population: scores describe unique unambiguous
    observations, not the original traffic frequency distribution.
    """
    features, target = separate_features_target(data)
    numeric, _ = identify_feature_types(features)
    audit = {'raw_rows': len(data), 'full_row_duplicates': int(data.duplicated().sum()),
             'feature_duplicates': int(features.duplicated().sum()),
             'missing_values': int(features.isna().sum().sum()),
             'infinite_values': int(np.isinf(features[numeric]).sum().sum())}
    observations = features.assign(label=target)
    conflicts = observations.groupby(list(features.columns), dropna=False)['label'].transform('nunique').gt(1)
    audit['conflicting_rows_removed'] = int(conflicts.sum())
    observations = remove_duplicate_rows(observations.loc[~conflicts], subset=list(features.columns))
    audit['duplicate_rows_removed'] = len(data) - audit['conflicting_rows_removed'] - len(observations)
    audit['clean_rows'] = len(observations)
    features, target = separate_features_target(observations)
    return handle_invalid_values(features), target, audit


def split_dataset(features, target):
    # Stratification preserves roughly the same class proportions in both subsets.
    return train_test_split(features, target, test_size=0.2, random_state=RANDOM_STATE, stratify=target)
