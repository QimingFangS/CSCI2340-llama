// Import the vscode module to interact with the Visual Studio Code API
import * as vscode from 'vscode';

// Import functions to generate HTML content for the webview
import { getWebviewContent } from './webviewContent';
import { getLoginPanel } from './loginContent';

// Activate the extension
export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "llama co-pilot" is now active!');

    // Register a command to open the standalone chat box
    let disposable = vscode.commands.registerCommand('chatbox.login', () => {
        console.log('Login init..');

        // Show login panel
        const loginPanel = vscode.window.createWebviewPanel(
            'loginChatbox', // Identifier for the webview
            'Login', // Title of the webview
            vscode.ViewColumn.Beside, // Open in a column beside the active editor
            {
                enableScripts: true, // Enable JavaScript in the webview
                retainContextWhenHidden: true, // Retain context to avoid refreshing
            }
        );

        // Set the HTML content for the login webview
        loginPanel.webview.html = getLoginPanel(loginPanel.webview, context);
        console.log('Waiting for login..');

        // Handle messages received from the login webview
        loginPanel.webview.onDidReceiveMessage(async (message) => {
            switch (message.command) {
                case 'submit': {
                    const { username, apiKey } = message;

                    // Initialize a session with the server
                    const sessionId = await initializeSession(username, apiKey);
                    if (sessionId) {
                        vscode.window.showInformationMessage(`Session initialized with ID: ${sessionId}`);
                        console.log('Session ID saved:', sessionId);

                        // Save session ID in the global state
                        await context.globalState.update('sessionId', sessionId);

                        // Dispose of the login panel
                        loginPanel.dispose();

                        // Open the chatbox panel
                        openChatboxPanel(context, sessionId, username);
                    } else {
                        vscode.window.showErrorMessage('Login failed. Please try again.');
                    }
                    return;
                }
            }
        });
    });

    // Add the disposable command to the context subscriptions for cleanup
    context.subscriptions.push(disposable);
}

// Function to open the chatbox panel
function openChatboxPanel(context: vscode.ExtensionContext, sessionId: string, username:string) {
    console.log('Sidebar chat box command executed');

    // Create a new webview panel for the chatbox
    const panel = vscode.window.createWebviewPanel(
        'sidebarChatbox', // Identifier for the webview
        'Sidebar Chat Box', // Title of the webview
        vscode.ViewColumn.Beside, // Open in a column beside the active editor
        {
            enableScripts: true, // Enable JavaScript in the webview
            retainContextWhenHidden: true, // Retain context to avoid refreshing
        }
    );

    // Set the HTML content for the webview
    panel.webview.html = getWebviewContent(panel.webview, context);

    // Handle messages from the webview
    panel.webview.onDidReceiveMessage((message) => {
        if (message.command === 'ready') { // Webview signals readiness
            panel.webview.postMessage({ command: 'setSessionId', sessionId: sessionId, username: username});
        }
    });

    // Listen for text selection changes in the editor
    vscode.window.onDidChangeTextEditorSelection((event) => {
        const editor = event.textEditor; // Get the active text editor
        const selection = editor.selection; // Get the current selection
        const selectedText = editor.document.getText(selection); // Get the selected text

        // Copy selected text to clipboard
        if (selectedText) {
            vscode.env.clipboard.writeText(selectedText); // Automatically copy selected text
        }
    });

    // Handle messages from the webview
    panel.webview.onDidReceiveMessage((message) => {
        switch (message.command) {
            case 'requestCodePaste': // Handle code paste requests
                pasteCodeToChatBox(panel); // Paste code into the chatbox
                return;
        }
    });

    panel.webview.onDidReceiveMessage(async (message) => {
        if (message.command === 'getFiles') {
            // Find all code files in the workspace
            // Python, C, C++, Java, C#, Javascript, TypeScript, Ruby, Go, Scala, PHP. HTML, CSS
            const files = await vscode.workspace.findFiles('**/*.{py,c,cpp,cs,java,js,ts,rb,go,scala,php,html,css}', '**/node_modules/**');
            const fileList = files.map((file) => file.fsPath);
            // Send the file list to the webview
            panel.webview.postMessage({ command: 'populateFiles', files: fileList });
        } else if (message.command === 'readFile') {
            const fileUri = vscode.Uri.file(message.filePath);
            const fileContent = await vscode.workspace.fs.readFile(fileUri);
            panel.webview.postMessage({
                command: 'fileContent',
                content: Buffer.from(fileContent).toString('utf8'),
                fileName: message.filePath.split(/[/\\]/).pop()
            });
        }
    });
}

// Interface representing the server API response
interface ApiResponse {
    message: boolean; // Indicates success or failure
    session_id: string; // Session ID returned by the server
    error?: string;   // Error message if the request fails
}

// Function to initialize a session with the server
async function initializeSession(username: string, apiKey: string) {
    try {
        const response = await fetch('http://127.0.0.1:8080/api/initialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, apiKey }),
        });

        const data = await response.json() as ApiResponse;
        if (response.ok) {
            vscode.window.showInformationMessage(`Welcome, ${username}!`);
            return data.session_id;
        } else {
            console.error(data.error || 'Failed to initialize session');
            return false;
        }
    } catch (error) {
        console.error('Error initializing session:', error);
        return false;
    }
}

// Function to paste code into the chatbox
async function pasteCodeToChatBox(panel: vscode.WebviewPanel) {
    const code = await vscode.env.clipboard.readText(); // Read text from the clipboard
    panel.webview.postMessage({ command: 'pasteCode', code: code }); // Send the code to the webview
}

// Deactivate the extension
export function deactivate() {}
