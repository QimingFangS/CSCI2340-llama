
// import { marked } from "marked";
// import { marked } from 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
// import marked from 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';

console.log("testing");

const textarea = document.getElementById("textarea");
const chat = document.getElementById("chat");

function submit() {
    console.log("submit!", textarea.value);

    const input = document.createElement("div");

    // input.textContent = marked(textarea.value);

    const formattedText = textarea.value.replace(/\n/g, '<br/>');
    input.innerHTML = formattedText;

    input.className = "chat--input";
    chat.appendChild(input);

    textarea.value = "";

    const output = document.createElement("div");
    output.textContent = "This is a test bot!";
    output.className = "chat--output"; //
    chat.appendChild(output);

}

document.getElementById("submit-button").addEventListener("click", () => {
    submit();
});

textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();  // Prevents newline if it's a text area
        submit();
    }
});
