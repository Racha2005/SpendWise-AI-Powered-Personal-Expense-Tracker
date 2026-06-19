from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.expense import Budget, Category, Expense
from app.services.analytics_service import AnalyticsService
from datetime import date, datetime

budget_bp = Blueprint('budget', __name__)


@budget_bp.route('/')
@login_required
def index():
    today    = date.today()
    year     = request.args.get('year', today.year, type=int)
    month    = request.args.get('month', today.month, type=int)
    month_dt = date(year, month, 1)

    budgets = Budget.query.filter_by(user_id=current_user.id, budget_month=month_dt).all()

    analytics = AnalyticsService(current_user.id)
    budget_overview = analytics.get_budget_overview(year, month)

    categories = Category.query.filter(
        (Category.user_id == current_user.id) | (Category.user_id == None)
    ).order_by(Category.name).all()

    return render_template(
        'budget/index.html',
        budgets=budgets,
        budget_overview=budget_overview,
        categories=categories,
        selected_year=year,
        selected_month=month,
        today=today,
    )


@budget_bp.route('/set', methods=['POST'])
@login_required
def set_budget():
    category_id   = request.form.get('category_id', type=int)
    amount        = float(request.form.get('amount', 0))
    alert_percent = int(request.form.get('alert_percent', 80))
    month_str     = request.form.get('budget_month', '')

    try:
        budget_month = datetime.strptime(month_str, '%Y-%m').date().replace(day=1)
    except ValueError:
        today = date.today()
        budget_month = date(today.year, today.month, 1)

    existing = Budget.query.filter_by(
        user_id=current_user.id,
        category_id=category_id,
        budget_month=budget_month
    ).first()

    if existing:
        existing.amount = amount
        existing.alert_percent = alert_percent
        flash('Budget updated.', 'success')
    else:
        budget = Budget(
            user_id=current_user.id,
            category_id=category_id,
            budget_month=budget_month,
            amount=amount,
            alert_percent=alert_percent,
        )
        db.session.add(budget)
        flash('Budget set successfully.', 'success')

    db.session.commit()
    return redirect(url_for('budget.index'))


@budget_bp.route('/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first_or_404()
    db.session.delete(budget)
    db.session.commit()
    flash('Budget removed.', 'success')
    return redirect(url_for('budget.index'))