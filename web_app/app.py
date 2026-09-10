from flask import Flask, render_template, request, redirect, url_for  # type: ignore[import-not-found]

from database import (
    create_table,
    get_all_expenses,
    add_expense,
    delete_expense,
    get_expense,
    update_expense,
    get_monthly_expenses,
    clear_all_expenses
)
app = Flask(__name__)


# Create database table when application starts
create_table()
@app.route("/")
def home():
    from datetime import datetime

    expenses = get_all_expenses()

    # Total spent across all expenses
    total_spent = sum(expense["amount"] for expense in expenses)

    # Total spent in the current month
    current_month = datetime.now().strftime("%Y-%m")
    monthly_expenses = get_monthly_expenses(current_month)
    this_month = sum(expense["amount"] for expense in monthly_expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total_spent=total_spent,
        this_month=this_month,
        expense_count=len(expenses)
    )

@app.route("/add", methods=["POST"])
def add():

    amount = request.form.get("amount")
    category = request.form.get("category")
    description = request.form.get("description")
    date = request.form.get("date")

    if amount and category and date:

        add_expense(
            float(amount),
            category,
            description,
            date
        )

    return redirect(url_for("home"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):

    delete_expense(expense_id)

    return redirect(url_for("home"))
@app.route("/clear-history", methods=["POST"])
def clear_history():
    clear_all_expenses()
    return redirect(url_for("home"))
@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):

    expense = get_expense(expense_id)

    if expense is None:
        return redirect(url_for("home"))

    if request.method == "POST":

        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        date = request.form.get("date")

        if amount and category and date:

            update_expense(
                expense_id,
                float(amount),
                category,
                description,
                date
            )

            return redirect(url_for("home"))

    return render_template(
        "edit_expense.html",
        expense=expense
    )
@app.route("/summary")
def summary():

    from datetime import datetime

    current_month = datetime.now().strftime("%Y-%m")

    expenses = get_monthly_expenses(current_month)

    total = sum(
        expense["amount"]
        for expense in expenses
    )

    category_totals = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        category_totals[category] = (
            category_totals.get(category, 0)
            + amount
        )

    return render_template(
        "summary.html",
        expenses=expenses,
        total=total,
        expense_count=len(expenses),
        category_totals=category_totals,
        current_month=current_month
    )
if __name__ == "__main__":
    app.run(debug=True)