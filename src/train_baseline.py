"""Run the Phase 2 baseline: python -m src.train_baseline."""
import hashlib
import json
import platform
import warnings

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline

from src.data_loader import load_dataset
from src.evaluation import calculate_metrics, print_classification_report, plot_confusion_matrix
from src.preprocessing import clean_observations, identify_feature_types, split_dataset, build_preprocessor
from src.utils import PROJECT_ROOT, RAW_DATA_DIR, RANDOM_STATE


def run_baseline():
    features, target, audit = clean_observations(load_dataset())
    x_train, x_test, y_train, y_test = split_dataset(features, target)
    numeric, categorical = identify_feature_types(x_train)
    pipeline = Pipeline([('preprocessing', build_preprocessor(numeric, categorical)),
                         ('classifier', LogisticRegression(random_state=RANDOM_STATE, max_iter=2000))])
    # Only this training subset supplies imputation, scaling and encoding statistics.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always', ConvergenceWarning)
        pipeline.fit(x_train, y_train)
    converged = not any(issubclass(w.category, ConvergenceWarning) for w in caught)
    for warning in caught:
        warnings.warn(str(warning.message), warning.category)
    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    metrics = calculate_metrics(y_test, predictions, probabilities)
    report = print_classification_report(y_test, predictions)
    summary = {**audit, 'train_rows': len(x_train), 'validation_rows': len(x_test),
               'class_counts': target.value_counts().sort_index().to_dict(),
               'train_class_counts': y_train.value_counts().sort_index().to_dict(),
               'validation_class_counts': y_test.value_counts().sort_index().to_dict(),
               'numeric_columns': numeric, 'categorical_columns': categorical,
               'confusion_matrix': confusion_matrix(y_test, predictions, labels=[0, 1]).tolist(),
               'metrics': metrics, 'converged': converged,
               'iterations': pipeline.named_steps['classifier'].n_iter_.tolist(),
               'python': platform.python_version(), 'sklearn': sklearn.__version__,
               'pandas': pd.__version__, 'random_state': RANDOM_STATE,
               'training_sha256': hashlib.sha256((RAW_DATA_DIR / 'UNSW_NB15_training-set.csv').read_bytes()).hexdigest()}
    for directory in ['results/metrics', 'results/figures', 'models']:
        (PROJECT_ROOT / directory).mkdir(parents=True, exist_ok=True)
    pd.DataFrame([metrics]).to_csv(PROJECT_ROOT / 'results/metrics/logistic_regression_metrics.csv', index=False)
    (PROJECT_ROOT / 'results/metrics/logistic_regression_run.json').write_text(json.dumps(summary, indent=2))
    (PROJECT_ROOT / 'results/metrics/logistic_regression_classification_report.txt').write_text(report)
    figure = plot_confusion_matrix(y_test, predictions)
    figure.savefig(PROJECT_ROOT / 'results/figures/logistic_regression_confusion_matrix.png', dpi=150)
    plt.close(figure)
    joblib.dump(pipeline, PROJECT_ROOT / 'models/logistic_regression_pipeline.joblib')
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    run_baseline()
