const factorial = (n) => (n <= 1 ? 1 : n * factorial(n - 1));

const poisson = (lambda, k) => {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
};

const CONFIG = {
  HOME_ADVANTAGE: 1.15,
  MAX_GOALS: 6
};

// =============================
// 🔥 LIGAS (VERSÃO FLEXÍVEL)
// =============================
const ALLOWED_LEAGUES = [
  "england",
  "spain",
  "italy",
  "germany",
  "france",
  "brazil",
  "argentina",
  "usa",
  "portugal",
  "netherlands",
  "turkey",
  "belgium",
  "austria",
  "denmark",
  "norway",
  "mexico"
];

// =============================
function isLeagueAllowed(leagueName) {
  if (!leagueName) return true; // 🔥 NÃO BLOQUEIA

  const name = leagueName.toLowerCase();

  return ALLOWED_LEAGUES.some((l) => name.includes(l));
}

// =============================
function calculateTeamStrengths(matches) {
  const teams = {};

  matches.forEach(m => {
    const homeGoals = m.home_goals ?? 1;
    const awayGoals = m.away_goals ?? 1;

    if (!teams[m.home_team]) {
      teams[m.home_team] = { scored: 0, conceded: 0, games: 0 };
    }
    if (!teams[m.away_team]) {
      teams[m.away_team] = { scored: 0, conceded: 0, games: 0 };
    }

    teams[m.home_team].scored += homeGoals;
    teams[m.home_team].conceded += awayGoals;
    teams[m.home_team].games += 1;

    teams[m.away_team].scored += awayGoals;
    teams[m.away_team].conceded += homeGoals;
    teams[m.away_team].games += 1;
  });

  return teams;
}

// =============================
function leagueAverages(matches) {
  let totalGoals = 0;

  matches.forEach(m => {
    const homeGoals = m.home_goals ?? 1;
    const awayGoals = m.away_goals ?? 1;
    totalGoals += homeGoals + awayGoals;
  });

  const games = matches.length || 1;

  return {
    avgHome: (totalGoals / games) * 0.5,
    avgAway: (totalGoals / games) * 0.5
  };
}

// =============================
function expectedGoals(home, away, teams, league) {
  const homeStats = teams[home];
  const awayStats = teams[away];

  if (!homeStats || !awayStats) {
    return { lambdaHome: 1.4, lambdaAway: 1.2 };
  }

  return {
    lambdaHome:
      ((homeStats.scored / homeStats.games) /
        league.avgHome) *
      ((awayStats.conceded / awayStats.games) /
        league.avgAway) *
      league.avgHome *
      CONFIG.HOME_ADVANTAGE,

    lambdaAway:
      ((awayStats.scored / awayStats.games) /
        league.avgAway) *
      ((homeStats.conceded / homeStats.games) /
        league.avgHome) *
      league.avgAway
  };
}

// =============================
function matchProbabilities(lambdaHome, lambdaAway) {
  let homeWin = 0;
  let awayWin = 0;
  let over25 = 0;
  let over15 = 0;
  let btts = 0;

  for (let i = 0; i <= CONFIG.MAX_GOALS; i++) {
    for (let j = 0; j <= CONFIG.MAX_GOALS; j++) {
      const p = poisson(lambdaHome, i) * poisson(lambdaAway, j);

      if (i > j) homeWin += p;
      else if (j > i) awayWin += p;

      if (i + j >= 3) over25 += p;
      if (i + j >= 2) over15 += p;
      if (i > 0 && j > 0) btts += p;
    }
  }

  return { homeWin, awayWin, over25, over15, btts };
}

// =============================
function firstHalfGoal(lambdaHome, lambdaAway) {
  const lambdaHT = (lambdaHome + lambdaAway) * 0.45;
  return 1 - Math.exp(-lambdaHT);
}

// =============================
function marketOdds(prob, type) {
  let margin = 1.04;

  if (type === "OVER_2_5" || type === "OVER_1_5") margin = 1.01;
  if (type === "BTTS") margin = 1.02;
  if (type === "HT_GOAL") margin = 1.02;

  return (1 / prob) * margin;
}

function calculateEV(prob, odds) {
  return prob * odds - 1;
}

function formatMarket(type) {
  return {
    HOME_WIN: "Casa vence",
    AWAY_WIN: "Fora vence",
    OVER_2_5: "Over 2.5",
    OVER_1_5: "Over 1.5",
    BTTS: "Ambas marcam",
    HT_GOAL: "Gol no 1º tempo"
  }[type];
}

// =============================
// 🚀 ENGINE FINAL
// =============================
function generateOpportunities(matches) {
  if (!matches || matches.length === 0) {
    console.log("⚠️ Nenhum jogo recebido");
    return [];
  }

  console.log("TOTAL MATCHES:", matches.length);

  const filteredMatches = matches.filter(m =>
    isLeagueAllowed(m.league)
  );

  console.log("MATCHES APÓS FILTRO:", filteredMatches.length);

  const teams = calculateTeamStrengths(filteredMatches);
  const league = leagueAverages(filteredMatches);

  const map = new Map();

  filteredMatches.forEach(match => {
    const { lambdaHome, lambdaAway } = expectedGoals(
      match.home_team,
      match.away_team,
      teams,
      league
    );

    const probs = matchProbabilities(lambdaHome, lambdaAway);
    const htGoal = firstHalfGoal(lambdaHome, lambdaAway);

    const markets = [
      { type: "HOME_WIN", prob: probs.homeWin },
      { type: "AWAY_WIN", prob: probs.awayWin },
      { type: "OVER_2_5", prob: probs.over25 },
      { type: "OVER_1_5", prob: probs.over15 },
      { type: "BTTS", prob: probs.btts },
      { type: "HT_GOAL", prob: htGoal }
    ];

    markets.forEach(m => {
      const key = `${match.home_team}-${match.away_team}-${m.type}`;

      const odds = marketOdds(m.prob, m.type);
      const ev = calculateEV(m.prob, odds);

      const item = {
        homeTeam: match.home_team,
        awayTeam: match.away_team,
        league: match.league || "unknown",
        market: formatMarket(m.type),
        probability: Number((m.prob * 100).toFixed(1)),
        confidence: Number((m.prob * 100).toFixed(0)),
        odds: Number(odds.toFixed(2)),
        ev: Number((ev * 100).toFixed(2))
      };

      if (!map.has(key) || item.ev > map.get(key).ev) {
        map.set(key, item);
      }
    });
  });

  return Array.from(map.values()).sort((a, b) => b.ev - a.ev);
}

module.exports = {
  generateOpportunities
};