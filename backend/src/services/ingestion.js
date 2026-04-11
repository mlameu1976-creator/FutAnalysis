const axios = require("axios");

console.log("🔥 INGESTION 100% LIMPO 🔥");

async function ingestAll() {
  try {
    const res = await axios.get(
      "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4328"
    );

    const data = res?.data;

    if (!data || !data.events || !Array.isArray(data.events)) {
      console.log("⚠️ sem eventos válidos");
      return [];
    }

    const matches = [];

    for (let i = 0; i < data.events.length; i++) {
      const ev = data.events[i];

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
    console.log("❌ ERRO:", err.message);
    return [];
  }
}

module.exports = { ingestAll };