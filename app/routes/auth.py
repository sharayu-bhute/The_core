from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.form import LoginForm

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

# Temporary in-memory user storage (for hackathon)
USERS = {
    'admin@gmail.com': {'name': 'Admin', 'password': '123456'}
}
@auth_bp.route("/")
def home():
    return render_template("index.html")

@auth_bp.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for("auth.login"))
    return render_template("user_dashboard.html")



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = USERS.get(email)

        if user and user['password'] == password:
            session['user'] = email
            flash('Login successful', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in USERS:
            flash('User already exists', 'danger')
            return redirect(url_for('auth.signup'))

        USERS[email] = {
            'name': name,
            'password': password
        }

        flash('Signup successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/logout')
def logout():
    session.pop("user", None)
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login'))


@admin_bp.route('/admin')
def admin_dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    return render_template('admin_dashboard.html')