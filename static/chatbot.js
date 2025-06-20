document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector(".inputarea input");
    const sendBtn = document.querySelector(".inputarea button");
    const chatbox = document.querySelector(".chatbox");

    sendBtn.addEventListener("click", async () => {
        const message = input.value.trim();
        if (!message) return;

        // Show user message
        const userMessage = document.createElement("p");
        userMessage.textContent = "You: " + message;
        chatbox.appendChild(userMessage);

        // Send to Flask
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();
        const botMessage = document.createElement("p");
        botMessage.textContent = "Serena: " + data.reply;
        chatbox.appendChild(botMessage);

        input.value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
    });
});
