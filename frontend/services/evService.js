export function calculateEV(probability, odd) {
  const prob = probability / 100;

  if (!odd || odd <= 1) return -100;

  return Number(((prob * odd - 1) * 100).toFixed(2));
}