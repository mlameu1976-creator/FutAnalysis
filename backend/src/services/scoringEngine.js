function calculateMatch(match) {
  const homeXG = match.home_xg_for || 1.4;
  const awayXG = match.away_xg_for || 1.2;

  const totalXG = homeXG + awayXG;

  const markets = [];

  // ===============================
  // OVER 1.5
  // ===============================
  const probOver15 = Math.min(95, (totalXG / 3) * 100);
  const odd15 = 1.6;
  const ev15 = ((probOver15 / 100) * odd15 - 1) * 100;

  markets.push({
    market: "Over 1.5",
    probability: probOver15.toFixed(1),
    odds: odd15,
    ev: ev15.toFixed(1),
  });

  // ===============================
  // OVER 2.5
  // ===============================
  const probOver25 = Math.min(85, (totalXG / 4) * 100);
  const odd25 = 2.7;
  const ev25 = ((probOver25 / 100) * odd25 - 1) * 100;

  markets.push({
    market: "Over 2.5",
    probability: probOver25.toFixed(1),
    odds: odd25,
    ev: ev25.toFixed(1),
  });

  // ===============================
  // CASA VENCE
  // ===============================
  const probHome = (homeXG / totalXG) * 100;
  const oddHome = 2.6;
  const evHome = ((probHome / 100) * oddHome - 1) * 100;

  markets.push({
    market: "Casa vence",
    probability: probHome.toFixed(1),
    odds: oddHome,
    ev: evHome.toFixed(1),
  });

  // ===============================
  // FORA VENCE
  // ===============================
  const probAway = (awayXG / totalXG) * 100;
  const oddAway = 3.3;
  const evAway = ((probAway / 100) * oddAway - 1) * 100;

  markets.push({
    market: "Fora vence",
    probability: probAway.toFixed(1),
    odds: oddAway,
    ev: evAway.toFixed(1),
  });

  // ===============================
  // GOL NO HT
  // ===============================
  const probHT = Math.min(90, (totalXG / 2.5) * 100);
  const oddHT = 1.65;
  const evHT = ((probHT / 100) * oddHT - 1) * 100;

  markets.push({
    market: "Gol no HT",
    probability: probHT.toFixed(1),
    odds: oddHT,
    ev: evHT.toFixed(1),
  });

  return markets;
}

module.exports = { calculateMatch };