-- ============================================================
-- SpendWise Database Schema
-- Database: spendwise_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS spendwise_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE spendwise_db;

-- ------------------------------------------------------------
-- Table: users
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(100),
    currency      CHAR(3)      NOT NULL DEFAULT 'INR',
    monthly_income DECIMAL(12,2) DEFAULT 0.00,
    avatar_url    VARCHAR(255),
    theme         ENUM('light','dark') DEFAULT 'light',
    is_active     BOOLEAN      DEFAULT TRUE,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login    DATETIME,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: categories
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED,  -- NULL = system default
    name        VARCHAR(60)  NOT NULL,
    icon        VARCHAR(10)  DEFAULT '💰',
    color       CHAR(7)      DEFAULT '#6366f1',
    is_default  BOOLEAN      DEFAULT FALSE,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;

-- Default categories (system-wide)
INSERT INTO categories (user_id, name, icon, color, is_default) VALUES
(NULL, 'Food & Dining',     '🍔', '#f59e0b', TRUE),
(NULL, 'Transportation',   '🚗', '#3b82f6', TRUE),
(NULL, 'Housing',          '🏠', '#8b5cf6', TRUE),
(NULL, 'Healthcare',       '🏥', '#ef4444', TRUE),
(NULL, 'Entertainment',    '🎬', '#ec4899', TRUE),
(NULL, 'Shopping',         '🛍️', '#14b8a6', TRUE),
(NULL, 'Education',        '📚', '#f97316', TRUE),
(NULL, 'Utilities',        '💡', '#84cc16', TRUE),
(NULL, 'Travel',           '✈️', '#06b6d4', TRUE),
(NULL, 'Savings',          '💰', '#22c55e', TRUE),
(NULL, 'Investments',      '📈', '#a855f7', TRUE),
(NULL, 'Personal Care',    '💆', '#fb7185', TRUE),
(NULL, 'Subscriptions',    '📱', '#0ea5e9', TRUE),
(NULL, 'Gifts & Donations','🎁', '#d97706', TRUE),
(NULL, 'Other',            '📦', '#6b7280', TRUE);

-- ------------------------------------------------------------
-- Table: expenses
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS expenses (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    category_id   INT UNSIGNED NOT NULL,
    amount        DECIMAL(12,2) NOT NULL,
    description   VARCHAR(255),
    note          TEXT,
    expense_date  DATE         NOT NULL,
    payment_method ENUM('cash','card','upi','netbanking','wallet','other') DEFAULT 'cash',
    is_recurring  BOOLEAN      DEFAULT FALSE,
    recurrence    ENUM('daily','weekly','monthly','yearly') DEFAULT NULL,
    tags          VARCHAR(255),
    receipt_url   VARCHAR(255),
    is_anomaly    BOOLEAN      DEFAULT FALSE,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    INDEX idx_user_date       (user_id, expense_date),
    INDEX idx_user_category   (user_id, category_id),
    INDEX idx_expense_date    (expense_date)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: budgets
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS budgets (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    category_id   INT UNSIGNED,  -- NULL = overall monthly budget
    budget_month  DATE         NOT NULL,  -- stored as first day of month
    amount        DECIMAL(12,2) NOT NULL,
    alert_percent INT          DEFAULT 80,  -- alert when X% consumed
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_cat_month (user_id, category_id, budget_month),
    INDEX idx_user_month (user_id, budget_month)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: ml_predictions
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ml_predictions (
    id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id        INT UNSIGNED NOT NULL,
    prediction_type ENUM('forecast','anomaly','health_score','budget_risk') NOT NULL,
    target_month   DATE,
    predicted_value DECIMAL(12,2),
    confidence     FLOAT,
    model_version  VARCHAR(20)  DEFAULT '1.0',
    metadata       JSON,
    created_at     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, prediction_type)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: audit_log
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_log (
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id    INT UNSIGNED NOT NULL,
    action     VARCHAR(100) NOT NULL,
    entity     VARCHAR(50),
    entity_id  INT UNSIGNED,
    ip_address VARCHAR(45),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_action (user_id, action)
) ENGINE=InnoDB;
