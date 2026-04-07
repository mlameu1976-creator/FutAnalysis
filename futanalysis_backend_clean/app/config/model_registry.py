# futanalysis_backend_clean/app/config/model_registry.py

from pathlib import Path

# Chave: (league, market)
MODEL_REGISTRY = {
    ("EPL", "1X2"): Path("futanalysis_ml_training/epl_1x2.pkl"),
    ("LaLiga", "1X2"): Path("futanalysis_ml_training/laliga_1x2.pkl"),
    # exemplos futuros:
    # ("EPL", "OVER_UNDER"): Path("futanalysis_ml_training/epl_ou.pkl"),
}

DEFAULT_MODEL = None  # força fallback se não encontrar
