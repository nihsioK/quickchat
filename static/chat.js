const chatWindow = document.getElementById("chat-window");
const messageForm = document.getElementById("message-form");
const messageInput = document.getElementById("message-input");

messageForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value;
  const response = await fetch(`/api/v1/chats/{chat_id}/messages/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    },
    body: JSON.stringify({ content: message }),
  });
  const newMessage = await response.json();
  displayMessage(newMessage);
  messageInput.value = "";
});

function displayMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.textContent = message.content;
  chatWindow.appendChild(messageElement);
}

// Fetch and display existing messages
async function loadMessages() {
  const response = await fetch(`/api/v1/chats/{chat_id}/messages/`);
  const messages = await response.json();
  messages.forEach(displayMessage);
}

loadMessages();
