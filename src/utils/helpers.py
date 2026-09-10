"""
Helper utilities for the expense tracker
"""

from datetime import datetime
from typing import Tuple


def validate_amount(amount_str: str) -> Tuple[bool, float, str]:
    """
    Validate and convert amount string to float
    
    Args:
        amount_str: String representation of amount
        
    Returns:
        Tuple of (is_valid, amount, error_message)
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, 0, "Amount must be greater than 0"
        return True, amount, ""
    except ValueError:
        return False, 0, "Invalid amount format"


def validate_date(date_str: str) -> Tuple[bool, str, str]:
    """
    Validate date format (YYYY-MM-DD)
    
    Args:
        date_str: Date string to validate
        
    Returns:
        Tuple of (is_valid, formatted_date, error_message)
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return True, date_str, ""
    except ValueError:
        return False, "", "Invalid date format. Use YYYY-MM-DD"


def validate_category(category: str) -> Tuple[bool, str]:
    """
    Validate category string
    
    Args:
        category: Category string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not category or len(category.strip()) == 0:
        return False, "Category cannot be empty"
    if len(category) > 50:
        return False, "Category name is too long (max 50 characters)"
    return True, ""


def format_currency(amount: float) -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:.2f}"


def get_current_date() -> str:
    """
    Get current date in YYYY-MM-DD format
    
    Returns:
        Current date string
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_month_name(month: int) -> str:
    """
    Get month name from month number
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Month name
    """
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    if 1 <= month <= 12:
        return months[month - 1]
    return "Unknown"


def parse_date(date_str: str) -> Tuple[int, int, int]:
    """
    Parse date string to year, month, day
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Tuple of (year, month, day)
    """
    parts = date_str.split("-")
    return int(parts[0]), int(parts[1]), int(parts[2])


def categories_list() -> list:
    """
    Get predefined list of expense categories
    
    Returns:
        List of category names
    """
    return [
        "Food & Dining",
        "Transportation",
        "Entertainment",
        "Utilities",
        "Healthcare",
        "Shopping",
        "Education",
        "Groceries",
        "Rent/Mortgage",
        "Insurance",
        "Savings",
        "Other"
    ]
