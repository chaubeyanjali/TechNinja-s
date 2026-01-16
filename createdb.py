from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SAME DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- TEACHER TABLE ----------
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    teacher_id = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    subjects = db.Column(db.String(200))

# ---------- STUDENT TABLE ----------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(10), unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(10), nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    class_teacher = db.Column(db.String(100), nullable=False)

# ---------- CREATE TABLES ----------
with app.app_context():
    db.create_all()
    print("✅ Teacher & Student tables created successfully")