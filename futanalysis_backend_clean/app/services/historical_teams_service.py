# app/services/historical_teams_service.py

class HistoricalTeamsService:
    """
    Serviço responsável por fornecer lista de times
    (base inicial, expansível futuramente)
    """

    @staticmethod
    def list_teams():
        # Base estática inicial (pode vir de DB ou API depois)
        return [
            "Flamengo",
            "Palmeiras",
            "Corinthians",
            "São Paulo",
            "Grêmio",
            "Internacional",
            "Atlético-MG",
            "Cruzeiro",
            "Vasco",
            "Botafogo"
        ]
