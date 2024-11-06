// webviewContent.ts

import * as vscode from 'vscode';

export function getWebviewContent(webview: vscode.Webview, context: vscode.ExtensionContext) {
    // 使用 webview.asWebviewUri 转换样式文件和脚本文件路径
    const styleUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'style.css')
    );

    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'script.js')
    );
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src ${webview.cspSource};">
        <title>Llama Co-pilot</title>
        <link rel="stylesheet" href="${styleUri}"> <!-- 引用外部 CSS -->
    </head>
    <body>
        <h1>Llama Co-pilot</h1>
        <div class="chat-box" id="chatBox">
            <p>Welcome to the Llama Co-pilot!</p>
        </div>
        <div class="input-area">
            <textarea id="userInput" placeholder="Type your message here" rows="5"></textarea>
            <button id="sendButton">Send</button>
        </div>
        <script src="${scriptUri}"></script> <!-- 引用外部 JS -->
    </body>
    </html>`;
}
//     return `<!DOCTYPE html>
//     <html lang="en">
//     <head>
//         <meta charset="UTF-8">
//         <meta name="viewport" content="width=device-width, initial-scale=1.0">
//         <title>Llama Co-pilot</title>
//         <style>
//             body {
//                 font-family: 'Arial', sans-serif;
//                 margin: 0;
//                 padding: 10px;
//                 background-color: #1e1e1e; /* Dark background */
//                 color: #ffffff; /* White font */
//             }
//             h1 {
//                 text-align: center;
//                 color: #007acc; /* Title color */
//                 font-size: 24px; /* Title font size */
//                 margin-bottom: 20px; /* Header bottom margin */
//             }
//             .chat-box {
//                 width: 100%;
//                 height: 400px;
//                 border: 1px solid #444; /* Border color */
//                 padding: 10px;
//                 overflow-y: auto;
//                 background-color: #2d2d2d; /* Chat box background color */
//                 border-radius: 5px; /* Border fillet */
//                 display: flex;
//                 flex-direction: column; /* Vertical layout */
//                 gap: 10px; /* The spacing between messages */
//             }
//             .message {
//                 padding: 10px;
//                 border-radius: 15px; /* Fillet corner */
//                 max-width: 80%; /* Maximum width */
//                 word-wrap: break-word; /* Auto wrap */
//                 position: relative; /* Provides positioning for pseudo-elements */
//                 white-space: pre-wrap; /* Keep whitespace and newlines */
//             }
//             .user-message {
//                 background-color: #007acc; /* User message background color */
//                 color: white; /* User message font color */
//                 align-self: flex-end; /* Justify right */
//             }
//             .code-message {
//                 background-color: #4d4d4d; /* Code block background color */
//                 color: #ffffff; /* Code block font color */
//                 border: 1px solid #555; /* Code block border */
//                 padding: 10px;
//                 border-radius: 5px; /* Code block rounded corners */
//                 white-space: pre-wrap; /* Keep whitespace and newlines */
//                 word-wrap: break-word; /* Auto wrap */
//             }
//             .input-area {
//                 display: flex;
//                 flex-direction: column; /* Vertical layout */
//                 margin-top: 10px;
//             }
//             .input-area textarea {
//                 flex: 1;
//                 padding: 10px;
//                 font-size: 14px;
//                 resize: none; /* Disallow resizing */
//                 border: 1px solid #444; /* Input box color */
//                 border-radius: 5px; /* Rounded corners of input box */
//                 background-color: #3d3d3d; /* Input box background color */
//                 color: #ffffff; /* Input box font color */
//             }
//             .input-area button {
//                 padding: 10px;
//                 background-color: #007acc; /* Button background color */
//                 color: white; /* Button font color */
//                 border: none;
//                 cursor: pointer;
//                 margin-top: 5px; /* Button top margin */
//                 border-radius: 5px; /* button rounded corners */
//                 transition: background-color 0.3s; /* Button background color transition effect */
//             }
//             .input-area button:hover {
//                 background-color: #005a9e; /* Button color on hover */
//             }
//         </style>
//     </head>
//     <body>
//         <h1>Llama Co-pilot</h1> <!-- Add title -->
//         <div class="chat-box" id="chatBox">
//             <p>Welcome to the Llama Co-pilot!</p>
//         </div>
//         <div class="input-area">
//             <textarea id="userInput" placeholder="Type your message here" rows="5"></textarea>
//             <button id="sendButton">Send</button>
//         </div>
//         <script>
//             const vscode = acquireVsCodeApi();
//             const API_URL = "http://localhost:8080/api";
//             let sessionId = null;
//             function sendMessage() {
//                 const input = document.getElementById('userInput');
//                 const message = input.value;
//                 if (message) {
//                     const chatBox = document.getElementById('chatBox');
//                     const messageDiv = document.createElement('div');
//                     messageDiv.className = 'message user-message'; // Add user message style
//                     messageDiv.textContent = message; // Use textContent to maintain original formatting
//                     chatBox.appendChild(messageDiv); // Add to chat
//                     input.value = '';
//                     chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content
//                 }
//             }

//             // Bind button click event
//             document.getElementById('sendButton').onclick = sendMessage;

//             // Right-click menu triggers paste operation
//             document.addEventListener('contextmenu', event => {
//                 event.preventDefault();
//                 vscode.postMessage({ command: 'requestCodePaste' });
//             });

//             // Handling paste messages from plugins
//             window.addEventListener('message', event => {
//                 const message = event.data;
//                 if (message.command === 'pasteCode') {
//                     const input = document.getElementById('userInput');
//                     input.value += message.code; // Paste the code into the input box
//                 }
//             });

//             // Handle keyboard events
//             document.getElementById('userInput').addEventListener('keydown', (event) => {
//                 if (event.key === 'Enter') {
//                     if (event.shiftKey) {
//                         // Shift + Enter newline
//                         const input = document.getElementById('userInput');
//                         input.value += '\\n'; // Add newline character
//                     } else {
//                         // Normal Enter key sends message
//                         sendMessage();
//                         event.preventDefault(); // Prevent line breaks from being inserted in a text area
//                     }
//                 }
//             });

//             function displayCodeMessage(code) {
//                 const chatBox = document.getElementById('chatBox');
//                 const codeMessageDiv = document.createElement('div');
//                 codeMessageDiv.className = 'message code-message'; // Add code message style
//                 codeMessageDiv.textContent = code; // Use textContent to maintain original formatting
//                 chatBox.appendChild(codeMessageDiv); // Add to chat
//                 chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest content
//             }
//         </script>
//     </body>
//     </html>`;
// }
