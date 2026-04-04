function factorial(n) {
  if (n === 0) return 1;
  return n * factorial(n - 1);
}

export function poisson(lambda, k) {
  return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
}

// probabilidade de over 2.5 gols
export function over25Prob(homeAvg, awayAvg) {
  let prob = 0;

  for (let i = 0; i <= 5; i++) {
    for (let j = 0; j <= 5; j++) {
      const total = i + j;
      const p =
        poisson(homeAvg, i) * poisson(awayAvg, j);

      if (total > 2) prob += p;
    }
  }

  return prob;
}