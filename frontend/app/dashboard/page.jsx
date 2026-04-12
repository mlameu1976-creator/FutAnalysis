import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/opportunities")
      .then(res => res.json())
      .then(json => setData(json));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>

      {data.map((item, i) => (
        <div key={i}>
          <h2>{item.match}</h2>
          <p>{item.league}</p>
        </div>
      ))}
    </div>
  );
}