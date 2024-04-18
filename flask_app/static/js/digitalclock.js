let hrs = document.getElementById("hrs");
let min = document.getElementById("min");
let sec = document.getElementById("sec");
let colon = document.getElementById("colon");
let showSeconds = true; // Flag to track whether to display seconds or not

setInterval(() => {
  let currentTime = new Date();
  hrs.innerHTML =
    (currentTime.getHours() < 10 ? "0" : "") + currentTime.getHours();
  min.innerHTML =
    (currentTime.getMinutes() < 10 ? "0" : "") + currentTime.getMinutes();

  if (showSeconds) {
    sec.style.display = "inline"; // Show the seconds
    colon.style.display = "inline"; // Show the colon
    sec.innerHTML =
      (currentTime.getSeconds() < 10 ? "0" : "") + currentTime.getSeconds();
  } else {
    sec.style.display = "none"; // Hide the seconds
    colon.style.display = "none"; // Hide the colon
  }
}, 1000);

// Function to toggle seconds display
function toggleSeconds(checkbox) {
  showSeconds = checkbox.checked;
}