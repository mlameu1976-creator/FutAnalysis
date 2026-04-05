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

// ---------------- MATRIZ ----------------
function matchMatrix(homeExp, awayExp) {
  let matrix = [];

  for (let i = 0; i <= 5; i++) {
    for (let j = 0; j <= 5; j++) {
      const prob = poisson(homeExp, i) * poisson(awayExp, j);
      matrix.push({ home: i, away: j, prob });
    }
  }

  return matrix;
}

// ---------------- MERCADOS ----------------
function over25(matrix) {
  return matrix.filter(m => m.home + m.away > 2)
    .reduce((acc, m) => acc + m.prob, 0);
}

function over15(matrix) {
  return matrix.filter(m => m.home + m.away > 1)
    .reduce((acc, m) => acc + m.prob, 0);
}

function btts(matrix) {
  return matrix.filter(m => m.home > 0 && m.away > 0)
    .reduce((acc, m) => acc + m.prob, 0);
}

function homeWin(matrix) {
  return matrix.filter(m => m.home > m.away)
    .reduce((acc, m) => acc + m.prob, 0);
}

function awayWin(matrix) {
  return matrix.filter(m => m.away > m.home)
    .reduce((acc, m) => acc + m.prob, 0);
}

function goalHT(homeExp, awayExp) {
  const htExp = (homeExp + awayExp) * 0.45;
  return 1 - Math.exp(-htExp);
}

// ---------------- EV ----------------
function calcEV(prob, odd) {
  return (prob * odd - 1) * 100;
}

// ---------------- ROTA PRINCIPAL ----------------
router.get("/opportunities", async (req, res) => {
  try {
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

        if (home.league_id !== away.league_id) continue;

        const homeAttack = Number(home.attack);
        const awayAttack = Number(away.attack);
        const homeDefense = Number(home.defense);
        const awayDefense = Number(away.defense);

        // 🔥 MODELO NORMALIZADO (CORRETO)
        const avgGoals = 2.6;

        const homeStrength = homeAttack / avgGoals;
        const awayStrength = awayAttack / avgGoals;

        const homeDefenseStrength = homeDefense / avgGoals;
        const awayDefenseStrength = awayDefense / avgGoals;

        const homeExp = homeStrength * awayDefenseStrength * avgGoals;
        const awayExp = awayStrength * homeDefenseStrength * avgGoals;

        const matrix = matchMatrix(homeExp, awayExp);

        const markets = [
          { name: "OVER 2.5", prob: over25(matrix), odd: 1.9 },
          { name: "OVER 1.5", prob: over15(matrix), odd: 1.4 },
          { name: "BTTS", prob: btts(matrix), odd: 1.8 },
          { name: "HOME WIN", prob: homeWin(matrix), odd: 2.2 },
          { name: "AWAY WIN", prob: awayWin(matrix), odd: 2.5 },
          { name: "GOAL HT", prob: goalHT(homeExp, awayExp), odd: 1.6 },
        ];

        markets.forEach(m => {

          // 🔥 LIMITAR PROBABILIDADE IRREAL
          const probability = Math.min(m.prob, 0.85);

          const ev = calcEV(probability, m.odd);

          // 🔥 FILTRO INTELIGENTE POR MERCADO
          let minProb = 0.55;

          if (m.name === "OVER 2.5") minProb = 0.58;
          if (m.name === "OVER 1.5") minProb = 0.70;
          if (m.name === "BTTS") minProb = 0.57;
          if (m.name === "HOME WIN" || m.name === "AWAY WIN") minProb = 0.52;
          if (m.name === "GOAL HT") minProb = 0.60;

          if (ev > 8 && probability > minProb) {
            opportunities.push({
              match: `${home.team} x ${away.team}`,
              league_id: home.league_id,
              market: m.name,
              probability: (probability * 100).toFixed(1) + "%",
              odd: m.odd,
              ev: ev.toFixed(2) + "%",
            });
          }
        });

      }
    }

    // 🔥 RANKING
    opportunities.sort((a, b) => parseFloat(b.ev) - parseFloat(a.ev));

    res.json(opportunities.slice(0, 50));

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;