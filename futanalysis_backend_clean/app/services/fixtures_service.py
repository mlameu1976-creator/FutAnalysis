from app.services.thesportsdb_client import TheSportsDBClient


class FixturesService:
    def __init__(self):
        self.client = TheSportsDBClient()

    def get_fixtures_today(self):
        return self.client.get_today_fixtures()
