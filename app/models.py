from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)  # Gamification

    complaints = db.relationship("Complaint", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

class admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(120), unique=True, nullable=False)
    admin_password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Admin {self.admin_email}>"

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(15))

    complaints = db.relationship("Complaint", backref="department", lazy=True)

    def __repr__(self):
        return f"<Department {self.name}>"


class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    # Complaint Details
    image_path = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    issue_type = db.Column(db.String(50))  # pothole / garbage / water

    # Location
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(200))

    # Status Tracking
    status = db.Column(
        db.String(20),
        default="Pending"  # Pending / Working / Done / Delayed
    )

    # Authority Assigned
    assigned_to = db.Column(db.String(100))  # Officer name

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Complaint {self.id} - {self.status}>"