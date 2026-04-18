import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import create_user, get_db, get_expenses_by_user, get_user_by_email, get_user_by_id, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        flash("All fields are required.")
        return render_template("register.html", form=request.form)

    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html", form=request.form)

    if get_user_by_email(email):
        flash("An account with that email already exists.")
        return render_template("register.html", form=request.form)

    create_user(name, email, generate_password_hash(password))
    flash("Account created! Please sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        flash("All fields are required.")
        return render_template("login.html")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.")
        return render_template("login.html")

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    expenses = get_expenses_by_user(session["user_id"])

    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    top_category = max(category_totals, key=category_totals.get) if category_totals else "—"
    max_category = max(category_totals.values(), default=0)

    # Format member since date: "15 Jan 2025"
    from datetime import datetime
    raw_date = user["created_at"] if user and user["created_at"] else ""
    try:
        member_since = datetime.strptime(raw_date[:10], "%Y-%m-%d").strftime("%-d %b %Y")
    except (ValueError, TypeError):
        member_since = ""

    # Build initials from name
    parts = (user["name"] if user else "").split()
    initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else (parts[0][:2].upper() if parts else "?")

    stats = {
        "total": sum(e["amount"] for e in expenses),
        "count": len(expenses),
        "top_category": top_category,
        "category_totals": category_totals,
        "max_category": max_category,
    }

    return render_template(
        "profile.html",
        expenses=expenses,
        stats=stats,
        user=user,
        initials=initials,
        member_since=member_since,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
