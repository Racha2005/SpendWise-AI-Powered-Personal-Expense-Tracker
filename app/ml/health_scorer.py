"""
Financial Health Scorer
Algorithm: Weighted Rule Engine (interpretable scoring system).
Justification: End users need to understand WHY they scored X; a black-box
model reduces trust. Weighted rules map directly to financial best practices
(50/30/20 rule, savings rate, budget adherence).
Score: 0-100 (Poor < 40, Fair 40-60, Good 60-80, Excellent > 80)
"""
from datetime import date
from app.extensions import db
from app.models.expense import Expense, Budget
from app.models.user import User
from sqlalchemy import func


class HealthScorer:
    WEIGHTS = {
        'savings_rate':      0.30,
        'budget_adherence':  0.25,
        'spending_stability': 0.20,
        'expense_diversity': 0.15,
        'anomaly_ratio':     0.10,
    }

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user    = User.query.get(user_id)

    def compute(self) -> dict:
        today = date.today()
        scores = {}
        details = {}

        # 1. Savings Rate (income - expenses) / income
        monthly_income = float(self.user.monthly_income or 0)
        current_month_spent = self._month_total(today.year, today.month)

        if monthly_income > 0:
            savings_rate = max(0, (monthly_income - current_month_spent) / monthly_income)
            scores['savings_rate'] = min(100, savings_rate * 200)  # 50% savings = 100 pts
            details['savings_rate'] = f'{savings_rate*100:.1f}% saved this month'
        else:
            scores['savings_rate'] = 50  # neutral if no income set
            details['savings_rate'] = 'Set your monthly income for accurate scoring'

        # 2. Budget Adherence
        budgets = Budget.query.filter_by(
            user_id=self.user_id,
            budget_month=date(today.year, today.month, 1)
        ).all()
        if budgets:
            adherences = []
            for b in budgets:
                spent = self._category_month_total(today.year, today.month, b.category_id)
                limit = float(b.amount)
                adherences.append(min(1.0, spent / limit) if limit > 0 else 0)
            avg_adherence = sum(adherences) / len(adherences)
            scores['budget_adherence'] = max(0, (1 - avg_adherence) * 100)
            details['budget_adherence'] = f'{len([a for a in adherences if a <= 1])}/{len(adherences)} budgets on track'
        else:
            scores['budget_adherence'] = 60
            details['budget_adherence'] = 'No budgets set — consider setting monthly budgets'

        # 3. Spending Stability (low variance = stable)
        monthly_totals = self._last_n_months_totals(6)
        if len(monthly_totals) >= 3:
            import numpy as np
            cv = (np.std(monthly_totals) / np.mean(monthly_totals)) if np.mean(monthly_totals) > 0 else 0
            scores['spending_stability'] = max(0, 100 - cv * 100)
            details['spending_stability'] = f'Coefficient of variation: {cv*100:.1f}%'
        else:
            scores['spending_stability'] = 70
            details['spending_stability'] = 'Need 3+ months of data'

        # 4. Expense Diversity (entropy — spending across many categories)
        cat_totals = self._category_totals_this_month(today.year, today.month)
        if cat_totals:
            import numpy as np
            total = sum(cat_totals)
            probs = [c / total for c in cat_totals]
            entropy = -sum(p * __import__('math').log2(p) for p in probs if p > 0)
            max_entropy = __import__('math').log2(max(len(cat_totals), 1))
            diversity = entropy / max_entropy if max_entropy > 0 else 0
            scores['expense_diversity'] = diversity * 100
            details['expense_diversity'] = f'Spending across {len(cat_totals)} categories'
        else:
            scores['expense_diversity'] = 50
            details['expense_diversity'] = 'No expenses this month'

        # 5. Anomaly Ratio
        total_expenses = Expense.query.filter_by(user_id=self.user_id).count()
        anomaly_count  = Expense.query.filter_by(user_id=self.user_id, is_anomaly=True).count()
        if total_expenses > 0:
            anomaly_ratio = anomaly_count / total_expenses
            scores['anomaly_ratio'] = max(0, 100 - anomaly_ratio * 500)
            details['anomaly_ratio'] = f'{anomaly_count} anomalous expenses detected'
        else:
            scores['anomaly_ratio'] = 100
            details['anomaly_ratio'] = 'No anomalies detected'

        # Weighted total
        total_score = sum(scores[k] * v for k, v in self.WEIGHTS.items())
        total_score = round(total_score, 1)

        grade = 'Excellent' if total_score >= 80 else \
                'Good'      if total_score >= 60 else \
                'Fair'      if total_score >= 40 else 'Poor'

        color = '#22c55e' if total_score >= 80 else \
                '#84cc16' if total_score >= 60 else \
                '#f59e0b' if total_score >= 40 else '#ef4444'

        return {
            'score':   total_score,
            'grade':   grade,
            'color':   color,
            'scores':  {k: round(v, 1) for k, v in scores.items()},
            'details': details,
            'weights': self.WEIGHTS,
        }

    def _month_total(self, year, month):
        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == self.user_id,
            db.extract('year', Expense.expense_date) == year,
            db.extract('month', Expense.expense_date) == month
        ).scalar()
        return float(result or 0)

    def _category_month_total(self, year, month, category_id):
        query = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == self.user_id,
            db.extract('year', Expense.expense_date) == year,
            db.extract('month', Expense.expense_date) == month,
        )
        if category_id:
            query = query.filter(Expense.category_id == category_id)
        return float(query.scalar() or 0)

    def _last_n_months_totals(self, n: int) -> list:
        rows = (
            db.session.query(func.sum(Expense.amount))
            .filter_by(user_id=self.user_id)
            .group_by(
                db.extract('year', Expense.expense_date),
                db.extract('month', Expense.expense_date)
            )
            .order_by(
                db.extract('year', Expense.expense_date).desc(),
                db.extract('month', Expense.expense_date).desc()
            )
            .limit(n).all()
        )
        return [float(r[0]) for r in rows]

    def _category_totals_this_month(self, year, month) -> list:
        rows = (
            db.session.query(func.sum(Expense.amount))
            .filter(
                Expense.user_id == self.user_id,
                db.extract('year', Expense.expense_date) == year,
                db.extract('month', Expense.expense_date) == month,
            )
            .group_by(Expense.category_id).all()
        )
        return [float(r[0]) for r in rows]
