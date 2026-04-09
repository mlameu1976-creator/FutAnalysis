const express = require("express");
const router = express.Router();

const db = require("./db");

// 🔥 IMPORT CORRETO DO ENGINE PROFISSIONAL
const { generateOpportunities } = require("./services/scoringEngine");

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
// OPPORTUNITIES (ENGINE PRO)
// ===============================
router.get("/opportunities", async (req, res) => {
  try {
    const result = await db.query(`
      SELECT * FROM matches
      ORDER BY match_date ASC
      LIMIT 50
    `);

    // 🔥 AQUI É A DIFERENÇA CRÍTICA
    const opportunities = generateOpportunities(result.rows);

    res.json(opportunities);

  } catch (err) {
    console.error("❌ ERRO /opportunities:", err);
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