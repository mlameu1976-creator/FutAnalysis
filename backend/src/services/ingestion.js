const axios = require("axios");

const API_KEY = process.env.SPORTDB_API_KEY;

// 🔥 IDS CORRETOS DAS LIGAS (SPORTDB)
const LEAGUES = [
  { id: "4328", name: "Premier League" },
  { id: "4329", name: "Championship" },
  { id: "4335", name: "La Liga" },
  { id: "4336", name: "La Liga 2" },
  { id: "4332", name: "Serie A" },
  { id: "4394", name: "Serie B" },
  { id: "4331", name: "Bundesliga" },
  { id: "4332", name: "2. Bundesliga" },
  { id: "4333", name: "3. Liga" },
  { id: "4334", name: "Ligue 1" },
  { id: "4337", name: "Ligue 2" },
  { id: "4337", name: "Eredivisie" },
  { id: "4344", name: "Eerste Divisie" },
  { id: "4447", name: "Eliteserien" },
  { id: "4351", name: "Brasileirão Série A" },
  { id: "4355", name: "Brasileirão Série B" },
  { id: "4346", name: "MLS" }
];

async function ingestAll() {
  const allMatches = [];

  for (const league of LEAGUES) {
    try {
      console.log(`📡 Buscando ${league.name}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=${league.id}`
      );

      const events = res.data.events;

      if (!Array.isArray(events)) continue;

      for (const e of events) {
        if (!e.strHomeTeam || !e.strAwayTeam) continue;

        allMatches.push({
          match: `${e.strHomeTeam} vs ${e.strAwayTeam}`,
          league: league.name,
          date: e.dateEvent
        });
      }

    } catch (err) {
      console.log(`❌ erro liga ${league.name}`);
    }
  }

  console.log("TOTAL:", allMatches.length);

  return allMatches;
}

module.exports = { ingestAll };