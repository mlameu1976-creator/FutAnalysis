const express = require("express");
const router = express.Router();

const db = require("../db");
const { generateOpportunities } = require("../services/scoringEngine");

router.get("/", async (req, res) => {
  try {
    console.log("🚀 Buscando partidas...");

    const result = await db.query(`
      SELECT *
      FROM matches
      LIMIT 50
    `);

    console.log("📊 Matches encontrados:", result.rows.length);

    const matches = result.rows;

    if (!matches || matches.length === 0) {
      return res.json({ error: "Nenhum dado encontrado no banco" });
    }

    console.log("⚙️ Gerando oportunidades...");

    const opportunities = generateOpportunities(matches);

    console.log("✅ Oportunidades geradas:", opportunities.length);

    res.json(opportunities);

  } catch (error) {
    console.error("🔥 ERRO REAL:", error);

    res.status(500).json({
      error: "Erro ao gerar oportunidades",
      details: error.message
    });
  }
});

module.exports = router;