from sklearn.linear_model import LogisticRegression


class MatchOutcomeModel:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_proba(self, features):
        probs = self.model.predict_proba([features])[0]
        return {
            "loss": round(probs[0] * 100, 2),
            "draw": round(probs[1] * 100, 2),
            "win": round(probs[2] * 100, 2),
        }
