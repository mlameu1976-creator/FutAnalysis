const axios = require("axios");

console.log("🔥 INGESTION HÍBRIDA (COMPLETA) 🔥");

const LEAGUES = [
  { id: 4336, name: "Eredivisie" },        // Holanda
  { id: 4356, name: "Eliteserien" },       // Noruega
  { id: 4351, name: "Brasileirão A" },
  { id: 4352, name: "Brasileirão B" },
  { id: 4346, name: "MLS" }
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

    // =========================
    // 1. PEGAR GERAL (eventsday)
    // =========================
    const dates = [getDate(0), getDate(1)];

    for (let date of dates) {
      console.log(`📅 GLOBAL ${date}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=${date}&s=Soccer`
      );

      const events = res.data?.events || [];

      for (let ev of events) {
        if (!ev.strHomeTeam || !ev.strAwayTeam) continue;

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

      await delay(800);
    }

    // =========================
    // 2. GARANTIR LIGAS ESPECÍFICAS
    // =========================
    for (let league of LEAGUES) {
      console.log(`🎯 FORÇANDO ${league.name}`);

      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=${league.id}`
      );

      const events = res.data?.events || [];

      for (let ev of events) {
        if (!ev.strHomeTeam || !ev.strAwayTeam) continue;

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