/**
 * This file contains functionality for frontend calls such as api calls
 * to the backend, code copy and pasting, and more.
 * 
 * Author: Daniel Cho
 */


// TODO
    // (ghost) code copy and pasting 


const textarea = document.getElementById("textarea");
const chat = document.getElementById("chat");

function submit() {
    /**
     * When a user writes to the text box and submits, this function is called.
     * Takes user input, appends it to the chat display, clears the input text box,
     * and then calls the backend, appending results from the call into the chat
     * display.
     */

    // append user input to frontend view 
    const userInput = textarea.value;

    const input = document.createElement("div");
    const formattedText = userInput.replace(/\n/g, '<br/>');
    input.innerHTML = formattedText;
    input.className = "chat--input";
    chat.appendChild(input);

    textarea.value = "";

    // call backend api
    const payload = {"query": userInput};

    fetch("http://127.0.0.1:8080/api/test", {
        method:  "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)  
    })
    .then(r => r.json())
    .then(r => {
        
        // append backend output to frontend ui
        const output = document.createElement("div");
        output.innerHTML = r.response;
        output.className = "chat--output"; //
        chat.appendChild(output);
    });
}

// when the submission button is pressed, calls the submit function
document.getElementById("submit-button").addEventListener("click", () => {
    submit();
});

// when 'enter' is pressed, calls the submit function
textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        // Prevents newline if it's a text area
        event.preventDefault();  

        submit();
    }
});
