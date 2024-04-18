const hrs = document.getElementById("hrs");
const min = document.getElementById("min");
const sec = document.getElementById("sec");
const colon = document.getElementById("colon");
let showSeconds = true; // Flag to track whether to display seconds or not

setInterval(() => {
  const currentTime = new Date();
  let currentHours = currentTime.getHours();
  const currentMinutes = currentTime.getMinutes();
  
  // Convert hours to 12-hour format
  if (currentHours > 12) {
    currentHours -= 12;
  } else if (currentHours === 0) {
    currentHours = 12;
  }

  hrs.innerHTML = (currentHours < 10 ? "0" : "") + currentHours;
  min.innerHTML = (currentMinutes < 10 ? "0" : "") + currentMinutes;

  if (showSeconds) {
    sec.style.display = "inline"; // Show the seconds
    colon.style.display = "inline"; // Show the colon
    sec.innerHTML = (currentTime.getSeconds() < 10 ? "0" : "") + currentTime.getSeconds();
  } else {
    sec.style.display = "none"; // Hide the seconds
    colon.style.display = "none"; // Hide the colon
  }
}, 1000);

// Function to toggle seconds display
document.addEventListener("DOMContentLoaded", () => {
  const checkbox = document.getElementById("showSeconds");
  checkbox.addEventListener("change", () => {
    toggleSeconds(checkbox);
  });
});

function toggleSeconds(checkbox) {
  showSeconds = checkbox.checked;
}
