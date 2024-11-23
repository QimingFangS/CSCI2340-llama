// Acquire the Visual Studio Code API to interact with the extension
const vscode = acquireVsCodeApi();
const API_URL = "http://127.0.0.1:8080/api"; // Backend API URL
let sessionId = null; // Session ID for user authentication

// Function to send user message to the server
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value;

    if (message) {
        const chatBox = document.getElementById('chatBox');

        // Display the user's message in the chat box
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message'; // Add user message style
        messageDiv.textContent = message; // Preserve original formatting
        chatBox.appendChild(messageDiv);

        // Create a loading spinner animation while waiting for a response
        const generatingDiv = document.createElement('div');
        generatingDiv.className = 'message generating-message'; // Loading message style
        generatingDiv.innerHTML = '<span class="spinner"></span>';
        chatBox.appendChild(generatingDiv);

        input.value = ''; // Clear input field
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content

        try {
            // Send user query to the server
            const response = await fetch(`${API_URL}/get_response`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message, session_id: sessionId })
            });

            const data = await response.json();

            // Remove the loading spinner
            chatBox.removeChild(generatingDiv);

            // Display the server's response with a typing effect
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message code-message';
            chatBox.appendChild(botMessageDiv);
            displayTextWithTypingEffect(botMessageDiv, data.response);
        } catch (error) {
            // Handle errors and display a message in the chat box
            console.error("Error getting response:", error);
            chatBox.removeChild(generatingDiv);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'message code-message';
            errorDiv.textContent = 'Error: ' + error.message;
            chatBox.appendChild(errorDiv);
        }
    } else {
        alert("No Input!"); // Alert the user if input is empty
    }
}

// Function to display text with a typing effect
function displayTextWithTypingEffect(element, text, callback) {
    let index = 0;
    const interval = setInterval(() => {
        if (index < text.length) {
            element.textContent += text[index];
            index++;
            const chatBox = document.getElementById('chatBox');
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content
        } else {
            clearInterval(interval);
            if (callback) {
                callback();
            }
        }
    }, 10); // Typing speed: 10ms per character
}

// Bind the send button to the sendMessage function
document.getElementById('sendButton').onclick = sendMessage;

// Initialize the webview and set up message listeners
window.addEventListener('DOMContentLoaded', () => {
    console.log('Webview DOM content loaded');
    vscode.postMessage({ command: 'ready' });

    // Listen for messages from the extension
    window.addEventListener('message', (event) => {
        const message = event.data;
        if (message.command === 'setSessionId') {
            sessionId = message.sessionId; // Store the session ID
            console.log('Received sessionId:', sessionId);
        }
    });
});

// Handle right-click context menu for code paste
document.addEventListener('contextmenu', (event) => {
    event.preventDefault(); // Prevent default context menu
    vscode.postMessage({ command: 'requestCodePaste' });
});

// Handle messages for code pasting from the extension
window.addEventListener('message', (event) => {
    const message = event.data;
    if (message.command === 'pasteCode') {
        const input = document.getElementById('userInput');
        input.value += message.code; // Append the pasted code to the input field
    }
});

// Handle keyboard events in the input field
document.getElementById('userInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift + Enter inserts a newline
            const input = document.getElementById('userInput');
            input.value += '\n';
        } else {
            // Enter sends the message
            sendMessage();
            event.preventDefault(); // Prevent a new line from being added
        }
    }
});
