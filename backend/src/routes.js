const express = require("express");
const router = express.Router();

const db = require("./db"); // ✅ CORRIGIDO

const { calculateMatch } = require("./services/scoringEngine");

// ===============================
// OPPORTUNITIES
// ===============================
router.get("/opportunities", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM matches LIMIT 100");

    const opportunities = [];

    for (const match of result.rows) {
      const markets = calculateMatch(match);

      for (const m of markets) {
        opportunities.push({
          match: `${match.home_team} vs ${match.away_team}`,
          league: match.league,
          market: m.market,
          probability: m.probability,
          odds: m.odds,
          ev: m.ev,
        });
      }
    }

    res.json(opportunities);
  } catch (err) {
    console.error("❌ ERRO OPPORTUNITIES:", err.message);
    res.status(500).json({ error: "Erro ao gerar oportunidades" });
  }
});

module.exports = router;