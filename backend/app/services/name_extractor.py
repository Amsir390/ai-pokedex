import re

def extract_pokemon_name(query: str):
    """
    Extract Pokémon name from common question patterns.
    Returns None if not found.
    """

    if not query:
        return None

    q = query.lower().strip()

    # Pattern: "tell me about X", "about X"
    match = re.search(r"(?:about|is|who is)\s+([a-zA-Z\- ]+)", q)
    if match:
        return match.group(1).strip().title()

    # If user enters only one word (e.g., "Abra")
    words = q.split()
    if len(words) == 1:
        return words[0].title()

    return None
