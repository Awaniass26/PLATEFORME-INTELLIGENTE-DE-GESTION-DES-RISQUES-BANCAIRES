"""Métriques et seuils sensibles aux coûts pour la détection de fraude."""

import numpy as np
from sklearn.metrics import confusion_matrix


def select_cost_sensitive_threshold(
    y_true,
    probabilities,
    *,
    false_negative_cost: float,
    false_positive_cost: float,
) -> dict[str, float | int]:
    """Choisir sur validation le seuil au coût d'erreur pondéré minimal.

    En cas d'égalité, préfère le seuil le plus élevé, qui déclenche moins
    d'alertes. Les coûts sont des unités relatives, à définir par le métier.
    """
    truth = np.asarray(y_true)
    scores = np.asarray(probabilities, dtype=float)
    if truth.ndim != 1 or scores.ndim != 1 or len(truth) != len(scores):
        raise ValueError("y_true et probabilities doivent être des vecteurs de même longueur.")
    if len(truth) == 0:
        raise ValueError("Il faut au moins une observation de validation.")
    if not np.isin(truth, [0, 1]).all():
        raise ValueError("y_true doit contenir uniquement les classes 0 et 1.")
    if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
        raise ValueError("Les probabilités doivent être finies et comprises entre 0 et 1.")
    if not np.isfinite(false_negative_cost) or false_negative_cost <= 0:
        raise ValueError("false_negative_cost doit être un nombre positif fini.")
    if not np.isfinite(false_positive_cost) or false_positive_cost <= 0:
        raise ValueError("false_positive_cost doit être un nombre positif fini.")
    if not truth.any() or truth.all():
        raise ValueError("La validation doit contenir des exemples des deux classes.")

    order = np.argsort(-scores, kind="stable")
    sorted_scores = scores[order]
    sorted_truth = truth[order].astype(bool)
    cumulative_true_positive = np.cumsum(sorted_truth)
    cumulative_false_positive = np.cumsum(~sorted_truth)
    end_of_score_groups = np.r_[
        np.flatnonzero(sorted_scores[:-1] != sorted_scores[1:]),
        len(sorted_scores) - 1,
    ]

    thresholds = np.r_[sorted_scores[end_of_score_groups], np.nextafter(scores.max(), np.inf)]
    true_positives = np.r_[cumulative_true_positive[end_of_score_groups], 0]
    false_positives = np.r_[cumulative_false_positive[end_of_score_groups], 0]
    positives = int(truth.sum())
    false_negatives = positives - true_positives
    costs = false_negatives * false_negative_cost + false_positives * false_positive_cost

    minimum_cost = costs.min()
    best = np.flatnonzero(costs == minimum_cost)
    best_index = best[np.argmax(thresholds[best])]
    return {
        "threshold": float(thresholds[best_index]),
        "validation_cost": float(costs[best_index]),
        "false_positives": int(false_positives[best_index]),
        "false_negatives": int(false_negatives[best_index]),
        "true_positives": int(true_positives[best_index]),
        "true_negatives": int(len(truth) - positives - false_positives[best_index]),
    }


def evaluate_fraud_threshold(y_true, probabilities, *, threshold: float) -> dict[str, int | float]:
    """Calculer la matrice de confusion et les métriques à un seuil fixé."""
    truth = np.asarray(y_true)
    scores = np.asarray(probabilities, dtype=float)
    if truth.ndim != 1 or scores.ndim != 1 or len(truth) != len(scores):
        raise ValueError("y_true et probabilities doivent être des vecteurs de même longueur.")
    if len(truth) == 0 or not np.isin(truth, [0, 1]).all():
        raise ValueError("y_true doit être non vide et contenir uniquement les classes 0 et 1.")
    if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
        raise ValueError("Les probabilités doivent être finies et comprises entre 0 et 1.")
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError("threshold doit être un nombre positif fini.")

    predictions = scores >= threshold
    tn, fp, fn, tp = confusion_matrix(truth, predictions, labels=[0, 1]).ravel()
    return {
        "threshold": float(threshold),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "precision": float(tp / (tp + fp)) if tp + fp else 0.0,
        "recall": float(tp / (tp + fn)) if tp + fn else 0.0,
    }
