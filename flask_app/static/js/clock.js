var showSeconds = true; // Set this variable to true to initially display seconds

function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    var ampm = hours >= 12 ? 'PM' : 'AM';

    // Convert hours to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12;

    // Add leading zeros if needed
    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;

    // Display the time in HH:MM:SS AM/PM format if showSeconds is true
    // Otherwise, display the time in HH:MM AM/PM format
    var timeString = hours + ":" + minutes;
    if (showSeconds) {
        timeString += ":" + seconds;
    }
    timeString += " " + ampm;
    document.getElementById('live-time').innerText = timeString;
}

// Call the updateClock function every second
setInterval(updateClock, 1000);

// Call updateClock once to immediately display the current time
updateClock();

// Function to toggle the display of seconds
function toggleSeconds() {
    showSeconds = !showSeconds;
    updateClock();
}
