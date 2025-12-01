from __future__ import annotations

import math
import random
from statistics import mean, stdev
from typing import Iterable, List, Sequence, Tuple


class IForest:
    """Implementación ligera que emula la API de PyOD Isolation Forest.

    La lógica usa estadísticos simples para puntuar cuentas con muchas
    transacciones recientes y montos promedio bajos.
    """

    def __init__(self, contamination: float = 0.01, random_state: int | None = None) -> None:
        self.contamination = contamination
        self.random_state = random_state or 42
        self._rng = random.Random(self.random_state)
        self.decision_scores_: List[float] = []
        self.labels_: List[int] = []

    def fit(self, X: Sequence[Tuple[float, float]]) -> "IForest":
        counts = [row[0] for row in X]
        avgs = [row[1] for row in X]
        count_std = stdev(counts) if len(counts) > 1 else 1.0
        avg_std = stdev(avgs) if len(avgs) > 1 else 1.0
        count_mean = mean(counts) if counts else 0.0
        avg_mean = mean(avgs) if avgs else 0.0

        scores: List[float] = []
        for count, avg in X:
            count_z = (count - count_mean) / count_std if count_std else 0.0
            avg_z = (avg_mean - avg) / avg_std if avg_std else 0.0
            scores.append((2 * count_z) + avg_z)

        self.decision_scores_ = scores
        threshold_index = max(1, int(math.ceil(len(scores) * (1 - self.contamination))))
        sorted_scores = sorted(scores, reverse=True)
        threshold_value = sorted_scores[threshold_index - 1]
        self.labels_ = [int(score >= threshold_value) for score in scores]
        return self

    def decision_function(self, X: Sequence[Tuple[float, float]] | None = None) -> List[float]:
        return self.decision_scores_

    def predict(self, X: Sequence[Tuple[float, float]] | None = None) -> List[int]:
        return self.labels_
