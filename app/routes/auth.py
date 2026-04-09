from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.form import LoginForm


auth_bp = Blueprint('auth', __name__)

# Fixed credentials (email match + password length)
USER_CREDENTIALS = {'username': 'admin@gmail.com', 'password': '1234'}

@auth_bp.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    
    return render_template("index.html")
         
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.email.data
        password = form.password.data

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash('Login successful', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
        
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.pop("user", None)
    flash('logout successful', 'success')
    return redirect(url_for('auth.login'))