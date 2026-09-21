"""
Database Module
Handles MySQL database operations for expense tracking.
"""

import os
import mysql.connector
from typing import List, Tuple, Optional


DB_NAME = os.getenv("MYSQL_DATABASE", "expense_tracker")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "rida34")


def _server_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )


class DatabaseManager:
    """Manages MySQL database operations for expenses."""

    def __init__(self):
        self.ensure_database_exists()

    def get_connection(self):
        return mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    def ensure_database_exists(self):
        """Create database and table if they don't exist."""
        conn = _server_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

        conn.commit()
        cursor.close()
        conn.close()

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT PRIMARY KEY AUTO_INCREMENT,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description VARCHAR(500),
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def add_expense(self, amount: float, category: str, description: str, date: str) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (amount, category, description, date)
            VALUES (%s, %s, %s, %s)
        """, (amount, category, description, date))

        conn.commit()
        expense_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return expense_id

    def get_all_expenses(self) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            ORDER BY date DESC, id DESC
        """)

        expenses = cursor.fetchall()
        cursor.close()
        conn.close()

        return expenses

    def get_expense_by_id(self, expense_id: int) -> Optional[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            WHERE id = %s
        """, (expense_id,))

        expense = cursor.fetchone()
        cursor.close()
        conn.close()

        return expense

    def update_expense(self, expense_id: int, amount: float, category: str,
                       description: str, date: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET amount = %s, category = %s, description = %s, date = %s
            WHERE id = %s
        """, (amount, category, description, date, expense_id))

        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()

        return success

    def delete_expense(self, expense_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))

        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()

        return success

    def get_monthly_summary(self, year: int, month: int) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()

        month_str = f"{year}-{month:02d}"

        cursor.execute("""
            SELECT category, SUM(amount) AS total, COUNT(*) AS count
            FROM expenses
            WHERE DATE_FORMAT(date, '%%Y-%%m') = %s
            GROUP BY category
            ORDER BY total DESC
        """, (month_str,))

        summary = cursor.fetchall()
        cursor.close()
        conn.close()

        return summary

    def get_total_by_month(self, year: int, month: int) -> float:
        conn = self.get_connection()
        cursor = conn.cursor()

        month_str = f"{year}-{month:02d}"

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE DATE_FORMAT(date, '%%Y-%%m') = %s
        """, (month_str,))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return float(result[0]) if result[0] is not None else 0.0

    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            WHERE date BETWEEN %s AND %s
            ORDER BY date DESC
        """, (start_date, end_date))

        expenses = cursor.fetchall()
        cursor.close()
        conn.close()

        return expenses

    def get_total_by_category(self) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)

        summary = cursor.fetchall()
        cursor.close()
        conn.close()

        return summary

    def clear_all_expenses(self) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses")

        conn.commit()
        success = cursor.rowcount >= 0
        cursor.close()
        conn.close()

        return success
