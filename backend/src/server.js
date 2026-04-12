throw new Error("🔥 SERVER ALTERADO 🔥");

const express = require("express");
const cors = require("cors");
const { ingestAll } = require("./services/ingestion");

const app = express();
app.use(cors());

app.get("/opportunities", async (req, res) => {
  const matches = await ingestAll();

  const opportunities = [];

  for (const m of matches) {
    const markets = [
      { name: "Over 1.5", prob: 0.75, odd: 1.6 },
      { name: "Over 2.5", prob: 0.6, odd: 2.7 },
      { name: "Casa vence", prob: 0.55, odd: 2.6 },
      { name: "Fora vence", prob: 0.45, odd: 3.3 },
      { name: "Gol no HT", prob: 0.65, odd: 1.65 }
    ];

    for (const mk of markets) {
      const ev = mk.prob * mk.odd - 1;

      if (ev > 0) {
        opportunities.push({
          match: m.match,
          league: m.league,
          market: mk.name,
          probability: (mk.prob * 100).toFixed(1),
          odds: mk.odd,
          ev: (ev * 100).toFixed(1)
        });
      }
    }
  }

  res.json(opportunities);
});

app.listen(8080, () => console.log("🚀 Rodando"));