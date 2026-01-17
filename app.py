from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Added secret_key for sessions

# 1. DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. DEFINE MODELS (MUST be above routes)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Increased length for security
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False, unique=True)
    student_class = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(10), nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    class_teacher = db.Column(db.String(100), nullable=False)

class StudentPassword(db.Model):
    password = db.Column(db.String(100), unique=True)

# 3. CREATE TABLES
with app.app_context():
    db.create_all()

# 1. Home Page Route
@app.route('/')
def index():
    # This renders your main landing page with the 3 cards
    return render_template('index.html')

@app.route('/register/student')
def student_registration():
    return render_template('StudentRegistration1.html')

@app.route('/register/teacher')
def teacher_registration():
    return render_template('TeacherRegistration1.html')

@app.route('/register/admin')
def admin_registration():
    return render_template('AdminRegistration1.html')

# 3. Unified Registration Route (The one you wrote)
@app.route('/register/<role>')
def register(role):
    if role == 'student':
        return render_template('StudentRegistration1.html')
    elif role == 'teacher':
        return render_template('teacher_register.html')
    elif role == 'admin':
        return render_template('admin_register.html')
    else:
        # If someone types /register/xyz, send them back home
        return redirect(url_for('index'))

# Step 1: Student Basic Details
@app.route('/register/student', methods=['GET', 'POST'])
def student_registration_step1():
    if request.method == 'POST':
        # Store data from the first form into the session
        new_student = Student(
            full_name=session.get('reg_name'),
            roll_number=session.get('reg_roll'),
            student_class=session.get('reg_class'),
            division=session.get('reg_div'),
            stream=session.get('reg_stream'),
            phone=session.get('reg_contact'),
            email=session.get('reg_email'),
            class_teacher=session.get('reg_teacher')
        )
        
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('student_registration_step3'))
    
    return render_template('StudentRegistration1.html')

@app.route("/register/student", methods=["GET", "POST"])
def student_registration_step1():
    if request.method == "POST":
        # later you can save step-1 data in session or DB
        return redirect(url_for("student_registration_step2"))

    return render_template("StudentRegistration1.html")


@app.route("/register/student/step2", methods=["GET", "POST"])
def student_registration_step2():
    if request.method == "POST":
        # save final student data here
        return redirect(url_for("login"))

    return render_template("StudentRegistration2.html")


# Step 2:Student Login Details
@app.route('/register/student/step-2', methods=['GET', 'POST'])
def student_registration_step2():
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')

        
        
        new_student = StudentPassword(
            password=password,
        )

        db.session.add(new_student)
        db.session.commit()
        
        return redirect(url_for('student_registration_step3'))
    
    return render_template('StudentRegistration2.html')

# Step 3: Success Page
@app.route('/register/student/success')
def student_registration_step3():
    # Clear the session now that registration is done
    session.pop('reg_name', None)
    return render_template('StudentRegistration3.html')

if __name__ == '__main__':
    app.run(debug=True)