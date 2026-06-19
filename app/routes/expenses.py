from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.expense import Expense, Category
from app.ml.anomaly_detector import AnomalyDetector
from datetime import date, datetime

expenses_bp = Blueprint('expenses', __name__)


def get_user_categories():
    """Return default + user-specific categories."""
    return Category.query.filter(
        (Category.user_id == current_user.id) | (Category.user_id == None)
    ).order_by(Category.name).all()


@expenses_bp.route('/')
@login_required
def list_expenses():
    page      = request.args.get('page', 1, type=int)
    per_page  = 20
    category  = request.args.get('category', type=int)
    month     = request.args.get('month', '')
    search    = request.args.get('search', '').strip()
    payment   = request.args.get('payment', '')
    sort      = request.args.get('sort', 'date_desc')

    query = Expense.query.filter_by(user_id=current_user.id)

    if category:
        query = query.filter_by(category_id=category)
    if month:
        try:
            yr, mo = map(int, month.split('-'))
            query = query.filter(
                db.extract('year', Expense.expense_date) == yr,
                db.extract('month', Expense.expense_date) == mo
            )
        except Exception:
            pass
    if search:
        query = query.filter(Expense.description.ilike(f'%{search}%'))
    if payment:
        query = query.filter_by(payment_method=payment)

    sort_map = {
        'date_desc': Expense.expense_date.desc(),
        'date_asc':  Expense.expense_date.asc(),
        'amount_desc': Expense.amount.desc(),
        'amount_asc':  Expense.amount.asc(),
    }
    query = query.order_by(sort_map.get(sort, Expense.expense_date.desc()))

    expenses   = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = get_user_categories()

    return render_template(
        'expenses/list.html',
        expenses=expenses,
        categories=categories,
        filters={'category': category, 'month': month, 'search': search, 'payment': payment, 'sort': sort}
    )


@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    categories = get_user_categories()

    if request.method == 'POST':
        try:
            amount       = float(request.form['amount'])
            category_id  = int(request.form['category_id'])
            description  = request.form.get('description', '').strip()
            expense_date = datetime.strptime(request.form['expense_date'], '%Y-%m-%d').date()
            payment      = request.form.get('payment_method', 'cash')
            note         = request.form.get('note', '').strip()
            tags         = request.form.get('tags', '').strip()
            is_recurring = bool(request.form.get('is_recurring'))
            recurrence   = request.form.get('recurrence') if is_recurring else None

            if amount <= 0:
                flash('Amount must be positive.', 'danger')
                return render_template('expenses/add.html', categories=categories, form_data=request.form)

            expense = Expense(
                user_id=current_user.id,
                category_id=category_id,
                amount=amount,
                description=description,
                expense_date=expense_date,
                payment_method=payment,
                note=note,
                tags=tags,
                is_recurring=is_recurring,
                recurrence=recurrence,
            )

            # Run anomaly detection
            detector = AnomalyDetector(current_user.id)
            expense.is_anomaly = detector.is_anomaly(amount, category_id)

            db.session.add(expense)
            db.session.commit()

            msg = 'Expense added!'
            if expense.is_anomaly:
                msg += ' ⚠️ This looks unusually high for this category.'
            flash(msg, 'success' if not expense.is_anomaly else 'warning')
            return redirect(url_for('expenses.list_expenses'))

        except (ValueError, KeyError) as e:
            flash(f'Invalid input: {str(e)}', 'danger')

    return render_template('expenses/add.html', categories=categories, today=date.today().isoformat())


@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense    = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    categories = get_user_categories()

    if request.method == 'POST':
        try:
            expense.amount        = float(request.form['amount'])
            expense.category_id   = int(request.form['category_id'])
            expense.description   = request.form.get('description', '').strip()
            expense.expense_date  = datetime.strptime(request.form['expense_date'], '%Y-%m-%d').date()
            expense.payment_method = request.form.get('payment_method', 'cash')
            expense.note          = request.form.get('note', '').strip()
            expense.tags          = request.form.get('tags', '').strip()
            expense.is_recurring  = bool(request.form.get('is_recurring'))
            expense.recurrence    = request.form.get('recurrence') if expense.is_recurring else None

            detector = AnomalyDetector(current_user.id)
            expense.is_anomaly = detector.is_anomaly(expense.amount, expense.category_id)

            db.session.commit()
            flash('Expense updated.', 'success')
            return redirect(url_for('expenses.list_expenses'))
        except (ValueError, KeyError) as e:
            flash(f'Invalid input: {str(e)}', 'danger')

    return render_template('expenses/edit.html', expense=expense, categories=categories)


@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('expenses.list_expenses'))


@expenses_bp.route('/category/add', methods=['POST'])
@login_required
def add_category():
    name  = request.form.get('name', '').strip()
    icon  = request.form.get('icon', '💰')
    color = request.form.get('color', '#6366f1')

    if not name:
        flash('Category name is required.', 'danger')
        return redirect(url_for('expenses.list_expenses'))

    cat = Category(user_id=current_user.id, name=name, icon=icon, color=color)
    db.session.add(cat)
    db.session.commit()
    flash(f'Category "{name}" created.', 'success')
    return redirect(request.referrer or url_for('expenses.list_expenses'))