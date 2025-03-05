from enum import Enum


ROWS = 8
COLS = 8
PIECES = 12


class ColorEnum(Enum):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)


class DirectionEnum(Enum):
    FORWARD = 1
    BACKWARD = -1
    BOTH = 0


class ColorInitialEnum(Enum):
    R = "R"
    B = "B"


SQUARE_STYLE = (
    "<style>.st-key-board .stHorizontalBlock:nth-child(even) .stColumn:nth-child(odd){ "
    "    background-color:#C19A6B }"
    ".st-key-board .stHorizontalBlock:nth-child(even) .stColumn:nth-child(even){ "
    "    background-color:#FFE4C4 }"
    ".st-key-board .stHorizontalBlock:nth-child(odd) .stColumn:nth-child(even){"
    "    background-color:#C19A6B }"
    ".st-key-board .stHorizontalBlock:nth-child(odd) .stColumn:nth-child(odd){"
    "    background-color:#FFE4C4 }"
    "<style>"
)

RED_CIRCLE_STYLE = (
    "<style>.circle{border-radius: 50%; width:70px; height:70px; background-color:}"
)


class PointsEnum(Enum):
    PIECE = 2
    KING = 10
    EMPTY = 1


INPUT_KEYS = ["row", "col", "new_row", "new_col"]
