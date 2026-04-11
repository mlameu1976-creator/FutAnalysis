const axios = require("axios");

console.log("🔥 INGESTION MULTI-LIGAS 🔥");

// IDs reais TheSportsDB
const LEAGUES = [
  { name: "Premier League", id: 4328 },
  { name: "Championship", id: 4329 },
  { name: "Serie A", id: 4332 },
  { name: "Serie B", id: 4394 },
  { name: "La Liga", id: 4335 },
  { name: "La Liga 2", id: 4400 },
  { name: "Bundesliga", id: 4331 },
  { name: "2. Bundesliga", id: 4396 },
  { name: "3. Liga", id: 4397 },
  { name: "Ligue 1", id: 4334 },
  { name: "Ligue 2", id: 4401 },
  { name: "Brasileirão Série A", id: 4351 },
  { name: "Brasileirão Série B", id: 4352 },
  { name: "MLS", id: 4346 },
  { name: "Eredivisie", id: 4337 },
  { name: "Primeira Liga", id: 4344 },
  { name: "Super Lig", id: 4339 }
];

async function ingestAll() {
  try {
    let allMatches = [];

    for (let league of LEAGUES) {
      console.log(`📥 Buscando: ${league.name}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=${league.id}`
      );

      const data = res?.data;

      if (!data || !Array.isArray(data.events)) {
        console.log(`⚠️ sem jogos: ${league.name}`);
        continue;
      }

      for (let ev of data.events) {
        if (!ev) continue;

        allMatches.push({
          match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
          league: league.name,
          date: ev.dateEvent
        });
      }
    }

    console.log(`✅ TOTAL DE JOGOS: ${allMatches.length}`);

    return allMatches;

  } catch (err) {
    console.log("❌ ERRO:", err.message);
    return [];
  }
}

module.exports = { ingestAll };