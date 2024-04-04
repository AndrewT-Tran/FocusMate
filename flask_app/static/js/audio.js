const audioPlayer = document.getElementById("audio-player");
const playPauseBtn = document.getElementById("play-pause-btn");
const trackTitle = document.getElementById("track-title");

playPauseBtn.addEventListener("click", () => {
	if (audioPlayer.paused) {
		audioPlayer.play();
		playPauseBtn.textContent = "Pause";
	} else {
		audioPlayer.pause();
		playPauseBtn.textContent = "Play";
	}
});

audioPlayer.addEventListener("play", () => {
	playPauseBtn.textContent = "Pause";
});

audioPlayer.addEventListener("pause", () => {
	playPauseBtn.textContent = "Play";
});
