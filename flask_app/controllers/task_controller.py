from flask import render_template, redirect, request, flash
from flask_app import app
from flask_app.models.task_model import Task
from flask_app.models.user_model import User
from flask_login import login_required, current_user


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
    return render_template("add_task.html", user=user)


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
    return redirect('/dashboard')


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    Task.delete(task_id)
    flash("Task deleted successfully", "success")
    return redirect('/dashboard')


@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        task.status = 'Completed'
        Task.update(task_id, task)  # Update the task
        flash("Task marked as completed", "success")
    else:
        flash("Task not found", "error")
    return redirect('/dashboard')


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
    return redirect('/dashboard')


@app.route('/mark_pending/<int:task_id>')
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
    return redirect('/dashboard')


@app.route('/test')
def testing():
    return render_template('index.html')

# Task Controller


@app.route('/update_priority/<int:task_id>', methods=['POST'])
@login_required
def update_priority(task_id):
    # Get the task by ID
    task = Task.get_by_id(task_id)

    # Check if the task exists
    if task:
        # Get the new priority from the form data
        new_priority = request.form.get('priority')

        # Validate the new priority (optional step)
        if new_priority in ['High', 'Medium', 'Low']:
            # Update the task's priority
            task.priority = new_priority

            # Save the updated task
            Task.update({
                'task_id': task_id,
                'title': task.title,
                'description': task.description,
                'priority': new_priority,  # Update the priority
                'deadline': task.deadline,
                'status': task.status
            })

            # Flash a success message
            flash("Priority updated successfully", "success")
        else:
            # Flash an error message if the priority is invalid
            flash("Invalid priority", "error")
    else:
        # Flash an error message if the task doesn't exist
        flash("Task not found", "error")

    # Redirect back to the dashboard
    return redirect('/dashboard')
