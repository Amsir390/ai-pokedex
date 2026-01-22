import subprocess

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are an expert Pokédex assistant.

Using ONLY the information in the context, generate a Pokédex entry
in the EXACT format below:

Name:
Type:
Species:
Height:
Weight:
Abilities:
Base Stats:
Description:

Rules:
- If information is missing, write "Unknown"
- Base Stats must be listed clearly
- Description must be 2–3 sentences only
- Do NOT add extra fields

Context:
{context}

Question:
{question}
"""

    process = subprocess.Popen(
        ["ollama", "run", "llama3:8b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    output, _ = process.communicate(prompt)
    return output.strip()
