from typing import List, Tuple
from app.services.api_football import APIFootballService
from app.services.team_analysis_service import TeamAnalysisService
from app.ml.feature_engineering import FeatureEngineering


class DatasetBuilder:
    """
    Constrói dataset supervisionado a partir de jogos reais
    """

    @staticmethod
    def build_for_team(team_id: int, season: int = 2024) -> Tuple[List[List[float]], List[int]]:
        matches = APIFootballService.get_last_team_matches(
            team_id=team_id,
            season=season,
            limit=20
        )

        X = []
        y = []

        for match in matches:
            summary = TeamAnalysisService.summarize([match], team_id)
            features = FeatureEngineering.summary_to_features(summary)

            goals_for = summary["goals_for"]
            goals_against = summary["goals_against"]

            if goals_for > goals_against:
                label = 2  # vitória
            elif goals_for == goals_against:
                label = 1  # empate
            else:
                label = 0  # derrota

            X.append(features)
            y.append(label)

        return X, y
