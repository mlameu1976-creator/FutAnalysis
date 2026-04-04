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

router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        home_team,
        away_team,
        league_id,
        COUNT(*) as games,
        AVG(home_goals + away_goals) as avg_goals,
        AVG(CASE WHEN over_25 = true THEN 1 ELSE 0 END) as over25_prob,
        AVG(CASE WHEN btts = true THEN 1 ELSE 0 END) as btts_prob
      FROM matches
      WHERE is_finished = true
      GROUP BY home_team, away_team, league_id
      HAVING COUNT(*) > 2
      LIMIT 100
    `);

    const games = result.rows.map((g) => {
      const probability = Number(g.over25_prob);
      const odd = 2.0;

      const ev = (probability * odd - 1) * 100;

      return {
        home_team: g.home_team,
        away_team: g.away_team,
        league: g.league_id,
        games: Number(g.games),
        avg_goals: Number(g.avg_goals).toFixed(2),
        probability,
        odd,
        ev,
        btts: Number(g.btts_prob),
      };
    });

    // 🔥 FILTRO MAIS FLEXÍVEL
    const filtered = games
      .filter((g) => g.ev > 0) // antes era >5
      .sort((a, b) => b.ev - a.ev);

    res.json(filtered);

  } catch (error) {
    console.error("ERRO:", error);
    res.status(500).json({ error: error.message });
  }
});

export default router;