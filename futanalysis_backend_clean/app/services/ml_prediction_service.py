# futanalysis_backend_clean/app/services/ml_prediction_service.py

import pickle
from pathlib import Path
from typing import Dict, Tuple

from app.config.model_registry import MODEL_REGISTRY, DEFAULT_MODEL


class MLModelNotAvailable(Exception):
    pass


class MLPredictionService:
    """
    Serviço de ML com seleção por liga e mercado.
    """

    @classmethod
    def _get_model_path(cls, league: str, market: str) -> Path:
        return MODEL_REGISTRY.get((league, market), DEFAULT_MODEL)

    @classmethod
    def predict(cls, features: Dict) -> Dict:
        """
        Espera no payload:
        - league
        - market
        - demais features numéricas
        """

        league = features.pop("league", None)
        market = features.pop("market", None)

        if not league or not market:
            raise MLModelNotAvailable("Liga ou mercado não informados")

        model_path = cls._get_model_path(league, market)

        if not model_path or not model_path.exists():
            raise MLModelNotAvailable("Modelo não encontrado para liga/mercado")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        probs = model.predict_proba([list(features.values())])[0]

        return {
            "win": round(probs[0] * 100, 2),
            "draw": round(probs[1] * 100, 2),
            "loss": round(probs[2] * 100, 2),
        }
