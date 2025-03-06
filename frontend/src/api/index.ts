import { useState } from "react";

export default function Chatbot() {
    const [input, setInput] = useState(""); // State for user input
    const [response, setResponse] = useState(""); // 🛠️ Fix: Define setResponse properly

    const sendFeedback = async () => {
        try {
            const res = await fetch("http://localhost:8000/feedback/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_input: input }),  // ✅ Ensure correct request format
            });
    
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
    
            const data = await res.json();
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
            <button onClick={sendFeedback}>Submit</button>
            <pre>{response}</pre>
        </div>
    );
}
