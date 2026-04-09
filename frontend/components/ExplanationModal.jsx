"use client";
import { useEffect, useState } from "react";

export default function ExplanationModal({ matchId, onClose }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/matches/${matchId}/explanation`)
      .then(res => res.json())
      .then(json => setData(json));
  }, [matchId]);

  if (!data) return null;

  return (
    <div style={overlay}>
      <div style={modal}>
        <h2>Análise da Sugestão</h2>

        <p><b>Mercado:</b> {data.suggestion}</p>
        <p><b>Confiança:</b> {data.confidence}%</p>

        <ul>
          {data.reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>

        <button onClick={onClose}>Fechar</button>
      </div>
    </div>
  );
}

const overlay = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100vw",
  height: "100vh",
  background: "rgba(0,0,0,0.6)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center"
};

const modal = {
  background: "#111",
  padding: 30,
  borderRadius: 8,
  width: 400,
  color: "#fff"
};
