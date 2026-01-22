import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/pokemon.csv")

def load_pokemon_df():
    if not DATA_PATH.exists():
        raise FileNotFoundError("pokemon.csv not found in data/")
    return pd.read_csv(DATA_PATH)
