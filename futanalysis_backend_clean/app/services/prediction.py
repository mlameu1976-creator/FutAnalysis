from sqlalchemy.orm import Session

from app.models import HistoricalMatches
from app.services.poisson import goal_distribution
from app.services.league_strength import league_goal_averages


def average_goals(db: Session, team_id: int, competition_id: int, season: int, side: str, limit: int):
    matches = (
        db.query(HistoricalMatches)
        .filter(
            HistoricalMatches.competition_id == competition_id,
            HistoricalMatches.season == season,
        )
        .filter(
            HistoricalMatches.home_team_id == team_id
            if side == "home"
            else HistoricalMatches.away_team_id == team_id
        )
        .order_by(HistoricalMatches.id.desc())
        .limit(limit)
        .all()
    )

    if not matches:
        return 0.0, 0.0

    gf = ga = 0
    for m in matches:
        if side == "home":
            gf += m.home_goals_ft
            ga += m.away_goals_ft
        else:
            gf += m.away_goals_ft
            ga += m.home_goals_ft

    n = len(matches)
    return gf / n, ga / n


def poisson_match_prediction(
    db: Session,
    home_team_id: int,
    away_team_id: int,
    competition_id: int,
    season: int,
    limit: int = 5,
):
    # médias da liga
    league_home_avg, league_away_avg = league_goal_averages(db, competition_id, season)

    # médias do time
    home_attack, home_defense = average_goals(db, home_team_id, competition_id, season, "home", limit)
    away_attack, away_defense = average_goals(db, away_team_id, competition_id, season, "away", limit)

    # forças relativas
    home_attack_strength = home_attack / league_home_avg if league_home_avg else 1
    away_attack_strength = away_attack / league_away_avg if league_away_avg else 1

    home_defense_strength = home_defense / league_away_avg if league_away_avg else 1
    away_defense_strength = away_defense / league_home_avg if league_home_avg else 1

    # xG ajustado
    home_xg = league_home_avg * home_attack_strength * away_defense_strength
    away_xg = league_away_avg * away_attack_strength * home_defense_strength

    home_dist = goal_distribution(home_xg)
    away_dist = goal_distribution(away_xg)

    prob_home_win = prob_draw = prob_away_win = 0.0
    prob_btts = prob_over_25 = prob_over_15 = 0.0

    for i, ph in enumerate(home_dist):
        for j, pa in enumerate(away_dist):
            p = ph * pa

            if i > j:
                prob_home_win += p
            elif i == j:
                prob_draw += p
            else:
                prob_away_win += p

            if i > 0 and j > 0:
                prob_btts += p
            if i + j > 2:
                prob_over_25 += p
            if i + j > 1:
                prob_over_15 += p

    return {
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "probabilities": {
            "home_win": round(prob_home_win, 3),
            "draw": round(prob_draw, 3),
            "away_win": round(prob_away_win, 3),
            "btts": round(prob_btts, 3),
            "over_1_5": round(prob_over_15, 3),
            "over_2_5": round(prob_over_25, 3),
        },
    }
