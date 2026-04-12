const axios = require("axios");

console.log("🚨🚨🚨 NOVA INGESTAO OFICIAL 🚨🚨🚨");

const LEAGUES = [
  { id: 9999, name: "TESTE LIGA NOVA" }
];

const delay = (ms) => new Promise(r => setTimeout(r, ms));

async function ingestAll() {
  const allMatches = [];
  const seen = new Set();

  for (let league of LEAGUES) {
    console.log("📥", league.name);

    try {
      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=${league.id}`
      );

      const events = res.data?.events || [];

      for (let ev of events) {
        if (!ev.strHomeTeam || !ev.strAwayTeam) continue;

        const key = `${ev.strHomeTeam}_${ev.strAwayTeam}_${ev.dateEvent}`;
        if (seen.has(key)) continue;
        seen.add(key);

        allMatches.push({
          match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
          league: league.name,
          date: ev.dateEvent
        });
      }

      await delay(1200);

    } catch (err) {
      console.log("❌ erro:", league.name);
    }
  }

  console.log("✅ TOTAL FINAL:", allMatches.length);

  return allMatches;
}

module.exports = { ingestAll };