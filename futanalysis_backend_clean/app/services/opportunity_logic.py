from typing import List, Dict, Tuple


def confidence_from_score(score: int) -> str:
    if score >= 75:
        return "Alta"
    if score >= 60:
        return "Média"
    return "Baixa"


# =========================
# OVER 1.5 FT
# =========================
def over_15_score(stats: dict) -> dict:
    score = 0
    reasons = []

    if stats.get("avg_goals", 0) >= 2.0:
        score += 20
        reasons.append("Média de gols alta")

    if stats.get("home_avg", 0) >= 1.2:
        score += 15
        reasons.append("Casa marca bem")

    if stats.get("away_avg", 0) >= 0.8:
        score += 10
        reasons.append("Fora marca regularmente")

    if stats.get("over_15_rate", 0) >= 0.7:
        score += 20
        reasons.append("Over 1.5 frequente")

    if stats.get("btts_rate", 0) >= 0.6:
        score += 15
        reasons.append("Ambos marcam com frequência")

    return {
        "market": "Over 1.5 FT",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons
    }


# =========================
# GOALS HT
# =========================
def goals_ht_score(stats_ht: dict) -> dict:
    score = 0
    reasons = []

    if stats_ht.get("avg_goals", 0) >= 0.8:
        score += 25
        reasons.append("Boa média de gols no 1º tempo")

    if stats_ht.get("avg_goals", 0) >= 1.0:
        score += 10
        reasons.append("1º tempo com tendência forte de gols")

    if stats_ht.get("over_05_rate", 0) >= 0.65:
        score += 25
        reasons.append("Over 0.5 HT frequente")

    if stats_ht.get("over_05_rate", 0) >= 0.75:
        score += 10
        reasons.append("Alta recorrência de gols no 1º tempo")

    return {
        "market": "Goals HT",
        "score": score,
        "confidence": confidence_from_score(score),
        "reasons": reasons
    }


# =========================
# BUILD OPPORTUNITIES (DEDUP GARANTIDO)
# =========================
def build_opportunities(
    home_team: str,
    away_team: str,
    kickoff,
    analysis: dict
) -> List[dict]:
    """
    Gera oportunidades SEM duplicar mercados.
    A unicidade é: (match, market, kickoff)
    """

    opportunities: List[dict] = []
    seen: set[Tuple[str, str, str]] = set()

    def add(op: dict):
        key = (f"{home_team} vs {away_team}", op["market"], str(kickoff))
        if key not in seen:
            seen.add(key)
            opportunities.append(op)

    if "ft" in analysis:
        add(over_15_score(analysis["ft"]))

    if "ht" in analysis:
        add(goals_ht_score(analysis["ht"]))

    return opportunities