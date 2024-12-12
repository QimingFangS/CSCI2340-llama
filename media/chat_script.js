// Acquire the Visual Studio Code API to interact with the extension
const vscode = acquireVsCodeApi();
// const API_URL = "http://127.0.0.1:8080/api"; // Backend API URL
const API_URL = "http://127.0.0.1:8000"; // Backend API URL

let sessionId = null; // Session ID for user authentication
let selectedFileContent = "";
let selectedMode = null; // Default mode null
let selectedLanguage = null; //Default language null
let currentUser = null;
let currentSessionId = null; // Session ID for chat history

// DOM Elements Initialization
// Select the sidebar element
const sidebar = document.getElementById('sidebar');
// Select the button that toggles the sidebar
const toggleSidebarBtn = document.getElementById('toggleSidebar');
// Select the icon used to forcefully expand the sidebar
const toggleSidebarIcon = document.getElementById('toggleSidebarIcon');

// Additional UI Elements Initialization
const chatBox = document.getElementById('chatBox'); // Chatbox container
const historyList = document.getElementById('historyList'); // Chat history container
const userInput = document.getElementById('userInput'); // User input field
const newChatBtn = document.getElementById('newChatBtn'); // Button to create a new chat
const sendMessageBtn = document.getElementById('sendButton'); // Send message button

const messageBoxForLanguage = document.getElementById("messageBoxForLanguage");
const messageBoxForMode = document.getElementById("messageBoxForMode");

// Fetch the user's chat history from local storage
function getHistory() {
    const history = JSON.parse(localStorage.getItem('chatHistory')) || {}; // Retrieve chat history or initialize as empty object
    return history[currentUser] || []; // Return the history for the current user, or an empty array if not found
}

// Save user chat history to local storage
function saveHistory(sessionId, messages) {
    const history = JSON.parse(localStorage.getItem('chatHistory')) || {}; // Get or initialize chat history
    history[currentUser] = history[currentUser] || []; // Ensure a history array exists for the current user
    const sessionIndex = history[currentUser].findIndex(s => s.id === sessionId); // Search if session already exists
    if (sessionIndex >= 0) {
        history[currentUser][sessionIndex].messages = messages; // Update messages if session already exists
    } else {
        history[currentUser].push({ id: sessionId, timestamp: new Date().toISOString(), messages }); // Create a new session
    }
    localStorage.setItem('chatHistory', JSON.stringify(history)); // Save the updated history to local storage
    renderHistory(); // Re-render history UI to reflect changes
}

// Render the history list in the UI
function renderHistory() {
    if (currentSessionId === null) {
        console.log('Create a new sessionId.'); // Log message if no current session exists
        newSession();
    }
    console.log('sessionId existed. Rendering history list...');
    historyList.innerHTML = ''; // Clear the history list UI
    const history = getHistory(); // Fetch the history data
    console.log('history', history);
    
    if (history.length !== 0) {
        console.log('history', history);
        // Convert the history object to an array and sort by timestamp
        const sortedHistory = Object.values(history).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        
        // Iterate through the sorted history to dynamically create and display UI entries
        for (let i = 0; i < sortedHistory.length; i++) {
            const session = sortedHistory[i];
            const item = document.createElement('div');
            item.className = 'history-item';
            // Set UI text with "Chat-x" and formatted date
            item.textContent = `Chat-${i + 1}\n(${new Date(session.timestamp).toLocaleString()})`;
            
            // Attach a click listener to load this specific session when clicked
            item.addEventListener('click', () => loadSession(session.id));
            historyList.appendChild(item);
        }
    }
}

