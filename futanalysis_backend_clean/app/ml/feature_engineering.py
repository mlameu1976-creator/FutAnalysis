from typing import Dict, List


class FeatureEngineering:
    """
    Converte summary em vetor numérico para ML
    """

    @staticmethod
    def summary_to_features(summary: Dict) -> List[float]:
        return [
            summary["points_percentage"],
            summary["average_goals_for"],
            summary["average_goals_against"],
            summary["goal_difference"],
            summary["clean_sheets"],
            summary["over_2_5"],
            summary["home"]["wins"],
            summary["away"]["wins"],
        ]
