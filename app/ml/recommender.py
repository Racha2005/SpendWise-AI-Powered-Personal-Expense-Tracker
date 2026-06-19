"""
Financial Recommender
Algorithm: Rule-based engine with spending pattern analysis.
Generates personalized tips based on category spending vs benchmarks.
"""
from datetime import date
from app.extensions import db
from app.models.expense import Expense, Category
from sqlalchemy import func


BENCHMARKS = {
    'Food & Dining':    0.15,
    'Transportation':   0.10,
    'Housing':          0.30,
    'Entertainment':    0.05,
    'Shopping':         0.10,
    'Healthcare':       0.05,
    'Subscriptions':    0.03,
}

TIPS_LIBRARY = {
    'Food & Dining':   ['Try meal prepping on weekends to cut dining costs by 30%.', 'Track grocery vs restaurant spend — restaurants often cost 3x more per meal.'],
    'Transportation':  ['Consider carpooling or public transit for daily commute savings.', 'Compare monthly transit pass vs per-trip costs.'],
    'Entertainment':   ['Audit streaming subscriptions — cancel ones used less than once/week.', 'Look for free local events and activities.'],
    'Shopping':        ['Implement a 48-hour rule before non-essential purchases.', 'Use cashback apps to earn back on regular shopping.'],
    'Subscriptions':   ['Review all subscriptions annually — the average person forgets 2-3 active ones.'],
}


class FinancialRecommender:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_recommendations(self) -> list:
        today = date.today()
        tips  = []

        # Get this month's spending by category
        rows = (
            db.session.query(
                Category.name,
                func.sum(Expense.amount).label('total')
            )
            .join(Category, Expense.category_id == Category.id)
            .filter(
                Expense.user_id == self.user_id,
                db.extract('year',  Expense.expense_date) == today.year,
                db.extract('month', Expense.expense_date) == today.month,
            )
            .group_by(Category.name).all()
        )

        total_spent = sum(float(r.total) for r in rows)
        if total_spent == 0:
            return [{'type': 'info', 'title': 'Start Tracking', 'message': 'Add your first expense to get personalized recommendations.', 'icon': '💡'}]

        for row in rows:
            cat_name = row.name
            cat_pct  = float(row.total) / total_spent
            benchmark = BENCHMARKS.get(cat_name)

            if benchmark and cat_pct > benchmark * 1.3:
                import random
                cat_tips = TIPS_LIBRARY.get(cat_name, [])
                tip_text = random.choice(cat_tips) if cat_tips else f'Your {cat_name} spending is {cat_pct*100:.0f}% of total — consider reviewing.'
                tips.append({
                    'type':    'warning',
                    'title':   f'High {cat_name} Spend',
                    'message': tip_text,
                    'icon':    '⚠️',
                    'category': cat_name,
                    'actual_pct':    round(cat_pct * 100, 1),
                    'benchmark_pct': round(benchmark * 100, 1),
                })

        # Savings tip
        from app.models.user import User
        user = User.query.get(self.user_id)
        if user and float(user.monthly_income or 0) > 0:
            income  = float(user.monthly_income)
            savings = income - total_spent
            rate    = savings / income
            if rate < 0.2:
                tips.append({
                    'type': 'danger', 'title': 'Low Savings Rate',
                    'message': f'You\'re saving {rate*100:.1f}% this month. Aim for at least 20% (₹{income*0.2:,.0f}).',
                    'icon': '💰'
                })
            elif rate >= 0.3:
                tips.append({
                    'type': 'success', 'title': 'Great Savings!',
                    'message': f'You\'re saving {rate*100:.1f}% — consider investing the surplus for better returns.',
                    'icon': '🎯'
                })

        if not tips:
            tips.append({'type': 'success', 'title': 'On Track!', 'message': 'Your spending looks balanced this month. Keep it up!', 'icon': '✅'})

        return tips[:5]
