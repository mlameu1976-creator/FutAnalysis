import { pool } from "../db.js";

export async function getMatchProbability(req, res) {
  const { home, away } = req.query;

  if (!home || !away) {
    return res.status(400).json({
      error: "Informe home e away",
    });
  }

  try {
    /* 🔥 BUSCA NO SEU BANCO REAL */
    const result = await pool.query(
      `
      SELECT *
      FROM historical_matches
      WHERE home_team = $1 OR away_team = $1
      ORDER BY date DESC
      LIMIT 100
    `,
      [home]
    );

    const matches = result.rows;

    if (!matches.length) {
      return res.json({
        home,
        away,
        samples: 0,
        over25: 50,
        btts: 50,
      });
    }

    let over25 = 0;
    let btts = 0;

    matches.forEach((m) => {
      const totalGoals = (m.home_goals || 0) + (m.away_goals || 0);

      if (totalGoals > 2) over25++;
      if ((m.home_goals || 0) > 0 && (m.away_goals || 0) > 0) btts++;
    });

    const total = matches.length;

    res.json({
      home,
      away,
      samples: total,
      over25: Number(((over25 / total) * 100).toFixed(2)),
      btts: Number(((btts / total) * 100).toFixed(2)),
    });
  } catch (err) {
    console.error("Erro backend:", err);
    res.status(500).json({
      error: "Erro interno",
    });
  }
}