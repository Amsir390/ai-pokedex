def parse_pokedex_row(row: dict) -> dict:
    """
    Converts a CSV Pokémon row into a structured Pokédex card
    """

    return {
        "name": row.get("Pokemon", "Unknown"),
        "type": row.get("Type", "Unknown"),
        "species": row.get("Species", "Unknown"),
        "height": row.get("Height", "Unknown"),
        "weight": row.get("Weight", "Unknown"),
        "abilities": row.get("Abilities", "Unknown"),

        # ✅ Base stats EXACTLY from CSV
        "base_stats": (
            f"HP: {row.get('HP Base', 'N/A')}\n"
            f"Attack: {row.get('Attack Base', 'N/A')}\n"
            f"Defense: {row.get('Defense Base', 'N/A')}\n"
            f"Special Attack: {row.get('Special Attack Base', 'N/A')}\n"
            f"Special Defense: {row.get('Special Defense Base', 'N/A')}\n"
            f"Speed: {row.get('Speed Base', 'N/A')}"
        ),

        # Description will be added by LLM later
        "description": ""
    }
