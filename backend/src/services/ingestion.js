const axios = require("axios");

const API_KEY = process.env.API_KEY;

async function ingestAll() {
  try {
    console.log("🔥 INICIANDO INGESTAO");

    const res = await axios.get(
      `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=4328`
    );

    // 🔥 PROTEÇÃO TOTAL
    if (!res || !res.data) {
      console.log("❌ resposta inválida");
      return [];
    }

    const events = res.data.events;

    if (!Array.isArray(events)) {
      console.log("⚠️ events nao é array");
      return [];
    }

    const matches = [];

    for (const ev of events) {
      if (!ev) continue;

      const home = ev.strHomeTeam || "Time A";
      const away = ev.strAwayTeam || "Time B";

      matches.push({
        match: `${home} vs ${away}`,
        league: ev.strLeague || "Unknown",
        date: ev.dateEvent || null
      });
    }

    console.log(`✅ ${matches.length} jogos carregados`);

    return matches;

  } catch (err) {
    console.log("❌ ERRO INGESTION:", err.message);
    return [];
  }
}

module.exports = { ingestAll };