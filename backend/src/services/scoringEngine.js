// services/scoringEngine.js

const factorial = (n) => (n <= 1 ? 1 : n * factorial(n - 1));

const poisson = (lambda, k) => {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
};

// =============================
// CONFIG PROFISSIONAL
// =============================

const CONFIG = {
  HOME_ADVANTAGE: 1.12,
  MAX_GOALS: 6,
  MIN_EV: 0.05
};

// =============================
// FORÇA DOS TIMES
// =============================

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
  let totalGames = matches.length;

  matches.forEach(m => {
    totalGoals += m.home_goals + m.away_goals;
  });

  return {
    avgGoals: totalGoals / totalGames,
    avgHome: totalGoals / totalGames / 2,
    avgAway: totalGoals / totalGames / 2
  };
}

// =============================
// EXPECTED GOALS AJUSTADO
// =============================

function expectedGoals(home, away, teams, league) {
  const homeStats = teams[home];
  const awayStats = teams[away];

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

// =============================
// MATRIZ DE PROBABILIDADE
// =============================

function matchProbabilities(lambdaHome, lambdaAway) {
  let homeWin = 0;
  let draw = 0;
  let awayWin = 0;
  let over25 = 0;
  let over15 = 0;
  let btts = 0;

  for (let i = 0; i <= CONFIG.MAX_GOALS; i++) {
    for (let j = 0; j <= CONFIG.MAX_GOALS; j++) {
      const p = poisson(lambdaHome, i) * poisson(lambdaAway, j);

      if (i > j) homeWin += p;
      else if (i === j) draw += p;
      else awayWin += p;

      if (i + j >= 3) over25 += p;
      if (i + j >= 2) over15 += p;
      if (i > 0 && j > 0) btts += p;
    }
  }

  return {
    homeWin,
    draw,
    awayWin,
    over25,
    over15,
    btts
  };
}

// =============================
// ODDS REALISTAS (ANTI-VIÉS)
// =============================

function fairOdds(prob) {
  return 1 / prob;
}

// simula margem de mercado (overround)
function marketOdds(prob) {
  const margin = 1.05;
  return (1 / prob) * margin;
}

// =============================
// EV REALISTA
// =============================

function calculateEV(prob, odds) {
  return prob * odds - 1;
}

// =============================
// ENGINE PRINCIPAL
// =============================

function generateOpportunities(matches) {
  const teams = calculateTeamStrengths(matches);
  const league = leagueAverages(matches);

  const opportunities = [];

  matches.forEach(match => {
    if (!teams[match.home_team] || !teams[match.away_team]) return;

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
      if (m.prob < 0.05) return; // filtro básico

      const odds = marketOdds(m.prob);
      const ev = calculateEV(m.prob, odds);

      if (ev >= CONFIG.MIN_EV) {
        opportunities.push({
          match: `${match.home_team} vs ${match.away_team}`,
          market: m.type,
          probability: Number(m.prob.toFixed(3)),
          odds: Number(odds.toFixed(2)),
          ev: Number(ev.toFixed(3))
        });
      }
    });
  });

  return opportunities;
}

module.exports = {
  generateOpportunities
};