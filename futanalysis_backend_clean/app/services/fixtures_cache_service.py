import json
from datetime import date
from pathlib import Path
from typing import List, Dict, Any


class FixturesCacheService:
    """
    Cache diário de fixtures (arquivo local).
    Evita múltiplas chamadas à SportMonks no mesmo dia.
    """

    CACHE_DIR = Path("cache")
    CACHE_FILE = CACHE_DIR / "fixtures_cache.json"

    def __init__(self):
        self.CACHE_DIR.mkdir(exist_ok=True)

    def _load_cache(self) -> Dict[str, Any]:
        if not self.CACHE_FILE.exists():
            return {}

        with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_cache(self, cache: Dict[str, Any]) -> None:
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def get_today(self) -> str:
        return date.today().isoformat()

    def get(self) -> List[Dict[str, Any]] | None:
        cache = self._load_cache()
        today = self.get_today()

        if today in cache:
            return cache[today]

        return None

    def set(self, fixtures: List[Dict[str, Any]]) -> None:
        cache = self._load_cache()
        today = self.get_today()

        cache[today] = fixtures
        self._save_cache(cache)
