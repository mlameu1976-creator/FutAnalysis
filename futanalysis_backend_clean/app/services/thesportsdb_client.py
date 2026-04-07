import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"


class TheSportsDBClient:

    def __init__(self):
        self.session = requests.Session()

        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"[API ERROR] {url} -> {str(e)}")
            return None

    # ===============================
    # ENDPOINTS
    # ===============================
    def get_all_leagues(self):
        return self._get("all_leagues.php")

    def get_events_by_league(self, league_id):
        return self._get("eventsseason.php", {"id": league_id})

    def get_teams_by_league(self, league_id):
        return self._get("lookup_all_teams.php", {"id": league_id})