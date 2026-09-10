"""
Monthly Summary Window
Window for viewing monthly expense summaries
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from src.utils.helpers import format_currency, get_month_name


class SummaryWindow:
    """Window for displaying monthly expense summary"""

    def __init__(self, parent, db):
        """
        Initialize the Summary window
        
        Args:
            parent: Parent window
            db: Database manager instance
        """
        self.db = db
        self.window = tk.Toplevel(parent)
        self.window.title("Monthly Summary")
        self.window.resizable(True, True)
        self.window.configure(bg="#f4f6f8")

        # Make dialog modal
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()
        self.load_current_month()

    def setup_ui(self):
        """Set up the window UI"""
        # Control frame
        control_frame = ttk.Frame(self.window, padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Month selection
        ttk.Label(control_frame, text="Month:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            control_frame,
            textvariable=self.month_var,
            values=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            state="readonly",
            width=15
        )
        month_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Year:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(
            control_frame,
            textvariable=self.year_var,
            values=[str(i) for i in range(2020, 2031)],
            state="readonly",
            width=10
        )
        year_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Load", command=self.load_summary).pack(side=tk.LEFT, padx=5)

        # Summary frame
        summary_frame = ttk.LabelFrame(self.window, text="Category Breakdown", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview columns
        columns = ("Category", "Total", "Count", "Average")
        self.tree = ttk.Treeview(summary_frame, columns=columns, height=15, show="headings")

        # Define column headings and widths
        self.tree.column("Category", width=150, anchor=tk.W)
        self.tree.column("Total", width=100, anchor="e")
        self.tree.column("Count", width=80, anchor=tk.CENTER)
        self.tree.column("Average", width=100, anchor="e")

        self.tree.heading("Category", text="Category")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Count", text="Count")
        self.tree.heading("Average", text="Average")

        # Scrollbar
        scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        # Total frame
        total_frame = ttk.LabelFrame(self.window, text="Total for Month", padding="10")
        total_frame.pack(fill=tk.X, padx=10, pady=5)

        self.total_label = ttk.Label(total_frame, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.total_label.pack(side=tk.LEFT, padx=10)

    def load_current_month(self):
        """Load current month's data"""
        today = datetime.now()
        self.month_var.set(get_month_name(today.month))
        self.year_var.set(str(today.year))
        self.load_summary()

    def load_summary(self):
        """Load and display monthly summary"""
        month_name = self.month_var.get()
        year_str = self.year_var.get()

        if not month_name or not year_str:
            return

        # Get month number
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month = months.index(month_name) + 1

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get summary data
        year = int(year_str)
        summary = self.db.get_monthly_summary(year, month)

        total = 0
        for category, total_amount, count in summary:
            average = total_amount / count if count > 0 else 0
            self.tree.insert(
                "",
                tk.END,
                values=(
                    category,
                    format_currency(total_amount),
                    count,
                    format_currency(average)
                )
            )
            total += total_amount

        # Update total label
        self.total_label.config(text=f"Total: {format_currency(total)}")
