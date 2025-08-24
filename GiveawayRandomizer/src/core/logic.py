import re
import random
from typing import List

def list_to_array(name_list: str) -> List[str]:
    if not name_list:
        return []
    array = re.split(r"\r?\n+", name_list.strip())
    seen = set()
    unique_array = []
    for name in array:
        key = name.replace(" ", "")
        if key and key not in seen:
            seen.add(key)
            unique_array.append(name.strip())
    return unique_array

def draw(participants: List[str], number_of_winners: int) -> List[str]:
    if number_of_winners <= 0 or not participants:
        return []
    number_of_winners = min(number_of_winners, len(participants))
    pool = list(participants)  # copie
    winners = []
    for _ in range(number_of_winners):
        idx = random.randrange(len(pool))
        winners.append(pool.pop(idx))
    return winners
