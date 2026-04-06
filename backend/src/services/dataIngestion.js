const axios = require("axios");
const db = require("../db");

const LEAGUE_IDS = [
  4328, // Premier League
  4329, // Championship
  4334, // La Liga
  4335, // Serie A
  4332, // Bundesliga
];

async function importMatches() {
  for (const leagueId of LEAGUE_IDS) {
    console.log("Importando liga:", leagueId);

    const res = await axios.get(
      `https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=${leagueId}`
    );

    const events = res.data.events || [];

    for (const game of events) {
      await db.query(
        `
        INSERT INTO matches (home_team, away_team, league)
        VALUES ($1, $2, $3)
        ON CONFLICT DO NOTHING
        `,
        [game.strHomeTeam, game.strAwayTeam, game.strLeague]
      );
    }
  }
}

module.exports = { importMatches };