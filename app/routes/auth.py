from flask import Blueprint,request,redirect,url_for,render_template,flash,session
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from 

auth_bp=Blueprint('auth',__name__)
USER_CREDENTIALS={'username':'admin','password':'1234'}


@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get("username")
        email=request.form.get("email",DataRequired())
        password=request.form.get("password",Length(min=6,max=20))
        if username==USER_CREDENTIALS['username'] and password==USER_CREDENTIALS['password']:
            session['user']=username
            flash('login successful','success')
        else:
            flash('invalid credentials','danger')   
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop("user",None)
    flash('logout successful','success')
    return redirect(url_for('auth.login'))