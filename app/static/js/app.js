function fillCircle(percentage) {
    const circle = document.getElementById('circle');
    const percent = Math.min(Math.max(percentage, 0), 100); // Ensure percentage is between 0 and 100

    // Set the background with animation
    setTimeout(() => {
        circle.className = `circle ${percent >= 70 ? 'green' : 'red'}`; // Change class based on percentage
        circle.style.background = `conic-gradient(${percent >= 70 ? 'green' : 'red'} 0% ${percent}%, lightgray ${percent}% 100%)`; // Create conic gradient
    }, 100); // Delay to allow animation

    // Update the text content
    document.getElementById('percentage').textContent = `${percent}%`;
}

// Assuming you are passing the percentage dynamically from the backend
// For example, let's set a sample score here. This can be dynamically set when the page loads.
window.onload = function() {
    // Assuming the 'percentage' value is passed from the backend or JavaScript variable
    const percentage = 85; // Replace with actual percentage from the backend or user input
    fillCircle(percentage); // Call the function to fill the circle with the percentage
};