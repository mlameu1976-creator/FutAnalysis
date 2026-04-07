class ValueBetEngine:

    @staticmethod
    def calculate_fair_odd(probability: float):

        if probability <= 0:
            return None

        return 1 / probability


    @staticmethod
    def calculate_edge(probability: float, market_odd: float):

        if probability <= 0 or market_odd <= 0:
            return None

        fair_odd = 1 / probability

        edge = (market_odd / fair_odd) - 1

        return edge


    @staticmethod
    def build_value_bet(probability: float, market_odd: float):

        fair_odd = ValueBetEngine.calculate_fair_odd(probability)

        edge = ValueBetEngine.calculate_edge(probability, market_odd)

        return {
            "probability": probability,
            "fair_odd": fair_odd,
            "market_odd": market_odd,
            "edge": edge
        }