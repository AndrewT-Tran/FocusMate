from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.task_model import Task
from flask_login import UserMixin
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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
    def create_user(cls, data):
        query = """
            INSERT INTO users 
            (first_name, last_name, email, username, password_hash, created_at, updated_at) 
            VALUES 
            (%(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password_hash)s, NOW(), NOW());
        """
        user_id = connectToMySQL('focusmate').query_db(query, data)
        return user_id

    @classmethod
    def checkuser_id(cls, username, password):
        query = """
            SELECT * FROM users
            WHERE username = %(username)s AND password_hash = %(password_hash)s;
        """
        data = {'username': username, 'password_hash': password}  # Assuming password is already hashed
        results = connectToMySQL('focusmate').query_db(query, data)
        if results:
            result = results[0]  # Get the first result
            user_data = {
                'user_id': result['user_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'username': result['username'],
                'password_hash': result['password_hash'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
            }
            return User(user_data)
        else:
            return None
        
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
        if len(data['last_name']) < 2:
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
        if len(data['username']) < 2:
            is_valid = False
        if len(data['password_hash']) < 8:
            is_valid = False
        if data['password_hash'] != data['confirm_password']:
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
