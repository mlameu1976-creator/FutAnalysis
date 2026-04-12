"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/opportunities", {
  cache: "no-store"
})
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error(err));
  }, []);

  const grouped = {};

  data.forEach((item) => {
    if (!grouped[item.match]) {
      grouped[item.match] = [];
    }
    grouped[item.match].push(item);
  });

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>

      {Object.keys(grouped).map((match) => (
        <div key={match} style={{ marginBottom: 40 }}>
          <h2>{match}</h2>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            {grouped[match].map((m, i) => (
              <div key={i} style={{ border: "1px solid #333", padding: 10 }}>
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