# SpendWise — Setup & Run Guide

## Prerequisites

* Python 3.11+
* MySQL 8.0+
* Power BI Desktop (for BI dashboard)
* MySQL ODBC Connector (for Power BI integration)

---

## Step 1 — Clone / Download Project

Place the `spendwise/` folder anywhere on your system.

Example:

```bash
C:\Users\DELL\Downloads\spendwise_project\spendwise
```

---

## Step 2 — Create Virtual Environment

```bash
cd spendwise
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Setup MySQL Database

Open MySQL Shell / Workbench:

```sql
SOURCE database/schema.sql;
```

Or use:

```bash
mysql -u root -p < database/schema.sql
```

This creates:

* `spendwise_db`
* All required tables
* Default categories

---

## Step 5 — Configure Environment Variables

Create `.env` file:

```bash
copy .env.example .env
```

Edit:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DEV_DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3307/spendwise_db
```

**Important:**
Use your actual MySQL port.
(Default may be 3306, mine is 3307.)

---

## Step 6 — Run the Application

```bash
python run.py
```

Application runs at:

```text
http://localhost:5000
```

---

## Step 7 — Power BI Dashboard Setup

Open:

```text
SpendWise_Dashboard.pbix
```

Connect:

```text
MySQL Database → spendwise_db
```

Load tables:

* users
* expenses
* categories
* budgets
* ml_predictions
* audit_log

Refresh data.

Use slicers:

* User
* Category
* Date

---

## Project Structure (Quick Reference)

```text
spendwise/
├── app/                  # Flask application package
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # Route handlers
│   ├── services/         # Analytics services
│   ├── ml/               # AI/ML modules
│   └── utils/            # Helper functions
│
├── static/
│   ├── css/              # UI styling
│   ├── js/               # Chart.js scripts
│   ├── uploads/          # Future receipt uploads
│   └── powerbi dashboard/# Power BI files
│
├── templates/            # Jinja2 templates
├── database/schema.sql   # Database schema
├── config.py             # Configuration
├── run.py                # Entry point
└── requirements.txt      # Dependencies
```

---

## ML Modules Summary

| Module                | Algorithm                   | Purpose                        |
| --------------------- | --------------------------- | ------------------------------ |
| `forecaster.py`       | Linear Regression           | Predict next 3 months expenses |
| `anomaly_detector.py` | IQR Statistical Method      | Detect unusual expenses        |
| `health_scorer.py`    | Weighted Rule Engine        | Generate 0–100 financial score |
| `recommender.py`      | Rule-Based Benchmark Engine | Personalized savings tips      |

---

## Default Categories (Auto Seeded)

* Food
* Transport
* Housing
* Healthcare
* Entertainment
* Shopping
* Education
* Utilities
* Travel
* Savings
* Investments
* Personal Care
* Subscriptions
* Gifts
* Other

---

## Tech Stack Used

| Layer                 | Technology                                   |
| --------------------- | -------------------------------------------- |
| Frontend              | HTML5, CSS3, Bootstrap, JavaScript, Chart.js |
| Backend               | Python 3, Flask 3                            |
| Database              | MySQL 8, SQLAlchemy, PyMySQL                 |
| Authentication        | Flask-Login, Flask-Bcrypt                    |
| Data Analysis         | Pandas, NumPy                                |
| Machine Learning      | Linear Regression, IQR, Rule Engine          |
| Business Intelligence | Power BI Desktop                             |
| Connector             | MySQL ODBC Connector                         |
| Migrations            | Flask-Migrate                                |

---

## Key Features

* Expense Tracking
* Budget Monitoring
* AI Expense Forecasting
* Anomaly Detection
* Financial Health Score
* Personalized Recommendations
* Analytics Dashboard
* Power BI Dashboard
* Interactive Charts
* Multi-user support

---