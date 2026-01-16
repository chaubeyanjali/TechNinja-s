from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# 1. DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. DEFINE MODEL
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID is handled automatically
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False, unique=True)
    student_class = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(10), nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    class_teacher = db.Column(db.String(100), nullable=False)
    # Put the password here so it is linked to the student!
    password = db.Column(db.String(100), nullable=False) 

# 3. CREATE TABLES
with app.app_context():
    db.create_all()

# 4. ROUTES
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

@app.route('/register/student', methods=['GET', 'POST'])
def student_registration_step1():
    if request.method == 'POST':
       session['reg_name'] = request.form.get('name')
       session['reg_roll'] = request.form.get('roll_number')
       session['reg_class'] = request.form.get('class')
       session['reg_div'] = request.form.get('div')
       session['reg_stream'] = request.form.get('stream')
       session['reg_contact'] = request.form.get('contact')
       session['reg_email'] = request.form.get('email')
       session['reg_teacher'] = request.form.get('teacher')

       return redirect(url_for('student_registration_step2'))
    
    return render_template('StudentRegistration1.html')



@app.route('/register/student/step-2', methods=['GET', 'POST'])
def student_registration_step2():
    if request.method == 'POST':
        # Get password from the current form (Step 2)
        password_input = request.form.get('password')

        # Create one student record with data from Session (Step 1) + Form (Step 2)
        new_student = Student(
            full_name=session.get('reg_name'),
            roll_number=session.get('reg_roll'),
            student_class=session.get('reg_class'),
            division=session.get('reg_div'),
            stream=session.get('reg_stream'),
            phone=session.get('reg_contact'),
            email=session.get('reg_email'),
            class_teacher=session.get('reg_teacher'),
            password= generate_password_hash('password')
        )
        
        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('student_registration_step3'))
        except Exception as e:
            db.session.rollback()
            return f"Database Error: {e}"
    
    return render_template('StudentRegistration2.html')

@app.route('/register/student/success')
def student_registration_step3():
    session.clear() # Clear everything after success
    return render_template('StudentRegistration3.html')

if __name__ == '__main__':
    app.run(debug=True)