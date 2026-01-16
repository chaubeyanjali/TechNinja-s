from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

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
        session['reg_name'] = request.form.get('name')
        session['reg_roll'] = request.form.get('roll-number')
        session['reg_class'] = request.form.get('class')
        session['reg_div'] = request.form.get('div')
        session['reg_stream'] = request.form.get('stream')
        session['reg_contact'] = request.form.get('contact')
        session['reg_email'] = request.form.get('email')
        session['reg_teacher'] = request.form.get('teacher')
    
        return redirect(url_for('student_registration_step2'))
    
    return render_template('StudentRegistration1.html')

# Step 2: Login Details
@app.route('/register/student/step-2', methods=['GET', 'POST'])
def student_registration_step2():
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')

        session['reg_userid'] = request.form.get('userid')
        session['reg_password'] = request.form.get('password')
        
        id = session.get('reg_userid')
        password = session.get('reg_password')
        full_name = session.get('reg_name')
        roll_number = session.get('reg_roll')
        student_class = session.get('reg_class')
        division = session.get('reg_div')
        stream = session.get('reg_stream')
        phone = session.get('reg_contact')
        email = session.get('reg_email')
        class_teacher = session.get('reg_teacher')
        
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