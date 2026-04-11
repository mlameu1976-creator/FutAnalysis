"use client";

import { useEffect, useState } from "react";

export default function OpportunitiesPage() {
  const [data, setData] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const [league, setLeague] = useState("ALL");
  const [market, setMarket] = useState("ALL");
  const [dateFilter, setDateFilter] = useState("ALL");

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/opportunities")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setFiltered(json);
      });
  }, []);

  useEffect(() => {
    let result = [...data];

    // 🔥 FILTRO LIGA
    if (league !== "ALL") {
      result = result.filter((r) => r.league === league);
    }

    // 🔥 FILTRO MERCADO
    if (market !== "ALL") {
      result = result.filter((r) => r.market === market);
    }

    // 🔥 FILTRO DATA
    if (dateFilter !== "ALL") {
      const today = new Date();
      const tomorrow = new Date();
      tomorrow.setDate(today.getDate() + 1);

      result = result.filter((r) => {
        const matchDate = new Date(r.date);

        if (dateFilter === "TODAY") {
          return matchDate.toDateString() === today.toDateString();
        }

        if (dateFilter === "TOMORROW") {
          return matchDate.toDateString() === tomorrow.toDateString();
        }

        return true;
      });
    }

    setFiltered(result);
  }, [league, market, dateFilter, data]);

  const leagues = [...new Set(data.map((d) => d.league))];
  const markets = [...new Set(data.map((d) => d.market))];

  return (
    <div style={{ padding: 20 }}>
      <h1>🔥 Oportunidades</h1>

      {/* FILTROS */}
      <div style={{ display: "flex", gap: 20, marginBottom: 20 }}>
        <select onChange={(e) => setLeague(e.target.value)}>
          <option value="ALL">Todas as ligas</option>
          {leagues.map((l, i) => (
            <option key={i} value={l}>
              {l}
            </option>
          ))}
        </select>

        <select onChange={(e) => setMarket(e.target.value)}>
          <option value="ALL">Todos mercados</option>
          {markets.map((m, i) => (
            <option key={i} value={m}>
              {m}
            </option>
          ))}
        </select>

        <select onChange={(e) => setDateFilter(e.target.value)}>
          <option value="ALL">Todas datas</option>
          <option value="TODAY">Hoje</option>
          <option value="TOMORROW">Amanhã</option>
        </select>
      </div>

      {/* LISTA */}
      <div style={{ display: "grid", gap: 20 }}>
        {filtered.map((item, i) => (
          <div
            key={i}
            style={{
              border: "1px solid #333",
              padding: 15,
            }}
          >
            <h3>{item.match}</h3>
            <p>Liga: {item.league}</p>
            <p>Mercado: {item.market}</p>
            <p>Prob: {item.probability}%</p>
            <p>Odd: {item.odds}</p>
            <p>EV: {item.ev}%</p>
          </div>
        ))}
      </div>
    </div>
  );
}