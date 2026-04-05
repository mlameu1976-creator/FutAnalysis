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

// 🔥 FUNÇÃO POISSON
function poisson(lambda, k) {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
}

function factorial(n) {
  if (n === 0) return 1;
  let result = 1;
  for (let i = 1; i <= n; i++) result *= i;
  return result;
}

// 🔥 PROBABILIDADE OVER 2.5 (REAL)
function over25Probability(homeExp, awayExp) {
  let prob = 0;

  for (let i = 0; i <= 5; i++) {
    for (let j = 0; j <= 5; j++) {
      const totalGoals = i + j;

      if (totalGoals > 2) {
        prob += poisson(homeExp, i) * poisson(awayExp, j);
      }
    }
  }

  return prob;
}

// 🔥 OPORTUNIDADES PROFISSIONAIS
router.get("/opportunities", async (req, res) => {
  try {
    // 🔥 stats por time + liga
    const stats = await pool.query(`
      SELECT 
        home_team as team,
        league_id,
        AVG(home_goals) as attack,
        AVG(away_goals) as defense
      FROM matches
      GROUP BY home_team, league_id
    `);

    const teams = stats.rows;

    let opportunities = [];

    for (let i = 0; i < teams.length; i++) {
      for (let j = 0; j < teams.length; j++) {
        if (i === j) continue;

        const home = teams[i];
        const away = teams[j];

        // 🔥 só mesma liga
        if (home.league_id !== away.league_id) continue;

        const homeAttack = Number(home.attack);
        const awayDefense = Number(away.defense);

        const awayAttack = Number(away.attack);
        const homeDefense = Number(home.defense);

        // 🔥 expectativa de gols (modelo simples)
        const homeExp = (homeAttack + awayDefense) / 2;
        const awayExp = (awayAttack + homeDefense) / 2;

        const totalExp = homeExp + awayExp;

        // 🔥 PROBABILIDADE REAL
        const probability = over25Probability(homeExp, awayExp);

        // 🔥 ODDS simulada mais real
        const odd = 1.7 + Math.random() * 0.8;

        // 🔥 EV
        const ev = (probability * odd - 1) * 100;

        if (ev > 5 && probability > 0.55) {
          opportunities.push({
            home_team: home.team,
            away_team: away.team,
            league_id: home.league_id,
            expectedGoals: totalExp.toFixed(2),
            probability: (probability * 100).toFixed(1) + "%",
            odd: odd.toFixed(2),
            ev: ev.toFixed(2) + "%",
          });
        }
      }
    }

    opportunities.sort((a, b) => parseFloat(b.ev) - parseFloat(a.ev));

    res.json(opportunities.slice(0, 50));

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;