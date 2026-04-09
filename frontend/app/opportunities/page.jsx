"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function load() {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/opportunities`
      );

      const json = await res.json();

      setData(json);
    }

    load();
  }, []);

  return (
    <div className="p-6 bg-black text-white min-h-screen">

      <h1 className="text-2xl mb-6">Dashboard</h1>

      {data.map((item, i) => (
        <div key={i} className="border p-4 mb-4">

          <h2>
            {item.home_team} x {item.away_team}
          </h2>

          <p>{item.market}</p>
          <p>Prob: {item.probability}</p>
          <p>Odd: {item.odd}</p>
          <p>EV: {item.ev}</p>

        </div>
      ))}

    </div>
  );
}