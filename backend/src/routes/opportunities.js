const express = require("express");
const router = express.Router();
const db = require("../db");

// IMPORTAÇÃO CRÍTICA
const { generateOpportunities } = require("../services/scoringEngine");

router.get("/", async (req, res) => {
  try {
    const result = await db.query(`
      SELECT *
      FROM matches
      WHERE home_goals IS NOT NULL
      AND away_goals IS NOT NULL
      ORDER BY match_date DESC
      LIMIT 500
    `);

    const matches = result.rows;

    // 🔥 USANDO O NOVO ENGINE
    const opportunities = generateOpportunities(matches);

    res.json(opportunities);
  } catch (error) {
    console.error("Error generating opportunities:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;