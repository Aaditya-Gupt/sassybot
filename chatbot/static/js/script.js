document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.querySelector(".chat-box");
    const chatButton = document.getElementById("chat-btn");
    const closeButton = document.querySelector(".close-btn");
    const sendButton = document.getElementById("send-btn");
    const chatInput = document.getElementById("chat-input");
    const chatBody = document.querySelector(".chat-box-body");

    // Open chatbot when button is clicked
    chatButton.addEventListener("click", function () {
        chatBox.style.visibility = "visible";
    });

    // Close chatbot when "X" is clicked
    closeButton.addEventListener("click", function () {
        chatBox.style.visibility = "hidden";
    });

    // Send message when button is clicked
    sendButton.addEventListener("click", function () {
        sendMessage();
    });

    // Send message when Enter key is pressed
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("chat-box-body-send");
            messageDiv.innerHTML = `<p>${message}</p>`;
            chatBody.appendChild(messageDiv);
            chatInput.value = "";
            chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to the latest message
        }
    }
});
