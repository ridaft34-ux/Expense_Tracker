"""
Expense Tracker - Main Entry Point
Run this file to start the application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import main

if __name__ == "__main__":
    main()