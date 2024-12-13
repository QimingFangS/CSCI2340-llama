// Acquire the Visual Studio Code API to communicate with the extension
const vscode = acquireVsCodeApi();

// Add an event listener to handle the login form submission
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting and refreshing the page

    // Get the username and API key from the input fields
    const username = document.getElementById('username').value;
    const apiKey = document.getElementById('apiKey').value;

    // Send the username and API key to the VSCode extension
    vscode.postMessage({
        command: 'submit', // Command identifier for the extension
        username: username, // User's inputted username
        apiKey: apiKey      // User's inputted API key
    });
});

// Listen for messages from the VSCode extension
window.addEventListener('message', event => {
    const message = event.data;

    // If the extension sends an error message, display it as an alert
    if (message.command === 'error') {
        alert(message.text); // Show the error message text
    }
});
