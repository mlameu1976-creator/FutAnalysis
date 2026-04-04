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

// 🔥 NOVO MOTOR (POR TIME)
router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        home_team,
        COUNT(*) as games,
        AVG(home_goals) as avg_scored,
        AVG(away_goals) as avg_conceded,
        AVG(CASE WHEN over_25 = true THEN 1 ELSE 0 END) as over25_prob
      FROM matches
      WHERE is_finished = true
      GROUP BY home_team
      HAVING COUNT(*) > 3
      LIMIT 50
    `);

    const games = result.rows.map((team) => {
      const probability = Number(team.over25_prob);
      const odd = 2.0;

      const ev = (probability * odd - 1) * 100;

      return {
        home_team: team.home_team,
        away_team: "vs Média Liga",
        league: "Global",
        avg_goals: Number(team.avg_scored).toFixed(2),
        probability,
        odd,
        ev,
      };
    });

    const filtered = games
      .filter((g) => g.ev > 0)
      .sort((a, b) => b.ev - a.ev);

    res.json(filtered);

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

export default router;