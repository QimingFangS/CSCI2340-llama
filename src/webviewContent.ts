import * as vscode from 'vscode';

/**
 * Generates the HTML content for the Webview.
 *
 * @param webview - The Webview instance where the content will be rendered.
 * @param context - The ExtensionContext to access extension's resources.
 * @returns The HTML content string.
 */
export function getWebviewContent(webview: vscode.Webview, context: vscode.ExtensionContext): string {
    const cspSource = webview.cspSource; // Content Security Policy source for secure resource loading

    // Generate URIs for the CSS and JavaScript files to ensure proper accessibility in the Webview
    const styleUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'chat_style.css') // Path to the CSS file
    );

    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'chat_script.js') // Path to the JavaScript file
    );

    // Return the HTML content for the Webview
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Content Security Policy (CSP) for secure content loading -->
        <meta http-equiv="Content-Security-Policy" content="default-src 'none';
            connect-src 'self' http://127.0.0.1:8080;
            style-src ${cspSource};
            script-src ${cspSource};">
        <title>Llama Co-pilot</title>
        <!-- Link to external stylesheet -->
        <link rel="stylesheet" href="${styleUri}">
    </head>
    <body>
        <h1>Llama Co-pilot</h1>
        <!-- Chat box to display messages -->
        <div class="chat-box" id="chatBox"></div>
        <!-- Input area for user messages -->
        <div class="input-area">
            <textarea id="userInput" placeholder="Type your message here" rows="5"></textarea>
            <button id="sendButton">Send</button>
        </div>
        <!-- Link to external JavaScript -->
        <script type="module" src="${scriptUri}"></script>
    </body>
    </html>`;
}
