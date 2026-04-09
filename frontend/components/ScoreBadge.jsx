export default function ScoreBadge({ score }) {
  let color = "bg-red-500";
  let label = "Ignorar";

  if (score >= 80) {
    color = "bg-green-600";
    label = "Forte";
  } else if (score >= 70) {
    color = "bg-green-400";
    label = "Boa";
  } else if (score >= 60) {
    color = "bg-yellow-400";
    label = "Moderada";
  }

  return (
    <div className={`px-3 py-1 text-white rounded ${color}`}>
      {score} • {label}
    </div>
  );
}
