from typing import Dict


class PredictionService:
    """
    Base para evolução futura:
    - probabilidades
    - machine learning
    - modelos estatísticos
    """

    @staticmethod
    def simple_probabilities(summary: Dict) -> Dict:
        played = summary["played"]

        if played == 0:
            return {"home_win": 0, "draw": 0, "away_win": 0}

        win_rate = summary["wins"] / played
        draw_rate = summary["draws"] / played
        loss_rate = summary["losses"] / played

        return {
            "win": round(win_rate * 100, 2),
            "draw": round(draw_rate * 100, 2),
            "loss": round(loss_rate * 100, 2)
        }
