const express = require("express");
const cors = require("cors");
const db = require("./db");

const { runIngestion } = require("./services/dataIngestion");

const app = express();

app.use(cors());
app.use(express.json());

console.log("🔥 SERVER NOVO RODANDO");

// ===============================
// TESTE
// ===============================
app.get("/", (req, res) => {
  res.send("FutAnalysis API rodando 🚀");
});

// ===============================
// OPPORTUNITIES
// ===============================
const { generateMarkets } = require("./services/modelEngine");

app.get("/opportunities", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM matches LIMIT 50");

    const leagueAvg = {
      home_goals: 1.4,
      away_goals: 1.2,
    };

    const opportunities = [];

    for (const match of result.rows) {
      const markets = generateMarkets(match, leagueAvg);

      opportunities.push({
        match: `${match.home_team} vs ${match.away_team}`,
        date: match.match_date,
        markets,
      });
    }

    res.json(opportunities);
  } catch (err) {
    console.error("Erro opportunities:", err.message);
    res.status(500).send("Erro interno");
  }
});

// ===============================
// START
// ===============================
async function start() {
  try {
    await db.query("SELECT 1");

    console.log("🔥 DB conectado");

    await runIngestion();

    app.listen(8080, () => {
      console.log("🚀 Server rodando na porta 8080");
    });
  } catch (err) {
    console.error("❌ ERRO START:", err);
  }
}

start();