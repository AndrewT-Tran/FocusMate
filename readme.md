# FocusMate

## A Simple Web App to Boost Productivity

"During my coding bootcamp, I often lost track of time during timed exams and assignments. This challenge persists while coding, so I started using this app. As I continue to use and seek improvements, more features will be added. Feel free to run it locally."

### Technologies Used

- Flask
- Flask APIs
- MySQL
- Flask-Login
- Jinja2

### Installation Guide

1. Install Python dependencies:

   ```python
   pipenv install PyMySQL flask flask-bcrypt
   ```

2. Setting up Tailwind CSS:
   - Within the `flask_app` directory, install Tailwind CSS:

     ```node
     npm install -D tailwindcss
     ```

   - Generate a new `tailwind.config` file:

     ```node
     npx tailwind init
     ```

   - Update the generated `tailwind.config` file to include:

     ```js
     module.exports = {
       content: [
         "./templates/**/*.html",
         "./static/src/**/*.js"
       ],
       theme: {
         extend: {},
       },
       plugins: [],
     }
     ```

   - Create a `static/src/` folder and add an `input.css` file with:

     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

   - Compile and monitor Tailwind CSS:

     ```node
     npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
     ```

3. Integrating Tailwind CSS into your HTML template:
   - In the header of `index.html`, insert:

     ```html
     <link rel="stylesheet" href="{{ url_for('static', filename='dist/css/output.css') }}">
     ```

### Acknowledgments

We extend our gratitude to [BoxRadio](https://player.boxradio.net/) for providing the music player featured in this project.

- Music Player Courtesy of [BoxRadio](https://player.boxradio.net/)

---
