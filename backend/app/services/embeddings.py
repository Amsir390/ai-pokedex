def pokemon_to_text(row):
    name = str(row["Pokemon"]).strip()
    ptype = str(row["Type"]).replace(",", " and")

    return (
        f"{name} is a Pokémon. "
        f"It is of type {ptype}. "
        f"Species: {row['Species']}. "
        f"Height: {row['Height']}. "
        f"Weight: {row['Weight']}. "
        f"Abilities include {row['Abilities']}. "
        f"Base stats include "
        f"HP {row['HP Base']}, "
        f"Attack {row['Attack Base']}, "
        f"Defense {row['Defense Base']}, "
        f"Special Attack {row['Special Attack Base']}, "
        f"Special Defense {row['Special Defense Base']}, "
        f"Speed {row['Speed Base']}."
    )
