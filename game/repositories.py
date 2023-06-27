from game.moves import Movement
from .game import ChessGame
from .player import Player

class GameRepository:
    def create_new_game(self, player1: Player, player2: Player) -> ChessGame:
        raise NotImplementedError

    def get_game_by_id(self, id: int) -> ChessGame:
        raise NotImplementedError

class MoveRepository:
    def save_move(self, move: Movement):
        raise NotImplementedError