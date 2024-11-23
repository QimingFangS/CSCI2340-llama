import * as vscode from 'vscode';

/**
 * Generates an HTML login panel for the VSCode Webview.
 *
 * @param webview - The Webview instance where the panel will be rendered.
 * @param context - The ExtensionContext to access the extension's resources.
 * @returns The HTML content for the login panel.
 */
export function getLoginPanel(webview: vscode.Webview, context: vscode.ExtensionContext): string {
    // Generate a URI for the CSS file to ensure it's properly accessible in the Webview
    const styleUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'login_style.css') // Path to the CSS file
    );

    // Generate a URI for the JavaScript file to ensure it's properly accessible in the Webview
    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'media', 'login_script.js') // Path to the JavaScript file
    );

    // Return the HTML content for the Webview
    return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <!-- Link to the external CSS for styling -->
            <link href="${styleUri}" rel="stylesheet">
            <title>Login</title>
        </head>
        <body>
            <div class="login-container">
                <h1>Login</h1>
                <!-- Login form with fields for username and API key -->
                <form id="login-form">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                    <label for="apiKey">API Key</label>
                    <input type="password" id="apiKey" name="apiKey" required>
                    <button type="submit">Login</button>
                </form>
            </div>
            <!-- Link to the external JavaScript for handling form submission -->
            <script src="${scriptUri}"></script>
        </body>
        </html>`;
}
