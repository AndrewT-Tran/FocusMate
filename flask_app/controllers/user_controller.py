from flask import render_template, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_login import login_user, logout_user, login_required


@app.route('/create/user', methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/signup')

    user_id = User.create_user(request.form)
    if user_id:
        flash("Successfully created account",
              "success")  # Flash success message
        return redirect('/login?signup_successful=True')

    else:
        flash("Failed to create account", "error")  # Flash error message
        return redirect('/signup')


@app.route('/')
@login_required
def index():
    return redirect("/dashboard")


@app.route('/signup')
def newUser():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.checkuser_id(username=username, password=password)
        if user:
            login_user(user)
            # Corrected redirection syntax
            return redirect(f"/user/tasks/{user.user_id}")
        else:
            flash('Invalid username or password', "error")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
