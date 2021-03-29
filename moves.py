from __future__ import annotations

import pieces
import typing

from typing import List, Tuple, Union

if typing.TYPE_CHECKING:
    from board import Board
    from pieces import Piece


def process_move(board: Board, piece: Piece, from_position: Tuple[int, int],
                 to_position: Tuple[int, int], captured_piece: Piece = None) -> 'Movement':
    if Castling.pre_condition(piece, from_position, to_position):
        return Castling(board, from_position, to_position)
    if EnPassant.pre_condition(piece, from_position, to_position, captured_piece):
        return EnPassant(board, piece, from_position, to_position)
    if Promotion.pre_condition(piece, to_position):
        return Promotion(board, piece, from_position, to_position, captured_piece)
    return Movement(board, piece, from_position, to_position, captured_piece)


class Movement:
    def __init__(self, board: Board, piece: Piece, from_position: Tuple[int, int],
                 to_position: Tuple[int, int], captured_piece: Piece = None):
        self.board = board
        self.piece = piece
        self.from_position = from_position
        self.to_position = to_position
        self.capture = captured_piece is not None
        self.captured_piece = captured_piece

        if piece is None:
            return

        self.changes_moved_state = not self.piece.has_moved

        self.notation = self.piece.notation
        if self.capture:
            self.notation += "x"
        self.notation += chr(ord('a') + self.to_position[1]) + str(8 - self.to_position[0])

    def do(self) -> None:
        self.board.move_piece(
            self.piece,
            self.from_position,
            self.to_position
        )

    def undo(self) -> None:
        self.board.move_piece(
            self.piece,
            self.to_position,
            self.from_position
        )

        if self.capture:
            self.board[self.to_position[0]
                       ][self.to_position[1]] = self.captured_piece

        if self.changes_moved_state:
            self.piece.has_moved = False

    def is_valid(self) -> bool:
        if self.piece is None:
            return False

        movement_not_blocked = True
        exists_trajectory = True

        trajectory = self.piece.trajectory(self.from_position, self.to_position)

        if not trajectory:
            exists_trajectory = False

        for intermediate_row, intermediate_col in trajectory:
            intermediary_square = self.board[intermediate_row][intermediate_col]

            piece_exists = intermediary_square is not None
            is_initial_position = (intermediate_row, intermediate_col) == self.from_position
            is_final_position = (intermediate_row, intermediate_col) == self.to_position
            if piece_exists and not is_final_position and not is_initial_position:
                movement_not_blocked = False

        can_move_to = exists_trajectory and movement_not_blocked

        if (can_move_to or isinstance(self.piece, pieces.Pawn)) and self.capture:
            return self.piece.can_capture(self.captured_piece, self.from_position, self.to_position)
        return can_move_to


class ComposedMove(Movement):
    moves = []

    def do(self) -> None:
        for move in self.moves:
            move.do()

    def undo(self) -> None:
        for move in self.moves[::-1]:
            move.undo()

    def is_valid(self) -> bool:
        raise NotImplementedError


