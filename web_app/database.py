"""
MySQL database module for the Expense Tracker web application.
"""

import os
import mysql.connector
from mysql.connector import Error


DB_NAME = os.getenv("MYSQL_DATABASE", "expense_tracker")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "rida34")


def _server_connection():
    """Connect to MySQL server without selecting a database."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )


def initialize_database():
    """Create the MySQL database if it does not already exist."""
    connection = _server_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_connection():
    """Return a connection to the Expense Tracker MySQL database."""
    initialize_database()

    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT PRIMARY KEY AUTO_INCREMENT,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description VARCHAR(500),
            date DATE NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def get_all_expenses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


def add_expense(amount, category, description, date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (%s, %s, %s, %s)
    """, (amount, category, description, date))

    connection.commit()
    cursor.close()
    connection.close()


def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = %s",
        (expense_id,)
    )

    connection.commit()
    cursor.close()
    connection.close()


def update_expense(expense_id, amount, category, description, date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = %s,
            category = %s,
            description = %s,
            date = %s
        WHERE id = %s
    """, (amount, category, description, date, expense_id))

    connection.commit()
    cursor.close()
    connection.close()


def get_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM expenses WHERE id = %s",
        (expense_id,)
    )

    expense = cursor.fetchone()

    cursor.close()
    connection.close()

    return expense


def get_monthly_expenses(month):
    """Get expenses for a specific month in YYYY-MM format."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE DATE_FORMAT(date, '%%Y-%%m') = %s
        ORDER BY date DESC, id DESC
    """, (month,))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


def clear_all_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")

    connection.commit()
    cursor.close()
    connection.close()
