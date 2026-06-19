"""
Anomaly Detector
Algorithm: IQR (Interquartile Range) method per category.
Justification: Works well with small, non-labeled datasets; no training required;
fast inference. Falls back to Z-score if insufficient data.
For larger datasets (1000+ expenses), Isolation Forest is preferred.
"""
import numpy as np
from app.extensions import db
from app.models.expense import Expense
from sqlalchemy import func


class AnomalyDetector:
    IQR_MULTIPLIER = 2.0  # more lenient than standard 1.5

    def __init__(self, user_id: int):
        self.user_id = user_id
        self._cache: dict[int, list[float]] = {}

    def _get_category_amounts(self, category_id: int) -> list[float]:
        if category_id in self._cache:
            return self._cache[category_id]
        rows = (
            db.session.query(Expense.amount)
            .filter_by(user_id=self.user_id, category_id=category_id)
            .all()
        )
        amounts = [float(r[0]) for r in rows]
        self._cache[category_id] = amounts
        return amounts

    def is_anomaly(self, amount: float, category_id: int) -> bool:
        amounts = self._get_category_amounts(category_id)
        if len(amounts) < 5:
            return False  # not enough history

        arr = np.array(amounts)
        q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
        iqr = q3 - q1

        if iqr == 0:
            # Fallback: Z-score
            mean, std = np.mean(arr), np.std(arr)
            return bool(std > 0 and abs(amount - mean) / std > 3)

        upper = q3 + self.IQR_MULTIPLIER * iqr
        return amount > upper

    def get_anomaly_score(self, amount: float, category_id: int) -> float:
        """Returns how many IQRs above the upper fence this amount is (0 = normal)."""
        amounts = self._get_category_amounts(category_id)
        if len(amounts) < 5:
            return 0.0
        arr = np.array(amounts)
        q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
        iqr = q3 - q1
        upper = q3 + self.IQR_MULTIPLIER * iqr
        return max(0.0, float((amount - upper) / iqr)) if iqr > 0 else 0.0
