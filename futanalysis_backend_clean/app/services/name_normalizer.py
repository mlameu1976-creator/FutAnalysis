import re
import unicodedata


def normalize_name(name: str) -> str:
    if not name:
        return ""

    # remove acentos
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    # lowercase
    name = name.lower()

    # remove caracteres especiais
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    # normaliza espaços
    name = re.sub(r"\s+", " ", name).strip()

    return name
