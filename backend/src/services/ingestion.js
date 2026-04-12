const axios = require("axios");

console.log("🔥 INGESTION POR DATA (CORRETA) 🔥");

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
  { name: "MLS", id: 4346 }
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

    const dates = [getDate(0), getDate(1)]; // hoje + amanhã

    for (let date of dates) {
      console.log(`📅 Buscando data: ${date}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=${date}&s=Soccer`
      );

      const events = res.data?.events;

      if (!Array.isArray(events)) continue;

      for (let ev of events) {
        if (!ev.strHomeTeam || !ev.strAwayTeam || !ev.strLeague) continue;

        const leagueAllowed = LEAGUES.some(l =>
          ev.strLeague.toLowerCase().includes(l.name.toLowerCase())
        );

        if (!leagueAllowed) continue;

        const key = `${ev.strHomeTeam}_${ev.strAwayTeam}_${ev.dateEvent}`;

        if (!seen.has(key)) {
          seen.add(key);

          allMatches.push({
            match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
            league: ev.strLeague,
            date: ev.dateEvent
          });
        }
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