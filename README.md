# 🎓 Student Management System

A modern, web-based Student Management System built with **Python Flask** and **Bootstrap 5**. Manage student records (Add, View, Search, Update, Delete) through a beautiful dark-themed browser interface. Data is stored in a lightweight JSON file — no database setup required.

---

## ✨ Features

- **Add Student** — Register new students with name, age, gender, course, email, and phone.
- **View Students** — Browse all student records in a responsive table.
- **Search Students** — Search by ID, name, course, email, or phone.
- **Update Student** — Edit existing student information.
- **Delete Student** — Remove records with a confirmation page.
- **Flash Messages** — Success/error feedback on every action.
- **Responsive Design** — Works on desktop, tablet, and mobile.

---

## 📁 Project Structure

```
StudentManagementSystem/
├── app.py                   # Flask application (routes + logic)
├── data.json                # JSON data store (auto-created)
├── README.md                # Project documentation
├── templates/
│   ├── base.html            # Base layout template
│   ├── home.html            # Dashboard / home page
│   ├── add_student.html     # Add student form
│   ├── view_students.html   # Student records table
│   ├── update_student.html  # Edit student form
│   ├── delete_student.html  # Delete confirmation page
│   └── search_student.html  # Search students page
└── venv/                    # Virtual environment (optional)
```

---

## 🚀 How to Run

### 1. Prerequisites

- **Python 3.7+** installed on your system
- **pip** (Python package manager)

### 2. Clone / Navigate to the Project

```bash
cd StudentManagementSystem
```

### 3. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (CMD):
venv\Scripts\activate.bat

# On macOS / Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open in Browser

Once the server starts, open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🛑 Stop the Server

Press `Ctrl + C` in the terminal to stop the Flask development server.

---

## 📦 Quick Start (All Commands)

```bash
cd StudentManagementSystem
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
pip install flask
python app.py
# Open http://127.0.0.1:5000 in your browser
```

---

## 🛠️ Tech Stack

| Technology    | Purpose                  |
|---------------|--------------------------|
| Python        | Backend language         |
| Flask         | Web framework            |
| Bootstrap 5   | Frontend UI framework    |
| JSON          | Data storage             |
| Jinja2        | Template engine          |

---

## 📄 License

This project is open source and available for educational purposes."# python" 
