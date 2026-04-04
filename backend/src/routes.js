import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// 🚀 ROOT
router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// 🔥 OPORTUNIDADES REAIS (BASEADO EM HISTÓRICO)
router.get("/opportunities", async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        home_team,
        away_team,
        league_id,
        AVG(home_goals + away_goals) as avg_goals,
        AVG(CASE WHEN over_25 = true THEN 1 ELSE 0 END) as over25_prob,
        AVG(CASE WHEN btts = true THEN 1 ELSE 0 END) as btts_prob
      FROM matches
      WHERE is_finished = true
      GROUP BY home_team, away_team, league_id
      HAVING COUNT(*) > 5
      LIMIT 50
    `);

    const games = result.rows.map((g) => {
      const probability = Number(g.over25_prob);
      const odd = 2.0;

      const ev = (probability * odd - 1) * 100;

      return {
        home_team: g.home_team,
        away_team: g.away_team,
        league: g.league_id,
        avg_goals: Number(g.avg_goals).toFixed(2),
        probability,
        odd,
        ev,
        btts: Number(g.btts_prob),
      };
    });

    // 🔥 FILTRO DE VALOR REAL
    const filtered = games
      .filter((g) => g.ev > 5)
      .sort((a, b) => b.ev - a.ev);

    res.json(filtered);

  } catch (error) {
    console.error("ERRO:", error);
    res.status(500).json({ error: error.message });
  }
});

export default router;