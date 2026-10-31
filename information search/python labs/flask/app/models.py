from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=True, nullable=False)
    short_name = db.Column(db.String(50), unique=True, nullable=False)
    foundation_date = db.Column(db.Date, nullable=False)
    students = db.relationship(
        "Student", back_populates="university", cascade="all, delete-orphan"
    )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    university_id = db.Column(
        db.Integer, db.ForeignKey("university.id", ondelete="CASCADE"), nullable=False
    )
    admission_year = db.Column(db.Integer, nullable=False)
    university = db.relationship("University", back_populates="students")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
