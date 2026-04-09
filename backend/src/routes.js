const express = require("express");
const router = express.Router();

const db = require("./db");
const { generateMarkets } = require("./services/scoringEngine");

// ===============================
// GET OPPORTUNITIES
// ===============================
router.get("/opportunities", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM matches LIMIT 50");

    const opportunities = [];

    for (const match of result.rows) {
      const markets = generateMarkets(match); // 🔥 CORRIGIDO

      markets.forEach((m) => {
        opportunities.push({
          match: `${match.home_team} vs ${match.away_team}`,
          market: m.market,
          probability: m.probability,
          odds: m.odds,
          ev: m.ev,
        });
      });
    }

    res.json(opportunities);
  } catch (err) {
    console.error("Erro opportunities:", err);
    res.status(500).json({ error: "Erro ao gerar oportunidades" });
  }
});

module.exports = router;