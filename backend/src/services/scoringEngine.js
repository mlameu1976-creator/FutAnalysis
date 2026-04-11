function calculateMatch(match) {
  const homeXG = match.home_xg_for;
  const awayXG = match.away_xg_for;

  const totalXG = homeXG + awayXG;

  // 🔥 PROBABILIDADES MAIS REALISTAS
  const probOver15 = Math.min(85, 50 + totalXG * 10);
  const probOver25 = Math.min(75, 35 + totalXG * 8);

  const probHome = 40 + (homeXG - awayXG) * 10;
  const probAway = 40 + (awayXG - homeXG) * 10;

  const probHTGoal = Math.min(80, 45 + totalXG * 8);

  // 🔥 ODDS MAIS REALISTAS
  const oddsOver15 = 1.5 + Math.random() * 0.4;
  const oddsOver25 = 2.2 + Math.random() * 0.8;
  const oddsHome = 2.0 + Math.random() * 1.2;
  const oddsAway = 2.0 + Math.random() * 1.2;
  const oddsHT = 1.5 + Math.random() * 0.4;

  function calcEV(prob, odd) {
    const p = prob / 100;
    return (p * odd - 1) * 100;
  }

  return [
    {
      market: "Over 1.5",
      probability: probOver15.toFixed(1),
      odds: oddsOver15.toFixed(2),
      ev: calcEV(probOver15, oddsOver15).toFixed(1),
    },
    {
      market: "Over 2.5",
      probability: probOver25.toFixed(1),
      odds: oddsOver25.toFixed(2),
      ev: calcEV(probOver25, oddsOver25).toFixed(1),
    },
    {
      market: "Casa vence",
      probability: probHome.toFixed(1),
      odds: oddsHome.toFixed(2),
      ev: calcEV(probHome, oddsHome).toFixed(1),
    },
    {
      market: "Fora vence",
      probability: probAway.toFixed(1),
      odds: oddsAway.toFixed(2),
      ev: calcEV(probAway, oddsAway).toFixed(1),
    },
    {
      market: "Gol no HT",
      probability: probHTGoal.toFixed(1),
      odds: oddsHT.toFixed(2),
      ev: calcEV(probHTGoal, oddsHT).toFixed(1),
    },
  ];
}

module.exports = { calculateMatch };