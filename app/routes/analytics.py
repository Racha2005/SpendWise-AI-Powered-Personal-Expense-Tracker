from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService
from app.ml.forecaster import ExpenseForecaster
from app.ml.recommender import FinancialRecommender
from app.ml.health_scorer import HealthScorer
from datetime import date

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def index():
    today = date.today()
    year  = request.args.get('year', today.year, type=int)

    analytics = AnalyticsService(current_user.id)

    # All analytics data
    monthly_trend   = analytics.get_monthly_trend(year)
    category_split  = analytics.get_category_split(year)
    weekly_pattern  = analytics.get_weekly_pattern(year)
    yoy_comparison  = analytics.get_yoy_comparison(year)
    payment_methods = analytics.get_payment_method_split(year)
    top_expenses    = analytics.get_top_expenses(year, limit=10)

    # ML features
    forecaster   = ExpenseForecaster(current_user.id)
    forecast     = forecaster.forecast_next_3_months()

    recommender  = FinancialRecommender(current_user.id)
    tips         = recommender.get_recommendations()

    scorer       = HealthScorer(current_user.id)
    health       = scorer.compute()

    return render_template(
        'analytics/index.html',
        monthly_trend=monthly_trend,
        category_split=category_split,
        weekly_pattern=weekly_pattern,
        yoy_comparison=yoy_comparison,
        payment_methods=payment_methods,
        top_expenses=top_expenses,
        forecast=forecast,
        tips=tips,
        health=health,
        selected_year=year,
        today=today,
    )