**# FocusMate**

## Simple Web App to Enhance Productivity

"During my time in a coding bootcamp, we had timed exams and assignments and always found myself losing track of time. Nowadays, I still have the same problem while coding, so here is an app that I personally use. Features will be added as soon as I continue to use and look to make improvements. Feel free to run locally."

### Tech Used

- Flask
- Flask APIs
- MySQL
- Flask-Login
- Jinja2

### Installation Guide

1. Install Python dependencies:
   ```
   pipenv install PyMySQL flask flask-bcrypt
   ```

2. Set up Tailwind CSS:
   - Inside the `flask_app` directory, install Tailwind CSS:
     ```
     npm install -D tailwindcss
     ```

   - Create a new `tailwind.config` file:
     ```
     npx tailwind init
     ```

   - Edit the generated `tailwind.config` file to include:
     ```javascript
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

   - Create a new folder `static/src/` and add `input.css` with:
     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

   - Compile and watch Tailwind CSS:
     ```
     npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
     ```

3. Include Tailwind CSS in the HTML template:
   - Add the following line in the header of `index.html`:
     ```html
     <link rel="stylesheet" href="{{ url_for('static', filename='dist/css/output.css') }}">
     ```

### Credits

We would like to thank [BoxRadio](https://player.boxradio.net/) for providing the music player used in this project.

- Music Player: [BoxRadio](https://player.boxradio.net/)

---

