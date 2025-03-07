// frontend/src/api/index.ts

export async function fetchAllFeedback() {
    const response = await fetch("http://localhost:8000/feedback");
    if (!response.ok) throw new Error("Failed to fetch feedback");
    return await response.json();
  }
  
  export async function sendFeedback(input: string) {
    const response = await fetch("http://localhost:8000/feedback/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: input }),
    });
  
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
  
    return await response.json();
  }
