import faiss
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD MODELS & DATA
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/pokemon.index")
texts = pickle.load(open("vector_store/texts.pkl", "rb"))

# Load CSV once
df = pd.read_csv("data/pokemon.csv")

# -----------------------------
# HELPERS
# -----------------------------
def find_pokemon_row(name: str):
    match = df[df["Pokemon"].str.lower() == name.lower()]
    if match.empty:
        return None
    return match.iloc[0].to_dict()

# -----------------------------
# RAG RETRIEVAL
# -----------------------------
def retrieve_context(query: str, k: int = 3):
    """
    Returns:
    - pokemon_row (dict or None)
    - context_text (str)
    """

    query_vec = model.encode([query])
    _, indices = index.search(np.array(query_vec), k)

    # Build text context for LLM
    context_text = "\n".join(texts[i] for i in indices[0])

    # Try extracting Pokémon name from best hit
    best_text = texts[indices[0][0]]

    # Assumes text starts with Pokémon name
    pokemon_name = best_text.split(" ")[0]

    pokemon_row = find_pokemon_row(pokemon_name)

    return pokemon_row, context_text

