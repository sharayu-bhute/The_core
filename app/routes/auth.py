from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.models import User, admin
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

@auth_bp.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('auth.login'))

    admin_user = admin.query.get(session['admin'])
    return render_template('admin_dashboard.html', admin=admin_user)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = user.id
            session['role'] = 'user'
            return redirect(url_for('auth.user_dashboard'))

        admin_user = admin.query.filter_by(admin_email=email).first()
        if admin_user and admin_user.admin_password == password:
            session['admin'] = admin_user.admin_id
            session['role'] = 'admin'
            return redirect(url_for('admin.admin_dashboard'))

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

        role = request.form.get('role_name')   # ✅ FIXED
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # 🔥 Check existing in BOTH tables
        existing_user = User.query.filter_by(email=email).first()
        existing_admin = admin.query.filter_by(admin_email=email).first()

        if existing_user or existing_admin:
            flash('User already exists', 'danger')
            return redirect(url_for('auth.signup'))

        # ✅ USER SIGNUP
        if role == 'user':
            new_user = User(
                name=name,
                email=email,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            flash('User registration successful', 'success')
            return redirect(url_for('auth.login'))

        # ✅ ADMIN SIGNUP
        elif role == 'admin':
            new_admin = admin(
                admin_name=name,
                admin_email=email,
                admin_password=password
            )

            db.session.add(new_admin)
            db.session.commit()

            flash('Admin registration successful', 'success')
            return redirect(url_for('auth.login'))

        else:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.signup'))

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