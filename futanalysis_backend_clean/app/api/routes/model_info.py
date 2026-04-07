# futanalysis_backend_clean/app/routes/model_info.py

from fastapi import APIRouter

router = APIRouter(prefix="/model", tags=["Model Info"])


@router.get("/info")
def get_model_info():
    """
    Retorna informações do modelo/estratégia de predição ativa.
    Endpoint informativo e seguro (sem ML por enquanto).
    """

    return {
        "status": "active",
        "prediction_type": "statistical",
        "service": "PredictionService.simple_probabilities",
        "ml_enabled": False,
        "description": (
            "Predição baseada em estatísticas simples "
            "(wins, draws, losses). "
            "Modelo de Machine Learning ainda não integrado."
        ),
        "api_version": "1.0.0"
    }