class Castling(ComposedMove):
    def __init__(self, board: Board, initial_king_position: Tuple[int, int],
                 target_king_position: Tuple[int, int]):
        king_initial_row, king_initial_col = initial_king_position
        king_target_row, king_target_col = target_king_position

        self.king = board[king_initial_row][king_initial_col]
        self.king_position = initial_king_position

        if king_target_col > king_initial_col:
            rook_initial_row, rook_initial_col = king_target_row, king_target_col + 1
            rook_final_row, rook_final_col = king_target_row, king_target_col - 1
            self.notation = "O-O"
        else:
            rook_initial_row, rook_initial_col = king_target_row, king_target_col - 2
            rook_final_row, rook_final_col = king_target_row, king_target_col + 1
            self.notation = "O-O-O"

        self.rook = board[rook_initial_row][rook_initial_col]
        self.rook_position = (rook_initial_row, rook_initial_col)
        self.final_rook_position = (rook_final_row, rook_final_col)
        self.target_king_position = target_king_position

        self.moves = [
            Movement(board, self.king, self.king_position, self.target_king_position),
            Movement(board, self.rook, self.rook_position, self.final_rook_position)
        ]
        
        super().__init__(board, self.king, self.king_position, target_king_position)
    
    def is_valid(self) -> bool:
        if self.king is None or self.rook is None:
            return False

        have_same_color = self.king.color == self.rook.color
        pieces_have_not_moved = not (self.king.has_moved or self.rook.has_moved)
        are_on_the_same_row = self.king_position[0] == self.rook_position[0]
        
        king_start, king_end = self.king_position[1], self.target_king_position[1]

        if king_start > king_end:
            king_start, king_end = king_end, king_start

        king_path_in_check = False

        for col in range(king_start, king_end + 1):
            if self.board.verify_check((self.king_position[0], col), self.king.color):
                king_path_in_check = True
        
        no_pieces_blocking = True
        total_start, total_end = king_start, self.rook_position[1]

        if total_start > total_end:
            total_start, total_end = total_end, total_start
        for col in range(total_start + 1, total_end):
            if self.board[self.king_position[0]][col] is not None:
                no_pieces_blocking = False
        
        return all([
            have_same_color,
            pieces_have_not_moved,
            are_on_the_same_row,
            not king_path_in_check,
            no_pieces_blocking,
        ])

    @staticmethod
    def pre_condition(piece: Piece, from_position: Tuple[int, int], to_position: Tuple[int, int]) -> bool:
        king_move = isinstance(piece, pieces.King)
        two_squares_to_side = abs(from_position[1] - to_position[1]) == 2
        on_the_same_row = from_position[0] == to_position[0]
        return all([king_move, two_squares_to_side, on_the_same_row])


class EnPassant(Movement):
    def __init__(self, board: Board, piece: Piece, from_position: Tuple[int, int],
                 to_position: Tuple[int, int], captured_piece: Piece = None):
        super().__init__(board, piece, from_position, to_position, captured_piece)
        self.previous_move = self.board.history[-1] if self.board.history else None
        self.captured_piece = self.previous_move.piece if self.previous_move is not None else None

    def do(self) -> None:
        self.board.move_piece(
            self.piece,
            self.from_position,
            self.to_position
        )
        capture_position_row, capture_position_col = self.previous_move.to_position
        self.board[capture_position_row][capture_position_col] = None

    def undo(self) -> None:
        self.board.move_piece(
            self.piece,
            self.to_position,
            self.from_position
        )
        capture_position_row, capture_position_col = self.previous_move.to_position
        self.board[capture_position_row][capture_position_col] = self.captured_piece

    def is_valid(self) -> bool:
        if self.piece is None or self.captured_piece is None:
            return False

        is_a_pawn_move = isinstance(self.piece, pieces.Pawn)
        captured_piece_is_a_pawn = isinstance(self.captured_piece, pieces.Pawn)
        pieces_with_opposite_colors = self.captured_piece.color != self.piece.color
        captured_pawn_moved_two_squares = abs(self.previous_move.to_position[0] - self.previous_move.from_position[0]) == 2
        pieces_on_the_same_row = self.previous_move.to_position[0] == self.from_position[0]
        pieces_will_end_on_same_col = self.to_position[1] == self.previous_move.from_position[1]
        pieces_on_adjacent_cols = abs(self.previous_move.to_position[1] - self.from_position[1]) == 1

        return all([
            is_a_pawn_move,
            captured_piece_is_a_pawn,
            pieces_with_opposite_colors,
            captured_pawn_moved_two_squares,
            pieces_on_the_same_row,
            pieces_will_end_on_same_col,
            pieces_on_adjacent_cols
        ])

    @staticmethod
    def pre_condition(piece: 'Piece', from_position: 'Tuple[int, int]', to_position: 'Tuple[int, int]',
                      captured_piece: 'Piece') -> bool:
        return isinstance(piece, pieces.Pawn) and (
            abs(from_position[0] - to_position[0]) == 1 and
            abs(from_position[1] - to_position[1]) == 1
        ) and captured_piece is None


class Promotion(Movement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.promotes_to = None

    def do(self) -> None:
        super().do()
        to_row, to_col = self.to_position
        self.board[to_row][to_col] = self.promotes_to(
            color=self.piece.color, has_moved=True
        )

    @staticmethod
    def pre_condition(piece: 'Piece', to_position: 'Tuple[int, int]') -> bool:
        if piece is None:
            return False
        is_pawn = isinstance(piece, pieces.Pawn)
        last_row = 0 if piece.color == pieces.Colors.WHITE else 7
        going_to_last_row = to_position[0] == last_row

        return is_pawn and going_to_last_row
