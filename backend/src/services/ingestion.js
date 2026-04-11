const axios = require("axios");

const API_KEY = process.env.API_KEY;

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
  "German 2. Bundesliga",
  "German 3. Liga",
  "Brazilian Serie A",
  "Brazilian Serie B",
  "MLS",
  "Saudi Pro League",
  "Dutch Eredivisie",
  "Dutch Eerste Divisie",
  "Danish Superliga",
  "Danish 1st Division",
  "Scottish Premiership",
  "Scottish Championship",
  "Norwegian Eliteserien",
  "Norwegian 1st Division",
  "Austrian Bundesliga",
  "Austrian 2. Liga",
  "Portuguese Primeira Liga",
  "Portuguese Segunda Liga",
  "Turkish Super Lig",
  "Turkish 1. Lig",
  "Polish Ekstraklasa",
  "Serbian SuperLiga",
  "Argentine Primera Division",
  "Colombian Primera A",
  "Mexican Liga MX",
  "Bolivian Primera Division",
  "Uruguayan Primera Division",
  "Paraguayan Primera Division"
];

async function ingestAll() {
  const allMatches = [];

  for (const league of LEAGUES) {
    try {
      const res = await axios.get(
        `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=4328`
      );

      // 🔥 CORREÇÃO CRÍTICA
      const events = res.data?.events;

      if (!Array.isArray(events)) {
        console.log(`⚠️ ${league} sem jogos`);
        continue;
      }

      for (const ev of events) {
        if (!ev.strHomeTeam || !ev.strAwayTeam) continue;

        allMatches.push({
          match: `${ev.strHomeTeam} vs ${ev.strAwayTeam}`,
          league: league,
          date: ev.dateEvent
        });
      }

      console.log(`✅ ${league}: ${events.length} jogos`);

    } catch (err) {
      console.log(`❌ erro liga ${league}`);
    }
  }

  return allMatches;
}

module.exports = { ingestAll };