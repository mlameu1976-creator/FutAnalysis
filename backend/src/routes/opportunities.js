const express = require("express");
const router = express.Router();

const db = require("../db");
const { generateOpportunities } = require("../services/scoringEngine");

router.get("/", async (req, res) => {
  try {
    const result = await db.query(`
      SELECT *
      FROM matches
      WHERE home_goals IS NOT NULL
      AND away_goals IS NOT NULL
      LIMIT 200
    `);

    const matches = result.rows;

    const opportunities = generateOpportunities(matches);

    res.json(opportunities);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Erro ao gerar oportunidades" });
  }
});

module.exports = router;