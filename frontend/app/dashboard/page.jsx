"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/opportunities")
      .then((res) => res.json())
      .then((res) => setData(res))
      .catch((err) => console.error(err));
  }, []);

  if (!data.length) {
    return <h1 style={{ color: "white" }}>Carregando oportunidades...</h1>;
  }

  // Agrupar por jogo
  const grouped = {};

  data.forEach((item) => {
    const key = item.match || `${item.homeTeam} vs ${item.awayTeam}`;

    if (!grouped[key]) {
      grouped[key] = [];
    }

    grouped[key].push(item);
  });

  return (
    <div style={{ background: "#000", color: "#fff", padding: 20 }}>
      <h1>Dashboard</h1>

      {Object.entries(grouped).map(([match, markets]) => (
        <div key={match} style={{ marginBottom: 30 }}>
          <h2>{match}</h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 10,
            }}
          >
            {markets.map((m, i) => (
              <div
                key={i}
                style={{
                  border: "1px solid #333",
                  padding: 10,
                }}
              >
                <p><strong>{m.market}</strong></p>
                <p>Prob: {m.probability}%</p>
                <p>Odd: {m.odds}</p>
                <p>EV: {m.ev}%</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}