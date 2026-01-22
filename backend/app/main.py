from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.services.rag_engine import retrieve_context
from backend.app.services.llm import generate_answer
from backend.app.services.name_extractor import extract_pokemon_name
from backend.app.services.image_resolver import get_pokemon_image
from backend.app.services.pokedex_parser import parse_pokedex_row

app = FastAPI(title="AI Pokédex")

# -----------------------------
# SERVE IMAGES
# -----------------------------
IMAGE_DIR = Path("data/images")
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

# -----------------------------
# SMALL TALK
# -----------------------------
SMALL_TALK = {
    "hi": "Hi! 👋 Ask me anything about Pokémon.",
    "hello": "Hello! 😊 I'm your AI Pokédex.",
    "hey": "Hey there! ⚡ Which Pokémon are you curious about?",
    "who are you": "I'm an AI Pokédex powered by Pokémon data and a local LLaMA model.",
    "help": "Ask me about Pokémon stats, abilities, types, or comparisons."
}

@app.get("/")
def root():
    return {"status": "AI Pokédex API running"}

@app.get("/ask")
def ask_pokedex(query: str):
    q = query.lower().strip()

    # 1️⃣ Small talk
    if q in SMALL_TALK:
        return {
            "question": query,
            "card": None,
            "answer": SMALL_TALK[q],
            "image": None
        }

    # 2️⃣ Normalize short queries
    if len(query.split()) == 1:
        query = f"Tell me about {query}"

    # 3️⃣ RAG: CSV row + context
    pokemon_row, context = retrieve_context(query)

    if not pokemon_row:
        return {
            "question": query,
            "card": None,
            "answer": "🤔 I don't have Pokémon data for that.",
            "image": None
        }

    # 4️⃣ Build Pokédex card FROM CSV (stats, type, etc.)
    card = parse_pokedex_row(pokemon_row)

    # 5️⃣ 🔥 GENERATE DESCRIPTION USING LLM (ONLY TEXT)
    description = generate_answer(context, query)
    card["description"] = description

    # 6️⃣ Resolve image from Pokémon name
    image = get_pokemon_image(card["name"])

    # 7️⃣ Return structured response
    return {
        "question": query,
        "card": card,
        "image": image
    }
