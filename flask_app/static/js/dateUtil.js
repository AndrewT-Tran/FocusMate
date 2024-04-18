// Function to format date as "Month day, year"
function formatDate(dateString) {
	const options = { month: 'long', day: 'numeric', year: 'numeric' };
	const date = new Date(dateString);
	return date.toLocaleDateString('en-US', options);
}
