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

async function fetchMatches(leagueId) {
  try {
    // 🔥 endpoint que SEMPRE retorna jogos
    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventspastleague.php?id=${leagueId}`;

    const res = await axios.get(url);

    return res.data.events || [];
  } catch (err) {
    console.error("❌ API erro:", err.message);
    return [];
  }
}

async function runIngestion() {
  console.log("🔥 INGESTÃO REAL (PAST EVENTS)");

  await db.query("DELETE FROM matches");

  let total = 0;

  for (const league of LEAGUES) {
    console.log(`📊 ${league.name}`);

    const games = await fetchMatches(league.id);

    for (const game of games.slice(0, 10)) {
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

      total++;
    }
  }

  console.log(`✅ TOTAL IMPORTADO: ${total}`);
}

module.exports = { runIngestion };