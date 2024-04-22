from flask import render_template, redirect, request, flash, url_for
from flask_app import app
from flask_app.models.task_model import Task
from flask_app.models.user_model import User
from flask_login import login_required, current_user
from datetime import date


@app.route('/dashboard')
@login_required
def dashboard():
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
        Task.update(task_id, task)  # Update the task
        flash("Task updated successfully", "success")
        return redirect('/dashboard')
    return render_template('edit_task.html', task=task)


@app.route('/add')
@login_required
def add_task():
    user = current_user  # Get the current user
    today_date = date.today().isoformat()
    return render_template("add_task.html", user=user,today_date=today_date)


@app.route('/post/task', methods=['POST'])
@login_required
def create_task():
    form_data = request.form.to_dict()
    form_data['user_id'] = current_user.user_id

    if not Task.validate(form_data):
        flash("Validation failed. Please check your inputs.", "error")
        return redirect('/add')

    Task.add_task(form_data)
    flash("Task added successfully", "success")
    return redirect(url_for('dashboard') + '#pending-tasks')

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    Task.delete(task_id)
    flash("Task deleted successfully", "success")
    return redirect('/dashboard')


@app.route('/mark_completed/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.status = 'Completed'
        Task.update({
                'task_id': task_id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'deadline': task.deadline,
                'status': task.status
            })
        flash("Task marked as completed", "success")
    else:
        flash("Task not found", "error")
    return redirect(url_for('dashboard') + '#main')

@app.route('/mark_in_progress/<int:task_id>')
@login_required
def mark_in_progress(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.status = 'InProgress'
        Task.update({
            'task_id': task_id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'deadline': task.deadline,
            'status': task.status
        })  # Update the task
        flash("Task marked as In Progress", "success")
    else:
        flash("Task not found", "error")
    return redirect(url_for('dashboard') + '#main')


@app.route('/mark_pending/<int:task_id>', methods=['GET'])
@login_required
def mark_pending(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.status = 'Pending'
        Task.update({
            'task_id': task_id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'deadline': task.deadline,
            'status': task.status
        })  # Update the task
        flash("Task marked as In Progress", "success")
    else:
        flash("Task not found", "error")
    return redirect(url_for('dashboard') + '#working-on')  # Redirect to the working-on section



@app.route('/test')
def testing():
    return render_template('index.html')

# Task Controller

@app.route('/update_priority/<int:task_id>', methods=['POST'])
@login_required
def update_priority(task_id):
    task = Task.get_by_id(task_id)  # Retrieve the task based on the task ID

    if task:
        new_priority = request.form.get('priority')
        if new_priority in ['High', 'Medium', 'Low']:
            # Set the new priority directly to the task object
            task.priority = new_priority
            Task.update({
                'task_id': task_id,
                'title': task.title,
                'description': task.description,
                'priority': new_priority,  # Update the priority here
                'deadline': task.deadline,
                'status': task.status
            })
            flash("Priority updated successfully", "success")
        else:
            flash("Invalid priority", "error")
    else:
        flash("Task not found", "error")

    # Redirect to the section on the dashboard page that directly shows the updated task
    return redirect(url_for('dashboard') + '#task-' + str(task_id))


@app.route('/clear_tasks/<int:user_id>')
@login_required
def delete_completed_tasks(user_id):
    Task.delete_completed_tasks(user_id)
    flash("Completed tasks deleted successfully", "success")
    return redirect(url_for('dashboard') + '#working-on')
