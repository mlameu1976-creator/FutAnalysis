from app.services.api_football import APIFootballService


class AnalysisService:
    @staticmethod
    def get_team_analysis(team_id: int, season: int, limit: int = 5):
        matches = APIFootballService.get_last_team_matches(
            team_id=team_id,
            season=season,
            limit=limit
        )

        return {
            "team_id": team_id,
            "season": season,
            "matches_found": len(matches),
            "matches": matches
        }

    @staticmethod
    def get_team_summary(team_id: int, limit: int = 5):
        matches = APIFootballService.get_last_team_matches(
            team_id=team_id,
            season=None,
            limit=limit
        )

        if not matches:
            return {
                "team_id": team_id,
                "matches_used": 0,
                "summary": {}
            }

        wins = draws = losses = 0
        goals_for = goals_against = 0
        home_games = away_games = 0
        home_wins = away_wins = 0

        for match in matches:
            home = match["teams"]["home"]
            away = match["teams"]["away"]
            goals = match["goals"]

            if home["id"] == team_id:
                home_games += 1
                goals_for += goals["home"]
                goals_against += goals["away"]

                if goals["home"] > goals["away"]:
                    wins += 1
                    home_wins += 1
                elif goals["home"] == goals["away"]:
                    draws += 1
                else:
                    losses += 1
            else:
                away_games += 1
                goals_for += goals["away"]
                goals_against += goals["home"]

                if goals["away"] > goals["home"]:
                    wins += 1
                    away_wins += 1
                elif goals["away"] == goals["home"]:
                    draws += 1
                else:
                    losses += 1

        total_games = wins + draws + losses

        summary = {
            "played": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "points": wins * 3 + draws,
            "points_percentage": round(
                ((wins * 3 + draws) / (total_games * 3)) * 100, 2
            ) if total_games else 0,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goals_for - goals_against,
            "average_goals_for": round(goals_for / total_games, 2) if total_games else 0,
            "average_goals_against": round(goals_against / total_games, 2) if total_games else 0,
            "home": {
                "games": home_games,
                "wins": home_wins
            },
            "away": {
                "games": away_games,
                "wins": away_wins
            }
        }

        return {
            "team_id": team_id,
            "matches_used": total_games,
            "summary": summary
        }
