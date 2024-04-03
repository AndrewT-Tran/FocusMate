# Task Controller
from flask_app import app
from flask_login import current_user

from flask import render_template, redirect, request, flash
from flask_app.models.task_model import Task
from flask_app.models.user_model import User
from flask_login import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.user_id
    user = User.get_by_id(user_id)
    tasks = Task.get_by_user_id(user_id)
    return render_template('dashboard.html', user=user, tasks=tasks)

@app.route('/user/tasks/<int:user_id>')
@login_required
def show_user_tasks(user_id=None):
    if user_id is None:
        user_id = current_user.user_id
    user = User.get_by_id(user_id)
    tasks = Task.get_by_user_id(user_id)
    return render_template('dashboard.html', user=user, tasks=tasks)


@app.route('/edit/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.get_by_id(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.deadline = request.form['deadline']
        task.status = request.form['status']
        task.save()  # Assuming you have a save method in your Task model
        return redirect(f'/user/tasks/{task.user_id}')
    return render_template('edit_task.html', task=task)

@app.route('/add')
def addtask():
    # Fetch the current user
    user = User.get_by_id(current_user.user_id)
    return render_template("create_task.html", user=user)

@app.route('/post/task', methods=['POST'])
def create_task():
    # Fetch the current user
    user_id = current_user.user_id
    
    # Create a new dictionary with the form data
    form_data = dict(request.form)
    
    # Add the user_id to the form data
    form_data['user_id'] = user_id
    
    # Validate the task
    if not Task.validate(form_data):
        return redirect('/add')
    
    # Add the task with the updated form data
    Task.add_task(form_data)
    
    return redirect(f'/user/tasks/{user_id}')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    Task.delete(task_id)
    user_id = current_user.user_id  # Obtain the user_id of the current user
    return redirect(f"/user/tasks/{user_id}")  # Redirect to the user's tasks page

@app.route('/edit/<int:task_id>')
def update_task(task_id):
    return render_template('update_task.html', task=Task.get_one(task_id))

@app.route('/save', methods=['POST'])
def save_task():
    Task.update(request.form)
    return redirect('/dashboard')

@app.route('/update', methods=['POST'])
def update_task_save():
    # Retrieve form data
    form_data = {
        'task_id': request.form['task_id'],
        'title': request.form['title'],
        'description': request.form['description'],
        'priority': request.form['priority'],
        'deadline': request.form['deadline'],
        'status': request.form['status']
    }

    # Call the update method with form data
    Task.update(form_data)

    # Redirect to a page where the user can see the updated task
    return redirect('/dashboard')

