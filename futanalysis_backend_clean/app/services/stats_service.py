from typing import Dict


class StatsService:
    """
    Serviço responsável por transformar dados brutos
    em métricas estatísticas utilizáveis.
    """

    def build_stats(self, home: Dict, away: Dict) -> Dict:
        """
        Espera dicionários com dados históricos dos times.
        """

        home_goalsd = home["goals_scored"]
        home_conceded = home["goals_conceded"]

        away_goalsd = away["goals_scored"]
        away_conceded = away["goals_conceded"]

        stats = {
            "home_avg_goals": home_goalsd,
            "away_avg_goals": away_goalsd,
            "home_conceded": home_conceded,
            "away_conceded": away_conceded,
            "total_avg_goals": home_goalsd + away_goalsd,
            "over_15_rate": home["over15_rate"] * 0.5 + away["over15_rate"] * 0.5,
            "over_25_rate": home["over25_rate"] * 0.5 + away["over25_rate"] * 0.5,
            "btts_rate": home["btts_rate"] * 0.5 + away["btts_rate"] * 0.5,
            "ht_goal_rate": home["ht_goal_rate"] * 0.5 + away["ht_goal_rate"] * 0.5,
        }

        return stats
