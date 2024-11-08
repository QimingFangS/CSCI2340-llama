
const textarea = document.getElementById("textarea");
const chat = document.getElementById("chat");

function submit() {

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

document.getElementById("submit-button").addEventListener("click", () => {
    submit();
});

textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        // Prevents newline if it's a text area
        event.preventDefault();  

        submit();
    }
});
