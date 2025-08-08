import React, { useState } from "react";
import axios from "axios";

// Local-first: default to your local FastAPI server
// You can override with REACT_APP_API_URL in a .env file if needed.
const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");

    try {
      const res = await axios.post(
        `${API_BASE}/query`,
        { question },
        { timeout: 60000, headers: { "Content-Type": "application/json" } }
      );

      const data = res.data ?? {};
      const msg =
        data.answer ??
        data.output ??
        (typeof data === "string" ? data : JSON.stringify(data));

      setAnswer(msg || "No answer received.");
    } catch (err) {
      setAnswer(
        err?.response?.data?.error
          ? `Error: ${err.response.data.error}`
          : "Error contacting the server."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🏀 NBA Query Engine</h1>

      <form onSubmit={askQuestion} style={styles.form}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about the NBA..."
          style={styles.input}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {answer && (
        <div style={styles.answerBox}>
          <h2 style={styles.answerHeading}>Answer:</h2>
          <p style={styles.answerText}>{answer}</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#f7f7f8",
    minHeight: "100vh",
    padding: "2rem",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    color: "#111",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  title: {
    fontSize: "2.5rem",
    marginBottom: "2rem",
    fontWeight: 600,
  },
  form: {
    width: "100%",
    maxWidth: "700px",
    display: "flex",
    gap: "1rem",
    marginBottom: "2rem",
  },
  input: {
    flex: 1,
    padding: "1rem",
    fontSize: "1.2rem",
    borderRadius: "10px",
    border: "1px solid #ccc",
    outline: "none",
    backgroundColor: "#fff",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
  },
  button: {
    padding: "1rem",
    fontSize: "1.1rem",
    borderRadius: "10px",
    backgroundColor: "#10a37f",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    fontWeight: "bold",
    height: "100%",
    whiteSpace: "nowrap",
  },
  answerBox: {
    backgroundColor: "#fff",
    padding: "1.5rem",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
    maxWidth: "700px",
    width: "100%",
  },
  answerHeading: {
    marginBottom: "0.5rem",
    fontSize: "1.2rem",
    fontWeight: "600",
  },
  answerText: {
    fontSize: "1.1rem",
    lineHeight: "1.6",
  },
};

export default App;
