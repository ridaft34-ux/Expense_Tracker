import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE = DATA_DIR / "expenses.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_expenses():
    connection = get_connection()

    expenses = connection.execute("""
        SELECT *
        FROM expenses
        ORDER BY date DESC, id DESC
    """).fetchall()

    connection.close()

    return expenses


def add_expense(amount, category, description, date):
    connection = get_connection()

    connection.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        date
    ))

    connection.commit()
    connection.close()


def delete_expense(expense_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()


def update_expense(
    expense_id,
    amount,
    category,
    description,
    date
):
    connection = get_connection()

    connection.execute("""
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (
        amount,
        category,
        description,
        date,
        expense_id
    ))

    connection.commit()
    connection.close()


def get_expense(expense_id):
    connection = get_connection()

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    connection.close()

    return expense
def get_monthly_expenses(month):
    """Get expenses for a specific month."""

    connection = get_connection()

    expenses = connection.execute("""
        SELECT *
        FROM expenses
        WHERE date LIKE ?
        ORDER BY date DESC, id DESC
    """, (
        month + "%",
    )).fetchall()

    connection.close()

    return expenses
def clear_all_expenses():
    connection = get_connection()
    connection.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()