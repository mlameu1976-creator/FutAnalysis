from typing import List, Dict


class RankingService:

    @staticmethod
    def build_team_ranking(teams_data: List[Dict]) -> List[Dict]:
        """
        Espera dados normalizados (summary) de vários times
        """
        ranking = sorted(
            teams_data,
            key=lambda t: (
                t["summary"]["points"],
                t["summary"]["goal_difference"],
                t["summary"]["goals_for"]
            ),
            reverse=True
        )

        for idx, team in enumerate(ranking, start=1):
            team["position"] = idx

        return ranking
