import React, { useState } from "react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      console.log('Sending request to:', `${API_BASE}/api/chat`);
      console.log('Request body:', JSON.stringify({ message: userMsg.content }));

      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.content }),
      });

      console.log('Response status:', res.status);
      console.log('Response ok:', res.ok);

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data: { reply: string } = await res.json();
      const assistantMsg: Message = { role: "assistant", content: data.reply };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      console.error('Error details:', err);
      if (err.message.includes("499") || err.message.includes("cancelled")) {
        setError("Request was cancelled");
      } else {
        setError(err.message ?? "Request failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24, fontFamily: "system-ui" }}>
      <h1>My Trial-Chat App</h1>

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: 16,
          minHeight: 300,
          marginBottom: 16,
          background: "#fafafa",
        }}
      >
        {messages.length === 0 && <div style={{ color: "#777" }}>Start the conversation...</div>}
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              marginBottom: 8,
              display: "flex",
              justifyContent: m.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "75%",
                padding: "8px 12px",
                borderRadius: 16,
                background: m.role === "user" ? "#2563eb" : "#e5e7eb",
                color: m.role === "user" ? "white" : "black",
              }}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage} style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1,
            padding: "8px 12px",
            borderRadius: 999,
            border: "1px solid #ddd",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "8px 16px",
            borderRadius: 999,
            border: "none",
            background: loading ? "#9ca3af" : "#2563eb",
            color: "white",
            cursor: loading ? "default" : "pointer",
          }}
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </form>

      {error && <div style={{ marginTop: 8, color: "red" }}>{error}</div>}

      {loading && (
        <div style={{ marginTop: 8, color: "#666", fontSize: "14px" }}>
          Your request is being processed. Due to API rate limits, it may take up to 60 seconds.
        </div>
      )}

      <div style={{ marginTop: 24, textAlign: "center", color: "#999", fontSize: "12px" }}>
        © Heaven LIU
      </div>
    </div>
  );
}

export default App;

