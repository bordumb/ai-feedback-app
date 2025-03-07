// frontend/src/components/Chatbot.tsx
import React, { useState } from "react";
import { sendFeedback } from "../api/index"; // ✅ Import only the API function

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const data = await sendFeedback(input);
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error("Error sending feedback:", error);
      setResponse("Error submitting feedback. Check the console for details.");
    }
  };

  return (
    <div>
      <h1>AI Feedback Chatbot</h1>
      <input
        type="text"
        placeholder="Type your feedback..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <pre>{response}</pre>
    </div>
  );
}
