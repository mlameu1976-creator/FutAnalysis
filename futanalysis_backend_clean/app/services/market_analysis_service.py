class MarketAnalysisService:
    @staticmethod
    def analyze(matches, team_name: str):
        if not matches:
            return {
                "over_1_5_pct": 0,
                "over_2_5_pct": 0,
                "btts_pct": 0,
                "ht_goal_pct": 0,
                "win_pct": 0,
            }

        total = len(matches)

        over_15 = over_25 = btts = ht_goal = wins = 0

        for m in matches:
            goals = (g.home_goals_ft or 0) + (g.away_goals_ft or 0)

            if goals >= 2:
                over_15 += 1
            if goals >= 3:
                over_25 += 1
            if m.home_goals > 0 and m.away_goals > 0:
                btts += 1
            if m.ht_home_goals + m.ht_away_goals > 0:
                ht_goal += 1

            if m.home_team == team_name and m.home_goals > m.away_goals:
                wins += 1
            if m.away_team == team_name and m.away_goals > m.home_goals:
                wins += 1

        return {
            "over_1_5_pct": round((over_15 / total) * 100),
            "over_2_5_pct": round((over_25 / total) * 100),
            "btts_pct": round((btts / total) * 100),
            "ht_goal_pct": round((ht_goal / total) * 100),
            "win_pct": round((wins / total) * 100),
        }
