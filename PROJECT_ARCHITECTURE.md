# SpendWise — AI-Powered Personal Expense Tracker
## Project Architecture

```
spendwise/
├── app/
│   ├── __init__.py                 # Flask application factory
│   ├── extensions.py               # Database, login manager initialization
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── expense.py              # Expense model
│   │   ├── category.py             # Category model
│   │   ├── budget.py               # Budget model
│   │   ├── ml_prediction.py        # Stores ML outputs
│   │   └── audit_log.py            # Activity logs
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── dashboard.py            # Main dashboard
│   │   ├── expenses.py             # Expense CRUD operations
│   │   ├── budget.py               # Budget management
│   │   ├── analytics.py            # Analytics routes
│   │   └── api.py                  # API endpoints
│   │
│   ├── services/
│   │   └── analytics_service.py    # Data analysis logic
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── forecaster.py           # Expense forecasting
│   │   ├── anomaly_detector.py     # Anomaly detection
│   │   ├── health_scorer.py        # Financial health scoring
│   │   └── recommender.py          # Savings recommendations
│   │
│   └── utils/
│       └── helpers.py              # Utility/helper functions
│
├── static/
│   ├── css/
│   │   └── main.css                # Main glassmorphism UI styling
│   │
│   ├── js/
│   │   ├── charts.js               # Chart rendering logic
│   │   └── dashboard.js            # Dashboard interactivity
│   │
│   ├── uploads/                    # Future receipt uploads
│   │
│   └── powerbi dashboard/
│       ├── SpendWise_Dashboard.pbix
│       └── SpendWise_Dashboard.pdf
│
├── templates/
│   ├── base.html                   # Master layout
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── dashboard/
│   │   └── index.html
│   │
│   ├── expenses/
│   │   ├── add.html
│   │   ├── edit.html
│   │   └── list.html
│   │
│   ├── budget/
│   │   └── index.html
│   │
│   ├── analytics/
│   │   └── index.html
│   │
│   └── profile/
│       └── index.html
│
├── database/
│   └── schema.sql                  # MySQL database schema
│
├── .env                            # Environment variables
├── .env.example                    # Sample environment file
├── config.py                       # Application configuration
├── run.py                          # Entry point
├── requirements.txt                # Dependencies
├── README.md                       # Project introduction
├── HOW_TO_RUN.md                   # Setup guide
├── PROJECT_DETAILS.md              # Full documentation
└── PROJECT_ARCHITECTURE.md         # Architecture documentation
```

## Database: spendwise_db

### Tables

- users — user accounts and profiles
- categories — expense categories
- expenses — expense transactions
- budgets — monthly/category budgets
- ml_predictions — AI/ML prediction outputs
- audit_log — user activity logs


## ML Algorithm Choices

| Feature | Algorithm | Justification |
|---|---|---|
| Expense Forecasting | Linear Regression | Predicts next 3 months based on spending trend |
| Anomaly Detection | IQR Statistical Method | Detects unusual spending using quartile ranges |
| Financial Health Score | Weighted Rule Engine | Calculates interpretable financial score |
| Personalized Recommendations | Rule-Based Benchmark Engine | Uses benchmark spending patterns like 50/30/20 |

## Frontend UI Architecture

Design Style:
- Dark theme
- Glassmorphism UI
- Fintech-inspired layout
- Responsive dashboard design

UI Components:
- Authentication pages
- Dashboard page
- Expense pages
- Budget page
- Analytics page
- Profile page

Client-side Features:
- Dynamic Chart.js rendering
- Interactive dashboard updates
- Budget progress bars
- Theme customization
- Real-time filtering
