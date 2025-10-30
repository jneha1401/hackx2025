import React, { useState } from "react";
import { synthesizeTTS } from "./api"; // make sure api.jsx is in same folder or adjust path

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSpeak = async () => {
    if (!text.trim()) {
      alert("Please enter some text!");
      return;
    }
    setLoading(true);
    try {
      const audioUrl = await synthesizeTTS(text);
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
      } else {
        alert("No audio returned from server!");
      }
    } catch (error) {
      console.error("Error during TTS synthesis:", error);
      alert("Something went wrong. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        backgroundColor: "#001f3f",
        color: "#fff",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "Poppins, sans-serif",
      }}
    >
      <h1>SwasthyaLink Voice Synthesizer 🎙️</h1>
      <textarea
        rows="4"
        cols="50"
        placeholder="Type what you want to hear..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{
          padding: "10px",
          borderRadius: "10px",
          width: "60%",
          marginBottom: "20px",
          fontSize: "16px",
        }}
      ></textarea>
      <button
        onClick={handleSpeak}
        disabled={loading}
        style={{
          backgroundColor: "#0074D9",
          color: "#fff",
          border: "none",
          padding: "12px 25px",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {loading ? "Generating voice..." : "Speak"}
      </button>
    </div>
  );
}

export default App;
