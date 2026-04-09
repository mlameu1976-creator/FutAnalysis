export default function OpportunityCard({ data }) {
  return (
    <div className="bg-[#161616] border border-gray-800 rounded-xl p-4 space-y-3">
      
      {/* TIMES */}
      <h3 className="text-lg font-semibold">
        {data.homeTeam} x {data.awayTeam}
      </h3>

      {/* MERCADO */}
      <p className="text-gray-300">
        {data.market}
      </p>

      {/* PROB */}
      <p className="text-sm text-gray-400">
        Prob: {data.probability}%
      </p>

      {/* ODDS */}
      <p className="text-sm text-gray-400">
        Odd: {data.odds ?? "-"}
      </p>

      {/* EV */}
      <p className="text-sm text-green-400 font-semibold">
        EV: {data.ev}%
      </p>

      {/* CONFIANÇA */}
      <p className="text-sm text-blue-400">
        Confiança: {data.confidence}%
      </p>

    </div>
  );
}