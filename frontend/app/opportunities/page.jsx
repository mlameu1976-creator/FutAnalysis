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
      .then(res => res.json())
      .then(json => {
        setData(json);
        setFiltered(json);
      });
  }, []);

  useEffect(() => {
    let result = [...data];

    // 🔥 CORREÇÃO AQUI
    if (league !== "ALL") {
      result = result.filter(d =>
        d.league.toLowerCase().includes(league.toLowerCase())
      );
    }

    if (market !== "ALL") {
      result = result.filter(d => d.market === market);
    }

    if (dateFilter !== "ALL") {
      const today = new Date().toISOString().split("T")[0];

      if (dateFilter === "TODAY") {
        result = result.filter(d => d.date === today);
      }

      if (dateFilter === "TOMORROW") {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);

        const t = tomorrow.toISOString().split("T")[0];

        result = result.filter(d => d.date === t);
      }
    }

    setFiltered(result);

  }, [league, market, dateFilter, data]);

  return (
    <div style={{ padding: 20 }}>
      <h1>🔥 Oportunidades</h1>

      <select onChange={e => setLeague(e.target.value)}>
        <option value="ALL">Todas ligas</option>
        <option value="premier">Inglês</option>
        <option value="serie">Italiano</option>
        <option value="liga">Espanhol</option>
        <option value="bundes">Alemão</option>
        <option value="brazil">Brasil</option>
        <option value="eredivisie">Holandês</option>
        <option value="norway">Norueguês</option>
      </select>

      <select onChange={e => setMarket(e.target.value)}>
        <option value="ALL">Todos mercados</option>
        <option value="Over 1.5">Over 1.5</option>
        <option value="Over 2.5">Over 2.5</option>
        <option value="Casa vence">Casa vence</option>
        <option value="Fora vence">Fora vence</option>
        <option value="Gol no HT">Gol no HT</option>
      </select>

      <select onChange={e => setDateFilter(e.target.value)}>
        <option value="ALL">Todas datas</option>
        <option value="TODAY">Hoje</option>
        <option value="TOMORROW">Amanhã</option>
      </select>

      {filtered.map((item, i) => (
        <div key={i} style={{ border: "1px solid #444", margin: 10, padding: 10 }}>
          <h3>{item.match}</h3>
          <p>Liga: {item.league}</p>
          <p>Mercado: {item.market}</p>
          <p>Prob: {item.probability}%</p>
          <p>Odd: {item.odds}</p>
          <p>EV: {item.ev}%</p>
        </div>
      ))}
    </div>
  );
}