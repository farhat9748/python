"""
Student Management System - Flask Web Application
A modern web-based student management system with CRUD operations.
Data is stored in a local JSON file (no database required).
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "student_management_secret_key_2026"

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")


def load_students():
    """Load student records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        save_students([])
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_students(students):
    """Save student records to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)


def get_next_id(students):
    """Generate the next unique student ID."""
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


def load_users():
    """Load user records from the JSON file."""
    if not os.path.exists(USERS_FILE):
        save_users([])
        return []
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_users(users):
    """Save user records to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def get_next_user_id(users):
    if not users:
        return 1
    return max(u["id"] for u in users) + 1


# ─────────────────────────── DECORATORS ───────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "Admin":
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("user_dashboard"))
        return f(*args, **kwargs)
    return decorated_function


# ─────────────────────────── ROUTES ───────────────────────────

@app.route("/")
def home():
    """Home page."""
    if "user_id" in session:
        if session.get("role") == "Admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("user_dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user or admin."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "User").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("register"))

        users = load_users()
        if any(u["username"].lower() == username.lower() for u in users):
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for("register"))

        new_user = {
            "id": get_next_user_id(users),
            "username": username,
            "password": generate_password_hash(password),
            "role": role if role in ["Admin", "User"] else "User"
        }
        users.append(new_user)
        save_users(users)

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User and Admin login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        users = load_users()
        user = next((u for u in users if u["username"].lower() == username.lower()), None)

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            
            flash(f"Welcome back, {user['username']}!", "success")
            if user["role"] == "Admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out the current user."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Analytical dashboard for admins."""
    students = load_students()
    total_students = len(students)
    courses = set(s.get("course", "") for s in students)
    
    # Calculate some simple analytics
    genders = {"Male": 0, "Female": 0, "Other": 0}
    for s in students:
        gender = s.get("gender", "Other")
        if gender in genders:
            genders[gender] += 1
        else:
            genders["Other"] += 1
            
    recent_students = list(reversed(students))[:5] # last 5 added

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_courses=len(courses),
        genders=genders,
        recent_students=recent_students
    )


@app.route("/user/dashboard")
@login_required
def user_dashboard():
    """Simple dashboard for regular users."""
    students = load_students()
    return render_template(
        "user_dashboard.html",
        total_students=len(students)
    )


@app.route("/students")
@login_required
def view_students():
    """Display all students in a table."""
    students = load_students()
    return render_template("view_students.html", students=students)


@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_student():
    """Add a new student."""
    if request.method == "POST":
        students = load_students()

        new_student = {
            "id": get_next_id(students),
            "name": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "course": request.form.get("course", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
        }

        # Basic validation
        if not new_student["name"] or not new_student["course"]:
            flash("Name and Course are required fields!", "danger")
            return render_template("add_student.html")

        students.append(new_student)
        save_students(students)
        flash(f"Student '{new_student['name']}' added successfully!", "success")
        return redirect(url_for("view_students"))

    return render_template("add_student.html")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
@admin_required
def edit_student(student_id):
    """Edit an existing student's details."""
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("view_students"))

    if request.method == "POST":
        student["name"] = request.form.get("name", "").strip()
        student["age"] = request.form.get("age", "").strip()
        student["gender"] = request.form.get("gender", "").strip()
        student["course"] = request.form.get("course", "").strip()
        student["email"] = request.form.get("email", "").strip()
        student["phone"] = request.form.get("phone", "").strip()

        if not student["name"] or not student["course"]:
            flash("Name and Course are required fields!", "danger")
            return render_template("update_student.html", student=student)

        save_students(students)
        flash(f"Student '{student['name']}' updated successfully!", "success")
        return redirect(url_for("view_students"))

    return render_template("update_student.html", student=student)


@app.route("/delete/<int:student_id>", methods=["GET", "POST"])
@admin_required
def delete_student(student_id):
    """Delete a student record with confirmation page."""
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("view_students"))

    if request.method == "POST":
        students = [s for s in students if s["id"] != student_id]
        save_students(students)
        flash(f"Student '{student['name']}' deleted successfully!", "success")
        return redirect(url_for("view_students"))

    return render_template("delete_student.html", student=student)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_student():
    """Search for students by keyword."""
    students = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip().lower()
        all_students = load_students()

        if keyword:
            students = [
                s for s in all_students
                if keyword in str(s.get("id", "")).lower()
                or keyword in s.get("name", "").lower()
                or keyword in s.get("course", "").lower()
                or keyword in s.get("email", "").lower()
                or keyword in s.get("phone", "").lower()
            ]

    return render_template(
        "search_student.html",
        students=students,
        keyword=keyword,
    )




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)