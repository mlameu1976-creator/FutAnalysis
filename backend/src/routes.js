import express from "express";
import pkg from "pg";

const { Pool } = pkg;

const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// ROOT
router.get("/", (req, res) => {
  res.send("🚀 FutAnalysis Backend ONLINE");
});

// 🔥 MOTOR REAL DE OPORTUNIDADES
router.get("/opportunities", async (req, res) => {
  try {
    // 🔥 estatísticas por time (ataque/defesa)
    const stats = await pool.query(`
      SELECT 
        home_team as team,
        AVG(home_goals) as attack,
        AVG(away_goals) as defense
      FROM matches
      GROUP BY home_team
    `);

    const teams = stats.rows;

    let opportunities = [];

    // 🔥 cruzar times (simulação de jogos)
    for (let i = 0; i < teams.length; i++) {
      for (let j = 0; j < teams.length; j++) {
        if (i === j) continue;

        const home = teams[i];
        const away = teams[j];

        // expectativa de gols
        const expectedGoals =
          (Number(home.attack) + Number(away.defense)) / 2;

        // probabilidade over 2.5 (simplificada)
        const probability = Math.min(expectedGoals / 3, 0.95);

        const odd = 2.0;

        const ev = (probability * odd - 1) * 100;

        if (ev > 5) {
          opportunities.push({
            home_team: home.team,
            away_team: away.team,
            expectedGoals: expectedGoals.toFixed(2),
            probability: (probability * 100).toFixed(0) + "%",
            ev: ev.toFixed(2) + "%",
          });
        }
      }
    }

    // ordenar por valor
    opportunities.sort((a, b) => parseFloat(b.ev) - parseFloat(a.ev));

    res.json(opportunities.slice(0, 50));

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;