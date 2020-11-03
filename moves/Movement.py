from .Command import Command


class Movement(Command):
    def __init__(self, piece, from_position, to_position, capture=False, captured_piece=None):
        self.piece = piece
        self.from_position = from_position
        self.to_position = to_position
        self.capture = capture
        self.captured_piece = captured_piece
        self.special = False

    def do(self, board):
        board.do_move(
            self.piece,
            self.from_position,
            self.to_position
        )

    def undo(self, board):
        board.do_move(
            self.piece,
            self.to_position,
            self.from_position
        )

        if self.capture:
            board[self.to_position[0]][self.to_position[1]] = self.captured_piece
