from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[
        DataRequired(message="Name is required")
    ])
    
    email = StringField("Email", validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])
    
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters")
    ])
    
    submit = SubmitField("Login")