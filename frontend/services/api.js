const API_KEY = process.env.NEXT_PUBLIC_SPORTSDB_API_KEY;

export async function fetchNextGames() {
  try {
    // 1. Buscar TODAS as ligas
    const leaguesRes = await fetch(
      `https://www.thesportsdb.com/api/v1/json/${API_KEY}/all_leagues.php`
    );

    const leaguesData = await leaguesRes.json();

    // 2. Filtrar só futebol
    const soccerLeagues = leaguesData.leagues.filter(
      (l) => l.strSport === "Soccer"
    );

    // 🔥 limitar pra não travar (depois aumentamos)
    const selectedLeagues = soccerLeagues.slice(0, 50);

    // 3. Buscar jogos de cada liga
    const requests = selectedLeagues.map((league) =>
      fetch(
        `https://www.thesportsdb.com/api/v1/json/${API_KEY}/eventsnextleague.php?id=${league.idLeague}`
      )
        .then((res) => res.json())
        .then((data) => data.events || [])
    );

    const results = await Promise.all(requests);

    // 4. Juntar tudo
    const allGames = results.flat();

    return allGames;
  } catch (error) {
    console.error("Erro geral API:", error);
    return [];
  }
}