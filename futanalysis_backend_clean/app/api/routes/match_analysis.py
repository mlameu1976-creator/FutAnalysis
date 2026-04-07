from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.match_service import MatchService
from app.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/matches",
    tags=["Match Analysis"]
)


def calc_odd(prob):
    if not prob or prob <= 0:
        return None
    return round(1 / prob, 2)


def calc_ev(prob, market_margin=0.08):
    """
    EV aproximado usando odd simulada (odd justa + margem)
    """
    if not prob or prob <= 0:
        return None

    odd_justa = 1 / prob
    odd_simulada = odd_justa * (1 + market_margin)

    return round((prob * odd_simulada) - 1, 3)


def generate_summary(markets):
    if not markets:
        return "Dados insuficientes para análise da partida."

    avg_prob = sum(m.probability for m in markets if m.probability) / len(markets)
    avg_xg = sum(m.expected_goals or 0 for m in markets) / len(markets)

    if avg_xg >= 2.8 and avg_prob >= 0.65:
        return "Jogo com forte tendência ofensiva, alta expectativa de gols e mercados Over bem posicionados."
    elif avg_xg >= 2.3:
        return "Partida com boa expectativa de gols, cenário interessante para mercados de gols."
    elif avg_xg < 2.0:
        return "Jogo com tendência mais equilibrada e menor expectativa de gols."
    else:
        return "Partida sem tendência clara, exige cautela na entrada em mercados."


@router.get("/{match_id}/analysis")
async def get_match_analysis(match_id: int, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    analysis_service = AnalysisService(db)

    match = await match_service.get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida não encontrada")

    markets = analysis_service.generate_markets_for_match(match)
    summary = generate_summary(markets)

    analysis = []
    for m in markets:
        odd = calc_odd(m.probability)
        ev = calc_ev(m.probability)

        analysis.append({
            "market": m.market,
            "probability": m.probability,
            "odd_justa": odd,
            "expected_goals": m.expected_goals,
            "home_attack": m.home_attack,
            "away_defense": m.away_defense,
            "ev": ev
        })

    return {
        "match": {
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "competition": match.competition,
            "date": match.match_date
        },
        "summary": summary,
        "analysis": analysis
    }
