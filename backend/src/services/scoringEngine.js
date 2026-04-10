function calculateMatch(match) {
  const homeXG = match.home_xg_for || 1.4;
  const awayXG = match.away_xg_for || 1.2;

  const totalXG = homeXG + awayXG;

  const markets = [];

  // Over 1.5
  const prob15 = Math.min(95, (totalXG / 3) * 100);
  const odd15 = 1.6;
  const ev15 = ((prob15 / 100) * odd15 - 1) * 100;

  markets.push({
    market: "Over 1.5",
    probability: Number(prob15.toFixed(1)),
    odds: odd15,
    ev: Number(ev15.toFixed(1)),
  });

  // Over 2.5
  const prob25 = Math.min(85, (totalXG / 4) * 100);
  const odd25 = 2.7;
  const ev25 = ((prob25 / 100) * odd25 - 1) * 100;

  markets.push({
    market: "Over 2.5",
    probability: Number(prob25.toFixed(1)),
    odds: odd25,
    ev: Number(ev25.toFixed(1)),
  });

  // Casa vence
  const probHome = (homeXG / totalXG) * 100;
  const oddHome = 2.6;
  const evHome = ((probHome / 100) * oddHome - 1) * 100;

  markets.push({
    market: "Casa vence",
    probability: Number(probHome.toFixed(1)),
    odds: oddHome,
    ev: Number(evHome.toFixed(1)),
  });

  // Fora vence
  const probAway = (awayXG / totalXG) * 100;
  const oddAway = 3.3;
  const evAway = ((probAway / 100) * oddAway - 1) * 100;

  markets.push({
    market: "Fora vence",
    probability: Number(probAway.toFixed(1)),
    odds: oddAway,
    ev: Number(evAway.toFixed(1)),
  });

  // Gol HT
  const probHT = Math.min(90, (totalXG / 2.5) * 100);
  const oddHT = 1.65;
  const evHT = ((probHT / 100) * oddHT - 1) * 100;

  markets.push({
    market: "Gol no HT",
    probability: Number(probHT.toFixed(1)),
    odds: oddHT,
    ev: Number(evHT.toFixed(1)),
  });

  return markets;
}

module.exports = { calculateMatch };