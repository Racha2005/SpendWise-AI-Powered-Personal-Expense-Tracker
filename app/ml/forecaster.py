"""
Expense Forecaster
Algorithm: Linear Regression on monthly totals.
Justification: Captures linear spending trends; fast, interpretable, 
works well with limited data (6-24 months history).
"""
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta
from app.extensions import db
from app.models.expense import Expense
from sqlalchemy import func


class ExpenseForecaster:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def _get_monthly_totals(self) -> list[tuple]:
        """Returns list of (year, month, total) ordered chronologically."""
        rows = (
            db.session.query(
                func.year(Expense.expense_date).label('yr'),
                func.month(Expense.expense_date).label('mo'),
                func.sum(Expense.amount).label('total'),
            )
            .filter_by(user_id=self.user_id)
            .group_by('yr', 'mo')
            .order_by('yr', 'mo')
            .all()
        )
        return [(r.yr, r.mo, float(r.total)) for r in rows]

    def forecast_next_3_months(self) -> dict:
        history = self._get_monthly_totals()

        if len(history) < 3:
            # Not enough data — return simple average
            avg = np.mean([h[2] for h in history]) if history else 0.0
            today = date.today()
            months = []
            for i in range(1, 4):
                d = today + relativedelta(months=i)
                months.append({'label': d.strftime('%b %Y'), 'predicted': round(float(avg), 2), 'confidence': 0.5})
            return {
                'months': months,
                'trend': 'stable',
                'model': 'average',
                'historical_labels': [f"{h[0]}-{h[1]:02d}" for h in history],
                'historical_data':   [h[2] for h in history],
            }

        X = np.arange(len(history)).reshape(-1, 1)
        y = np.array([h[2] for h in history])

        # Simple linear regression (no sklearn dependency required)
        X_flat = X.flatten()
        m = np.polyfit(X_flat, y, 1)
        slope, intercept = m[0], m[1]

        # R² for confidence
        y_pred_hist = slope * X_flat + intercept
        ss_res = np.sum((y - y_pred_hist) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = max(0.0, 1 - ss_res / ss_tot) if ss_tot > 0 else 0.5

        # Forecast
        last_yr, last_mo, _ = history[-1]
        last_date = date(last_yr, last_mo, 1)
        months = []
        for i in range(1, 4):
            future_x = len(history) - 1 + i
            pred = slope * future_x + intercept
            pred = max(0.0, pred)
            d = last_date + relativedelta(months=i)
            months.append({
                'label': d.strftime('%b %Y'),
                'predicted': round(pred, 2),
                'confidence': round(r2, 2),
            })

        trend = 'increasing' if slope > 50 else ('decreasing' if slope < -50 else 'stable')

        return {
            'months':             months,
            'trend':              trend,
            'slope':              round(float(slope), 2),
            'model':              'linear_regression',
            'r2_score':           round(r2, 3),
            'historical_labels':  [f"{h[0]}-{h[1]:02d}" for h in history],
            'historical_data':    [round(h[2], 2) for h in history],
        }
