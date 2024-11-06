const vscode = acquireVsCodeApi();
const API_URL = "http://localhost:8080/api";
let sessionId = null;
// Initialize session
async function initializeSession() {
    const apiKey = prompt("Enter your API key:");
    const username = prompt("Enter your username:");
    if (!apiKey || !username) {
        alert("API key and username are required.");
        return;
    }
    try {
        const response = await fetch(`${API_URL}/initialize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ api_key: apiKey, username: username })
        });
        const data = await response.json();
        if (response.ok) {
            sessionId = data.session_id;
        } else {
            alert("Initialization failed: " + data.error);
        }
    } catch (error) {
        console.error("Error initializing session:", error);
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value;
    if (message) {
        const chatBox = document.getElementById('chatBox');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message'; // Add user message style
        messageDiv.textContent = message; // Use textContent to maintain original formatting
        chatBox.appendChild(messageDiv); // Add to chat
        input.value = '';
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content
        try {
            const response = await fetch(`${API_URL}/get_response`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message, session_id: sessionId })
            });

            const data = await response.json();
            if (response.ok) {
                displayCodeMessage(data.response); // Display server response
            } else {
                displayCodeMessage("Error: " + data.error);
            }
        } catch (error) {
            console.error("Error getting response:", error);
            displayCodeMessage("An error occurred while fetching response");
        }
    } else if (!sessionId) {
        alert("Session is not initialized. Please reload and try again.");
    }
}

// Display code message in chat box
function displayCodeMessage(code) {
    const chatBox = document.getElementById('chatBox');
    const codeMessageDiv = document.createElement('div');
    codeMessageDiv.className = 'message code-message';
    codeMessageDiv.textContent = code;
    chatBox.appendChild(codeMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Initialize session on page load
document.addEventListener("DOMContentLoaded", initializeSession);

// Bind button click event
document.getElementById('sendButton').onclick = sendMessage;

// Right-click menu triggers paste operation
document.addEventListener('contextmenu', event => {
    event.preventDefault();
    vscode.postMessage({ command: 'requestCodePaste' });
});

// Handling paste messages from plugins
window.addEventListener('message', event => {
    const message = event.data;
    if (message.command === 'pasteCode') {
        const input = document.getElementById('userInput');
        input.value += message.code; // Paste the code into the input box
    }
});

// Handle keyboard events
document.getElementById('userInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift + Enter newline
            const input = document.getElementById('userInput');
            input.value += '\\n'; // Add newline character
        } else {
            // Normal Enter key sends message
            sendMessage();
            event.preventDefault(); // Prevent line breaks from being inserted in a text area
        }
    }
});