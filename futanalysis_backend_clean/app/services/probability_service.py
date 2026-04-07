import math


MAX_GOALS = 7


def poisson(lmbda, k):
    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)


def match_probability_matrix(home_lambda, away_lambda):

    matrix = []

    for i in range(MAX_GOALS):
        row = []

        for j in range(MAX_GOALS):

            prob = poisson(home_lambda, i) * poisson(away_lambda, j)

            row.append(prob)

        matrix.append(row)

    return matrix


def probability_over_15(matrix):

    prob = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if i + j >= 2:
                prob += matrix[i][j]

    return prob


def probability_over_25(matrix):

    prob = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if i + j >= 3:
                prob += matrix[i][j]

    return prob


def probability_under_25(matrix):

    prob = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if i + j <= 2:
                prob += matrix[i][j]

    return prob


def probability_btts(matrix):

    prob = 0

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):

            prob += matrix[i][j]

    return prob


def probability_home_win(matrix):

    prob = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if i > j:
                prob += matrix[i][j]

    return prob


def probability_away_win(matrix):

    prob = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if j > i:
                prob += matrix[i][j]

    return prob


def probability_goal_ht(home_lambda, away_lambda):

    # Aproximação: metade dos gols esperados no 1º tempo

    home_ht = home_lambda / 2
    away_ht = away_lambda / 2

    prob_home_zero = poisson(home_ht, 0)
    prob_away_zero = poisson(away_ht, 0)

    return 1 - (prob_home_zero * prob_away_zero)


def calculate_market_probabilities(home_lambda, away_lambda):

    matrix = match_probability_matrix(home_lambda, away_lambda)

    return {

        "OVER_1_5": probability_over_15(matrix),
        "OVER_2_5": probability_over_25(matrix),
        "UNDER_2_5": probability_under_25(matrix),
        "BTTS": probability_btts(matrix),
        "HOME_WIN": probability_home_win(matrix),
        "AWAY_WIN": probability_away_win(matrix),
        "GOAL_HT": probability_goal_ht(home_lambda, away_lambda),

    }
