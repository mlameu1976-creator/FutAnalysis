const db = require("../db");
const { LEAGUES } = require("../config/leagues");

async function runIngestion() {
  console.log("🔥 INGESTÃO TOTAL (TODAS AS LIGAS)");

  try {
    // LIMPA TUDO
    await db.query("DELETE FROM matches");

    console.log(`📊 TOTAL DE LIGAS: ${LEAGUES.length}`);

    for (let i = 0; i < LEAGUES.length; i++) {
      const league = LEAGUES[i];

      console.log(`➡️ ${i + 1}/${LEAGUES.length} - ${league.name}`);

      const home = `${league.name} Team A`;
      const away = `${league.name} Team B`;

      await db.query(
        `
        INSERT INTO matches 
        (home_team, away_team, match_date, league, home_xg_for, away_xg_for)
        VALUES ($1, $2, NOW(), $3, $4, $5)
        `,
        [
          home,
          away,
          league.name,
          1.2 + Math.random(),
          1.1 + Math.random(),
        ]
      );
    }

    console.log("✅ INGESTÃO FINALIZADA - TODAS AS LIGAS");
  } catch (err) {
    console.error("❌ ERRO INGESTÃO:", err.message);
  }
}

module.exports = { runIngestion };