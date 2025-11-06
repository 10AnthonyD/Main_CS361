# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    from models.user import User
    from app import db

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('auth.register'))

        # Create new user and hash password
        new_user = User(username=username)
        new_user.set_password(password)  # Use the method we added to the model

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    from models.user import User

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
        if user and user.check_password(password):
            login_user(user)
            # Redirect to the main page after login
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for('auth.login'))  # Redirect to login page after logout
