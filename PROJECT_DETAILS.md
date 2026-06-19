# **SpendWise — AI-Powered Personal Expense Tracker - Project Details**

---

# **1. Abstract**

SpendWise is a full-stack, AI-powered personal expense tracking web application designed to simplify personal financial management by combining transactional expense tracking, machine learning, and business intelligence analytics into one unified platform.

Built using Flask (Python) with a MySQL relational database, the system enables users to securely record expenses, manage budgets, analyze spending patterns, and receive intelligent financial insights.

SpendWise integrates advanced AI/ML features such as **3-month expense forecasting** using Linear Regression, **anomaly detection** using the IQR statistical method, **financial health scoring** using a weighted rule engine, and **personalized recommendations** based on spending benchmarks.

The application uses a modern dark-themed **glassmorphism fintech UI** built with HTML, CSS3, Bootstrap, JavaScript, and Chart.js. To enhance analytical capabilities, the same MySQL database is connected to **Power BI** using MySQL ODBC, allowing advanced interactive dashboards with slicers, treemaps, waterfalls, KPI cards, and comparative charts.

This creates a complete finance analytics ecosystem:

**Operational Tracking (Flask) + Intelligent Prediction (AI/ML) + Strategic Analytics (Power BI)**

---

# **2. Project Overview**

| Attribute     | Detail                                                                              |
| ------------- | ----------------------------------------------------------------------------------- |
| Project Name  | SpendWise — AI-Powered Personal Expense Tracker                                     |
| Domain        | Personal Finance / FinTech / Data Analytics                                         |
| Project Type  | Full-stack Web Application + Business Intelligence Dashboard                        |
| Primary Users | Individuals managing personal and household finances                                |
| Core Idea     | Replace manual spreadsheets with an intelligent automated financial tracking system |

---

# **3. Objectives**

1. Build a secure multi-user personal finance management system.
2. Allow users to record and manage expenses efficiently.
3. Enable budget planning and tracking.
4. Visualize financial behavior using interactive dashboards.
5. Forecast future expenses using machine learning.
6. Detect unusual spending patterns automatically.
7. Calculate a financial health score.
8. Provide personalized savings recommendations.
9. Deliver a modern fintech-style user experience.
10. Extend analytics with Power BI for advanced business intelligence reporting.

---

# **4. Scope**

## **In Scope**

* User registration, login, and profile management
* Expense CRUD operations
* Category-wise expense management
* Budget setup and monitoring
* Analytics dashboard
* AI/ML predictions
* Financial health score
* Recommendation engine
* Power BI integration


## **Out of Scope**

* Direct bank integration
* UPI synchronization
* Multi-currency conversion
* Mobile native application
* Shared/family budgeting
* OCR receipt scanning
* Email/SMS notifications

---

# **5. Features**

## **User Management**

* User registration
* Login/logout
* Profile editing
* Password management
* Theme preference
* Currency preference
* Monthly income management


## **Expense Management**

* Add expenses
* Edit expenses
* Delete expenses
* Search expenses
* Filter by category/date/payment method
* Sorting
* Pagination
* Notes and tags
* Recurring expense management


## **Budget Management**

* Monthly budget setup
* Category-wise budget setup
* Budget tracking
* Adjustable thresholds
* Visual progress bars
* Overspending alerts


## **Analytics Dashboard (Flask)**

* Monthly trend analysis
* Category distribution
* Weekly spending patterns
* Year-over-year comparison
* Payment method analysis
* Top expenses analysis
* Budget usage visualization


## **AI/ML Features**

### **Expense Forecasting**

Uses **Linear Regression** to predict the next three months of expenses.


### **Anomaly Detection**

Uses the **IQR statistical method** to identify unusual spending.


### **Financial Health Score**

Calculates a weighted score based on:

* Savings rate
* Budget adherence
* Spending consistency
* Category diversity
* Anomaly ratio


### **Personalized Recommendations**

Provides:

* Spending control suggestions
* Budget optimization tips
* Saving recommendations


## **Dashboard UI**

* KPI cards
* Chart.js charts
* Budget overview panel
* AI health panel
* Recent transactions
* Interactive filtering


## **Power BI Dashboard**

Power BI is integrated using MySQL ODBC for advanced visual analytics.

### **Visualizations**

* KPI Cards
* Pie Chart
* Donut Chart
* Treemap
* Waterfall Chart
* Clustered Column Chart
* Clustered Bar Chart
* Line Chart


### **Interactive Slicers**

* User
* Category
* Expense Date

---

# **6. Advantages**

* Single source of truth (same MySQL database for Flask and Power BI)
* Full-stack + BI integration
* Explainable AI architecture
* Real-time anomaly detection
* Modular ML structure
* No paid infrastructure needed
* Strong visual analytics
* Professional Power BI reporting
* Modern fintech-style UI
* Scalable architecture for future upgrades

---

# **7. Limitations**

