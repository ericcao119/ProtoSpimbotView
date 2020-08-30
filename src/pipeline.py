"""A basic pipeline for other objects to inherit from. This exists to formalize
the separation between the game, the MIPS emulator, and graphical state as several "concurrent"
processes.

Note: This pipeline can be Turing complete and it is recommended that you add a state controller
to handle the transition. However, refrain from including large state machines since they complicate
the code. Instead prefer including subcomponents that run their own state machines in a hierarchical fashion.
"""
from typing import Any, List


class Pipeline:
    def __init__(self):
        self.__post_init__()

    def __post_init__(self):
        pass

    def feed(self, inp) -> Any:
        return None

    def feed_many(self, inputs) -> List[Any]:
        return [self.feed(inp) for inp in inputs]
