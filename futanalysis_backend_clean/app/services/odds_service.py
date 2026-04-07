import os
import requests
from sqlalchemy.orm import Session

from app.models import MatchOdds

ODDS_API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds"


SUPPORTED_MARKETS = {
    "HOME": "h2h",
    "AWAY": "h2h",
    "DRAW": "h2h",
    "OVER_15": "totals",
    "OVER_25": "totals",
    "BTTS_YES": "btts",
}


def get_cached_odds(db: Session, match_id: int):
    odds = db.query(MatchOdds).filter(MatchOdds.match_id == match_id).all()
    if not odds:
        return None
    return {o.market: o.odd for o in odds}


def save_odds(db: Session, match_id: int, odds: dict):
    for market, odd in odds.items():
        db.add(MatchOdds(match_id=match_id, market=market, odd=odd))
    db.commit()


def fetch_match_odds(db: Session, match):
    cached = get_cached_odds(db, match.id)
    if cached:
        return cached

    if not ODDS_API_KEY:
        return None

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h,totals,btts",
        "oddsFormat": "decimal",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except Exception:
        return None

    games = response.json()
    odds = {}

    for game in games:
        if (
            match.home_team.lower() in game.get("home_team", "").lower()
            and match.away_team.lower() in game.get("away_team", "").lower()
        ):
            for bookmaker in game.get("bookmakers", []):
                for market in bookmaker.get("markets", []):

                    # 🔹 RESULTADO
                    if market["key"] == "h2h":
                        for o in market["outcomes"]:
                            if o["name"] == match.home_team:
                                odds["HOME"] = o["price"]
                            elif o["name"] == match.away_team:
                                odds["AWAY"] = o["price"]
                            elif o["name"].lower() == "draw":
                                odds["DRAW"] = o["price"]

                    # 🔹 OVER / UNDER
                    if market["key"] == "totals":
                        for o in market["outcomes"]:
                            if o["name"] == "Over" and o["point"] == 1.5:
                                odds["OVER_15"] = o["price"]
                            if o["name"] == "Over" and o["point"] == 2.5:
                                odds["OVER_25"] = o["price"]

                    # 🔹 BTTS
                    if market["key"] == "btts":
                        for o in market["outcomes"]:
                            if o["name"].lower() == "yes":
                                odds["BTTS_YES"] = o["price"]

            if odds:
                save_odds(db, match.id, odds)
                return odds

    return None
