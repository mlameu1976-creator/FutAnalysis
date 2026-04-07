import unicodedata


class TeamNameNormalizer:
    """
    Serviço responsável por normalizar nomes de times
    entre SportMonks e banco histórico.
    """

    # 🎯 MAPEAMENTO EXPLÍCITO (AJUSTÁVEL)
    TEAM_ALIASES = {
        # Inglaterra
        "Manchester United": "Man United",
        "Manchester City": "Man City",
        "Tottenham Hotspur": "Tottenham",
        "Wolverhampton Wanderers": "Wolves",

        # Espanha
        "Atlético Madrid": "Atletico Madrid",

        # Itália
        "Internazionale": "Inter",
        "AC Milan": "Milan",

        # Portugal
        "Sporting CP": "Sporting",

        # Brasil (exemplos)
        "Atlético Mineiro": "Atletico Mineiro",
    }

    @classmethod
    def normalize(cls, name: str) -> str:
        """
        Retorna o nome normalizado para busca no banco.
        """

        if not name:
            return name

        # 1️⃣ Mapeamento explícito
        if name in cls.TEAM_ALIASES:
            return cls.TEAM_ALIASES[name]

        # 2️⃣ Normalização genérica (fallback)
        normalized = cls._basic_normalize(name)

        return normalized

    @staticmethod
    def _basic_normalize(name: str) -> str:
        """
        Normalização genérica:
        - lowercase
        - remove acentos
        - remove sufixos comuns
        """
        name = name.lower()

        name = unicodedata.normalize("NFD", name)
        name = "".join(c for c in name if unicodedata.category(c) != "Mn")

        for suffix in [" fc", " cf", " sc", " ac"]:
            if name.endswith(suffix):
                name = name.replace(suffix, "")

        return name.strip()
