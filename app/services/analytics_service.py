import pandas as pd
import numpy as np
from datetime import date, timedelta
from app.extensions import db
from app.models.expense import Expense, Category, Budget
from sqlalchemy import func


class AnalyticsService:
    """Core analytics using Pandas and NumPy."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def _fetch_expenses_df(self, year: int = None, month: int = None) -> pd.DataFrame:
        """Fetch all user expenses as a DataFrame."""
        query = (
            db.session.query(
                Expense.amount,
                Expense.expense_date,
                Expense.payment_method,
                Expense.is_anomaly,
                Category.name.label('category_name'),
                Category.color.label('category_color'),
                Category.id.label('category_id'),
            )
            .join(Category, Expense.category_id == Category.id)
            .filter(Expense.user_id == self.user_id)
        )
        if year:
            query = query.filter(db.extract('year', Expense.expense_date) == year)
        if month:
            query = query.filter(db.extract('month', Expense.expense_date) == month)

        rows = query.all()
        if not rows:
            return pd.DataFrame(columns=['amount','expense_date','payment_method',
                                         'is_anomaly','category_name','category_color','category_id'])

        df = pd.DataFrame(rows, columns=['amount','expense_date','payment_method',
                                          'is_anomaly','category_name','category_color','category_id'])
        df['amount'] = df['amount'].astype(float)
        df['expense_date'] = pd.to_datetime(df['expense_date'])
        df['month'] = df['expense_date'].dt.to_period('M')
        df['week']  = df['expense_date'].dt.day_name()
        return df

    def get_monthly_kpis(self, year: int, month: int) -> dict:
        df      = self._fetch_expenses_df(year, month)
        df_prev = self._fetch_expenses_df(year, month - 1 if month > 1 else 12)

        curr_total = float(df['amount'].sum()) if not df.empty else 0.0
        prev_total = float(df_prev['amount'].sum()) if not df_prev.empty else 0.0
        change_pct = ((curr_total - prev_total) / prev_total * 100) if prev_total > 0 else 0.0

        avg_daily = float(df['amount'].mean()) if not df.empty else 0.0
        txn_count = len(df)
        top_cat   = df.groupby('category_name')['amount'].sum().idxmax() if not df.empty else 'N/A'

        return {
            'total_spent':    round(curr_total, 2),
            'prev_total':     round(prev_total, 2),
            'change_pct':     round(change_pct, 1),
            'avg_transaction': round(avg_daily, 2),
            'transaction_count': txn_count,
            'top_category':   top_cat,
        }

    def get_monthly_trend(self, year: int) -> dict:
        df = self._fetch_expenses_df(year)
        if df.empty:
            months = [f'{year}-{m:02d}' for m in range(1, 13)]
            return {'labels': months, 'data': [0] * 12}

        monthly = df.groupby(df['expense_date'].dt.month)['amount'].sum()
        months  = [f'{year}-{m:02d}' for m in range(1, 13)]
        values  = [round(float(monthly.get(m, 0)), 2) for m in range(1, 13)]
        return {'labels': months, 'data': values}

    def get_category_split(self, year: int, month: int = None) -> dict:
        df = self._fetch_expenses_df(year, month)
        if df.empty:
            return {'labels': [], 'data': [], 'colors': []}

        grouped = df.groupby(['category_name', 'category_color'])['amount'].sum().reset_index()
        grouped = grouped.sort_values('amount', ascending=False)
        return {
            'labels': grouped['category_name'].tolist(),
            'data':   [round(float(x), 2) for x in grouped['amount'].tolist()],
            'colors': grouped['category_color'].tolist(),
        }

    def get_weekly_pattern(self, year: int) -> dict:
        df = self._fetch_expenses_df(year)
        if df.empty:
            days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            return {'labels': days, 'data': [0]*7}

        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        df['day_name'] = df['expense_date'].dt.day_name()
        weekly = df.groupby('day_name')['amount'].mean().reindex(day_order, fill_value=0)
        return {
            'labels': day_order,
            'data':   [round(float(v), 2) for v in weekly.values],
        }

    def get_yoy_comparison(self, year: int) -> dict:
        df_curr = self._fetch_expenses_df(year)
        df_prev = self._fetch_expenses_df(year - 1)

        months = [f'M{m:02d}' for m in range(1, 13)]

        def monthly_totals(df):
            if df.empty:
                return [0] * 12
            m = df.groupby(df['expense_date'].dt.month)['amount'].sum()
            return [round(float(m.get(i, 0)), 2) for i in range(1, 13)]

        return {
            'labels':   months,
            'current':  monthly_totals(df_curr),
            'previous': monthly_totals(df_prev),
        }

    def get_payment_method_split(self, year: int) -> dict:
        df = self._fetch_expenses_df(year)
        if df.empty:
            return {'labels': [], 'data': []}

        split = df.groupby('payment_method')['amount'].sum().sort_values(ascending=False)
        return {
            'labels': split.index.tolist(),
            'data':   [round(float(v), 2) for v in split.values],
        }

    def get_top_expenses(self, year: int, limit: int = 10) -> list:
        df = self._fetch_expenses_df(year)
        if df.empty:
            return []
        top = df.nlargest(limit, 'amount')
        return top[['amount','category_name','expense_date']].to_dict(orient='records')

    def get_budget_overview(self, year: int, month: int) -> list:
        """Compare budgets vs actual spending for the month."""
        month_dt = date(year, month, 1)
        budgets  = Budget.query.filter_by(user_id=self.user_id, budget_month=month_dt).all()
        df       = self._fetch_expenses_df(year, month)

        overview = []
        for budget in budgets:
            if budget.category_id:
                spent = float(
                    df[df['category_id'] == budget.category_id]['amount'].sum()
                ) if not df.empty else 0.0
                cat_name = budget.category.name if budget.category else 'Unknown'
                cat_icon = budget.category.icon if budget.category else '💰'
            else:
                spent    = float(df['amount'].sum()) if not df.empty else 0.0
                cat_name = 'Overall'
                cat_icon = '📊'

            limit  = float(budget.amount)
            pct    = round((spent / limit * 100) if limit > 0 else 0, 1)
            status = 'danger' if pct >= 100 else ('warning' if pct >= budget.alert_percent else 'success')

            overview.append({
                'budget_id':   budget.id,
                'category':    cat_name,
                'icon':        cat_icon,
                'budget':      limit,
                'spent':       round(spent, 2),
                'remaining':   round(limit - spent, 2),
                'percent':     pct,
                'status':      status,
                'alert_pct':   budget.alert_percent,
            })

        return sorted(overview, key=lambda x: x['percent'], reverse=True)
