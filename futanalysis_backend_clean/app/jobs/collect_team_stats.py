from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.match import Match
from app.models.team_stats import TeamStats


def calculate_team_stats(db: Session):
    teams = {}

    matches = (
        db.query(Match)
        .filter(
            Match.status == "Finished",
            Match.home_team.isnot(None),
            Match.away_team.isnot(None),
        )
        .all()
    )

    for m in matches:
        for side in ["home", "away"]:
            team = m.home_team if side == "home" else m.away_team
            conceded = m.away_goals if side == "home" else m.home_goals
            scored = m.home_goals if side == "home" else m.away_goals

            conceded_ht = m.away_goals_ht if side == "home" else m.home_goals_ht
            scored_ht = m.home_goals_ht if side == "home" else m.away_goals_ht

            key = (team, m.league_id)

            if key not in teams:
                teams[key] = {
                    "matches": 0,
                    "scored": 0,
                    "conceded": 0,
                    "scored_ht": 0,
                    "conceded_ht": 0,
                    "btts": 0,
                    "over_15": 0,
                    "over_25": 0,
                }

            t = teams[key]
            t["matches"] += 1
            t["scored"] += scored or 0
            t["conceded"] += conceded or 0
            t["scored_ht"] += scored_ht or 0
            t["conceded_ht"] += conceded_ht or 0

            if m.btts:
                t["btts"] += 1
            if m.over_15:
                t["over_15"] += 1
            if m.over_25:
                t["over_25"] += 1

    db.query(TeamStats).delete()

    for (team, league), t in teams.items():
        matches = t["matches"] or 1

        stats = TeamStats(
            team_name=team,
            league_id=league,
            matches_played=matches,
            goals_scored_avg=round(t["scored"] / matches, 2),
            goals_conceded_avg=round(t["conceded"] / matches, 2),
            goals_scored_ht_avg=round(t["scored_ht"] / matches, 2),
            goals_conceded_ht_avg=round(t["conceded_ht"] / matches, 2),
            btts_rate=round((t["btts"] / matches) * 100, 2),
            over_15_rate=round((t["over_15"] / matches) * 100, 2),
            over_25_rate=round((t["over_25"] / matches) * 100, 2),
        )

        db.add(stats)

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    calculate_team_stats(db)
    db.close()
    print("Team stats geradas com sucesso")