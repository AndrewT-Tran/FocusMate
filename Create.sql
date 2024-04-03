use focusmate;
-- Create the users table
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

-- Create the tasks table
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
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert sample data into the users table
INSERT INTO users (first_name, last_name, email, username, password_hash) VALUES
('John', 'Doe', 'john@example.com', 'johndoe', 'password_hash_1'),
('Jane', 'Smith', 'jane@example.com', 'janesmith', 'password_hash_2'),
('Michael', 'Johnson', 'michael@example.com', 'michaeljohnson', 'password_hash_3');

-- Insert sample data into the tasks table
INSERT INTO tasks (user_id, title, description, priority, deadline, status) VALUES
(1, 'Task 1', 'Description of Task 1', 'Medium', '2024-04-10', 'InProgress'),
(1, 'Task 2', 'Description of Task 2', 'High', '2024-04-15', 'Pending'),
(1, 'Do WORK', 'Description of Task 3', 'High', '2024-04-15', 'Pending'),
(2, 'Task 3', 'Description of Task 3', 'Low', '2024-04-20', 'Completed'),
(2, 'Task 4', 'Description of Task 4', 'High', '2024-04-25', 'Pending'),
(3, 'Task 5', 'Description of Task 5', 'Medium', '2024-04-30', 'InProgress');
