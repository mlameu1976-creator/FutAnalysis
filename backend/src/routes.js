import express from "express";
import pkg from "pg";

const { Pool } = pkg;
const router = express.Router();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// ---------------- POISSON ----------------
function factorial(n) {
  if (n === 0) return 1;
  let r = 1;
  for (let i = 1; i <= n; i++) r *= i;
  return r;
}

function poisson(lambda, k) {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
}

function matrix(homeExp, awayExp) {
  let arr = [];
  for (let i = 0; i <= 5; i++) {
    for (let j = 0; j <= 5; j++) {
      arr.push({ home: i, away: j, prob: poisson(homeExp, i) * poisson(awayExp, j) });
    }
  }
  return arr;
}

// ---------------- MERCADOS ----------------
function calc(matrix, type) {
  if (type === "OVER25") return matrix.filter(m => m.home + m.away > 2).reduce((a, b) => a + b.prob, 0);
  if (type === "OVER15") return matrix.filter(m => m.home + m.away > 1).reduce((a, b) => a + b.prob, 0);
  if (type === "BTTS") return matrix.filter(m => m.home > 0 && m.away > 0).reduce((a, b) => a + b.prob, 0);
  if (type === "HOME") return matrix.filter(m => m.home > m.away).reduce((a, b) => a + b.prob, 0);
  if (type === "AWAY") return matrix.filter(m => m.away > m.home).reduce((a, b) => a + b.prob, 0);
}

// ---------------- EV ----------------
function ev(prob, odd) {
  return (prob * odd - 1) * 100;
}

// ---------------- ROTA ----------------
router.get("/opportunities", async (req, res) => {
  try {
    const stats = await pool.query(`
      SELECT home_team, league_id,
      AVG(home_goals) as attack,
      AVG(away_goals) as defense
      FROM matches
      GROUP BY home_team, league_id
    `);

    const teams = stats.rows;
    let results = [];

    for (let i = 0; i < teams.length; i++) {
      for (let j = 0; j < teams.length; j++) {

        if (i === j) continue;

        const home = teams[i];
        const away = teams[j];

        if (home.league_id !== away.league_id) continue;

        const avg = 2.6;

        const homeExp = (home.attack / avg) * (away.defense / avg) * avg;
        const awayExp = (away.attack / avg) * (home.defense / avg) * avg;

        const m = matrix(homeExp, awayExp);

        const markets = [
          { name: "OVER 2.5", prob: calc(m, "OVER25"), odd: 1.9 },
          { name: "OVER 1.5", prob: calc(m, "OVER15"), odd: 1.4 },
          { name: "BTTS", prob: calc(m, "BTTS"), odd: 1.8 },
          { name: "HOME WIN", prob: calc(m, "HOME"), odd: 2.3 },
          { name: "AWAY WIN", prob: calc(m, "AWAY"), odd: 2.3 },
        ];

        markets.forEach(mkt => {

          const probability = Math.min(mkt.prob, 0.75); // 🔥 trava realista
          const value = ev(probability, mkt.odd);

          if (value > 5 && probability > 0.55) {
            results.push({
              home_team: home.home_team,
              away_team: away.home_team,
              market: mkt.name,
              probability: (probability * 100).toFixed(1) + "%",
              odd: mkt.odd,
              ev: value.toFixed(2) + "%",
            });
          }

        });

      }
    }

    results.sort((a, b) => parseFloat(b.ev) - parseFloat(a.ev));

    res.json(results.slice(0, 50));

  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

export default router;