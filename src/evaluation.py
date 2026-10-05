"""Binary classification evaluation: attack (1) is the positive class."""
import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, classification_report, ConfusionMatrixDisplay)


def calculate_metrics(target, predictions, probabilities=None):
    metrics = {'accuracy': accuracy_score(target, predictions),
               'precision': precision_score(target, predictions, zero_division=0),
               'recall': recall_score(target, predictions, zero_division=0),
               'f1': f1_score(target, predictions, zero_division=0)}
    if probabilities is not None:
        metrics['roc_auc'] = roc_auc_score(target, probabilities)
    return metrics


def print_classification_report(target, predictions):
    report = classification_report(target, predictions, labels=[0, 1],
                                   target_names=['normal', 'attack'], zero_division=0)
    print(report)
    return report


def plot_confusion_matrix(target, predictions):
    figure, axis = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_predictions(target, predictions, labels=[0, 1],
        display_labels=['normal', 'attack'], cmap='Blues', colorbar=False, ax=axis)
    axis.set_title('Logistic Regression — held-out validation')
    figure.tight_layout()
    return figure
