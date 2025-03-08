import { useState } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/router";
import { sendFeedback } from "../api/index"; // ✅ Use the abstracted API function
import Navbar from "../components/Navbar"; 

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async () => {
    setError(""); // Clear previous errors
    const token = Cookies.get("access_token");

    if (!token) {
      setError("You must be logged in to submit feedback.");
      router.push("/auth"); // Redirect to login if not authenticated
      return;
    }

    try {
      const data = await sendFeedback(input); // ✅ Uses abstracted function
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error("Error sending feedback:", err);
      setError("Failed to submit feedback. Please try again.");
    }
  };

  return (
    <div>
      <h1>AI Feedback Chatbot</h1>
      
      {error && <p style={{ color: "red" }}>{error}</p>}

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
