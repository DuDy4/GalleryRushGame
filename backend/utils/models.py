from typing import List, TypeAlias
from enum import Enum

GridType: TypeAlias = List[List[int]]

class WinReason(str, Enum):
    STATIC = "You got to a static state! Some district are probably more artistic then others ¯\_(ツ)_/¯"
    CYCLE = "You found yourself in a cycle. Art districts go!"
    EXTINCTION = "All galleries were closed... Nobody care about art anymore :("

class WinException(Exception):

    def __init__(self, reason: WinReason = None):
        self.reason: WinReason | None = reason
        super().__init__(reason.value if reason else "Game won")
