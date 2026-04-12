const axios = require("axios");

console.log("🔥 INGESTION FINAL FORÇADA POR LIGA 🔥");

// TODAS as ligas que você pediu
const LEAGUES = [
  { id: 4328, name: "Premier League" },
  { id: 4329, name: "Championship" },
  { id: 4332, name: "Serie A" },
  { id: 4394, name: "Serie B" },
  { id: 4335, name: "La Liga" },
  { id: 4400, name: "La Liga 2" },
  { id: 4331, name: "Bundesliga" },
  { id: 4396, name: "2. Bundesliga" },
  { id: 4397, name: "3. Liga" },
  { id: 4334, name: "Ligue 1" },
  { id: 4401, name: "Ligue 2" },
  { id: 4351, name: "Brasileirão Série A" },
  { id: 4352, name: "Brasileirão Série B" },
  { id: 4346, name: "MLS" },

  // 🔥 AS QUE NÃO ESTÃO VINDO
  { id: 4336, name: "Eredivisie" },       // Holanda
  { id: 4356, name: "Eliteserien" },      // Noruega
  { id: 4337, name: "Primeira Liga" },    // Portugal
  { id: 4339, name: "Turkish Super Lig" },
  { id: 4358, name: "Argentina" },
  { id: 4359, name: "Colombia" },
  { id: 4354, name: "Liga MX" }
];

const delay = (ms) => new Promise(res => setTimeout(res, ms));

async function ingestAll() {
  try {
    const allMatches = [];
    const seen = new Set();

    for (let league of LEAGUES) {
      console.log(`📥 ${league.name}`);

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
        console.log(`❌ erro ${league.name}`);
      }
    }

    console.log(`✅ TOTAL FINAL: ${allMatches.length}`);

    return allMatches;

  } catch (err) {
    console.log("❌ ERRO:", err.message);
    return [];
  }
}

module.exports = { ingestAll };