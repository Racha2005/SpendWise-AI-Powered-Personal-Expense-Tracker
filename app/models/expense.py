from datetime import datetime
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    name       = db.Column(db.String(60), nullable=False)
    icon       = db.Column(db.String(10), default='💰')
    color      = db.Column(db.String(7), default='#6366f1')
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    expenses   = db.relationship('Expense', backref='category', lazy='dynamic')
    budgets    = db.relationship('Budget', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name,
            'icon': self.icon, 'color': self.color
        }

    def __repr__(self):
        return f'<Category {self.name}>'


class Expense(db.Model):
    __tablename__ = 'expenses'

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id    = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)
    amount         = db.Column(db.Numeric(12, 2), nullable=False)
    description    = db.Column(db.String(255))
    note           = db.Column(db.Text)
    expense_date   = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Enum('cash','card','upi','netbanking','wallet','other'), default='cash')
    is_recurring   = db.Column(db.Boolean, default=False)
    recurrence     = db.Column(db.Enum('daily','weekly','monthly','yearly'), nullable=True)
    tags           = db.Column(db.String(255))
    receipt_url    = db.Column(db.String(255))
    is_anomaly     = db.Column(db.Boolean, default=False)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'description': self.description,
            'expense_date': self.expense_date.isoformat(),
            'category': self.category.to_dict() if self.category else None,
            'payment_method': self.payment_method,
            'is_anomaly': self.is_anomaly,
            'tags': self.tags,
        }

    def __repr__(self):
        return f'<Expense {self.amount} on {self.expense_date}>'


class Budget(db.Model):
    __tablename__ = 'budgets'

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id   = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    budget_month  = db.Column(db.Date, nullable=False)
    amount        = db.Column(db.Numeric(12, 2), nullable=False)
    alert_percent = db.Column(db.Integer, default=80)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'budget_month': self.budget_month.isoformat(),
            'category': self.category.to_dict() if self.category else None,
            'alert_percent': self.alert_percent,
        }
