from app.services.fixtures_service import FixturesService
from app.services.analysis_service import AnalysisService


class OpportunityService:
    def __init__(self):
        self.fixtures_service = FixturesService()
        self.analysis_service = AnalysisService()

    def get_opportunities(self, market: str = "all"):
        fixtures = self.fixtures_service.get_fixtures_today_and_tomorrow()

        opportunities = []

        for fixture in fixtures:
            home = fixture["home_team"]
            away = fixture["away_team"]

            home_stats = self.analysis_service.get_last_games_analysis(home, limit=5)
            away_stats = self.analysis_service.get_last_games_analysis(away, limit=5)

            if not home_stats or not away_stats:
                continue

            # ===== MERCADOS =====
            if home_stats["over_25_rate"] >= 0.6 and away_stats["over_25_rate"] >= 0.6:
                opportunities.append({
                    "market": "over_2_5",
                    "home": home,
                    "away": away,
                    "confidence": round((home_stats["over_25_rate"] + away_stats["over_25_rate"]) / 2, 2)
                })

            if home_stats["btts_rate"] >= 0.6 and away_stats["btts_rate"] >= 0.6:
                opportunities.append({
                    "market": "btts",
                    "home": home,
                    "away": away,
                    "confidence": round((home_stats["btts_rate"] + away_stats["btts_rate"]) / 2, 2)
                })

            if home_stats["avg_goals"] + away_stats["avg_goals"] >= 2.0:
                opportunities.append({
                    "market": "over_1_5",
                    "home": home,
                    "away": away,
                    "confidence": round((home_stats["avg_goals"] + away_stats["avg_goals"]) / 3, 2)
                })

            if home_stats["home_win_rate"] >= 0.6:
                opportunities.append({
                    "market": "home_win",
                    "home": home,
                    "away": away,
                    "confidence": home_stats["home_win_rate"]
                })

            if away_stats["away_win_rate"] >= 0.6:
                opportunities.append({
                    "market": "away_win",
                    "home": home,
                    "away": away,
                    "confidence": away_stats["away_win_rate"]
                })

        # ===== FILTRO POR MERCADO =====
        if market != "all":
            opportunities = [o for o in opportunities if o["market"] == market]

        return {
            "market": market,
            "count": len(opportunities),
            "data": opportunities
        }
