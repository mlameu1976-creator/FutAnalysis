const factorial = (n) => (n <= 1 ? 1 : n * factorial(n - 1));

const poisson = (lambda, k) => {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
};

const CONFIG = {
  HOME_ADVANTAGE: 1.15,
  MAX_GOALS: 6,
  MIN_EV: 0.04,
  MIN_PROB: 0.15
};

function calculateTeamStrengths(matches) {
  const teams = {};

  matches.forEach(m => {
    if (!teams[m.home_team]) {
      teams[m.home_team] = { scored: 0, conceded: 0, games: 0 };
    }
    if (!teams[m.away_team]) {
      teams[m.away_team] = { scored: 0, conceded: 0, games: 0 };
    }

    teams[m.home_team].scored += m.home_goals;
    teams[m.home_team].conceded += m.away_goals;
    teams[m.home_team].games += 1;

    teams[m.away_team].scored += m.away_goals;
    teams[m.away_team].conceded += m.home_goals;
    teams[m.away_team].games += 1;
  });

  return teams;
}

function leagueAverages(matches) {
  let totalGoals = 0;

  matches.forEach(m => {
    totalGoals += m.home_goals + m.away_goals;
  });

  const games = matches.length;

  return {
    avgHome: (totalGoals / games) * 0.5,
    avgAway: (totalGoals / games) * 0.5
  };
}

function expectedGoals(home, away, teams, league) {
  const homeStats = teams[home];
  const awayStats = teams[away];

  if (!homeStats || !awayStats) {
    return { lambdaHome: 1.2, lambdaAway: 1.0 };
  }

  const homeAttack = (homeStats.scored / homeStats.games) / league.avgHome;
  const homeDefense = (homeStats.conceded / homeStats.games) / league.avgAway;

  const awayAttack = (awayStats.scored / awayStats.games) / league.avgAway;
  const awayDefense = (awayStats.conceded / awayStats.games) / league.avgHome;

  const lambdaHome =
    homeAttack * awayDefense * league.avgHome * CONFIG.HOME_ADVANTAGE;

  const lambdaAway =
    awayAttack * homeDefense * league.avgAway;

  return { lambdaHome, lambdaAway };
}

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

function marketOdds(prob) {
  return (1 / prob) * 1.06;
}

function calculateEV(prob, odds) {
  return prob * odds - 1;
}

function formatMarketName(type) {
  const map = {
    HOME_WIN: "Casa vence",
    AWAY_WIN: "Fora vence",
    OVER_2_5: "Over 2.5",
    OVER_1_5: "Over 1.5",
    BTTS: "Ambas marcam"
  };
  return map[type] || type;
}

function generateOpportunities(matches) {
  const teams = calculateTeamStrengths(matches);
  const league = leagueAverages(matches);

  const opportunities = [];

  matches.forEach(match => {
    const { lambdaHome, lambdaAway } = expectedGoals(
      match.home_team,
      match.away_team,
      teams,
      league
    );

    const probs = matchProbabilities(lambdaHome, lambdaAway);

    const markets = [
      { type: "HOME_WIN", prob: probs.homeWin },
      { type: "AWAY_WIN", prob: probs.awayWin },
      { type: "OVER_2_5", prob: probs.over25 },
      { type: "OVER_1_5", prob: probs.over15 },
      { type: "BTTS", prob: probs.btts }
    ];

    markets.forEach(m => {
      if (m.prob < CONFIG.MIN_PROB) return;

      const odds = marketOdds(m.prob);
      const ev = calculateEV(m.prob, odds);

      if (ev >= CONFIG.MIN_EV) {
        opportunities.push({
          homeTeam: match.home_team,
          awayTeam: match.away_team,
          match: `${match.home_team} vs ${match.away_team}`,
          market: formatMarketName(m.type),
          probability: Number(m.prob.toFixed(2)),
          confidence: Number((m.prob * 100).toFixed(0)),
          odds: Number(odds.toFixed(2)),
          ev: Number((ev * 100).toFixed(2))
        });
      }
    });
  });

  return opportunities;
}

module.exports = {
  generateOpportunities
};