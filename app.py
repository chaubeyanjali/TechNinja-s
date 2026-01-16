from flask import Flask, render_template, redirect, url_for

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

if __name__ == '__main__':
    app.run(debug=True)