// Load a specific chat session by sessionId
function loadSession(sessionId) {
    console.log('sessionId', sessionId);
    const history = getHistory(); // Get user's chat history
    console.log('Loaded history:', history);
    
    const session = history.find(s => JSON.stringify(s.id) === JSON.stringify(sessionId)); // Find the session by ID
    console.log('cur session', session);

    if (session) {
        currentSessionId = sessionId; // Update the current session
        chatBox.innerHTML = ''; // Clear the current chatbox
        session.messages.forEach(msg => {
            const msgDiv = document.createElement('div');
            // msgDiv.textContent = `${msg.content}`;
            msgDiv.innerHTML = msg.content;
            // Style the message depending on role
            msgDiv.className = msg.role === 'user' ? 'message user-message' : 'message code-message';
            chatBox.appendChild(msgDiv); // Add message to the chat UI
        });
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest message
    } else {
        console.log(`Session with id ${JSON.stringify(sessionId)} not found.`);
    }
}

// Start a new chat session
function newSession() {
    const history = getHistory(); // Fetch chat history
    if (history.length === 0) {
        console.log('No history found. This is a new user.');
        currentSessionId = 'chat-' + Date.now(); // Create a new session ID
        return;
    }
    
    currentSessionId = 'chat-' + Date.now();
    // Create new session details
    const newSession = {
        id: currentSessionId,
        timestamp: new Date().toLocaleString(), // Set timestamp to the current date and time
        messages: [] // Initialize as empty message list
    };
    
    history.push(newSession); // Push the new session into history
    saveHistory(currentSessionId, newSession.messages); // Save the new session to storage
    chatBox.innerHTML = ''; // Clear the chatbox UI
    renderHistory(); // Refresh the history UI
}

// Function to send user message to the server -- generate_output
async function sendMessage() {
    const input = document.getElementById('userInput');
    if (!selectedLanguage) {
        messageBoxForLanguage.style.display = "block";
        return;
    }
    if (!selectedMode) {
        messageBoxForMode.style.display = "block";
        return;
    }
    // file display
    var message = input.value;
    if (fileDisplay.textContent !== '--No file selected--') {
        message += '\n\n<code>' + fileDisplay.textContent + '</code>';
    }

    console.log(message);
    if (message) {
        const chatBox = document.getElementById('chatBox');

        // Display the user's message in the chat box
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message'; // Add user message style
        // messageDiv.textContent = message; // Preserve original formatting
        messageDiv.innerHTML = message; // Format using html code
        chatBox.appendChild(messageDiv);

        // Create a loading spinner animation while waiting for a response
        const generatingDiv = document.createElement('div');
        generatingDiv.className = 'message generating-message'; // Loading message style
        generatingDiv.innerHTML = '<span class="spinner"></span>';
        chatBox.appendChild(generatingDiv);

        input.value = ''; // Clear input field
        // fileDisplay.textContent = '--No file selected--'; // Reset fileDisplay
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content

        try {
            // Send user query to the server
            const response = await fetch(`${API_URL}/generate_output`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mode: selectedMode,
                    code: message,
                    language: selectedLanguage
                })
            });
            const htmlContent = await response.text();
            console.log('HTML Content:', htmlContent);
            // debugging without backend
            const data = {
                "response": htmlContent
            };

            // Remove the loading spinner
            chatBox.removeChild(generatingDiv);

            // Display the server's response with a typing effect
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message code-message';
            chatBox.appendChild(botMessageDiv);

            // displayTextWithTypingEffect(botMessageDiv, data.response);
            displayHTMLWithTypingEffect(botMessageDiv, data.response);
            const history = getHistory();

            let session = history.find(s => s.id === currentSessionId);
            if (!session) {
                session = { id: currentSessionId, timestamp: new Date().toISOString(), messages: [] };
                history.push(session);
            } else {
                console.log('Previous chat found! Adding chat history to it now...');
            }
            session.messages.push({ role: 'user', content: message + '\n' + selectedFileContent });
            session.messages.push({ role: 'bot', content: data.response }); // save bot response
            saveHistory(currentSessionId, session.messages);

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

