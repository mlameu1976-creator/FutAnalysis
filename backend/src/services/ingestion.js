const axios = require("axios");

const API_KEY = process.env.SPORTSDB_API_KEY;
const BASE_URL = `https://www.thesportsdb.com/api/v1/json/${API_KEY}`;

// ✅ TODAS AS LIGAS (SUA LISTA COMPLETA)
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
  "Danish 1st Division",
  "Scottish Premiership",
  "Scottish Championship",
  "Norwegian Eliteserien",
  "Norwegian First Division",
  "Austrian Bundesliga",
  "Austrian 2. Liga",
  "Portuguese Primeira Liga",
  "Portuguese Segunda Liga",
  "Turkish Super Lig",
  "Turkish 1. Lig",
  "Polish Ekstraklasa",
  "Serbian SuperLiga",
  "Argentinian Primera Division",
  "Colombian Primera A",
  "Mexican Liga MX",
  "Bolivian Primera Division",
  "Uruguayan Primera Division",
  "Paraguayan Primera Division"
];

// 🔥 BUSCAR EVENTOS POR LIGA
async function fetchLeagueEvents(league) {
  try {
    const res = await axios.get(`${BASE_URL}/eventsnextleague.php`, {
      params: { id: await getLeagueId(league) }
    });

    return res.data.events || [];
  } catch (err) {
    console.log("Erro liga:", league);
    return [];
  }
}

// 🔥 PEGAR ID DA LIGA DINAMICAMENTE
async function getLeagueId(name) {
  try {
    const res = await axios.get(`${BASE_URL}/search_all_leagues.php`, {
      params: { s: "Soccer" }
    });

    const league = res.data.countrys.find(
      (l) => l.strLeague.toLowerCase() === name.toLowerCase()
    );

    return league ? league.idLeague : null;
  } catch {
    return null;
  }
}

// 🔥 INGESTÃO COMPLETA
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

    console.log(`✔ ${league} carregada`);
  }

  return allMatches;
}

module.exports = { ingestAll };