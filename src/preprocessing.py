"""Small, leakage-safe preparation helpers for the binary UNSW-NB15 task."""
import numpy as np
import pandas as pd


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
