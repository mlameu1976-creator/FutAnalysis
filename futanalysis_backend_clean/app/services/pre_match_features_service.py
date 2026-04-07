from sqlalchemy.orm import Session
from sqlalchemy import func
from multiprocessing import Pool, cpu_count

from app.models.match import Match
from app.models.pre_match_features import PreMatchFeatures
from app.services.poisson import PoissonModel


# ===============================
# 🔥 FUNÇÃO PARA PARALELISMO
# ===============================
def process_chunk(args):
    matches_chunk, team_stats, league_avg = args

    results = []

    for match in matches_chunk:

        home_stats = team_stats.get(match.home_team)
        away_stats = team_stats.get(match.away_team)

        if not home_stats or not away_stats:
            continue

        league_avg_half = league_avg / 2

        exp_home = (home_stats["home_scored"] / league_avg_half) * (away_stats["away_conceded"] / league_avg_half) * league_avg_half
        exp_away = (away_stats["away_scored"] / league_avg_half) * (home_stats["home_conceded"] / league_avg_half) * league_avg_half

        probs = PoissonModel.calculate_probabilities(exp_home, exp_away)

        results.append({
            "match_id": match.id,
            "exp_home_goals": exp_home,
            "exp_away_goals": exp_away,
            "exp_total_goals": exp_home + exp_away,
            "prob_btts": probs["prob_btts"],
            "prob_over_15": probs["prob_over_15"],
            "prob_over_25": probs["prob_over_25"],
            "prob_under_25": probs["prob_under_25"],
            "prob_home_win": probs["prob_home_win"],
            "prob_away_win": probs["prob_away_win"],
            "prob_goal_ht": probs["prob_goal_ht"],
        })

    return results


class PreMatchFeaturesService:

    def __init__(self, db: Session):
        self.db = db
        self.team_stats_cache = self.load_team_stats()
        self.league_avg_goals = self.calculate_league_avg_goals()

    def calculate_league_avg_goals(self):
        avg_home = self.db.query(func.avg(Match.home_goals)).scalar()
        avg_away = self.db.query(func.avg(Match.away_goals)).scalar()
        return float((avg_home or 1.2) + (avg_away or 1.2))

    # 🔥 UMA QUERY (CRUCIAL)
    def load_team_stats(self):

        print("Carregando stats ULTRA...")

        stats = {}

        home = (
            self.db.query(
                Match.home_team,
                func.avg(Match.home_goals),
                func.avg(Match.away_goals)
            )
            .group_by(Match.home_team)
            .all()
        )

        away = (
            self.db.query(
                Match.away_team,
                func.avg(Match.away_goals),
                func.avg(Match.home_goals)
            )
            .group_by(Match.away_team)
            .all()
        )

        for t, s, c in home:
            stats[t] = {
                "home_scored": float(s or 1.2),
                "home_conceded": float(c or 1.2),
                "away_scored": 1.2,
                "away_conceded": 1.2,
            }

        for t, s, c in away:
            if t not in stats:
                stats[t] = {}

            stats[t]["away_scored"] = float(s or 1.2)
            stats[t]["away_conceded"] = float(c or 1.2)

        return stats


# ===============================
# 🚀 ENGINE ULTRA RÁPIDO
# ===============================
def generate_pre_match_features(db: Session):

    print("🚀 ULTRA PIPELINE INICIADO")

    service = PreMatchFeaturesService(db)

    matches = db.query(Match).all()

    # 🔥 dividir em chunks
    num_cores = cpu_count()
    chunk_size = len(matches) // num_cores

    chunks = [
        matches[i:i + chunk_size]
        for i in range(0, len(matches), chunk_size)
    ]

    print(f"🔥 Usando {num_cores} cores")

    args = [
        (chunk, service.team_stats_cache, service.league_avg_goals)
        for chunk in chunks
    ]

    # 🔥 PROCESSAMENTO PARALELO
    with Pool(num_cores) as pool:
        results = pool.map(process_chunk, args)

    # 🔥 FLATTEN
    all_features = [item for sublist in results for item in sublist]

    print(f"🔥 Features calculadas: {len(all_features)}")

    # 🔥 INSERT MASSIVO
    objects = [PreMatchFeatures(**f) for f in all_features]

    db.bulk_save_objects(objects)
    db.commit()

    print("✅ FINALIZADO ULTRA RÁPIDO")

    return len(objects)