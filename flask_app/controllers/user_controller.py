from flask import render_template, redirect, request, flash, url_for
from flask_app import app
from flask_app.models.user_model import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
import logging
bcrypt = Bcrypt(app)


@app.route('/create/user', methods=['POST'])
def create_user():
    form_data = request.form.to_dict()  # Convert ImmutableMultiDict to dictionary

    # Check if username already exists
    query_username = "SELECT COUNT(*) FROM users WHERE username = %(username)s"
    result_username = connectToMySQL('focusmate').query_db(
        query_username, {'username': form_data['username']})
    if result_username[0]['COUNT(*)'] > 0:
        flash("Username already exists", "username_error")
        return redirect('/signup')

    # Check if email already exists
    query_email = "SELECT COUNT(*) FROM users WHERE email = %(email)s"
    result_email = connectToMySQL('focusmate').query_db(
        query_email, {'email': form_data['email']})
    if result_email[0]['COUNT(*)'] > 0:
        flash("Email already exists", "email_error")
        return redirect('/signup')

    if not User.validate(form_data):

        return redirect('/signup')

    # Hash the password before storing it in the database
    hashed_password = bcrypt.generate_password_hash(
        form_data['password']).decode('utf-8')

    user_id = User.create_user(form_data, hashed_password)
    if user_id:
        flash("Successfully created account, please log in", "success")
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


@app.route('/profile')
@login_required
def user_profile():
    # Retrieve user information from the database
    user_id = current_user.user_id
    user = User.get_by_id(user_id)
    # Render the template with user information
    return render_template('user_profile.html', user=user)

@app.route('/user/profile/edit')
@login_required
def user_profile_edit():
    # Retrieve user information from the database
    user_id = current_user.user_id
    user = User.get_by_id(user_id)  # This method should fetch the user based on ID

    if user is None:
        flash("User not found.", "error")
        return redirect(url_for('some_fallback_route'))  # Redirect to a fallback route if user is not found

    # Render the template with user information
    return render_template('edit_user.html', user=user)


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




@app.route('/user/update', methods=['POST'])
@login_required
def update_user_profile():
    form_data = request.form.to_dict()
    user_id = current_user.user_id

    # Validate the incoming data except for password fields unless a new password is entered
    if 'password' in form_data and form_data['password'].strip():  # Check if password field is not empty
        if form_data['password'] != form_data.get('confirm_password', ''):
            flash("Passwords do not match.", "error")
            return redirect(url_for('user_profile_edit'))
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(url_for('user_profile_edit'))
        # Hash the new password if provided and valid
        form_data['password_hash'] = bcrypt.generate_password_hash(form_data['password']).decode('utf-8')
    else:
        # If no new password is provided, remove password keys to avoid affecting the hash in the database
        form_data.pop('password', None)
        form_data.pop('confirm_password', None)
        form_data.pop('password_hash', None)

    # Validate other incoming data
    if not User.validate(form_data, check_password=False):  # Assuming you have modified validate to conditionally check passwords
        flash("Validation error: Please check your data.", "error")
        return redirect(url_for('user_profile_edit'))

    # Update the user's information
    if User.update_user(user_id, form_data):
        flash("User profile successfully updated.", "success")
    else:
        flash("Failed to update user profile.", "error")

    return redirect(url_for('user_profile'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
