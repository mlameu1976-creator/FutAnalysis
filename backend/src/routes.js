const express = require("express");
const router = express.Router();

const db = require("./db");
const { generateMarkets } = require("./services/scoringEngine");

// ===============================
// HEALTH CHECK
// ===============================
router.get("/", (req, res) => {
  res.json({
    status: "ok",
    service: "FutAnalysis API",
  });
});

// ===============================
// MATCHES
// ===============================
router.get("/matches", async (req, res) => {
  try {
    const result = await db.query(`
      SELECT * FROM matches
      ORDER BY match_date ASC
      LIMIT 50
    `);

    res.json(result.rows);
  } catch (err) {
    console.error("Erro /matches:", err.message);
    res.status(500).json({ error: "Erro ao buscar partidas" });
  }
});

// ===============================
// OPPORTUNITIES (DEBUG ATIVO)
// ===============================
router.get("/opportunities", async (req, res) => {
  try {
    const result = await db.query(`
      SELECT * FROM matches
      ORDER BY match_date ASC
      LIMIT 50
    `);

    const leagueAvg = {
      home_goals: 1.4,
      away_goals: 1.2,
    };

    const opportunities = [];

    for (const match of result.rows) {
      try {
        const markets = generateMarkets(match, leagueAvg);

        opportunities.push({
          match: `${match.home_team} vs ${match.away_team}`,
          date: match.match_date,
          markets: markets || [],
        });

      } catch (err) {
        console.error("❌ ERRO MATCH:", match.home_team, "vs", match.away_team);
        console.error(err);
      }
    }

    res.json(opportunities);

  } catch (err) {
    console.error("❌ ERRO GERAL /opportunities:", err);
    res.status(500).json({ error: "Erro ao gerar oportunidades" });
  }
});

// ===============================
// DEBUG DB
// ===============================
router.get("/debug/db", async (req, res) => {
  try {
    const result = await db.query("SELECT COUNT(*) FROM matches");

    res.json({
      total_matches: result.rows[0].count,
    });
  } catch (err) {
    console.error("Erro debug DB:", err.message);
    res.status(500).json({ error: "Erro no debug" });
  }
});

module.exports = router;