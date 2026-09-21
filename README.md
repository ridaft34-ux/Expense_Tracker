# Expense Tracker

A Python Expense Tracker with desktop and Flask web applications.

## 🌐 Live Demo

[Expense Tracker - Live Demo](https://expense-tracker-ua7l.onrender.com/)

## ✨ Features
...

## 🗄️ MySQL Setup

This version uses **MySQL instead of SQLite3**.

### 1. Install MySQL
Install MySQL Server and make sure the MySQL service is running.

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your MySQL password

The application reads these environment variables:

- `MYSQL_HOST` (default: `localhost`)
- `MYSQL_PORT` (default: `3306`)
- `MYSQL_USER` (default: `root`)
- `MYSQL_PASSWORD` (required: your MySQL password)
- `MYSQL_DATABASE` (default: `expense_tracker`)

For Windows Command Prompt:

```bat
set MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
```

Or, for a quick local test, replace `YOUR_MYSQL_PASSWORD` in `web_app/database.py` and `src/database.py`.

### 4. Run the web application

```bash
cd web_app
python app.py
```

The application automatically creates the `expense_tracker` database and `expenses` table the first time it connects.

### 5. Open the application

Go to:

```text
http://127.0.0.1:5000
```

### SQLite vs MySQL

The original SQLite database files are kept in the project for reference, but the application code now uses MySQL. Existing SQLite data is **not automatically copied** into MySQL.
