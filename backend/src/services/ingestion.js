const axios = require("axios");

console.log("🔥 INGESTION FINAL COM FILTRO POR ID 🔥");

// LISTA REAL (baseada no que você pediu)
const LEAGUE_IDS = [
  4328, // Premier League
  4329, // Championship
  4332, // Serie A
  4394, // Serie B
  4335, // La Liga
  4400, // La Liga 2
  4331, // Bundesliga
  4396, // 2 Bundesliga
  4397, // 3 Liga
  4334, // Ligue 1
  4401, // Ligue 2
  4351, // Brasileirão A
  4352, // Brasileirão B
  4346, // MLS

  // ADICIONANDO MAIS DO QUE VOCÊ PEDIU
  4336, // Eredivisie (Holanda)
  4337, // Primeira Liga (Portugal)
  4344, // Scottish Premiership
  4355, // Danish Superliga
  4356, // Norwegian Eliteserien
  4350, // Austrian Bundesliga
  4339, // Turkish Super Lig
  4380, // Polish Ekstraklasa
  4358, // Argentine Primera
  4359, // Colombia Primera A
  4354  // Liga MX
];

const delay = (ms) => new Promise(res => setTimeout(res, ms));

function getDate(offset = 0) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return d.toISOString().split("T")[0];
}

async function ingestAll() {
  try {
    const allMatches = [];
    const seen = new Set();

    const dates = [getDate(0), getDate(1)];

    for (let date of dates) {
      console.log(`📅 ${date}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=${date}&s=Soccer`
      );

      const events = res.data?.events;

      if (!Array.isArray(events)) continue;

      for (let ev of events) {
        if (!ev.idLeague) continue;

        // 🔥 FILTRO REAL
        if (!LEAGUE_IDS.includes(parseInt(ev.idLeague))) continue;

        if (!ev.strHomeTeam || !ev.strAwayTeam) continue;

        const key = `${ev.strHomeTeam}_${ev.strAwayTeam}_${ev.dateEvent}`;

        if (seen.has(key)) continue;
        seen.add(key);

        allMatches.push({
          match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
          league: ev.strLeague,
          date: ev.dateEvent
        });
      }

      await delay(1200);
    }

    console.log(`✅ TOTAL FINAL: ${allMatches.length}`);

    return allMatches;

  } catch (err) {
    console.log("❌ ERRO:", err.message);
    return [];
  }
}

module.exports = { ingestAll };