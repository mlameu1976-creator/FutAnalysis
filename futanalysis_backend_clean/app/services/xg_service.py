from sqlalchemy import func
from app.models.match import Match


HOME_ADVANTAGE = 1.10


def calculate_league_average(db, league_id):

    avg_goals = db.query(
        func.avg(Match.home_goals + Match.away_goals)
    ).filter(
        Match.league_id == league_id,
        Match.is_finished == True
    ).scalar()

    return avg_goals or 2.6


def calculate_team_attack_strength(db, team_name, league_id):

    avg_goals = db.query(
        func.avg(Match.home_goals)
    ).filter(
        Match.home_team == team_name,
        Match.is_finished == True
    ).scalar()

    return avg_goals or 1.2


def calculate_team_defense_strength(db, team_name, league_id):

    avg_conceded = db.query(
        func.avg(Match.away_goals)
    ).filter(
        Match.home_team == team_name,
        Match.is_finished == True
    ).scalar()

    return avg_conceded or 1.2


def expected_goals(db, league_id, home_team, away_team):

    league_avg = calculate_league_average(db, league_id)

    home_attack = calculate_team_attack_strength(db, home_team, league_id)
    away_attack = calculate_team_attack_strength(db, away_team, league_id)

    home_defense = calculate_team_defense_strength(db, home_team, league_id)
    away_defense = calculate_team_defense_strength(db, away_team, league_id)

    lambda_home = home_attack * away_defense * HOME_ADVANTAGE
    lambda_away = away_attack * home_defense

    return lambda_home, lambda_away
