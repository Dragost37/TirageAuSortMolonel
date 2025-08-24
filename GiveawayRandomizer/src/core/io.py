from typing import Iterable

def save_winners(path: str, winners: Iterable[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("Résultats du tirage\n\n")
        for i, w in enumerate(winners, 1):
            f.write(f"Gagnant {i} : {w}\n")

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
