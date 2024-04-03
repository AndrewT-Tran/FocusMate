from flask import Flask
from flask_login import LoginManager  
from flask_app.models.user_model import User  # Import the User model

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view route
app.secret_key = 'keepitsecret'
db = "focusmate"

@login_manager.user_loader
def load_user(user_id):
    # Load and return the User object from the database based on user_id
    return User.get_by_id(user_id)

print('---------')
print('Success is the sum of small efforts,\nrepeated day in and day out.')
print('---------')
