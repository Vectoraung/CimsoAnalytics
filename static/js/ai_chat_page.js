document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("sendMessageButton").addEventListener("click", function() {
        let messageText = document.getElementById("floatingTextarea2").value.trim();

        if (messageText !== "") {
            // Create user message (right-aligned)
            let userMessage = document.createElement("div");
            userMessage.className = "row justify-content-end";
            userMessage.innerHTML = `<div class="chat-message user-message d-inline-flex p-2 w-auto">${messageText}</div>`;
            document.getElementById("chat-content").appendChild(userMessage);

            // Create bot response placeholder (Loading...)
            let botMessageContainer = document.createElement("div");
            botMessageContainer.className = "row justify-content-start";
            let botMessage = document.createElement("div");
            botMessage.className = "chat-message bot-message d-inline-flex p-2 w-auto";
            botMessage.innerHTML = `
            <div class="spinner-grow" style="width: 0.5rem; height: 0.5rem; margin-right:5px;" role="status"></div>
            <div class="spinner-grow" style="width: 0.5rem; height: 0.5rem; margin-right:5px;" role="status"></div>
            <div class="spinner-grow" style="width: 0.5rem; height: 0.5rem; margin-right:5px;" role="status"></div>
            `;
            botMessageContainer.appendChild(botMessage);
            document.getElementById("chat-content").appendChild(botMessageContainer);

            // Send the message to Django backend using Fetch API
            fetch('/send-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // Ensure CSRF token is sent
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    // Replace "Loading..." with actual response
                    botMessage.innerHTML = data.response;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                botMessage.innerHTML = "⚠️ Failed to load response!";
            });

            // Clear the textarea after sending
            document.getElementById("floatingTextarea2").value = "";
        }
    });
});

// Function to get CSRF token from Django
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1] || '';
}
