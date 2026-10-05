"""Small synthetic checks; no real dataset is needed."""
import unittest
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.preprocessing import (separate_features_target, clean_observations,
    handle_invalid_values, identify_feature_types, split_dataset, build_preprocessor)
from src.evaluation import calculate_metrics


class PreprocessingTests(unittest.TestCase):
    def test_feature_target_separation(self):
        raw = pd.DataFrame({'id': [1, 2], 'attack_cat': ['Normal', 'Attack'],
                            'label': [0, 1], 'dur': [0.1, 1.0]})
        features, target = separate_features_target(raw)
        self.assertEqual(features.columns.tolist(), ['dur'])
        self.assertEqual(target.tolist(), [0, 1])
        self.assertIn('label', raw)  # helpers never mutate the caller
        with self.assertRaises(ValueError):
            separate_features_target(raw.assign(label=2))

    def test_duplicate_and_conflicting_observations(self):
        raw = pd.DataFrame({'id': range(5), 'dur': [1, 1, 2, 2, 3],
                            'label': [0, 0, 0, 1, 1]})
        features, target, audit = clean_observations(raw)
        self.assertEqual(features.dur.tolist(), [1, 3])
        self.assertEqual(target.tolist(), [0, 1])
        self.assertEqual(audit['conflicting_rows_removed'], 2)
        self.assertEqual(audit['duplicate_rows_removed'], 1)

    def test_invalid_values_preserve_zero_and_service_sentinel(self):
        features = pd.DataFrame({'dur': [0, np.inf, -np.inf], 'service': ['-', None, 'dns']})
        cleaned = handle_invalid_values(features)
        self.assertEqual(cleaned.dur.iloc[0], 0)
        self.assertEqual(cleaned.dur.isna().sum(), 2)
        self.assertEqual(cleaned.service.iloc[0], '-')
        self.assertTrue(np.isinf(features.dur.iloc[1]))

    def test_split_reproducible_stratified_and_disjoint(self):
        features = pd.DataFrame({'dur': range(40)})
        target = pd.Series([0, 1] * 20)
        first = split_dataset(features, target)
        second = split_dataset(features, target)
        for a, b in zip(first, second):
            self.assertTrue(a.equals(b))
        self.assertFalse(set(first[0].index) & set(first[1].index))
        self.assertEqual(first[3].value_counts().to_dict(), {0: 4, 1: 4})

    def test_training_only_statistics_and_unseen_categories(self):
        train = pd.DataFrame({'dur': [1., 3., np.nan, 5.], 'proto': ['tcp', 'udp', None, 'tcp']})
        train = handle_invalid_values(train)
        numeric, categorical = identify_feature_types(train)
        pipeline = Pipeline([('preprocessing', build_preprocessor(numeric, categorical)),
                             ('classifier', LogisticRegression(random_state=42))])
        pipeline.fit(train, [0, 1, 0, 1])
        preprocessor = pipeline.named_steps['preprocessing']
        transformed = preprocessor.transform(pd.DataFrame({'dur': [999., np.nan], 'proto': ['unseen', 'tcp']}))
        dense = transformed.toarray() if hasattr(transformed, 'toarray') else transformed
        self.assertTrue(np.isfinite(dense).all())
        self.assertEqual(dense.shape, (2, 3))
        self.assertEqual(preprocessor.named_transformers_['numeric'].named_steps['impute'].statistics_[0], 3.)
        self.assertEqual(preprocessor.named_transformers_['numeric'].named_steps['scale'].mean_[0], 3.)
        self.assertEqual(pipeline.predict(pd.DataFrame({'dur': [2.], 'proto': ['unseen']})).shape, (1,))

    def test_attack_metrics(self):
        metrics = calculate_metrics([0, 0, 1, 1], [0, 1, 0, 1], [0.1, 0.8, 0.2, 0.9])
        for name in ['accuracy', 'precision', 'recall', 'f1']:
            self.assertEqual(metrics[name], 0.5)
        self.assertEqual(metrics['roc_auc'], 0.75)


if __name__ == '__main__':
    unittest.main()
