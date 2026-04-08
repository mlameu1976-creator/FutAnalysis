const axios = require("axios");
const db = require("../db");

console.log("🔥 INGESTION REAL RODANDO");

const API_KEY =
  process.env.THESPORTSDB_API_KEY || process.env.SPORTSDB_API_KEY;

const LEAGUES = [4328, 4331, 4332, 4334, 4335];

const api = axios.create({
  timeout: 10000,
});

// ===============================
// FETCH
// ===============================
async function fetchMatches(leagueId) {
  try {
    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=${leagueId}`;

    const res = await api.get(url);

    if (!res.data || !res.data.events) {
      console.log(`⚠️ Liga ${leagueId} sem eventos`);
      return [];
    }

    console.log(`✅ Liga ${leagueId}: ${res.data.events.length} jogos`);

    return res.data.events;
  } catch (err) {
    console.log(`❌ ERRO API liga ${leagueId}:`, err.message);
    return [];
  }
}

// ===============================
// XG FAKE
// ===============================
function generateFakeXG() {
  return {
    home_xg_for: 1.2 + Math.random(),
    home_xg_against: 1.0 + Math.random(),
    away_xg_for: 1.0 + Math.random(),
    away_xg_against: 1.2 + Math.random(),
  };
}

// ===============================
// INGESTÃO
// ===============================
async function runIngestion() {
  console.log("🚀 INICIANDO INGESTÃO...");

  let total = 0;

  for (const leagueId of LEAGUES) {
    const matches = await fetchMatches(leagueId);

    for (const m of matches) {
      try {
        if (!m.strHomeTeam || !m.strAwayTeam || !m.dateEvent) {
          console.log("⚠️ Jogo inválido ignorado");
          continue;
        }

        const xg = generateFakeXG();

        await db.query(
          `
          INSERT INTO matches (
            home_team,
            away_team,
            match_date,
            home_xg_for,
            home_xg_against,
            away_xg_for,
            away_xg_against
          )
          VALUES ($1,$2,$3,$4,$5,$6,$7)
        `,
          [
            m.strHomeTeam,
            m.strAwayTeam,
            m.dateEvent,
            xg.home_xg_for,
            xg.home_xg_against,
            xg.away_xg_for,
            xg.away_xg_against,
          ]
        );

        total++;
      } catch (err) {
        console.log("❌ ERRO INSERT:", err.message);
      }
    }
  }

  console.log(`✅ TOTAL IMPORTADO: ${total}`);
}

module.exports = {
  runIngestion,
};