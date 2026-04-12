const axios = require("axios");

console.log("🔥 INGESTION REAL COMPLETA 🔥");

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

async function ingestAll() {
  try {
    const allMatches = [];
    const seen = new Set();

    for (let league of LEAGUES) {
      try {
        console.log(`📥 ${league.name}`);

        const res = await axios.get(
          `https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=${league.id}&s=2024-2025`
        );

        const data = res?.data;

        if (data && Array.isArray(data.events)) {
          for (let ev of data.events) {
            if (!ev || !ev.strHomeTeam || !ev.strAwayTeam) continue;

            const key = `${ev.strHomeTeam}_${ev.strAwayTeam}_${ev.dateEvent}`;

            if (!seen.has(key)) {
              seen.add(key);

              allMatches.push({
                match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
                league: league.name,
                date: ev.dateEvent
              });
            }
          }
        }

        await delay(1200);

      } catch (err) {
        console.log(`❌ erro ${league.name}:`, err.message);
        await delay(1500);
      }
    }

    console.log(`✅ TOTAL FINAL: ${allMatches.length}`);

    return allMatches;

  } catch (err) {
    console.log("❌ ERRO GERAL:", err.message);
    return [];
  }
}

module.exports = { ingestAll };