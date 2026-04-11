const express = require("express");
const router = express.Router();

const { ingestAll } = require("../services/ingestion");

router.get("/opportunities", async (req, res) => {
  try {
    const matches = await ingestAll();

    // 🔥 GARANTIA ABSOLUTA
    if (!Array.isArray(matches)) {
      return res.json([]);
    }

    const opportunities = [];

    for (let i = 0; i < matches.length; i++) {
      const m = matches[i];

      const markets = [
        { name: "Over 1.5", prob: 0.75, odd: 1.6 },
        { name: "Over 2.5", prob: 0.60, odd: 2.7 },
        { name: "Casa vence", prob: 0.55, odd: 2.6 },
        { name: "Fora vence", prob: 0.45, odd: 3.3 },
        { name: "Gol no HT", prob: 0.65, odd: 1.65 }
      ];

      for (let j = 0; j < markets.length; j++) {
        const mk = markets[j];

        const ev = mk.prob * mk.odd - 1;

        if (ev > 0) {
          opportunities.push({
            match: m.match,
            league: m.league,
            date: m.date,
            market: mk.name,
            probability: (mk.prob * 100).toFixed(1),
            odds: mk.odd,
            ev: (ev * 100).toFixed(1)
          });
        }
      }
    }

    res.json(opportunities);

  } catch (err) {
    console.error("ERRO ROUTES:", err);
    res.status(500).json([]);
  }
});

module.exports = router;