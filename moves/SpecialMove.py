from .Command import Command


class SpecialMove(Command):
    def __init__(self, moves):
        self.moves = moves

    def do(self, board):
        for move in self.moves:
            move.do(board)

    def undo(self, board):
        for move in self.moves[::-1]:
            move.undo(board)
