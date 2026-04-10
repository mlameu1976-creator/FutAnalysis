const db = require("../db");
const { LEAGUES } = require("../config/leagues");

// ⚠️ SIMULAÇÃO DE FETCH (ajuste se já tiver API real)
async function fetchMatchesByLeague(leagueId) {
  // Aqui você conecta com sua API real
  // Por enquanto retorna vazio para evitar crash
  return [];
}

// SALVAR NO BANCO
async function saveMatches(matches, leagueName) {
  for (const match of matches) {
    try {
      await db.query(
        `
        INSERT INTO matches 
        (home_team, away_team, match_date, league, home_xg_for, away_xg_for)
        VALUES ($1, $2, $3, $4, $5, $6)
        `,
        [
          match.homeTeam,
          match.awayTeam,
          match.date,
          leagueName,
          match.home_xg_for || 1.4,
          match.away_xg_for || 1.2,
        ]
      );
    } catch (err) {
      console.error("Erro ao salvar jogo:", err.message);
    }
  }
}

// INGESTÃO PRINCIPAL
async function runIngestion() {
  console.log("🚀 INICIANDO INGESTÃO...");

  for (const league of LEAGUES) {
    try {
      console.log(`📊 Liga: ${league.name}`);

      const matches = await fetchMatchesByLeague(league.id);

      console.log(`✔ ${matches.length} jogos`);

      await saveMatches(matches, league.name);
    } catch (err) {
      console.error(`❌ Erro liga ${league.name}`, err.message);
    }
  }

  console.log("✅ INGESTÃO FINALIZADA");
}

module.exports = { runIngestion };