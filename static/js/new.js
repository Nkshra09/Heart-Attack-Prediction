// Get the button element using its ID
const button = document.getElementById('myButton');

// Add a click event listener to the button element
button.addEventListener('click', function(event) {
    // Add your code here to handle the button click event
    console.log('Button Clicked!');
    
    // Stop the event from propagating further
    event.stopPropagation();
});
