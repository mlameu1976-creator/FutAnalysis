import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// ✅ TESTE BANCO
router.get("/debug", async (req, res) => {
  try {
    const total = await pool.query("SELECT COUNT(*) FROM matches");

    const sample = await pool.query(`
      SELECT home_team, away_team, home_goals, away_goals
      FROM matches
      LIMIT 10
    `);

    res.json({
      total_matches: total.rows[0].count,
      sample: sample.rows,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 🔥 SEM FILTRO (FORÇADO)
router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        home_team,
        COUNT(*) as games,
        AVG(home_goals + away_goals) as avg_goals
      FROM matches
      GROUP BY home_team
      LIMIT 50
    `);

    const data = result.rows.map((team) => ({
      home_team: team.home_team,
      avg_goals: Number(team.avg_goals).toFixed(2),
      games: team.games,
    }));

    res.json(data);

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;