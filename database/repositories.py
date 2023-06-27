from game.repositories import GameRepository, MoveRepository
from game.player import Player
from game.game import ChessGame
from game.moves import Movement


class InMemoryGameRepository(GameRepository):
    def __init__(self):
        self.games = {}
    
    def create_new_game(self, player1: Player, player2: Player) -> ChessGame:
        game_id = len(self.games)
        self.games[game_id] = ChessGame(game_id, player1, player2)
        return self.games[game_id]
    
    def get_game_by_id(self, id: int) -> ChessGame:
        return self.games[id]
