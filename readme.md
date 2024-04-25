# FocusMate

## A Simple Web App to Boost Productivity

"During my coding bootcamp, I often lost track of time during timed exams and assignments. This challenge persists while coding, so I started using this app. As I continue to use and seek improvements, more features will be added. Feel free to run it locally."

### Technologies Used

- Flask
- Flask APIs
- MySQL
- Flask-Login
- BCrypt
- Jinja2
- TailwindCSS

### Installation Guide

#### 1. Install Python dependencies:
   Run the following command to install necessary Python packages:
   ```bash
   pipenv install PyMySQL flask flask-bcrypt
   ```

#### 2. Setting up MySQL database:
   Execute the following SQL commands to set up the database and tables:

   ```sql
   CREATE DATABASE focusmate;

   USE focusmate;

   CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       username VARCHAR(50) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
   );

   CREATE TABLE tasks (
       task_id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       title VARCHAR(100) NOT NULL,
       description TEXT,
       priority ENUM('Low', 'Medium', 'High') NOT NULL,
       deadline DATE,
       status ENUM('Pending', 'InProgress', 'Completed') NOT NULL DEFAULT 'Pending',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users (user_id)
   );

   -- Insert demo data into the users table
   INSERT INTO users (first_name, last_name, email, username, password_hash)
   VALUES
       ('John', 'Doe', 'john.doe@example.com', 'johndoe', 'hashed_password_1'),
       ('Jane', 'Smith', 'jane.smith@example.com', 'janesmith', 'hashed_password_2'),
       ('Alice', 'Johnson', 'alice.johnson@example.com', 'alicejohnson', 'hashed_password_3');

   -- Insert demo data into the tasks table
   INSERT INTO tasks (user_id, title, description, priority, deadline, status)
   VALUES
       (1, 'Complete project proposal', 'Write a proposal for the upcoming project.', 'High', '2024-04-15', 'InProgress'),
       (1, 'Prepare presentation slides', 'Create slides for the project presentation.', 'Medium', '2024-04-20', 'Pending'),
       (2, 'Review documentation', 'Review and update project documentation.', 'High', '2024-04-18', 'InProgress'),
       (3, 'Conduct user testing', 'Gather feedback from users on the new feature.', 'Medium', '2024-04-25', 'Pending');
   ```

#### 3. Setting up Tailwind CSS:
   Follow these steps within the `flask_app` directory to integrate Tailwind CSS:

   - Install Tailwind CSS:
     ```bash
     npm install -D tailwindcss
     ```

   - Generate a `tailwind.config.js` file:
     ```bash
     npx tailwindcss init
     ```

   - Configure the `tailwind.config.js` file to include:
     ```javascript
     module.exports = {
       content: ["./templates/**/*.html", "./static/src/**/*.js"],
       theme: { extend: {} },
       plugins: [],
     }
     ```

   - Set up the CSS file:
     Create a `static/src/input.css` file containing:
     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

   - Compile Tailwind CSS with watch mode:
     ```bash
     npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
     ```

#### 4. Integrating Tailwind CSS into your HTML template:
   Include the following link in the header of your HTML files to use the compiled CSS:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='dist/css/output.css') }}">
   ```

### Acknowledgments

Special thanks to [PythonAnywhere](https://www.pythonanywhere.com/) for hosting our web application, and to [BoxRadio](https://player.boxradio.net/) for providing the music player integrated into this project.

### Future Implentations
- [ ] Timer
- [ ] React Front-End for more responsive UI
---

