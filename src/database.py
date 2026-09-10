"""
Database Module
Handles all SQLite database operations for expense tracking
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


class DatabaseManager:
    """Manages SQLite database operations for expenses"""

    def __init__(self, db_path: str = "data/expenses.db"):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_exists()

    def ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path) or "data", exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def add_expense(self, amount: float, category: str, description: str, date: str) -> int:
        """
        Add a new expense to the database
        
        Args:
            amount: Expense amount
            category: Expense category
            description: Expense description
            date: Expense date (YYYY-MM-DD format)
            
        Returns:
            ID of the newly added expense
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        """, (amount, category, description, date))

        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()

        return expense_id

    def get_all_expenses(self) -> List[Tuple]:
        """
        Retrieve all expenses from the database
        
        Returns:
            List of expense tuples (id, amount, category, description, date, created_at)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            ORDER BY date DESC
        """)

        expenses = cursor.fetchall()
        conn.close()

        return expenses

    def get_expense_by_id(self, expense_id: int) -> Optional[Tuple]:
        """
        Retrieve a specific expense by ID
        
        Args:
            expense_id: ID of the expense to retrieve
            
        Returns:
            Expense tuple or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            WHERE id = ?
        """, (expense_id,))

        expense = cursor.fetchone()
        conn.close()

        return expense

    def update_expense(self, expense_id: int, amount: float, category: str, 
                      description: str, date: str) -> bool:
        """
        Update an existing expense
        
        Args:
            expense_id: ID of the expense to update
            amount: New amount
            category: New category
            description: New description
            date: New date
            
        Returns:
            True if update was successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?
            WHERE id = ?
        """, (amount, category, description, date, expense_id))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success

    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense from the database
        
        Args:
            expense_id: ID of the expense to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success

    def get_monthly_summary(self, year: int, month: int) -> List[Tuple]:
        """
        Get summary of expenses for a specific month grouped by category
        
        Args:
            year: Year (YYYY)
            month: Month (MM)
            
        Returns:
            List of tuples (category, total_amount, count)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Format month for filtering
        month_str = f"{year}-{month:02d}"

        cursor.execute("""
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            WHERE date LIKE ?
            GROUP BY category
            ORDER BY total DESC
        """, (f"{month_str}%",))

        summary = cursor.fetchall()
        conn.close()

        return summary

    def get_total_by_month(self, year: int, month: int) -> float:
        """
        Get total expenses for a specific month
        
        Args:
            year: Year (YYYY)
            month: Month (MM)
            
        Returns:
            Total amount for the month
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        month_str = f"{year}-{month:02d}"

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE date LIKE ?
        """, (f"{month_str}%",))

        result = cursor.fetchone()
        conn.close()

        total = result[0] if result[0] is not None else 0.0
        return total

    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Tuple]:
        """
        Get expenses within a date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of expenses within the range
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date, created_at
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        """, (start_date, end_date))

        expenses = cursor.fetchall()
        conn.close()

        return expenses

    def get_total_by_category(self) -> List[Tuple]:
        """
        Get total expenses grouped by category
        
        Returns:
            List of tuples (category, total_amount)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)

        summary = cursor.fetchall()
        conn.close()

        return summary
    def clear_all_expenses(self) -> bool:
        """Delete all expenses from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses")

        conn.commit()
        success = cursor.rowcount >= 0
        conn.close()

        return success