* Linear Regression does not capture seasonal patterns
* IQR anomaly detection needs historical data
* Manual data entry only
* No real-time bank integration
* Power BI requires manual refresh
* No automated testing suite
* Fixed financial health score weights
* Currency conversion not supported

---

# **8. Tools & Skills Used**

| Category       | Tool / Skill              | Purpose               |
| -------------- | ------------------------- | --------------------- |
| Language       | Python 3.11               | Backend and ML        |
| Framework      | Flask 3                   | Web application       |
| ORM            | SQLAlchemy                | Database modeling     |
| Database       | MySQL                     | Data storage          |
| DB Driver      | PyMySQL                   | MySQL connectivity    |
| Authentication | Flask-Login, Flask-Bcrypt | User authentication   |
| Migration      | Flask-Migrate             | Schema migration      |
| Data Analysis  | Pandas, NumPy             | Analytics & ML        |
| Visualization  | Chart.js                  | Web charts            |
| Styling        | CSS3, Bootstrap           | UI design             |
| BI Tool        | Power BI Desktop          | Advanced analytics    |
| Connector      | MySQL ODBC Connector      | Power BI integration  |
| Development    | VS Code                   | Coding                |
| DB Tools       | MySQL Shell / Workbench   | Database management   |
| Notebook       | Jupyter Notebook          | Testing and analysis  |
| Environment    | venv                      | Dependency management |


## **Skills Demonstrated**

* Flask blueprint architecture
* Database design
* ORM implementation
* Session authentication
* REST API development
* Data wrangling
* Statistical machine learning
* Financial analytics
* Power BI dashboard development
* UI/UX design

---

# **9. System Architecture**

SpendWise follows a modular multi-layer architecture.


## **Architecture Layers**

### **1. Presentation Layer**

Technologies:

* HTML
* CSS
* Bootstrap
* JavaScript
* Chart.js

Responsibilities:

* User interface
* Forms
* Charts
* Dashboard rendering


### **2. Application Layer**

Technology:

* Flask

Responsibilities:

* Business logic
* Authentication
* Routing
* Session handling


### **3. Database Layer**

Technology:

* MySQL

Stores:

* Users
* Expenses
* Categories
* Budgets
* Predictions
* Audit logs


### **4. AI/ML Layer**

Handles:

* Forecasting
* Anomaly detection
* Financial health scoring
* Recommendations


### **5. BI Layer**

Technology:

* Power BI

Handles:

* Interactive filtering
* Advanced analytics
* Comparative reports
* Visual insights


## **Architecture Flow**

```text
User → Frontend UI → Flask Backend → MySQL Database
                        ↓
                 AI/ML Processing
                        ↓
              Flask Dashboard Visualization
                        ↓
                Power BI Analytics Layer
```

---

# **10. Database Design**

SpendWise uses a relational database:

**spendwise_db**


## **Main Tables**

### **users**

Stores user profile information.

Fields:

* id
* username
* email
* password_hash
* monthly_income
* currency
* theme


### **expenses**

Stores all expense transactions.

Fields:

* id
* user_id
* category_id
* amount
* description
* expense_date
* payment_method
* recurring_flag


### **categories**

Stores expense categories.

Fields:

* id
* user_id
* name
* icon
* color
* is_default


### **budgets**

Stores budget allocation.

Fields:

* id
* user_id
* category_id
* amount
* budget_month


### **ml_predictions**

Stores machine learning outputs.

Fields:

* id
* user_id
* prediction_type
* predicted_value
* generated_at


### **audit_log**

Stores system/user activity logs.

Fields:

* id
* user_id
* action
* created_at


## **Relationships**

* One user → Many expenses
* One user → Many categories
* One user → Many budgets
* One category → Many expenses
* One category → Many budgets

---

# **11. Workflow / Process Flow**

### Step 1

User registers or logs in.

↓

### Step 2

User adds expense entries.

↓

### Step 3

Data stored in MySQL.

↓

### Step 4

User sets budgets.

↓

### Step 5

Analytics processing starts.

↓

### Step 6

AI modules process:

* Forecasting
* Anomaly detection
* Financial health scoring
* Recommendations

↓

### Step 7

Flask dashboard renders analytics.

↓

### Step 8

Power BI generates advanced reports.

↓

### Step 9

User uses insights to improve financial decisions.

---

# **12. How Each Piece Is Used (Where / Why / How)**

| Component             | Location         | Purpose                          |
| --------------------- | ---------------- | -------------------------------- |
| `config.py`           | Root             | Configuration settings           |
| `app/models`          | Models folder    | Database schema                  |
| `app/routes`          | Routes folder    | Feature routing                  |
| `app/services`        | Services folder  | Analytics logic                  |
| `app/ml`              | ML folder        | AI/ML modules                    |
| `templates`           | Templates folder | Frontend UI pages                |
| `static/css`          | CSS folder       | Styling and themes               |
| `static/js`           | JS folder        | Charts and UI logic              |
| `database/schema.sql` | Database folder  | Database creation and seed setup |

---
