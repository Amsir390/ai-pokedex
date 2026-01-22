import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

from backend.app.services.data_loader import load_pokemon_df
from backend.app.services.embeddings import pokemon_to_text

print("🔹 Loading Pokémon data...")
df = load_pokemon_df()

print("🔹 Converting Pokémon to text...")
texts = df.apply(pokemon_to_text, axis=1).tolist()

print("🔹 Creating embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)

print("🔹 Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print("🔹 Saving vector store...")
faiss.write_index(index, "vector_store/pokemon.index")

with open("vector_store/texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("✅ Vector store built successfully!")
