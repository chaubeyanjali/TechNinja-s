from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# 1. DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. DEFINE MODEL
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID is handled automatically
    full_name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    # Put the password here so it is linked to the teacher!
    password = db.Column(db.String(100), nullable=False) 

# 3. CREATE TABLES
with app.app_context():
    db.create_all()

# 4. ROUTES
@app.route('/')
def index():
    # This renders your main landing page with the 3 cards
    return render_template('index.html')

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

@app.route('/register/teacher', methods=['GET', 'POST'])
def teacher_registration_step1():
    if request.method == 'POST':
       session['reg_name'] = request.form.get('name')
       session['reg_id'] = request.form.get('teacher_id')
       session['reg_contact'] = request.form.get('contact')
       session['reg_email'] = request.form.get('email')
       session['reg_subject'] = request.form.get('subject')

       return redirect(url_for('teacher_registration_step2'))
    
    return render_template('TeacherRegistration1.html')



@app.route('/register/teacher/step-2', methods=['GET', 'POST'])
def teacher_registration_step2():
    if request.method == 'POST':
        # Get password from the current form (Step 2)
        password_input = request.form.get('password')

        # Create one student record with data from Session (Step 1) + Form (Step 2)
        new_teacher = Teacher(
            full_name=session.get('reg_name'),
            teacher_id=session.get('reg_id'),
            phone=session.get('reg_contact'),
            email=session.get('reg_email'),
            subjects=session.get('reg_subjects'),
            password=password_input 
        )
        
        try:
            db.session.add(new_teacher)
            db.session.commit()
            return redirect(url_for('teacher_registration_step3'))
        except Exception as e:
            db.session.rollback()
            return f"Database Error: {e}"
    
    return render_template('TeacherRegistration2.html')

@app.route('/register/teacher/success')
def teacher_registration_step3():
    session.clear() # Clear everything after success
    return render_template('TeacherRegistration3.html')

if __name__ == '__main__':
    app.run(debug=True)