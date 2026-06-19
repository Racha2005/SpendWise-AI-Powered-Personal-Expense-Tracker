from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService
from app.ml.forecaster import ExpenseForecaster
from app.ml.health_scorer import HealthScorer
from app.models.expense import Category
from datetime import date

api_bp = Blueprint('api', __name__)


@api_bp.route('/chart/monthly-trend')
@login_required
def monthly_trend():
    year = request.args.get('year', date.today().year, type=int)
    analytics = AnalyticsService(current_user.id)
    data = analytics.get_monthly_trend(year)
    return jsonify(data)


@api_bp.route('/chart/category-split')
@login_required
def category_split():
    year  = request.args.get('year',  date.today().year,  type=int)
    month = request.args.get('month', date.today().month, type=int)
    analytics = AnalyticsService(current_user.id)
    data = analytics.get_category_split(year, month)
    return jsonify(data)


@api_bp.route('/chart/weekly-pattern')
@login_required
def weekly_pattern():
    year = request.args.get('year', date.today().year, type=int)
    analytics = AnalyticsService(current_user.id)
    data = analytics.get_weekly_pattern(year)
    return jsonify(data)


@api_bp.route('/chart/forecast')
@login_required
def forecast():
    forecaster = ExpenseForecaster(current_user.id)
    data = forecaster.forecast_next_3_months()
    return jsonify(data)


@api_bp.route('/health-score')
@login_required
def health_score():
    scorer = HealthScorer(current_user.id)
    return jsonify(scorer.compute())


@api_bp.route('/categories')
@login_required
def categories():
    cats = Category.query.filter(
        (Category.user_id == current_user.id) | (Category.user_id == None)
    ).all()
    return jsonify([c.to_dict() for c in cats])


@api_bp.route('/kpis')
@login_required
def kpis():
    today = date.today()
    analytics = AnalyticsService(current_user.id)
    return jsonify(analytics.get_monthly_kpis(today.year, today.month))
