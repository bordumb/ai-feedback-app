import { useState } from "react";

export default function Chatbot() {
    const [input, setInput] = useState("");
    const [response, setResponse] = useState("");

    const sendFeedback = async () => {
        const res = await fetch("http://localhost:8000/feedback/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: input }),
        });
        const data = await res.json();
        setResponse(JSON.stringify(data, null, 2));
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
