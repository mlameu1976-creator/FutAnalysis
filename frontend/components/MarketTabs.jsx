export default function MarketTabs({ active, onChange }) {
  const tabs = [
    { key: "all", label: "Todos" },
    { key: "over", label: "Over 2.5" },
    { key: "btts", label: "BTTS" },
  ];

  return (
    <div className="flex gap-4 mb-6">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`px-4 py-2 rounded ${
            active === tab.key
              ? "bg-blue-600 text-white"
              : "bg-gray-200"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
