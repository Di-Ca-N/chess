from .SpecialMove import SpecialMove
from .Movement import Movement


def rook(king, king_position, tower, tower_position):
    king_row, king_col = king_position
    tower_row, tower_col = tower_position

    if king_col > tower_col:
        king_to_position = (king_row, king_col - 2)
        tower_to_position = (tower_row, tower_col + 3)
    else:
        king_to_position = (king_row, king_col + 2)
        tower_to_position = (tower_row, tower_col - 2)

    return SpecialMove([
        Movement(king, king_position, king_to_position),
        Movement(tower, tower_position, tower_to_position)
    ])
