const axios = require("axios");
const db = require("../db");

// 🔥 LIGAS PROFISSIONAIS (GLOBAL)
const LEAGUE_IDS = [
  // Inglaterra
  4328, // Premier League
  4329, // Championship
  4396, // League One
  4397, // League Two

  // Espanha
  4335, // La Liga
  4406, // Segunda División

  // Itália
  4332, // Serie A
  4394, // Serie B

  // Alemanha
  4331, // Bundesliga
  4390, // 2. Bundesliga
  4391, // 3. Liga

  // França
  4334, // Ligue 1
  4403, // Ligue 2

  // Brasil
  4351, // Serie A
  4400, // Serie B

  // Holanda
  4337, // Eredivisie
  4405, // Eerste Divisie

  // Portugal
  4344, // Primeira Liga
  4402, // Liga Portugal 2

  // MLS
  4346, // MLS

  // Argentina
  4350, // Liga Profesional

  // México
  4355, // Liga MX

  // Bélgica
  4338, // Jupiler Pro League

  // Turquia
  4339, // Super Lig

  // Escócia
  4330, // Premiership
];

// =============================

async function importMatches() {
  console.log("🚀 INICIANDO INGESTÃO GLOBAL...");

  let total = 0;

  for (const leagueId of LEAGUE_IDS) {
    try {
      console.log(`📥 Liga ${leagueId}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=${leagueId}`
      );

      const events = res.data.events || [];

      console.log(`➡️ ${events.length} jogos`);

      for (const game of events) {
        if (!game.strHomeTeam || !game.strAwayTeam) continue;

        await db.query(
          `
          INSERT INTO matches (home_team, away_team, league)
          VALUES ($1, $2, $3)
          ON CONFLICT DO NOTHING
          `,
          [
            game.strHomeTeam,
            game.strAwayTeam,
            game.strLeague || "unknown"
          ]
        );

        total++;
      }
    } catch (err) {
      console.log("Erro liga:", leagueId);
    }
  }

  console.log("✅ TOTAL IMPORTADO:", total);
}

module.exports = { importMatches };