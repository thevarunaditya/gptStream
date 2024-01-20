// Set constants for the form and chat log
const form = document.querySelector("#chat-form");
const chatlog = document.querySelector("#chat-log");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  // Get the user's message from the form
  const message = form.elements.message.value;

  // Send a request to the Flask server with the user's message
  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ messages: [{ role: "user", content: message }] }),
  });

  // Create a new TextDecoder to decode the streamed response text
  const decoder = new TextDecoder();

  // Set up a new ReadableStream to read the response body
  const reader = response.body.getReader();
  let chunks = "";

  // Read the response stream as chunks and append them to the chat log
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks += decoder.decode(value);
    chatlog.innerHTML = chunks;
  }
});