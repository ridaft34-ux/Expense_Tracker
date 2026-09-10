"""
Main Application Window
Primary window for the Expense Tracker application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.database import DatabaseManager
from src.gui.summary import SummaryWindow
from src.utils.helpers import format_currency


class MainWindow:
    """Main application window"""

    def __init__(self, root):
        """Initialize the main window"""

        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg="#f4f6f8")

        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Arial", 20, "bold"),
            foreground="#1f2937"
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 10),
            foreground="#6b7280"
        )

        style.configure(
            "Section.TLabelframe",
            padding=12
        )

        style.configure(
            "Section.TLabelframe.Label",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Action.TButton",
            font=("Arial", 10, "bold"),
            padding=(12, 7)
        )

        style.configure(
            "Treeview",
            rowheight=20,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )
        # Initialize database
        self.db = DatabaseManager()
                # Dashboard values
        self.total_label = None
        self.month_label = None
        self.count_label = None
        self.search_var = tk.StringVar()

        # Create interface
        self.setup_ui()

        # Load existing expenses
        self.refresh_expenses()

    # ==========================================================
    # SETUP UI
    # ==========================================================

    def setup_ui(self):
        """Create the main application interface"""

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        title_label = ttk.Label(
            self.root,
            text="Expense Tracker",
            style="Title.TLabel"
        )
        title_label.pack(pady=(9, 5))

        subtitle_label = ttk.Label(
            self.root,
            text="Manage your daily expenses",
            style="Subtitle.TLabel"
        )
        subtitle_label.pack(pady=(0, 8))
                # ======================================================
        # DASHBOARD CARDS
        # ======================================================

        dashboard_frame = ttk.Frame(
            self.root
        )
        dashboard_frame.pack(
            fill=tk.X,
            padx=8,
            pady=(0, 5)
        )

        # Make the three columns expand equally
        dashboard_frame.columnconfigure(
            0,
            weight=1
        )

        dashboard_frame.columnconfigure(
            1,
            weight=1
        )

        dashboard_frame.columnconfigure(
            2,
            weight=1
        )

        # ------------------------------------------------------
        # Total Spent Card
        # ------------------------------------------------------

        total_card = ttk.LabelFrame(
            dashboard_frame,
            text="TOTAL SPENT",
            padding=12
        )
        total_card.grid(
            row=0,
            column=0,
            padx=5,
            sticky="nsew"
        )

        self.total_label = ttk.Label(
            total_card,
            text="₹0.00",
            font=("Arial", 15, "bold")
        )
        self.total_label.pack(
            pady=5
        )

        # ------------------------------------------------------
        # This Month Card
        # ------------------------------------------------------

        month_card = ttk.LabelFrame(
            dashboard_frame,
            text="THIS MONTH",
            padding=12
        )
        month_card.grid(
            row=0,
            column=1,
            padx=5,
            sticky="nsew"
        )

        self.month_label = ttk.Label(
            month_card,
            text="₹0.00",
            font=("Arial", 15, "bold")
        )
        self.month_label.pack(
            pady=5
        )

        # ------------------------------------------------------
        # Expense Count Card
        # ------------------------------------------------------

        count_card = ttk.LabelFrame(
            dashboard_frame,
            text="EXPENSES",
            padding=12
        )
        count_card.grid(
            row=0,
            column=2,
            padx=5,
            sticky="nsew"
        )

        self.count_label = ttk.Label(
            count_card,
            text="0",
            font=("Arial", 15, "bold")
        )
        self.count_label.pack(
            pady=5
        )

        # ------------------------------------------------------
        # Add Expense Frame
        # ------------------------------------------------------

        input_frame = ttk.LabelFrame(
            self.root,
            text="Add Expense",
            style="Section.TLabelframe",
            padding=15
        )
        input_frame.pack(
            fill=tk.X,
            padx=15,
            pady=5
        )

        # Amount
        ttk.Label(
            input_frame,
            text="Amount:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.amount_entry = ttk.Entry(
            input_frame,
            width=18
        )
        self.amount_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Category
        ttk.Label(
            input_frame,
            text="Category:"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.category_var = tk.StringVar()

        self.category_entry = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=[
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Education",
                "Entertainment",
                "Health",
                "Other"
                ],
            width=16,
            state="readonly"
            )
        self.category_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )
# Default category
        self.category_entry.set("Food")
        # Description
        ttk.Label(
            input_frame,
            text="Description:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.description_entry = ttk.Entry(
            input_frame,
            width=35
        )
        self.description_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="we"
        )

        # Date
        ttk.Label(
            input_frame,
            text="Date:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.date_entry = ttk.Entry(
            input_frame,
            width=15
        )
        self.date_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # Today's date
        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Add button
        add_button = ttk.Button(
            input_frame,
            text="Add Expense",
            style="Action.TButton",
            command=self.add_expense
        )
        add_button.grid(
            row=2,
            column=3,
            padx=5,
            pady=5
        )

        # ------------------------------------------------------
        # Expense History Frame
        # ------------------------------------------------------

        history_frame = ttk.LabelFrame(
            self.root,
            text="Expense History",
            padding=8
        )
        history_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=6,
            pady=4
        )

        # Treeview columns
        columns = (
            "No.",
            "Amount",
            "Category",
            "Description",
            "Date"
        )

        self.tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings"
        )

        # Headings
        self.tree.heading(
            "No.",
            text="No."
        )

        self.tree.heading(
            "Amount",
            text="Amount"
        )

        self.tree.heading(
            "Category",
            text="Category"
        )

        self.tree.heading(
            "Description",
            text="Description"
        )

        self.tree.heading(
            "Date",
            text="Date"
        )

        # Columns
        self.tree.column(
            "No.",
            width=45,
            anchor="center"
        )

        self.tree.column(
            "Amount",
            width=100,
            anchor="e"
        )

        self.tree.column(
            "Category",
            width=120,
            anchor="w"
        )

        self.tree.column(
            "Description",
            width=250,
            anchor="w"
        )

        self.tree.column(
            "Date",
            width=110,
            anchor="center"
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            history_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
                # ======================================================
        # SEARCH BAR
        # ======================================================

        search_frame = ttk.Frame(history_frame)
        search_frame.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side=tk.LEFT,
            padx=(0, 5)
        )

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )
        self.search_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        clear_search_button = ttk.Button(
            search_frame,
            text="Clear Search",
            command=self.clear_search
        )
        clear_search_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # Search whenever the user types
        self.search_var.trace_add(
            "write",
            lambda *args: self.search_expenses()
        )

        # ------------------------------------------------------
        # Buttons
        # ------------------------------------------------------

        button_frame = ttk.Frame(
            self.root
        )
        button_frame.pack(
            pady=(0, 15)
        )

        # Monthly Summary
        summary_button = ttk.Button(
            button_frame,
            text="Monthly Summary",
            style="Action.TButton",
            command=self.open_summary
        )
        summary_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # Edit Selected
        edit_button = ttk.Button(
            button_frame,
            text="Edit Selected",
            style="Action.TButton",
            command=self.edit_selected
        )
        edit_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # Delete Selected
        delete_button = ttk.Button(
            button_frame,
            text="Delete Selected",
            style="Action.TButton",
            command=self.delete_selected
        )
        delete_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # Clear All History
        clear_button = ttk.Button(
            button_frame,
            text="Clear All History",
            style="Action.TButton",
            command=self.clear_all_history
        )
        clear_button.pack(
            side=tk.LEFT,
            padx=5
        )

    # ==========================================================
    # ADD EXPENSE
    # ==========================================================

    def add_expense(self):
        """Add a new expense"""

        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()
        date = self.date_entry.get().strip()

        # Check required fields
        if not amount or not category or not date:
            messagebox.showwarning(
                "Missing Information",
                "Please enter amount, category and date."
            )
            return

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Amount must be greater than 0."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid number."
            )
            return

        # Validate date
        try:
            datetime.strptime(
                date,
                "%Y-%m-%d"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format."
            )
            return

        # Save to database
        self.db.add_expense(
            amount,
            category,
            description,
            date
        )

        # Success message
        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        # Clear fields
        self.amount_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
    0,
    tk.END
)

        self.category_entry.set("Food")

        self.description_entry.delete(
            0,
            tk.END
            )

        self.description_entry.delete(
            0,
            tk.END
        )

        # Reset date to today
        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # Refresh table
        self.refresh_expenses()

    # ==========================================================
    # REFRESH EXPENSES
    # ==========================================================

    def refresh_expenses(self):
        """Refresh the expense history table"""

        # Remove old rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get expenses
        expenses = self.db.get_all_expenses()

        # Add expenses to table
        for number, expense in enumerate(expenses, start=1):
            expense_id = expense[0]
            amount = expense[1]
            category = expense[2]
            description = expense[3]
            date = expense[4]

            self.tree.insert(
                "",
                tk.END,
                iid=str(expense_id),
                 values=(
                    number,
                    format_currency(amount),
                    category,
                    description,
                    date
                )
            ) 
        self.update_dashboard()
        # ==========================================================
    # SEARCH EXPENSES
    # ==========================================================

    def search_expenses(self):
        """Filter expenses by category or description"""

        search_text = self.search_var.get().strip().lower()

        # Remove current rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get all expenses
        expenses = self.db.get_all_expenses()

        # Filter expenses
        filtered_expenses = []

        for expense in expenses:

            category = str(expense[2]).lower()
            description = str(expense[3] or "").lower()

            if (
                search_text in category
                or search_text in description
            ):
                filtered_expenses.append(expense)

        # Display filtered expenses
        for number, expense in enumerate(
            filtered_expenses,
            start=1
        ):

            expense_id = expense[0]
            amount = expense[1]
            category = expense[2]
            description = expense[3]
            date = expense[4]

            self.tree.insert(
                "",
                tk.END,
                iid=str(expense_id),
                values=(
                    number,
                    format_currency(amount),
                    category,
                    description,
                    date
                )
            )

    def clear_search(self):
        """Clear the search box"""

        self.search_var.set("")

        self.refresh_expenses()
    # ==========================================================
    # UPDATE DASHBOARD
    # ==========================================================

    def update_dashboard(self):
        """Update dashboard statistics"""

        expenses = self.db.get_all_expenses()

        # Total number of expenses
        expense_count = len(expenses)

        # Total amount
        total_amount = sum(
            float(expense[1])
            for expense in expenses
        )

        # Current month
        current_month = datetime.now().strftime("%Y-%m")

        # Current month's total
        month_total = sum(
            float(expense[1])
            for expense in expenses
            if str(expense[4]).startswith(current_month)
        )

        # Update labels
        self.total_label.config(
            text=format_currency(total_amount)
        )

        self.month_label.config(
            text=format_currency(month_total)
        )

        self.count_label.config(
            text=str(expense_count)
        )
    # ==========================================================
    # EDIT EXPENSE
    # ==========================================================

    def edit_selected(self):
        """Edit the selected expense"""

        selected = self.tree.selection()

        # Check selection
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to edit."
            )
            return

        # Get selected row
        expense_id = int(selected[0])
        # Get original expense from database
        expense = self.db.get_expense_by_id(
            expense_id
        )

        if not expense:
            messagebox.showerror(
                "Error",
                "Expense could not be found."
            )
            return

        # Expense information
        _, amount, category, description, date, _ = expense

        # ------------------------------------------------------
        # Edit Window
        # ------------------------------------------------------

        edit_window = tk.Toplevel(
            self.root
        )

        edit_window.title(
            "Edit Expense"
        )

        edit_window.geometry(
            "400x350"
        )

        edit_window.resizable(
            False,
            False
        )

        edit_window.transient(
            self.root
        )

        edit_window.grab_set()

        # Title
        ttk.Label(
            edit_window,
            text="Edit Expense",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(15, 10)
        )

        # ------------------------------------------------------
        # Amount
        # ------------------------------------------------------

        ttk.Label(
            edit_window,
            text="Amount:"
        ).pack(
            pady=(5, 3)
        )

        amount_entry = ttk.Entry(
            edit_window,
            width=30
        )

        amount_entry.pack()

        amount_entry.insert(
            0,
            str(amount)
        )

        # ------------------------------------------------------
        # Category
        # ------------------------------------------------------

        ttk.Label(
            edit_window,
            text="Category:"
        ).pack(
            pady=(10, 3)
        )
        category_var = tk.StringVar()

        category_entry = ttk.Combobox(
            edit_window,
            textvariable=category_var,
            values=[
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Education",
            "Entertainment",
            "Health",
            "Other"
            ],
            width=27,
            state="readonly"
            )

        category_entry.pack()

        category_entry.set(category)

        # ------------------------------------------------------
        # Description
        # ------------------------------------------------------

        ttk.Label(
            edit_window,
            text="Description:"
        ).pack(
            pady=(10, 3)
        )

        description_entry = ttk.Entry(
            edit_window,
            width=30
        )

        description_entry.pack()

        description_entry.insert(
            0,
            description or ""
        )

        # ------------------------------------------------------
        # Date
        # ------------------------------------------------------

        ttk.Label(
            edit_window,
            text="Date (YYYY-MM-DD):"
        ).pack(
            pady=(10, 3)
        )

        date_entry = ttk.Entry(
            edit_window,
            width=30
        )

        date_entry.pack()

        date_entry.insert(
            0,
            date
        )

        # ------------------------------------------------------
        # Update function
        # ------------------------------------------------------

        def update_expense():

            new_amount = amount_entry.get().strip()
            new_category = category_entry.get().strip()
            new_description = description_entry.get().strip()
            new_date = date_entry.get().strip()

            # Required fields
            if not new_amount or not new_category or not new_date:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter amount, category and date.",
                    parent=edit_window
                )

                return

            # Validate amount
            try:

                new_amount = float(
                    new_amount
                )

                if new_amount <= 0:

                    messagebox.showwarning(
                        "Invalid Amount",
                        "Amount must be greater than 0.",
                        parent=edit_window
                    )

                    return

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid number.",
                    parent=edit_window
                )

                return

            # Validate date
            try:

                datetime.strptime(
                    new_date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date",
                    "Please use YYYY-MM-DD format.",
                    parent=edit_window
                )

                return

            # Update database
            success = self.db.update_expense(
                expense_id,
                new_amount,
                new_category,
                new_description,
                new_date
            )

            if success:

                self.refresh_expenses()

                messagebox.showinfo(
                    "Success",
                    "Expense updated successfully!",
                    parent=edit_window
                )

                edit_window.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    "Could not update the expense.",
                    parent=edit_window
                )

        # ------------------------------------------------------
        # Update Button
        # ------------------------------------------------------

        update_button = ttk.Button(
            edit_window,
            text="Update Expense",
            command=update_expense
        )

        update_button.pack(
            pady=20
        )
    def delete_selected(self):
        """Delete the selected expense"""

        selected = self.tree.selection()

        # Check selection
        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )

            return

        # Get selected row
        expense_id = int(selected[0])
        # Confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        # Delete
        success = self.db.delete_expense(
            expense_id
        )

        if success:

            self.refresh_expenses()

            messagebox.showinfo(
                "Deleted",
                "Expense deleted successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Could not delete the expense."
            )

    # ==========================================================
    # CLEAR ALL HISTORY
    # ==========================================================

    def clear_all_history(self):
        """Delete all expenses"""

        # Confirmation
        confirm = messagebox.askyesno(
            "Clear All History",
            "Are you sure you want to delete ALL expense history?\n\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        # Delete all
        self.db.clear_all_expenses()

        # Refresh table
        self.refresh_expenses()

        messagebox.showinfo(
            "History Cleared",
            "All expense history has been deleted."
        )

    # ==========================================================
    # MONTHLY SUMMARY
    # ==========================================================

    def open_summary(self):
        """Open the monthly summary window"""

        SummaryWindow(
            self.root,
            self.db
        )


# ==============================================================
# MAIN
# ==============================================================

def main():
    """Main entry point for the application"""

    root = tk.Tk()

    app = MainWindow(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()