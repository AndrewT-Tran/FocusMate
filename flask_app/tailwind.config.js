/** @type {import('tailwindcss').Config} */
module.exports = {
  extend: {
    colors: {
      'poppin-blue': '#243c5a',
    },
    fontFamily: {
      'poppins': ['Poppins', 'sans-serif']
    }
  },
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js,*.css"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}