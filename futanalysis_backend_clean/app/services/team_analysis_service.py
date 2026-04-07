from sqlalchemy.orm import Session
from app.models import HistoricalMatch


class TeamAnalysisService:
    @staticmethod
    def last_games_analysis(db: Session, team: str, limit: int = 5):
        games = (
            db.query(HistoricalMatch)
            .filter(
                (HistoricalMatch.home_team == team)
                | (HistoricalMatch.away_team == team)
            )
            .order_by(HistoricalMatch.id.desc())
            .limit(limit)
            .all()
        )

        if not games:
            return None

        total_games = len(games)

        over_15 = 0
        over_25 = 0
        btts = 0
        goal_ht = 0
        home_win = 0
        away_win = 0

        for g in games:
            home_goals = g.home_goals_ft or 0
            away_goals = g.away_goals_ft or 0
            total_goals = home_goals + away_goals

            # Over markets
            if total_goals >= 2:
                over_15 += 1
            if total_goals >= 3:
                over_25 += 1

            # BTTS
            if home_goals > 0 and away_goals > 0:
                btts += 1

            # Goal HT
            if (g.home_goals_ht or 0) + (g.away_goals_ht or 0) > 0:
                goal_ht += 1

            # Winner
            if g.home_team == team and home_goals > away_goals:
                home_win += 1
            if g.away_team == team and away_goals > home_goals:
                away_win += 1

        # Percentuais
        over_15_pct = round((over_15 / total_games) * 100)
        over_25_pct = round((over_25 / total_games) * 100)
        btts_pct = round((btts / total_games) * 100)
        goal_ht_pct = round((goal_ht / total_games) * 100)
        home_win_pct = round((home_win / total_games) * 100)
        away_win_pct = round((away_win / total_games) * 100)

        # Bias de vitória
        win_bias = max(home_win_pct, away_win_pct)

        # 🎯 SCORE DE CONFIANÇA
        confidence = round(
            over_15_pct * 0.25
            + over_25_pct * 0.25
            + btts_pct * 0.20
            + goal_ht_pct * 0.15
            + win_bias * 0.15
        )

        # Mercado principal
        market_scores = {
            "over_1_5": over_15_pct,
            "over_2_5": over_25_pct,
            "btts": btts_pct,
            "goal_ht": goal_ht_pct,
            "home_win": home_win_pct,
            "away_win": away_win_pct,
        }

        main_market = max(market_scores, key=market_scores.get)

        return {
            "team": team,
            "games_analyzed": total_games,
            "markets": market_scores,
            "main_market": main_market,
            "confidence": confidence,
        }
