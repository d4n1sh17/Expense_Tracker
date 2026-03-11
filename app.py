from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "expense-tracker-secret"

DATABASE = os.path.join(os.path.dirname(__file__), "expenses.db")


def get_db_connection():
    """Create a SQLite connection and enable dictionary-like row access."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the expenses table on first run."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def validate_expense_form(form_data):
    """Validate form values and return clean data for DB operations."""
    errors = []

    title = form_data.get("title", "").strip()
    category = form_data.get("category", "").strip()
    amount_text = form_data.get("amount", "").strip()
    expense_date = form_data.get("expense_date", "").strip()

    if not title:
        errors.append("Title is required.")
    elif len(title) > 100:
        errors.append("Title must be under 100 characters.")

    if not category:
        errors.append("Category is required.")
    elif len(category) > 50:
        errors.append("Category must be under 50 characters.")

    amount = None
    if not amount_text:
        errors.append("Amount is required.")
    else:
        try:
            amount = float(amount_text)
            if amount <= 0:
                errors.append("Amount must be greater than 0.")
        except ValueError:
            errors.append("Amount must be a valid number.")

    if not expense_date:
        errors.append("Date is required.")
    else:
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")

    clean_data = {
        "title": title,
        "category": category,
        "amount": amount,
        "expense_date": expense_date,
    }
    return errors, clean_data


@app.route("/")
def index():
    """Show all expenses and simple dashboard stats."""
    expenses = []
    total_spent = 0.0
    total_records = 0
    latest_date = "-"

    try:
        conn = get_db_connection()
        expenses = conn.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()

        stats = conn.execute(
            "SELECT COUNT(*) AS total_records, COALESCE(SUM(amount), 0) AS total_spent FROM expenses"
        ).fetchone()
        total_records = stats["total_records"]
        total_spent = float(stats["total_spent"])

        latest = conn.execute(
            "SELECT expense_date FROM expenses ORDER BY expense_date DESC, id DESC LIMIT 1"
        ).fetchone()
        if latest:
            latest_date = latest["expense_date"]
        conn.close()
    except sqlite3.Error:
        flash("Could not load expenses due to a database error.", "error")

    return render_template(
        "index.html",
        expenses=expenses,
        total_spent=total_spent,
        total_records=total_records,
        latest_date=latest_date,
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    """Render add form and create a new expense."""
    if request.method == "POST":
        errors, clean_data = validate_expense_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_expense.html", form_data=request.form)

        try:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO expenses (title, category, amount, expense_date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    clean_data["title"],
                    clean_data["category"],
                    clean_data["amount"],
                    clean_data["expense_date"],
                ),
            )
            conn.commit()
            conn.close()
            flash("Expense added successfully.", "success")
            return redirect(url_for("index"))
        except sqlite3.Error:
            flash("Could not add expense due to a database error.", "error")
            return render_template("add_expense.html", form_data=request.form)

    return render_template("add_expense.html", form_data={})


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    """Render edit form and update the selected expense."""
    try:
        conn = get_db_connection()
        expense = conn.execute("SELECT * FROM expenses WHERE id = ?", (id,)).fetchone()
    except sqlite3.Error:
        flash("Could not access expense due to a database error.", "error")
        return redirect(url_for("index"))

    if not expense:
        conn.close()
        flash("Expense not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        errors, clean_data = validate_expense_form(request.form)

        if errors:
            conn.close()
            for error in errors:
                flash(error, "error")
            return render_template(
                "edit_expense.html", form_data=request.form, expense_id=id
            )

        try:
            conn.execute(
                """
                UPDATE expenses
                SET title = ?, category = ?, amount = ?, expense_date = ?
                WHERE id = ?
                """,
                (
                    clean_data["title"],
                    clean_data["category"],
                    clean_data["amount"],
                    clean_data["expense_date"],
                    id,
                ),
            )
            conn.commit()
            conn.close()
            flash("Expense updated successfully.", "success")
            return redirect(url_for("index"))
        except sqlite3.Error:
            conn.close()
            flash("Could not update expense due to a database error.", "error")
            return render_template(
                "edit_expense.html", form_data=request.form, expense_id=id
            )

    conn.close()
    return render_template("edit_expense.html", form_data=dict(expense), expense_id=id)


@app.route("/delete/<int:id>")
def delete_expense(id):
    """Delete an expense by id."""
    try:
        conn = get_db_connection()
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            flash("Expense not found.", "error")
        else:
            flash("Expense deleted successfully.", "success")
    except sqlite3.Error:
        flash("Could not delete expense due to a database error.", "error")

    return redirect(url_for("index"))


# Ensure table exists before the first request.
init_db()


if __name__ == "__main__":
    app.run(debug=True)
