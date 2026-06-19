from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(50), unique=True, nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password_hash  = db.Column(db.String(255), nullable=False)
    full_name      = db.Column(db.String(100))
    currency       = db.Column(db.String(3), default='INR')
    monthly_income = db.Column(db.Numeric(12, 2), default=0.00)
    avatar_url     = db.Column(db.String(255))
    theme          = db.Column(db.Enum('light', 'dark'), default='light')
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login     = db.Column(db.DateTime)

    # Relationships
    expenses    = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    budgets     = db.relationship('Budget', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    categories  = db.relationship('Category', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    @property
    def display_name(self):
        return self.full_name or self.username

    @property
    def currency_symbol(self):
        symbols = {'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
        return symbols.get(self.currency, self.currency)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
