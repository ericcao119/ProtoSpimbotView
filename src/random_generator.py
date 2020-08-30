import random

import yaml

from src.config import WORLD_SIZE
from src.types import *


def generate_random_state():
    state = {"Bots": [], "Photons": [], "Metrics": {}, "Map": ""}

    state["Bots"] += [
        Bot(
            id=0,
            x=random.randint(0, WORLD_SIZE),
            y=random.randint(0, WORLD_SIZE),
            angle=random.randint(-360, 360),
        ),
        Bot(
            id=1,
            x=random.randint(0, WORLD_SIZE),
            y=random.randint(0, WORLD_SIZE),
            angle=random.randint(-360, 360),
        ),
    ]

    for i in range(random.randint(0, 10)):
        state["Photons"].append(
            Photon(
                color=random.randint(0, 1),
                x=random.random() * WORLD_SIZE,
                y=random.random() * WORLD_SIZE,
            )
        )

    state["Map"] = [Map("F" * int(WORLD_SIZE / HEIGHT) * int(WORLD_SIZE / WIDTH))]
    state["Metrics"]["Score"] = [random.randint(0, 1000), random.randint(0, 1000)]
    return state


def generate_random_yaml():
    with open("random.yml", "w") as f:
        yaml.dump_all([generate_random_state() for i in range(2000)], f)


if __name__ == "__main__":
    generate_random_yaml()
