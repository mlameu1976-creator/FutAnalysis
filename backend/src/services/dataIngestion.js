throw new Error("🔥 TESTE FORÇADO DE DEPLOY");
console.log("🔥 NOVA VERSÃO DO INGESTION RODANDO");
const axios = require("axios");
const db = require("../db");

const API_KEY =
  process.env.THESPORTSDB_API_KEY || process.env.SPORTSDB_API_KEY;

const LEAGUES = [4328, 4331, 4332, 4334, 4335];

// ===============================
// AXIOS CONFIG (ANTI-FALHA)
// ===============================
const api = axios.create({
  timeout: 10000,
});

// ===============================
// FETCH COM DEBUG REAL
// ===============================
async function fetchMatches(leagueId) {
  const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=${leagueId}`;

  try {
    console.log(`🌍 Fetch liga ${leagueId}`);

    const res = await api.get(url);

    if (!res.data) {
      console.log(`❌ Sem data`);
      return [];
    }

    if (!res.data.events) {
      console.log(`⚠️ Sem eventos`);
      return [];
    }

    console.log(`✅ ${res.data.events.length} jogos encontrados`);

    return res.data.events;
  } catch (err) {
    console.log(`❌ ERRO DETALHADO liga ${leagueId}`);
    console.log("➡️ status:", err.response?.status);
    console.log("➡️ data:", err.response?.data);
    console.log("➡️ message:", err.message);

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
    console.log(`📊 Liga ${leagueId}`);

    const matches = await fetchMatches(leagueId);

    for (const m of matches) {
      try {
        if (!m.strHomeTeam || !m.strAwayTeam || !m.dateEvent) {
          console.log("⚠️ Jogo inválido");
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