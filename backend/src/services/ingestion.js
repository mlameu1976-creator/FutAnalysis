const axios = require("axios");

const API_KEY = process.env.SPORTSDB_API_KEY;
const BASE_URL = `https://www.thesportsdb.com/api/v1/json/${API_KEY}`;

// LISTA COMPLETA
const LEAGUES = [
  "English Premier League",
  "English Championship",
  "Italian Serie A",
  "Italian Serie B",
  "Spanish La Liga",
  "Spanish Segunda Division",
  "French Ligue 1",
  "French Ligue 2",
  "German Bundesliga",
  "German Bundesliga 2",
  "German 3. Liga",
  "Brazil Serie A",
  "Brazil Serie B",
  "MLS",
  "Saudi Pro League",
  "Dutch Eredivisie",
  "Dutch Eerste Divisie",
  "Danish Superliga",
  "Scottish Premiership",
  "Norwegian Eliteserien",
  "Austrian Bundesliga",
  "Portuguese Primeira Liga",
  "Turkish Super Lig",
  "Polish Ekstraklasa",
  "Argentinian Primera Division",
  "Colombian Primera A",
  "Mexican Liga MX",
  "Uruguayan Primera Division"
];

// CACHE IDs (evita chamada repetida)
let leaguesCache = null;

async function getAllLeagues() {
  if (leaguesCache) return leaguesCache;

  const res = await axios.get(`${BASE_URL}/all_leagues.php`);
  leaguesCache = res.data.leagues;

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

    // 🔥 CORREÇÃO CRÍTICA
    const events = res.data.events;

    if (!Array.isArray(events)) {
      console.log(`⚠️ Sem jogos: ${leagueName}`);
      return [];
    }

    return events;
  } catch (err) {
    console.log("Erro liga:", leagueName);
    return [];
  }
}

async function ingestAll() {
  let allMatches = [];

  for (const league of LEAGUES) {
    const events = await fetchLeagueEvents(league);

    events.forEach((e) => {
      if (!e.strHomeTeam || !e.strAwayTeam) return;

      allMatches.push({
        match: `${e.strHomeTeam} vs ${e.strAwayTeam}`,
        league: league,
        date: e.dateEvent
      });
    });

    console.log(`✔ ${league} (${events.length} jogos)`);
  }

  console.log("🔥 TOTAL DE JOGOS:", allMatches.length);

  return allMatches;
}

module.exports = { ingestAll };