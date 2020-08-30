from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent / "config.yml"
TEST_PATH = Path(__file__).parent / "test.yml"

config = yaml.load(CONFIG_PATH.read_text())


def SCALE(x):
    return config["SCALE"] * x


FFMPEG_BIN = config["FFMPEG_BIN"]
WORLD_SIZE = config["WORLD_SIZE"]
LABEL_SPACE = config["LABEL_SPACE"]
CYCLE_LIMIT = config["CYCLE_LIMIT"]
DRAW_CYCLES = config["DRAW_CYCLES"]
NUM_CONTEXTS = config["NUM_CONTEXTS"]
LAB_PART_NUM = config["LAB_PART_NUM"]
DARKEN_CYCLE = config["DARKEN_CYCLE"]
