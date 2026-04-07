import math


class PoissonModel:

    MAX_GOALS = 10

    @staticmethod
    def poisson_probability(lmbda: float, k: int) -> float:
        """
        Probability of scoring k goals with expected value lambda
        """
        return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)

    @classmethod
    def goal_distribution(cls, expected_goals: float):
        """
        Returns probability distribution for goals 0..MAX_GOALS
        """
        probs = []

        for k in range(cls.MAX_GOALS + 1):
            probs.append(cls.poisson_probability(expected_goals, k))

        return probs

    @classmethod
    def match_matrix(cls, home_xg: float, away_xg: float):
        """
        Create score probability matrix
        """
        home_probs = cls.goal_distribution(home_xg)
        away_probs = cls.goal_distribution(away_xg)

        matrix = []

        for h in range(cls.MAX_GOALS + 1):
            row = []
            for a in range(cls.MAX_GOALS + 1):
                row.append(home_probs[h] * away_probs[a])
            matrix.append(row)

        return matrix

    @classmethod
    def calculate_probabilities(cls, home_xg: float, away_xg: float):

        matrix = cls.match_matrix(home_xg, away_xg)

        prob_home_win = 0
        prob_away_win = 0
        prob_draw = 0

        prob_over_15 = 0
        prob_over_25 = 0
        prob_under_25 = 0

        prob_btts = 0

        for h in range(cls.MAX_GOALS + 1):
            for a in range(cls.MAX_GOALS + 1):

                p = matrix[h][a]

                total_goals = h + a

                if h > a:
                    prob_home_win += p
                elif a > h:
                    prob_away_win += p
                else:
                    prob_draw += p

                if total_goals >= 2:
                    prob_over_15 += p

                if total_goals >= 3:
                    prob_over_25 += p

                if total_goals <= 2:
                    prob_under_25 += p

                if h > 0 and a > 0:
                    prob_btts += p

        # -----------------------------
        # GOAL HT CALCULATION
        # -----------------------------

        total_xg = home_xg + away_xg

        # média de gols no primeiro tempo (~45%)
        ht_xg = total_xg * 0.45

        prob_zero_ht = cls.poisson_probability(ht_xg, 0)

        prob_goal_ht = 1 - prob_zero_ht

        return {
            "prob_home_win": prob_home_win,
            "prob_away_win": prob_away_win,
            "prob_draw": prob_draw,
            "prob_over_15": prob_over_15,
            "prob_over_25": prob_over_25,
            "prob_under_25": prob_under_25,
            "prob_btts": prob_btts,
            "prob_goal_ht": prob_goal_ht
        }