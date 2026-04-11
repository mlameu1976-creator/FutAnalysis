const axios = require("axios");

const API_KEY = process.env.SPORTSDB_API_KEY;
const BASE_URL = `https://www.thesportsdb.com/api/v1/json/${API_KEY}`;

// 🔥 LIGAS (PODE EXPANDIR DEPOIS)
const LEAGUES = [
  "English Premier League",
  "Brazil Serie A",
  "Spanish La Liga",
  "Italian Serie A",
  "German Bundesliga",
  "Argentinian Primera Division",
  "Mexican Liga MX",
  "MLS"
];

// 🔥 BUSCA ID DAS LIGAS
async function getLeagueId(name) {
  try {
    const res = await axios.get(`${BASE_URL}/all_leagues.php`);
    const leagues = res.data.leagues || [];

    const found = leagues.find(
      (l) => l.strLeague.toLowerCase() === name.toLowerCase()
    );

    return found ? found.idLeague : null;
  } catch {
    return null;
  }
}

// 🔥 BUSCA JOGOS
async function fetchEvents(league) {
  try {
    const id = await getLeagueId(league);
    if (!id) return [];

    const res = await axios.get(`${BASE_URL}/eventsnextleague.php?id=${id}`);

    if (!res.data || !Array.isArray(res.data.events)) {
      return [];
    }

    return res.data.events;
  } catch {
    return [];
  }
}

// 🔥 INGESTÃO FINAL (SEM FOREACH!)
async function ingestAll() {
  const matches = [];

  for (let i = 0; i < LEAGUES.length; i++) {
    const league = LEAGUES[i];

    const events = await fetchEvents(league);

    if (!Array.isArray(events)) continue;

    for (let j = 0; j < events.length; j++) {
      const e = events[j];

      if (!e || !e.strHomeTeam || !e.strAwayTeam) continue;

      matches.push({
        match: e.strHomeTeam + " vs " + e.strAwayTeam,
        league: league,
        date: e.dateEvent
      });
    }

    console.log("✔", league, events.length);
  }

  console.log("🔥 TOTAL:", matches.length);

  return matches;
}

module.exports = { ingestAll };