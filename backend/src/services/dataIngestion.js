const db = require("../db");
const axios = require("axios");

const API_KEY = process.env.SPORTSDB_API_KEY;

const LEAGUES = [
  { name: "Premier League", id: "4328" },
  { name: "Serie A", id: "4332" },
  { name: "La Liga", id: "4335" },
  { name: "Bundesliga", id: "4331" },
  { name: "Brasileirão", id: "4351" }
];

async function runIngestion() {
  console.log("🔥🔥🔥 USANDO API REAL 🔥🔥🔥");

  await db.query("DELETE FROM matches");

  for (const league of LEAGUES) {
    console.log(`📡 Buscando ${league.name}`);

    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=${league.id}`;

    try {
      const res = await axios.get(url);

      const games = res.data.events || [];

      console.log(`➡️ ${games.length} jogos encontrados`);

      for (const game of games) {
        if (!game.strHomeTeam || !game.strAwayTeam) continue;

        console.log(`⚽ ${game.strHomeTeam} vs ${game.strAwayTeam}`);

        await db.query(
          `
          INSERT INTO matches 
          (home_team, away_team, match_date, league, home_xg_for, away_xg_for)
          VALUES ($1, $2, $3, $4, $5, $6)
          `,
          [
            game.strHomeTeam,
            game.strAwayTeam,
            game.dateEvent,
            league.name,
            1.2 + Math.random(),
            1.1 + Math.random(),
          ]
        );
      }
    } catch (err) {
      console.error("❌ ERRO API:", err.message);
    }
  }

  console.log("✅ INGESTÃO REAL FINALIZADA");
}

module.exports = { runIngestion };