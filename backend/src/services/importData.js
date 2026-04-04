import pkg from "pg";

const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

const API_KEY = "3"; // 🔥 TESTE COM API PÚBLICA

export async function importLeague(leagueId) {
  try {
    const url = `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventspastleague.php?id=${leagueId}`;

    console.log("Buscando:", url);

    const res = await fetch(url);
    const data = await res.json();

    console.log("Resposta API:", data);

    if (!data.events) {
      console.log("⚠️ Nenhum evento encontrado");
      return;
    }

    let inserted = 0;

    for (const game of data.events) {
      if (!game.intHomeScore || !game.intAwayScore) continue;

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
    }

    console.log(`✅ Inseridos: ${inserted}`);

  } catch (error) {
    console.error("❌ Erro import:", error);
  }
}