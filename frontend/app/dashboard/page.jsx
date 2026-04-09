"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      const res = await fetch(
        "https://futanalysis-backend-production.up.railway.app/opportunities",
        { cache: "no-store" }
      );

      const json = await res.json();

      console.log("🔥 NOVO BUILD RODANDO", json);

      setData(json);
    }

    load();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>

      {data.map((item, i) => (
        <div key={i} style={{ border: "1px solid #444", margin: 10, padding: 10 }}>
          <h2>{item.match}</h2>

          <p>{item.market}</p>
          <p>Prob: {item.probability}%</p>
          <p>Odd: {item.odds}</p>
          <p>EV: {item.ev}%</p>
        </div>
      ))}
    </div>
  );
}