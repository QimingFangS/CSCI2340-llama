// Import the vscode module to interact with the Visual Studio Code API
import * as vscode from 'vscode';
// Import the function to get HTML content for the webview
import { getWebviewContent } from './webviewContent';

// Activate the extension
export function activate(context: vscode.ExtensionContext) {
    // Register a command to open the chat box
    let disposable = vscode.commands.registerCommand('chatbox.open', () => {
        // Create a new webview panel for the chat box
        const panel = vscode.window.createWebviewPanel(
            'chatbox', // Identifier for the webview
            'Chat Box', // Title of the webview
            vscode.ViewColumn.One, // Show the webview in the first column
            {
                enableScripts: true // Enable JavaScript in the webview
            }
        );

        // Set the HTML content for the webview
        panel.webview.html = getWebviewContent();

        // Listen for changes in text editor selection
        vscode.window.onDidChangeTextEditorSelection(event => {
            const editor = event.textEditor; // Get the active text editor
            const selection = editor.selection; // Get the current selection
            const selectedText = editor.document.getText(selection); // Get the selected text

            // If there is selected text, copy it to the clipboard
            if (selectedText) {
                vscode.env.clipboard.writeText(selectedText); // Automatically copy selected text to clipboard while preserving original formatting
            }
        });

        // Handle messages received from the webview
        panel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'requestCodePaste': // Check if the command is for pasting code
                    pasteCodeToChatBox(panel); // Call function to paste code to the chat box
                    return; // Exit the switch statement
            }
        });
    });

    // Function to paste code into the webview
    async function pasteCodeToChatBox(panel: vscode.WebviewPanel) {
        const code = await vscode.env.clipboard.readText(); // Read text from the clipboard
        panel.webview.postMessage({ command: 'pasteCode', code: code }); // Send the code to the webview
    }

    // Add the disposable command to the context subscriptions for cleanup
    context.subscriptions.push(disposable);
}

// Deactivate the extension
export function deactivate() {}
