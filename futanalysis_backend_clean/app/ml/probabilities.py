# futanalysis_backend_clean/app/ml/probabilities.py

import numpy as np
from typing import Dict


def softmax(scores: np.ndarray) -> np.ndarray:
    """
    Softmax numericamente estável.
    """
    scores = scores.astype(float)
    max_score = np.max(scores)
    exp_scores = np.exp(scores - max_score)
    return exp_scores / np.sum(exp_scores)


def scores_to_probabilities(raw_scores: Dict[str, float]) -> Dict[str, float]:
    """
    Converte scores brutos do modelo em probabilidades (%).
    """

    labels = list(raw_scores.keys())
    values = np.array(list(raw_scores.values()))

    probabilities = softmax(values) * 100

    return {
        label: round(prob, 2)
        for label, prob in zip(labels, probabilities)
    }
