from flask import render_template, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
bcrypt = Bcrypt(app)


@app.route('/create/user', methods=['POST'])
def create_user():
    form_data = request.form.to_dict()  # Convert ImmutableMultiDict to dictionary

    # Check if username already exists
    query_username = "SELECT COUNT(*) FROM users WHERE username = %(username)s"
    result_username = connectToMySQL('focusmate').query_db(
        query_username, {'username': form_data['username']})
    if result_username[0]['COUNT(*)'] > 0:
        flash("Username already exists", "error")
        return redirect('/signup')

    # Check if email already exists
    query_email = "SELECT COUNT(*) FROM users WHERE email = %(email)s"
    result_email = connectToMySQL('focusmate').query_db(
        query_email, {'email': form_data['email']})
    if result_email[0]['COUNT(*)'] > 0:
        flash("Email already exists", "error")
        return redirect('/signup')

    if not User.validate(form_data):
        return redirect('/signup')

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(
        form_data['password']).decode('utf-8')

    user_id = User.create_user(form_data, hashed_password)
    if user_id:
        flash("Successfully created account", "success")
        return redirect('/login')
    else:
        flash("Failed to create account", "error")
        return redirect('/signup')


@app.route('/')
def index():
    if current_user.is_authenticated:  # Check if user is logged in
        return redirect('/dashboard')  # Redirect logged-in user to dashboard
    # Render login page for non-logged-in user
    return render_template('login.html')


@app.route('/signup')
def newUser():
    return render_template('signup.html')


@app.route('/user/profile')
@login_required
def user_profile():
    # Retrieve user information from the database
    user_id = current_user.user_id
    user = User.get_by_id(user_id)
    # Render the template with user information
    return render_template('user_profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.checkuser_id(username=username, password=password)
        if user:
            login_user(user)
            return redirect('/dashboard')  # Redirect to the dashboard page
        else:
            flash('Invalid username or password', "error")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
