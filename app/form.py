from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    
    name=StringField("Full Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(), Email()])
    password=PasswordField("password",validators=[Length(min=6)])
    submit=SubmitField("Register")
    
    