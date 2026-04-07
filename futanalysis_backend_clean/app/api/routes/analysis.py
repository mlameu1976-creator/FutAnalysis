from fastapi import APIRouter
from app.services.ml_prediction_service import MLPredictionService

router = APIRouter()

@router.post("/analysis/ml-prediction")
def get_ml_prediction(payload: dict):
    service = MLPredictionService()   # 👈 cria instância
    return service.predict(payload)   # 👈 chama corretamente
