import pkg from "pg";

const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

const API_KEY = "3";

export async function importLeague(leagueId) {
  try {
    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventspastleague.php?id=${leagueId}`;

    const res = await fetch(url);
    const data = await res.json();

    if (!data.events) {
      console.log("Sem eventos");
      return;
    }

    // 🔥 DESATIVA FK TEMPORARIAMENTE
    await pool.query(`SET session_replication_role = 'replica';`);

    let inserted = 0;

    for (const game of data.events) {
      try {
        if (game.intHomeScore === null || game.intAwayScore === null) continue;

        await pool.query(
          `
          INSERT INTO matches (
            home_team,
            away_team,
            league_id,
            home_goals,
            away_goals,
            over_25,
            btts,
            is_finished
          )
          VALUES ($1,$2,$3,$4,$5,$6,$7,true)
          `,
          [
            game.strHomeTeam,
            game.strAwayTeam,
            leagueId,
            Number(game.intHomeScore),
            Number(game.intAwayScore),
            (game.intHomeScore + game.intAwayScore) > 2,
            (game.intHomeScore > 0 && game.intAwayScore > 0),
          ]
        );

        inserted++;

      } catch (err) {
        console.error("ERRO INSERT:", err.message);
      }
    }

    // 🔥 REATIVA FK
    await pool.query(`SET session_replication_role = 'origin';`);

    console.log(`✅ Inseridos: ${inserted}`);

  } catch (error) {
    console.error("Erro geral:", error.message);
  }
}