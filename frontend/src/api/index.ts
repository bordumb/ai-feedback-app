// frontend/src/api/index.ts
import Cookies from "js-cookie";

const API_BASE_URL = "http://localhost:8000";

async function apiRequest<T>(endpoint: string, method: string = "GET", body?: object): Promise<T> {
  const token = Cookies.get("access_token");
  if (!token) throw new Error("No authentication token found!");

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Authorization": `Bearer ${token}`,  // ✅ Include token in request
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  return await response.json();
}

export function sendFeedback(input: string) {
  return apiRequest("/feedback", "POST", { user_input: input });
}

export function fetchAllFeedback() {
  return apiRequest("/feedback", "GET");
}

