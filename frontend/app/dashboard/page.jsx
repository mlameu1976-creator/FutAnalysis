"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(
          "https://futanalysis-backend-production.up.railway.app/opportunities"
        );

        const json = await res.json();

        console.log("DATA FINAL:", json);

        setData(json);
      } catch (err) {
        console.error(err);
      }
    }

    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>

      {data.length === 0 && <p>Nenhuma oportunidade</p>}

      {data.map((item, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #444",
            marginBottom: 20,
            padding: 15,
          }}
        >
          {/* 🔥 CORREÇÃO REAL */}
          <h2>{item.match}</h2>

          <div style={{ marginTop: 10 }}>
            <p><strong>{item.market}</strong></p>
            <p>Prob: {item.probability}%</p>
            <p>Odd: {item.odds}</p>
            <p>EV: {item.ev}%</p>
          </div>
        </div>
      ))}
    </div>
  );
}