# app/routes/historical_teams.py

from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter(
    prefix="/historical",
    tags=["Historical"]
)

# 🔹 MOCK ORGANIZADO POR LIGA (estrutura realista)
FAKE_TEAMS_BY_LEAGUE = {
    39: [  # Premier League
        "Arsenal",
        "Chelsea",
        "Liverpool",
        "Manchester City",
        "Manchester United",
        "Tottenham"
    ],
    71: [  # Brasileirão
        "Flamengo",
        "Palmeiras",
        "Corinthians",
        "São Paulo",
        "Grêmio",
        "Internacional",
        "Atlético-MG",
        "Cruzeiro",
        "Vasco",
        "Botafogo"
    ],
    140: [  # La Liga
        "Real Madrid",
        "Barcelona",
        "Atlético Madrid",
        "Sevilla",
        "Villarreal"
    ]
}

@router.get("/teams", response_model=List[str])
def list_historical_teams(
    league: Optional[int] = Query(
        None,
        description="ID da liga (ex: 39 Premier League, 71 Brasileirão)"
    )
):
    """
    Lista times históricos por liga.

    🔹 Se league for informado → filtra por liga
    🔹 Se não for informado → retorna todos os times
    🔹 Estrutura pronta para API-Football
    """

    # 🔹 Se não passar liga, retorna todos os times
    if league is None:
        all_teams = []
        for teams in FAKE_TEAMS_BY_LEAGUE.values():
            all_teams.extend(teams)
        return sorted(set(all_teams))

    # 🔹 Se passar liga inexistente, retorna lista vazia (controlado)
    return FAKE_TEAMS_BY_LEAGUE.get(league, [])
