from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.ml.predict import predict_with_probabilities
from app.services.model_service import load_model, run_model


router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/")
def predict(data: Dict[str, Any]):
    """
    Endpoint de predição.
    Recebe features, executa o modelo e retorna probabilidades.
    """

    try:
        # 1. Carrega modelo
        model = load_model()

        # 2. Executa modelo → retorna SCORES BRUTOS
        raw_scores = run_model(model, data)

        # Exemplo esperado de raw_scores:
        # {
        #   "home_win": 1.42,
        #   "draw": 0.87,
        #   "away_win": -0.12
        # }

        # 3. Converte scores em probabilidades (%)
        probabilities = predict_with_probabilities(raw_scores)

        return {
            "status": "success",
            "probabilities": probabilities
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar predição: {str(e)}"
        )
