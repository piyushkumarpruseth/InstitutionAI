// Change this URL if your deployed API uses a different address.
const API_BASE_URL = "http://127.0.0.1:8000";

const institutionInput = document.getElementById("institution-id");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-question");
const statusBox = document.getElementById("chat-status");
const chatLog = document.getElementById("chat-log");

function addMessage(text, kind) {
  const message = document.createElement("div");
  message.className = `chat-message ${kind}-message`;
  message.textContent = text;
  chatLog.appendChild(message);
}

async function sendQuestion() {
  const institution_id = institutionInput.value.trim();
  const question = questionInput.value.trim();

  if (!institution_id || !question) {
    statusBox.textContent = "Enter both an institution ID and a question.";
    return;
  }

  addMessage(question, "user");
  questionInput.value = "";
  sendButton.disabled = true;
  statusBox.textContent = "Thinking…";

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ institution_id, question })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || `Request failed (${response.status})`);
    }

    addMessage(data.answer, "bot");
    statusBox.textContent = "Response received from the InstitutionAI backend.";
  } catch (error) {
    addMessage(`Unable to reach the chatbot: ${error.message}`, "bot");
    statusBox.textContent =
      "Check that FastAPI is running and that the API URL/CORS settings are correct.";
  } finally {
    sendButton.disabled = false;
    questionInput.focus();
  }
}

sendButton.addEventListener("click", sendQuestion);
questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendQuestion();
  }
});
