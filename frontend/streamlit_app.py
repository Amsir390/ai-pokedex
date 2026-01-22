import streamlit as st
import requests

# -----------------------------
# CONFIG
# -----------------------------
BACKEND_URL = "http://127.0.0.1:8000"
ASK_API = f"{BACKEND_URL}/ask"

st.set_page_config(
    page_title="AI Pokédex",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ AI Pokédex")
st.caption("Pokédex Cards • Images • Stats • Comparison • Local LLM")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# HELPERS
# -----------------------------
def is_comparison_query(text: str) -> bool:
    return " vs " in text.lower()

def render_type_badges(type_text: str):
    type_icons = {
        "electric": "⚡", "water": "💧", "fire": "🔥", "grass": "🌿",
        "psychic": "🔮", "dark": "🌑", "steel": "⚙️", "fairy": "✨",
        "dragon": "🐉", "ice": "❄️", "fighting": "🥊", "rock": "🪨",
        "ground": "🌍", "ghost": "👻", "poison": "☠️", "bug": "🐛",
        "flying": "🕊️", "normal": "⚪"
    }

    if not type_text:
        return

    cleaned = type_text.replace("/", ",")
    types = [t.strip().lower() for t in cleaned.split(",")]

    badges = []
    for t in types:
        icon = type_icons.get(t, "❓")
        badges.append(f"`{icon} {t.capitalize()}`")

    st.markdown(" ".join(badges))

def render_stat_bars(base_stats: str):
    for line in base_stats.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            try:
                value = int(v.strip())
                st.progress(min(value / 150, 1.0), text=f"{k.strip()}: {value}")
            except:
                pass

def render_pokedex_card(card: dict, image: str | None):
    if image:
        st.image(f"{BACKEND_URL}{image}", width=260)

    st.subheader(card.get("name", "Unknown"))

    render_type_badges(card.get("type", ""))

    st.markdown(
        f"**Species:** {card.get('species', 'Unknown')}  \n"
        f"**Height:** {card.get('height', 'Unknown')}  "
        f"**Weight:** {card.get('weight', 'Unknown')}  \n"
        f"**Abilities:** {card.get('abilities', 'Unknown')}"
    )

    st.markdown("### 📊 Base Stats")
    render_stat_bars(card.get("base_stats", ""))

    st.markdown("### 📝 Description")
    st.markdown(card.get("description", ""))

# -----------------------------
# RENDER CHAT HISTORY (SAFE)
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg.get("type") == "comparison":
            col1, col2 = st.columns(2)

            with col1:
                render_pokedex_card(msg["left"]["card"], msg["left"].get("image"))

            with col2:
                render_pokedex_card(msg["right"]["card"], msg["right"].get("image"))

        elif msg.get("type") == "card":
            render_pokedex_card(msg["card"], msg.get("image"))

        else:
            st.markdown(msg.get("content", ""))

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Ask about any Pokémon (or try: Dialga vs Palkia)")

if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Handle assistant logic
    with st.spinner("Thinking..."):

        if is_comparison_query(user_input):
            left, right = user_input.lower().split(" vs ")

            res1 = requests.get(ASK_API, params={"query": left.strip()}).json()
            res2 = requests.get(ASK_API, params={"query": right.strip()}).json()

            st.session_state.messages.append({
                "role": "assistant",
                "type": "comparison",
                "left": res1,
                "right": res2
            })

        else:
            res = requests.get(ASK_API, params={"query": user_input}).json()

            if res.get("card"):
                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "card",
                    "card": res["card"],
                    "image": res.get("image")
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": res.get("answer", "No response")
                })

    st.rerun()
