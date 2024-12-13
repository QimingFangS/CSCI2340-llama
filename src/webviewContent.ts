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
        vscode.Uri.joinPath(context.extensionUri, 'src', 'style', 'chat_style_2.css') // Path to the CSS file
    );

    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'src', 'components', 'chat_script.js') // Path to the JavaScript file
    );

    // Return the HTML content for the Webview
    return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="Content-Security-Policy" content="default-src 'none'; connect-src 'self' http://127.0.0.1:8000; style-src ${cspSource}; script-src ${cspSource};">
            <title>Llama Co-pilot</title>
            <link rel="stylesheet" href="${styleUri}">
        </head>
        <body>
            <!-- Side Bar -->
            <div id="sidebar" class="collapsed">
                <button id="toggleSidebar" class="toggle-btn">☰</button>
                <div id="sidebarContent" class="sidebar-content">
                    <h3>Chat History</h3>
                    <ul id="historyList">
                        <!-- Chat History List-->
                    </ul>
                    <!-- New Chat Button -->
                    <button id="newChatBtn" class="new-chat-btn">New Chat</button>
                </div>
            </div>
            <div id="mainContent" class="main-content">
                <h1>Llama Co-pilot</h1>
                <div class="chat-box" id="chatBox"></div>

                <div class="dropdowns">
                    <span>
                        <label for="fileSelect">Select File:</label>
                        <select id="fileSelect">
                            <option value="">--Choose a file--</option>
                        </select>
                        <div id="fileDisplay">--No file selected--</div>
                    </span>
                </div>
                <div class="mode-language-select">
                    <div class="dropdowns">
                        <span>
                            <label for="modeSelect">Select Mode:</label>
                            <select id="modeSelect">
                                <option value=null>---</option>
                                <option value="mode_1">Mode 1</option>
                                <option value="mode_2">Mode 2</option>
                            </select>
                        </span>
                        <div id="messageBoxForLanguage">
                            Please select Language!
                        </div>
                    </div>
                    <div class="dropdowns">
                        <span>
                            <label for="languageSelect">Select Language:</label>
                            <select id="languageSelect">
                                <option value=null>----</option>
                                <option value="Python">Python</option>
                                <option value="C">C</option>
                                <option value="C++">C++</option>
                                <option value="C#">C#</option>
                                <option value="Java">Java</option>
                                <option value="JavaScript">JavaScript</option>
                                <option value="TypeScript">TypeScript</option>
                                <option value="Ruby">Ruby</option>
                                <option value="Go">Go</option>
                                <option value="Scala">Scala</option>
                                <option value="PHP">PHP</option>
                                <option value="CSS">CSS</option>
                                <option value="HTML">HTML</option>
                                <option value="Dafny">Dafny</option>
                            </select>
                        </span>
                        <div id="messageBoxForMode">
                            Please select Mode!
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <textarea id="userInput" placeholder="Send your code to LLAMA Co-Pilot" rows="5"></textarea>
                    <button id="sendButton">Analyze</button>
                </div>
            </div>
            <div id="toggleSidebarIcon">
                ☰
            </div>

            <script type="module" src="${scriptUri}"></script>
        </body>
        </html>`;
}
