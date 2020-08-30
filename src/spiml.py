from dataclasses import Field, dataclass
from pathlib import Path
from typing import List, Union

from yaml import load_all

from src.types import Bot, Photon, Tile


def from_yaml(stream: Union[str, Path]):
    # Handle if yaml file
    if isinstance(stream, Path):
        if stream.is_file():
            return from_yaml(stream.read_text())
        else:
            raise ValueError(f"Yaml file: {stream} is not a file")

    documents = load_all(stream)

    return documents
