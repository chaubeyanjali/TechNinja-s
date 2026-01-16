from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ---------------- APP CONFIG ----------------
app = Flask(__name__)
app.secret_key = "edu_schedule_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- STUDENT MODEL ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False, unique=True)
    student_class = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(10), nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    class_teacher = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ---------------- TEACHER MODEL ----------------
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ---------------- ADMIN MODEL ----------------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# ---------------- LOGIN REQUIRED DECORATOR ----------------
@app.route('/')
def index():
    # This renders your main landing page with the 3 cards
    return render_template('index.html')

@app.route('/signin')
def signin():
    # This renders your main landing page with the 3 cards
    return render_template('Signin.html')

@app.route('/register/<role>')
def register(role):
    if role == 'student':
        return render_template('StudentRegistration1.html')
    elif role == 'teacher':
        return render_template('TeacherRegistration1.html')
    elif role == 'admin':
        return render_template('AdminRegistration1.html')
    else:
        # If someone types /register/xyz, send them back home
        return redirect(url_for('index'))

def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "role" not in session or session["role"] != role:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ---------------- LOGIN ROUTE ---------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        user = None

        # ---- ADMIN LOGIN ----
        if role == "admin":
            user = Admin.query.filter_by(admin_id=user_id).first()

        # ---- TEACHER LOGIN ----
        elif role == "teacher":
            user = Teacher.query.filter_by(teacher_id=user_id).first()

        # ---- STUDENT LOGIN ----
        elif role == "student":
            user = Student.query.filter_by(roll_number=user_id).first()

        if user and check_password_hash(user.password, password):
            session["role"] = role
            session["user_id"] = user_id

            if role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif role == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ---------------- DASHBOARDS ----------------
@app.route("/admin/dashboard")
@login_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/admin/dashboard/edit_timetable")
@login_required("admin")
def admin_dashboard1():
    return render_template("admin_dashboard1.html")

@app.route("/admin/dashboard/post_notice")
@login_required("admin")
def admin_dashboard2():
    return render_template("admin_dashboard2.html")

@app.route("/admin/dashboard/view_notice")
@login_required("admin")
def admin_dashboard3():
    return render_template("admin_dashboard3.html")

@app.route("/admin/dashboard/view_request")
@login_required("admin")
def admin_dashboard4():
    return render_template("admin_dashboard4.html")


@app.route("/teacher/dashboard")
@login_required("teacher")
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

@app.route("/teacher/dashboard/availability")
@login_required("teacher")
def teacher_dashboard2():
    return render_template("teacher_dashboard1.html")

@app.route("/teacher/dashboard/view_timetable")
@login_required("teacher")
def teacher_dashboard3():
    return render_template("teacher_dashboard2.html")

@app.route("/teacher/dashboard/view_notice")
@login_required("teacher")
def teacher_dashboard4():
    return render_template("teacher_dashboard3.html")

@app.route("/teacher/dashboard/post_notice")
@login_required("teacher")
def teacher_dashboard5():
    return render_template("teacher_dashboard4.html")

@app.route("/teacher/dashboard/send_request")
@login_required("teacher")
def teacher_dashboard5():
    return render_template("teacher_dashboard5.html")

@app.route("/student/dashboard")
@login_required("student")
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/student/dashboard/view_notice")
@login_required("student")
def student_dashboard1():
    return render_template("student_dashboard1.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- INIT DB ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
