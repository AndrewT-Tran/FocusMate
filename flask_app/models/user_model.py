from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.task_model import Task
from flask_login import UserMixin
from flask import flash
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, data):
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tasks = []  # Add 'tasks' attribute

    def get_id(self):
        return str(self.user_id)

    @classmethod
    def create_user(cls, data, hashed_password):  # Add hashed_password as an argument
        query = """
            INSERT INTO users
            (first_name, last_name, email, username, password_hash, created_at, updated_at)
            VALUES
            (%(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password_hash)s, NOW(), NOW());
        """
        data['password_hash'] = hashed_password  # Assign hashed_password to the data dictionary
        user_id = connectToMySQL('focusmate').query_db(query, data)
        return user_id


    @classmethod
    def checkuser_id(cls, username, password):
        query = """
            SELECT * FROM users
            WHERE username = %(username)s;
        """
        data = {'username': username}
        user = connectToMySQL('focusmate').query_db(query, data)
        if user and bcrypt.check_password_hash(user[0]['password_hash'], password):
            user_data = {
                'user_id': user[0]['user_id'],
                'first_name': user[0]['first_name'],
                'last_name': user[0]['last_name'],
                'email': user[0]['email'],
                'username': user[0]['username'],
                'password_hash': user[0]['password_hash'],
                'created_at': user[0]['created_at'],
                'updated_at': user[0]['updated_at'],
            }
            return User(user_data)
        else:
            return None
    @staticmethod
    def validate(data, check_password=True):
        is_valid = True
        if len(data.get('first_name', '')) < 2:
            flash("What's your real name?", "first_name_error")
            is_valid = False
        if len(data.get('last_name', '')) < 2:
            is_valid = False
        if not EMAIL_REGEX.match(data.get('email', '')):
            is_valid = False
        if len(data.get('username', '')) < 1:
            is_valid = False

        # Check password only if check_password is True
        if check_password:
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
            if len(password) < 8:
                flash("Password must be at least 8 characters", "password_error")
                is_valid = False
            if password != confirm_password:
                flash("Passwords do not match", "confirm_password_error")
                is_valid = False

        return is_valid


    @classmethod
    def get_by_id(cls, user_id):
        query = """
            SELECT * FROM users
            LEFT JOIN tasks ON users.user_id = tasks.user_id
            WHERE users.user_id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL('focusmate').query_db(query, data)

        user = None
        tasks = []
        for row in results:
            if user is None:
                user_data = {
                    'user_id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'username': row['username'],
                    'password_hash': row['password_hash'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                }
                user = User(user_data)

            if row['task_id']:
                task_data = {
                    **row,
                    'task_id': row['task_id'],
                    'title': row['title'],
                    'description': row['description'],
                    'priority': row['priority'],
                    'deadline': row['deadline'],
                    'status': row['status'],
                    'created_at': row['tasks.created_at'],
                    'updated_at': row['tasks.updated_at']
                }
                tasks.append(Task(task_data))

        user.tasks = tasks
        return user
    @classmethod
    def update_user(cls, user_id, form_data):
        # Check and hash the password if present and not empty
        if 'password' in form_data and form_data['password'].strip():
            hashed_password = bcrypt.generate_password_hash(form_data['password']).decode('utf-8')
            form_data['password_hash'] = hashed_password
        else:
            # If no new password is provided, retain the old password hash
            # Fetch only if necessary
            existing_user = cls.get_by_id(user_id)
            if existing_user is not None:
                form_data['password_hash'] = existing_user.password_hash
            else:
                return False  # If the user does not exist, return False

        # Prepare the SQL query to update the user's data
        query = """
            UPDATE users
            SET
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s,
                username = %(username)s,
                password_hash = %(password_hash)s,
                updated_at = NOW()
            WHERE user_id = %(user_id)s;
        """
        params = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'username': form_data['username'],
            'password_hash': form_data['password_hash'],
            'user_id': user_id
        }

        # Execute the update query and handle potential errors
        try:
            connectToMySQL('focusmate').query_db(query, params)
            return True
        except Exception as e:
            logging.error(f"Error updating user {user_id}: {e}")
            return False

