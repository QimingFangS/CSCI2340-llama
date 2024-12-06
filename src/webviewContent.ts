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
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; connect-src 'self' http://127.0.0.1:8080; style-src ${cspSource}; script-src ${cspSource};">
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
            <label for="fileSelect">Select File:</label>
            <select id="fileSelect">
                <option value="">--Choose a file--</option>
            </select>
            <div id="fileDisplay">--No file selected--</div> <!-- 显示文件选择状态 -->
        </div>
        <div class="mode-language-select">
            <div class="dropdowns">
                <label for="modeSelect">Select Mode:</label>
                <select id="modeSelect">
                    <option value="basic">Basic</option>
                    <option value="advanced">Advanced</option>
                </select>
            </div>
            <div class="dropdowns">
                <label for="languageSelect">Select Language:</label>
                <select id="languageSelect">
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                    <option value="c#">C#</option>
                    <option value="ruby">Ruby</option>
                    <option value="go">Go</option>
                    <option value="scala">Scala</option>
                    <option value="php">PHP</option>
                    <option value="html">HTML</option>
                    <option value="css">CSS</option>
                </select>
            </div>
        </div>

        <div class="input-area">
            <textarea id="userInput" placeholder="Send your code to LLAMA Co-Pilot" rows="5"></textarea>
            <button id="sendButton">Send</button>
        </div>
    </div>
    <!-- 小图标按钮 -->
    <div id="toggleSidebarIcon">
        ☰
    </div>

    <script type="module" src="${scriptUri}"></script>
</body>
</html>
`;
}
