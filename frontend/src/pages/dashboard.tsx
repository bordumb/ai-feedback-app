// frontend/src/pages/dashboard.tsx

import React, { useEffect, useState } from "react";
import { fetchAllFeedback } from "../api/index"; // ✅ Use the abstracted API function
import Cookies from "js-cookie";
import { useRouter } from "next/router";
import { Feedback } from "../types"; // Import the Feedback type


export default function Dashboard() {
  const [feedbackList, setFeedbackList] = useState<Feedback[]>([]);
  const [sentimentFilter, setSentimentFilter] = useState<string>("all");
  const [sortColumn, setSortColumn] = useState<keyof Feedback>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // ✅ Fetch Feedback & Check Auth
  useEffect(() => {
    const token = Cookies.get("access_token");

    if (!token) {
      router.push("/auth"); // Redirect to login if no token
      return;
    }

    fetchAllFeedback()
      .then((data: Feedback[]) => {
        setFeedbackList(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching feedback:", err);
        Cookies.remove("access_token");
        setError("Session expired. Please log in again.");
        router.push("/auth");
      });
  }, [router]); // ✅ Dependency array ensures re-run on navigation

  // ✅ Handle Logout
  const handleLogout = () => {
    Cookies.remove("access_token");
    router.push("/auth");
  };

  // ✅ Filter feedback by number of stars
  const filteredFeedback = feedbackList.filter((item) => {
    const itemStars = item.sentiment?.toLowerCase().replace(" stars", "").replace(" star", "").trim() || "0";
    return sentimentFilter === "all" ? true : itemStars === sentimentFilter;
  });

  // ✅ Sort feedback
  const sortedFeedback = [...filteredFeedback].sort((a, b) => {
    const valA = a[sortColumn];
    const valB = b[sortColumn];

    if (valA < valB) return sortOrder === "asc" ? -1 : 1;
    if (valA > valB) return sortOrder === "asc" ? 1 : -1;
    return 0;
  });

  // ✅ Handle sorting logic
  const handleSort = (column: keyof Feedback) => {
    if (sortColumn === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortOrder("asc");
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Feedback Dashboard</h1>

      {/* Logout Button */}
      <button onClick={handleLogout} style={{ marginBottom: "1rem" }}>
        Logout
      </button>

      {/* Show loading/error messages */}
      {loading && <p>Loading feedback...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Filter by sentiment */}
      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="sentiment-filter">Filter by Sentiment: </label>
        <select id="sentiment-filter" value={sentimentFilter} onChange={(e) => setSentimentFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="5">5 Stars</option>
          <option value="4">4 Stars</option>
          <option value="3">3 Stars</option>
          <option value="2">2 Stars</option>
          <option value="1">1 Star</option>
        </select>
      </div>

      {/* Feedback Table */}
      <table border={1} cellPadding={6} cellSpacing={0}>
        <thead>
          <tr>
            <th onClick={() => handleSort("id")}>ID</th>
            <th onClick={() => handleSort("user_input")}>User Input</th>
            <th onClick={() => handleSort("category")}>Category</th>
            <th onClick={() => handleSort("sentiment")}>Sentiment</th>
            <th onClick={() => handleSort("created_at")}>Date</th>
          </tr>
        </thead>
        <tbody>
          {sortedFeedback.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.user_input}</td>
              <td>{item.category}</td>
              <td>{item.sentiment}</td>
              <td>{new Date(item.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
