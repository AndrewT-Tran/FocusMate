from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Task:
    def __init__(self, data):
        self.task_id = data["task_id"]
        self.user_id = data["user_id"]
        self.title = data["title"]
        self.description = data["description"]
        self.priority = data["priority"]
        self.deadline = data["deadline"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks"
        results = connectToMySQL("focusmate").query_db(query)
        all_tasks = [cls(row) for row in results]
        return all_tasks

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM tasks WHERE user_id = %(user_id)s"
        data = {'user_id': user_id}
        results = connectToMySQL("focusmate").query_db(query, data)
        user_tasks = [cls(row) for row in results]
        return user_tasks

    @classmethod
    def add_task(cls, data):
        query = """
        INSERT INTO tasks
            (user_id,
            title,
            description,
            priority,
            deadline,
            status,
            created_at,
            updated_at)
        VALUES
            (%(user_id)s,
            %(title)s,
            %(description)s,
            %(priority)s,
            %(deadline)s,
            %(status)s,
            NOW(),
            NOW())
        """
        return connectToMySQL("focusmate").query_db(query, data)

    @classmethod
    def delete(cls, task_id):
        data = {
            'task_id': task_id
        }
        query = """
        DELETE FROM tasks
        WHERE task_id = %(task_id)s
        """
        connectToMySQL("focusmate").query_db(query, data)

    @classmethod
    def get_one(cls, task_id):
        data = {
            'task_id': task_id
        }
        query = """
            SELECT * FROM tasks where task_id = %(task_id)s
        """
        results = connectToMySQL("focusmate").query_db(query, data)

        if results:
            row = results[0]
            return cls(row)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE tasks SET
            title = %(title)s,
            description = %(description)s,
            priority = %(priority)s,
            deadline = %(deadline)s,
            status = %(status)s
            WHERE task_id = %(task_id)s
        """
        connectToMySQL("focusmate").query_db(query, data)

    @staticmethod
    def validate(form):
        is_valid = True

        if len(form["title"]) < 3:
            flash("Title must be at least 3 characters.", "title_error")
            is_valid = False

        if len(form["description"]) < 3:
            flash("Be a little more descriptive.", "description_error")
            is_valid = False

        if len(form["priority"]) < 1:
            flash("Please select a priority.")
            is_valid = False

        if len(form["deadline"]) < 1:
            flash("Please set deadline.")
            is_valid = False

        if len(form["status"]) < 1:
            flash("Set a status we can see how it's going so far?")
            is_valid = False

        return is_valid
