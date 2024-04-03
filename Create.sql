-- Create a new database named 'focusmate'
Create DATABASE focusmate;

-- Use the 'focusmate' database
USE focusmate;

-- Create the users table
CREATE TABLE
    users (
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
CREATE TABLE
    tasks (
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
INSERT INTO
    users (
        first_name,
        last_name,
        email,
        username,
        password_hash
    )
VALUES
    (
        'John',
        'Doe',
        'john.doe@example.com',
        'johndoe',
        'hashed_password_1'
    ),
    (
        'Jane',
        'Smith',
        'jane.smith@example.com',
        'janesmith',
        'hashed_password_2'
    ),
    (
        'Alice',
        'Johnson',
        'alice.johnson@example.com',
        'alicejohnson',
        'hashed_password_3'
    );

-- Insert demo data into the tasks table
INSERT INTO
    tasks (
        user_id,
        title,
        description,
        priority,
        deadline,
        status
    )
VALUES
    (
        1,
        'Complete project proposal',
        'Write a proposal for the upcoming project.',
        'High',
        '2024-04-15',
        'InProgress'
    ),
    (
        1,
        'Prepare presentation slides',
        'Create slides for the project presentation.',
        'Medium',
        '2024-04-20',
        'Pending'
    ),
    (
        2,
        'Review documentation',
        'Review and update project documentation.',
        'High',
        '2024-04-18',
        'InProgress'
    ),
    (
        3,
        'Conduct user testing',
        'Gather feedback from users on the new feature.',
        'Medium',
        '2024-04-25',
        'Pending'
    );