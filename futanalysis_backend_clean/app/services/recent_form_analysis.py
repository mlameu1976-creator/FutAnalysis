from sqlalchemy.orm import Session
from app.models.match import Match


def get_last_matches(db: Session, team: str, limit: int = 5):
    return (
        db.query(Match)
        .filter(
            (Match.home_team == team) | (Match.away_team == team),
            Match.is_finished == True
        )
        .order_by(Match.match_date.desc())
        .limit(limit)
        .all()
    )


def analyze_recent_form(db: Session, home_team: str, away_team: str):
    home_matches = get_last_matches(db, home_team)
    away_matches = get_last_matches(db, away_team)

    all_matches = home_matches + away_matches

    if not all_matches:
        return {}

    total_ft_goals = 0
    total_ht_goals = 0
    over_15 = 0
    over_25 = 0
    btts = 0
    ht_over_05 = 0

    for m in all_matches:
        ft_goals = (m.home_goals or 0) + (m.away_goals or 0)
        ht_goals = (m.home_goals_ht or 0) + (m.away_goals_ht or 0)

        total_ft_goals += ft_goals
        total_ht_goals += ht_goals

        if ft_goals >= 2:
            over_15 += 1
        if ft_goals >= 3:
            over_25 += 1
        if (m.home_goals or 0) > 0 and (m.away_goals or 0) > 0:
            btts += 1
        if ht_goals >= 1:
            ht_over_05 += 1

    total = len(all_matches)

    return {
        "ft": {
            "avg_goals": round(total_ft_goals / total, 2),
            "over_15_rate": int((over_15 / total) * 100),
            "over_25_rate": int((over_25 / total) * 100),
            "btts_rate": int((btts / total) * 100),
        },
        "ht": {
            "avg_goals": round(total_ht_goals / total, 2),
            "over_05_rate": int((ht_over_05 / total) * 100),
        }
    }
 # ============================
# Alias de compatibilidade
# ============================

build_recent_form_analysis = analyze_recent_form