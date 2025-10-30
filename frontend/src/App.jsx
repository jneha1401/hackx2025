// frontend/src/api.js
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function synthesizeTTS(text, lang = "en") {
  const res = await fetch(`${API_BASE}/api/tts/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, lang })
  });
  if (!res.ok) {
    const err = await res.json().catch(()=>({detail:'unknown error'}));
    throw new Error(err.detail || 'TTS failed');
  }
  return res.json(); // { url: "/audio/<file>" }
}
