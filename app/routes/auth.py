from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)


@auth_bp.route("/")
def home():
    return render_template("index.html")


@auth_bp.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session['user'])
    return render_template("index.html", user=user)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('auth.user_dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')
@auth_bp.route('/user-dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user'])
    return render_template('user_dashboard.html', user=user)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

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