// Function to display HTML with a typing effect
function displayHTMLWithTypingEffect(element, html, callback) {
    const parser = new DOMParser();
    const parsedDoc = parser.parseFromString(html, 'text/html');
    const nodes = Array.from(parsedDoc.body.childNodes); // Get all child nodes of the parsed HTML
    let currentNodeIndex = 0; // Track which node we're currently typing
    let charIndex = 0; // Track character position within text nodes

    function typeCharacter() {
        if (currentNodeIndex >= nodes.length) {
            if (callback) {callback();} // Call the callback when done
            return;
        }

        const currentNode = nodes[currentNodeIndex];

        if (currentNode.nodeType === Node.TEXT_NODE) {
            // Handle text nodes
            const text = currentNode.textContent;
            if (charIndex < text.length) {
                element.innerHTML += text[charIndex];
                charIndex++;
            } else {
                charIndex = 0; // Reset for the next node
                currentNodeIndex++;
            }
        } else if (currentNode.nodeType === Node.ELEMENT_NODE) {
            // Handle element nodes
            const newElement = document.createElement(currentNode.nodeName);
            Array.from(currentNode.attributes).forEach(attr => {
                newElement.setAttribute(attr.name, attr.value);
            });
            element.appendChild(newElement); // Append the element to the parent

            // Recursively type the child nodes of the current element
            currentNodeIndex++; // Move to the next node
            displayHTMLWithTypingEffect(newElement, currentNode.innerHTML, typeCharacter);
            return; // Exit to let the recursion handle typing the child content
        }

        setTimeout(typeCharacter, 10); // Typing speed: 10ms per character
    }
    typeCharacter();
}

/** 
 * Event Listener: Open chat history
 */
toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.add('collapsed');
});

/** 
 * Event Listener: Close chat history
 */
toggleSidebarIcon.addEventListener('click', () => {
    sidebar.classList.remove('collapsed');
});

/** 
 * Event Listener: Close sidebar when clicking outside
 */
document.addEventListener('click', (event) => {
    const isClickInsideSidebar = sidebar.contains(event.target);
    const isClickToggleIcon = toggleSidebarIcon.contains(event.target);
    const isClickToggleBtn = toggleSidebarBtn.contains(event.target);
    if (!isClickInsideSidebar && !isClickToggleIcon && !isClickToggleBtn) {
        sidebar.classList.add('collapsed');
    }
});

/** 
 * Event Listener: Handle click on the file selection button to fetch available files
 */
document.getElementById('fileSelect').addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    console.log('Activate fileSelect!'); // Log activation for debugging purposes
    vscode.postMessage({ command: 'getFiles' }); // Send message to VSCode to retrieve files
});

/** 
 * Event Listener: Handle change in file selection and send the selected file path to VSCode
 */
document.getElementById('fileSelect').addEventListener('change', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    const selectedFilePath = event.target.value; // Capture the selected file path
    if (selectedFilePath) {
        vscode.postMessage({ command: 'readFile', filePath: selectedFilePath }); // Send the file path to VSCode
    }
});

/** 
 * Event Listener: Trigger message sending on clicking the send button
 */
document.getElementById('sendButton').addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    sendMessage(); // Call the sendMessage function
});

/** 
 * Event Listener: Initialize a new chat session on clicking the "new chat" button
 */
document.getElementById('newChatBtn').addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    newSession(); // Call the newSession function
});

/** 
 * Event Listener: Wait for webview DOM content to load and notify VSCode that it's ready
 */
window.addEventListener('DOMContentLoaded', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    console.log('Webview DOM content loaded'); 
    vscode.postMessage({ command: 'ready' }); // Notify VSCode that the webview is initialized
});

/** 
 * Event Listener: Handle changes in mode selection dropdown and log the selected mode
 */
document.getElementById('modeSelect').addEventListener('change', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    selectedMode = event.target.value; // Update the selected mode
    console.log('Selected Mode:', selectedMode); 
});

/** 
 * Event Listener: Handle changes in language selection dropdown and log the selected language
 */
