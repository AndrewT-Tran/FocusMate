const hrs = document.getElementById("hrs");
const min = document.getElementById("min");
const sec = document.getElementById("sec");
const colon = document.getElementById("colon");
let showSeconds = true; // Flag to track whether to display seconds or not

setInterval(() => {
  const currentTime = new Date();
  const currentSeconds = currentTime.getSeconds();
  const currentMinutes = currentTime.getMinutes();

  hrs.innerHTML = (currentTime.getHours() < 10 ? "0" : "") + currentTime.getHours();
  min.innerHTML = (currentMinutes < 10 ? "0" : "") + currentMinutes;

  if (showSeconds) {
    sec.style.display = "inline"; // Show the seconds
    colon.style.display = "inline"; // Show the colon
    sec.innerHTML = (currentSeconds < 10 ? "0" : "") + currentSeconds;
  } else {
    sec.style.display = "none"; // Hide the seconds
    colon.style.display = "none"; // Hide the colon
  }
}, 1000);

// Function to toggle seconds display
function toggleSeconds(checkbox) {
  showSeconds = checkbox.checked;
}