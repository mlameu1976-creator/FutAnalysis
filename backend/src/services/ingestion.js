const axios = require("axios");

const API_KEY = process.env.SPORTSDB_API_KEY;
const BASE_URL = `https://www.thesportsdb.com/api/v1/json/${API_KEY}`;

// LISTA DE LIGAS
const LEAGUES = [
  "English Premier League",
  "English Championship",
  "Italian Serie A",
  "Italian Serie B",
  "Spanish La Liga",
  "Spanish Segunda Division",
  "French Ligue 1",
  "German Bundesliga",
  "Brazil Serie A",
  "MLS",
  "Argentinian Primera Division",
  "Mexican Liga MX"
];

// CACHE
let leaguesCache = null;

async function getAllLeagues() {
  if (leaguesCache) return leaguesCache;

  const res = await axios.get(`${BASE_URL}/all_leagues.php`);
  leaguesCache = res.data.leagues || [];

  return leaguesCache;
}

async function getLeagueId(name) {
  const leagues = await getAllLeagues();

  const league = leagues.find(
    (l) => l.strLeague.toLowerCase() === name.toLowerCase()
  );

  return league ? league.idLeague : null;
}

async function fetchLeagueEvents(leagueName) {
  try {
    const id = await getLeagueId(leagueName);

    if (!id) {
      console.log("❌ Liga não encontrada:", leagueName);
      return [];
    }

    const res = await axios.get(`${BASE_URL}/eventsnextleague.php?id=${id}`);

    // 🔥 GARANTIA ABSOLUTA
    if (!res.data || !Array.isArray(res.data.events)) {
      console.log(`⚠️ Sem jogos: ${leagueName}`);
      return [];
    }

    return res.data.events;
  } catch (err) {
    console.log("Erro liga:", leagueName);
    return [];
  }
}

async function ingestAll() {
  let allMatches = [];

  for (const league of LEAGUES) {
    const events = await fetchLeagueEvents(league);

    // 🔥 PROTEÇÃO FINAL (ANTI-CRASH)
    if (!Array.isArray(events)) continue;

    for (const e of events) {
      if (!e.strHomeTeam || !e.strAwayTeam) continue;

      allMatches.push({
        match: `${e.strHomeTeam} vs ${e.strAwayTeam}`,
        league: league,
        date: e.dateEvent
      });
    }

    console.log(`✔ ${league} (${events.length} jogos)`);
  }

  console.log("🔥 TOTAL:", allMatches.length);

  return allMatches;
}

module.exports = { ingestAll };