from pathlib import Path

IMAGE_ROOT = Path("data/images")

def get_pokemon_image(pokemon_name: str):
    if not pokemon_name:
        return None

    target = pokemon_name.strip().lower()

    for folder in IMAGE_ROOT.iterdir():
        if folder.is_dir() and folder.name.lower() == target:
            for img in folder.iterdir():
                if img.suffix.lower() == ".png":
                    return f"/images/{folder.name}/{img.name}"

    return None
