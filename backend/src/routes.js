import express from "express";
import pool from "./db.js";
import { over25Prob } from "./services/poisson.js";

const router = express.Router();

router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        m.id,
        m.home_team,
        m.away_team,
        l.name as league,
        m.home_goals_avg,
        m.away_goals_avg
      FROM matches m
      JOIN leagues l ON l.id = m.league_id
      LIMIT 100
    `);

    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Erro ao buscar dados" });
  }
});

export default router;