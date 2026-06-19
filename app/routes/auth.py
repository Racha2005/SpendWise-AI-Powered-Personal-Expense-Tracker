from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username  = request.form.get('username', '').strip()
        email     = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        password  = request.form.get('password', '')
        confirm   = request.form.get('confirm_password', '')
        currency  = request.form.get('currency', 'INR')

        # Validation
        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken.')
        if not email or '@' not in email:
            errors.append('Valid email is required.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html', form_data=request.form)

        user = User(username=username, email=email, full_name=full_name, currency=currency)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Account created! Welcome to SpendWise.', 'success')
        login_user(user)
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password   = request.form.get('password', '')
        remember   = bool(request.form.get('remember'))

        user = User.query.filter(
            (User.email == identifier.lower()) | (User.username == identifier)
        ).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            user.update_last_login()
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.display_name}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))

        flash('Invalid credentials. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.currency  = request.form.get('currency', 'INR')
        current_user.monthly_income = float(request.form.get('monthly_income', 0) or 0)
        current_user.theme     = request.form.get('theme', 'light')

        new_password = request.form.get('new_password', '')
        if new_password:
            current_password = request.form.get('current_password', '')
            if not current_user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('auth.profile'))
            if len(new_password) < 8:
                flash('New password must be at least 8 characters.', 'danger')
                return redirect(url_for('auth.profile'))
            current_user.set_password(new_password)

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile/index.html')
