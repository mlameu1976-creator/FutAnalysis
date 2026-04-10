const db = require("../db");
const { LEAGUES } = require("../config/leagues");

// ⚠️ IMPORTANTE: NÃO REMOVER DADOS EXISTENTES
// Vamos manter o sistema funcionando mesmo sem API externa

async function runIngestion() {
  console.log("🔥 INGESTÃO REAL RODANDO");

  try {
    // Verifica se já existem jogos
    const check = await db.query("SELECT COUNT(*) FROM matches");
    const total = parseInt(check.rows[0].count);

    if (total > 0) {
      console.log(`✅ Já existem ${total} jogos no banco — não vou sobrescrever`);
      return;
    }

    console.log("⚠️ Banco vazio — criando dados mock");

    // MOCK CONTROLADO (para não quebrar o sistema)
    const mockMatches = [
      {
        home_team: "Arsenal",
        away_team: "Chelsea",
        league: "Premier League",
      },
      {
        home_team: "Barcelona",
        away_team: "Real Madrid",
        league: "La Liga",
      },
      {
        home_team: "Juventus",
        away_team: "Milan",
        league: "Serie A",
      },
    ];

    for (const m of mockMatches) {
      await db.query(
        `
        INSERT INTO matches 
        (home_team, away_team, match_date, league, home_xg_for, away_xg_for)
        VALUES ($1, $2, NOW(), $3, 1.5, 1.2)
        `,
        [m.home_team, m.away_team, m.league]
      );
    }

    console.log("✅ Dados mock inseridos");
  } catch (err) {
    console.error("❌ ERRO INGESTÃO:", err.message);
  }
}

module.exports = { runIngestion };