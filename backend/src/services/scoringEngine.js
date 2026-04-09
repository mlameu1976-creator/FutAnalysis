function calculateEV(prob, odds) {
  const p = prob / 100;
  return ((p * odds) - 1) * 100;
}

function generateMarkets(match) {
  const markets = [];

  const homeAttack = match.home_xg_for || 1.4;
  const awayAttack = match.away_xg_for || 1.2;

  const totalGoals = homeAttack + awayAttack;

  // ===============================
  // OVER 1.5
  // ===============================
  const probOver15 = Math.min(90, totalGoals * 25);
  const oddsOver15 = 1.6;

  markets.push({
    market: "Over 1.5",
    probability: probOver15.toFixed(1),
    odds: oddsOver15,
    ev: calculateEV(probOver15, oddsOver15).toFixed(1),
  });

  // ===============================
  // OVER 2.5
  // ===============================
  const probOver25 = Math.min(80, totalGoals * 18);
  const oddsOver25 = 2.7;

  markets.push({
    market: "Over 2.5",
    probability: probOver25.toFixed(1),
    odds: oddsOver25,
    ev: calculateEV(probOver25, oddsOver25).toFixed(1),
  });

  // ===============================
  // CASA VENCE
  // ===============================
  const probHome = 50 + (homeAttack - awayAttack) * 10;
  const oddsHome = 2.6;

  markets.push({
    market: "Casa vence",
    probability: probHome.toFixed(1),
    odds: oddsHome,
    ev: calculateEV(probHome, oddsHome).toFixed(1),
  });

  // ===============================
  // FORA VENCE
  // ===============================
  const probAway = 50 + (awayAttack - homeAttack) * 10;
  const oddsAway = 3.3;

  markets.push({
    market: "Fora vence",
    probability: probAway.toFixed(1),
    odds: oddsAway,
    ev: calculateEV(probAway, oddsAway).toFixed(1),
  });

  // ===============================
  // GOL HT (1º TEMPO)
  // ===============================
  const probHT = Math.min(85, totalGoals * 22);
  const oddsHT = 1.65;

  markets.push({
    market: "Gol no HT",
    probability: probHT.toFixed(1),
    odds: oddsHT,
    ev: calculateEV(probHT, oddsHT).toFixed(1),
  });

  return markets;
}

module.exports = { generateMarkets };