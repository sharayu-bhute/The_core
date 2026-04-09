from flask import Blueprint,request,redirect,url_for,render_template,flash,session
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from app.form import RegistrationForm
auth_bp=Blueprint('auth',__name__)
USER_CREDENTIALS={'username':'admin','password':'1234'}


@auth_bp.route('/login',methods=['GET','POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():  
        username = form.name.data
        email = form.email.data
        password = form.password.data
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash('Login successful', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.pop("user",None)
    flash('logout successful','success')
    return redirect(url_for('auth.login'))



