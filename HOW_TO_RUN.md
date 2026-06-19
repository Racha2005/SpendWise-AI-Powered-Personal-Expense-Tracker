# SpendWise — Exact Run Commands (Windows / PowerShell)

Use your correct project path:
```
C:\Users\DELL\Downloads\spendwise_project\spendwise
```

This guide gives you the **separate commands for every single time** you open
a new terminal, plus the **one-time setup** you only do once.

---

## PART A — ONE-TIME SETUP (do this only the first time)

Open PowerShell, then run these **one at a time**, pressing Enter after each:

### A1. Go to the project folder
```powershell
cd "C:\Users\DELL\Downloads\spendwise_project\spendwise"
```

### A2. Create a virtual environment (only if `venv` folder doesn't exist yet)
```powershell
python -m venv venv
```
> If `python` isn't recognized, use `py -3 -m venv venv` instead.

### A3. Activate the virtual environment
```powershell
venv\Scripts\activate
```
Your prompt should now show `(venv)` at the start of the line, like:
```
(venv) PS C:\Users\DELL\Downloads\spendwise_project\spendwise>
```

> ⚠️ If you get a script-execution error like *"running scripts is disabled on this system"*, run this once (as the same user, not admin needed for CurrentUser scope):
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Then retry `venv\Scripts\activate`.

### A4. Install all dependencies into the venv
```powershell
pip install -r requirements.txt
```
This installs Flask, SQLAlchemy, PyMySQL, Pandas, NumPy, etc. — wait for it to finish (1–3 minutes).

### A5. Create the MySQL database (one time)
Open a **separate** terminal/PowerShell window for this (don't touch your venv window):
```powershell
mysql -u root -p < database\schema.sql
```
Enter your MySQL root password when prompted. This creates `spendwise_db` and all tables + default categories.

> If `mysql` isn't recognized, open **MySQL Shell** or **MySQL Workbench** instead, and run the contents of `database\schema.sql` there.

### A6. Configure your `.env` file (one time)
```powershell
copy .env.example .env
notepad .env
```
Edit the line to match your real MySQL password:
```
DEV_DATABASE_URL=mysql+pymysql://root:YOUR_ACTUAL_PASSWORD@localhost/spendwise_db
```
Save and close Notepad.

---

## PART B — EVERY TIME YOU WANT TO RUN THE SITE (after setup is done)

Each time you open a **new** PowerShell window, repeat these 3 commands, in order:

### B1. Go to the project folder
```powershell
cd "C:\Users\DELL\Downloads\spendwise_project\spendwise"
```

### B2. Activate the virtual environment
```powershell
venv\Scripts\activate
```
You must see `(venv)` appear before your prompt — if you don't see it, the next step will fail with "module not found" errors.

### B3. Run the Flask app
```powershell
python run.py
```
You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### B4. Open the site
Go to your browser and visit:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

### B5. Stop the server
When you're done, go back to the PowerShell window and press:
```
CTRL + C
```

---

## Quick Reference Card (copy-paste block for daily use)

```powershell
cd "C:\Users\DELL\Downloads\spendwise_project\spendwise"
venv\Scripts\activate
python run.py
```
Then open: `http://127.0.0.1:5000`

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `'python' is not recognized` | Use `py run.py` instead, or reinstall Python with "Add to PATH" checked |
| `ModuleNotFoundError: No module named 'flask'` | Your venv isn't activated — run `venv\Scripts\activate` first, then `pip install -r requirements.txt` again |
| `(venv)` doesn't show after activate | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then retry |
| `sqlalchemy.exc.OperationalError` / can't connect to MySQL | Check `.env` password matches your real MySQL root password, and that MySQL service is running (`services.msc` → MySQL80 → Start) |
| `Access denied for user 'root'@'localhost'` | Wrong password in `.env` — double check it |
| Port 5000 already in use | Close other Flask instances, or run `python run.py` after editing `run.py`'s `port=5000` to `port=5050` |
| Page loads but looks unstyled (no colors) | Hard refresh with `CTRL + F5` — browser may have cached an old CSS file |

---

## Why each command exists

- `cd "..."` — PowerShell needs to be *inside* the project folder so relative paths (`templates/`, `static/`, `run.py`) resolve correctly.
- `python -m venv venv` — creates an isolated Python environment so SpendWise's specific package versions (Flask 3.0.3, SQLAlchemy 3.1.1, etc.) don't conflict with other Python projects on your machine.
- `venv\Scripts\activate` — switches your terminal session to use the venv's Python/pip instead of your system-wide Python. This is **not permanent** — it only lasts for that one terminal window, which is why you repeat it every time you open a new window.
- `pip install -r requirements.txt` — reads the dependency list and installs the exact versions tested with this project.
- `mysql -u root -p < database\schema.sql` — runs the SQL file that creates the database, tables, and default categories — only needs to happen once, unless you wipe the database.
- `python run.py` — starts the Flask development server defined in `run.py`, which calls `create_app()` from `app/__init__.py`.
