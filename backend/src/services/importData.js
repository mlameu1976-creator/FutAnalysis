import pkg from "pg";

const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

const API_KEY = process.env.API_KEY;

// 🔥 IMPORTAR LIGA
export async function importLeague(leagueId) {
  try {
    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventspastleague.php?id=${leagueId}`;

    // ✅ fetch nativo (SEM node-fetch)
    const res = await fetch(url);
    const data = await res.json();

    if (!data.events) {
      console.log("Nenhum dado retornado");
      return;
    }

    for (const game of data.events) {
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
        ON CONFLICT DO NOTHING
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
    }

    console.log("✅ Liga importada:", leagueId);
  } catch (error) {
    console.error("❌ Erro import:", error);
  }
}