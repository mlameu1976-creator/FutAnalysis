const db = require("../db");
const { LEAGUES } = require("../config/leagues");

function generateTeamName(league, index) {
  return `${league.name.split(" ")[0]} FC ${index}`;
}

async function runIngestion() {
  console.log("🔥 INGESTÃO REALISTA");

  try {
    await db.query("DELETE FROM matches");

    for (const league of LEAGUES) {
      console.log(`📊 ${league.name}`);

      for (let i = 1; i <= 3; i++) {
        const home = generateTeamName(league, i);
        const away = generateTeamName(league, i + 10);

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
    }

    console.log("✅ INGESTÃO FINALIZADA");
  } catch (err) {
    console.error("❌ ERRO:", err.message);
  }
}

module.exports = { runIngestion };