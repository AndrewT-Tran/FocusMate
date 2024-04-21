const hrs = document.getElementById("hrs");
const min = document.getElementById("min");
const sec = document.getElementById("sec");
const colon = document.getElementById("colon");
let showSeconds = true; // Flag to track whether to display seconds or not

function updateClock() {
    const currentTime = new Date();
    let currentHours = currentTime.getHours();
    const currentMinutes = currentTime.getMinutes();
    const currentSeconds = currentTime.getSeconds();

    // Convert hours to 12-hour format and adjust display format
    if (currentHours > 12) {
        currentHours -= 12;
    } else if (currentHours === 0) {
        currentHours = 12;
    }

    hrs.textContent = (currentHours < 10 ? "0" : "") + currentHours;
    min.textContent = (currentMinutes < 10 ? "0" : "") + currentMinutes;

    // Conditionally display seconds and colon based on the showSeconds flag
    if (showSeconds) {
        sec.textContent = (currentSeconds < 10 ? "0" : "") + currentSeconds;
        sec.style.display = "inline";
        colon.style.display = "inline";
    } else {
        sec.style.display = "none";
        colon.style.display = "none";
    }
}

setInterval(updateClock, 1000); // Update the clock every second

document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("secondToggle"); // Updated to use the correct id
    checkbox.addEventListener('change', () => {
        showSeconds = checkbox.checked;
        updateClock(); // Update immediately on toggle
    });
});
