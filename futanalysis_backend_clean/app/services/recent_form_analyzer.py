from sqlalchemy.orm import Session
from app.models.match import Match


def get_last_matches(
    db: Session,
    team: str,
    limit: int = 5,
):
    return (
        db.query(Match)
        .filter(
            Match.is_finished == True,
            (Match.home_team == team) | (Match.away_team == team),
        )
        .order_by(Match.match_date.desc())
        .limit(limit)
        .all()
    )


def calculate_team_form(db: Session, team: str):
    matches = get_last_matches(db, team)

    if len(matches) < 3:
        return None  # dados insuficientes

    goals_for = 0
    goals_against = 0
    btts = 0
    over_15 = 0
    over_25 = 0

    for m in matches:
        if m.home_team == team:
            gf = m.home_goals or 0
            ga = m.away_goals or 0
        else:
            gf = m.away_goals or 0
            ga = m.home_goals or 0

        goals_for += gf
        goals_against += ga

        if m.btts:
            btts += 1
        if m.over_15:
            over_15 += 1
        if m.over_25:
            over_25 += 1

    games = len(matches)

    return {
        "games": games,
        "avg_goals_for": goals_for / games,
        "avg_goals_against": goals_against / games,
        "btts_rate": btts / games,
        "over_15_rate": over_15 / games,
        "over_25_rate": over_25 / games,
    }