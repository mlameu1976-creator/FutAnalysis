export function calculateEV(probability, odd) {
  const prob = probability / 100;
  return (prob * odd - 1) * 100;
}