document.getElementById('languageSelect').addEventListener('change', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    selectedLanguage = event.target.value; // Update the selected language
    console.log('Selected Language:', selectedLanguage);
});

/** 
 * Event Listener: Handle right-click for triggering custom code paste functionality
 */
document.addEventListener('contextmenu', (event) => {
    event.preventDefault(); // Prevent default context menu
    vscode.postMessage({ command: 'requestCodePaste' }); // Notify VSCode to trigger the paste functionality
});

/** 
 * Event Listener: Handle keyboard events in the input field for custom message handling
 */
document.getElementById('userInput').addEventListener('keydown', (event) => {
    event.stopPropagation(); // Prevent event from bubbling up to parent elements
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            const input = document.getElementById('userInput');
            input.value += '\n'; // Insert newline on Shift + Enter
        } else {
            sendMessage(); // Send message on Enter
            event.preventDefault(); // Prevent new line creation
        }
    }
});

/** 
 * Event Listener: Handle messages received from VSCode or other communication sources
 */
window.addEventListener('message', (event) => {
    const message = event.data; // Parse the incoming message

    switch (message.command) {
        /** 
         * Command: Populate the file dropdown with available files
         */
        case 'populateFiles':
            console.log("Files received:", message.files); // Log received file list
            const fileSelect = document.getElementById('fileSelect');
            fileSelect.innerHTML = '<option value="">--Choose a file--</option>'; // Clear the dropdown menu first

            // Loop through the received files and dynamically create dropdown options
            message.files.forEach((file) => {
                if (file) {
                    const option = document.createElement('option');
                    option.value = file;
                    option.textContent = file;
                    fileSelect.appendChild(option);
                } else {
                    console.error("Invalid file object:", file); // Log any invalid files
                }
            });
            break;

        /** 
         * Command: Handle received file content and determine programming language type
         */
        case 'fileContent':
            selectedFileContent = message.content; // Store file content
            const fileDisplay = document.getElementById('fileDisplay');
            fileDisplay.textContent = `Selected file: ${message.fileName}`; // Display the selected file's name

            // Determine the language type based on the file extension
            switch (fileDisplay.textContent.split('.').pop()) {
                case 'py':
                    selectedLanguage = 'Python';
                    break;
                case 'cpp':
                    selectedLanguage = 'C++';
                    break;
                case 'c':
                    selectedLanguage = 'C';
                    break;
                case 'cs':
                    selectedLanguage = 'C#';
                    break;
                case 'java':
                    selectedLanguage = 'Java';
                    break;
                case 'js':
                    selectedLanguage = 'JavaScript';
                    break;
                case 'ts':
                    selectedLanguage = 'TypeScript';
                    break;
                case 'rb':
                    selectedLanguage = 'Ruby';
                    break;
                case 'go':
                    selectedLanguage = 'Go';
                    break;
                case 'scala':
                    selectedLanguage = 'Scala';
                    break;
                case 'php':
                    selectedLanguage = 'PHP';
                    break;
                case 'css':
                    selectedLanguage = 'CSS';
                    break;
                case 'html':
                    selectedLanguage = 'HTML';
                    break;
                case 'dfy':
                    selectedLanguage = 'Dafny';
                    break;
                default:
                    selectedLanguage = '';
                    break;
            }
            break;

        /** 
         * Command: Handle session information and render user history
         */
        case 'setSessionId':
            sessionId = message.sessionId; // Store the session ID
            currentUser = message.username; // Store the username
            console.log('Received sessionId:', sessionId);
            console.log('Received currentUser:', currentUser);
            renderHistory(); // Call function to render the user's interaction history
            break;

        /** 
         * Command: Paste code into the user input area
         */
        case 'pasteCode':
            const input = document.getElementById('userInput');
            input.value += message.code; // Append the received code to the input field
            break;

        /** 
         * Default: Handle any unrecognized or unsupported messages
         */
        default:
            console.log("Unhandled message:", message);
    }
});
