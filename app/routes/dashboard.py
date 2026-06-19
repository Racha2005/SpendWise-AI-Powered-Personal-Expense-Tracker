from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService
from app.ml.health_scorer import HealthScorer
from app.ml.forecaster import ExpenseForecaster
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    analytics = AnalyticsService(current_user.id)
    today = date.today()

    # KPI data
    kpis = analytics.get_monthly_kpis(today.year, today.month)

    # Health score
    scorer = HealthScorer(current_user.id)
    health = scorer.compute()

    # Recent expenses (last 10)
    from app.models.expense import Expense
    recent_expenses = (
        Expense.query
        .filter_by(user_id=current_user.id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .limit(10).all()
    )

    # Budget overview
    budget_overview = analytics.get_budget_overview(today.year, today.month)

    # Anomaly count this month
    anomaly_count = (
        Expense.query
        .filter_by(user_id=current_user.id, is_anomaly=True)
        .filter(
            Expense.expense_date >= date(today.year, today.month, 1)
        ).count()
    )

    return render_template(
        'dashboard/index.html',
        kpis=kpis,
        health=health,
        recent_expenses=recent_expenses,
        budget_overview=budget_overview,
        anomaly_count=anomaly_count,
        today=today,
    )
