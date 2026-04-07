from typing import Dict


class AdvancedPredictionService:
    """
    Predição estatística avançada (sem ML):
    Combina múltiplos indicadores de performance recente.
    """

    @staticmethod
    def predict(summary: Dict, is_home: bool = True) -> Dict:
        played = summary["played"]

        if played == 0:
            return {
                "home_win": 0,
                "draw": 0,
                "away_win": 0,
                "confidence": 0
            }

        # métricas base
        win_rate = summary["wins"] / played
        draw_rate = summary["draws"] / played
        loss_rate = summary["losses"] / played

        avg_goals_for = summary["average_goals_for"]
        avg_goals_against = summary["average_goals_against"]
        goal_diff = summary["goal_difference"]

        clean_sheet_rate = summary["clean_sheets"] / played

        # pesos (ajustáveis futuramente)
        score = 0
        score += win_rate * 0.35
        score += clean_sheet_rate * 0.20
        score += (avg_goals_for / (avg_goals_for + avg_goals_against + 0.1)) * 0.25
        score += (goal_diff / (abs(goal_diff) + 1)) * 0.10

        # fator casa / fora
        if is_home:
            score += 0.10
        else:
            score -= 0.05

        # normalização
        win_prob = max(min(score, 1), 0)
        draw_prob = max(min(draw_rate * 0.5, 0.3), 0)
        loss_prob = max(1 - win_prob - draw_prob, 0)

        confidence = round((win_prob + (1 - loss_prob)) / 2 * 100, 2)

        return {
            "win": round(win_prob * 100, 2),
            "draw": round(draw_prob * 100, 2),
            "loss": round(loss_prob * 100, 2),
            "confidence": confidence
        }
