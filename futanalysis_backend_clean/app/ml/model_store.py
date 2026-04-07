import pickle
from pathlib import Path

MODEL_PATH = Path("models")
MODEL_PATH.mkdir(exist_ok=True)


class ModelStore:
    @staticmethod
    def save(model, name: str):
        with open(MODEL_PATH / f"{name}.pkl", "wb") as f:
            pickle.dump(model, f)

    @staticmethod
    def load(name: str):
        with open(MODEL_PATH / f"{name}.pkl", "rb") as f:
            return pickle.load(f)
