from game.player import Player
from game.repositories import GameRepository


def create_new_game(repo: GameRepository, player_white: Player, player_black: Player):
    return repo.create_new_game(player_white, player_black)

def make_move(repo: GameRepository, game_id: int, origin: tuple[int, int], target: tuple[int, int]):
    game = repo.get_game_by_id(game_id)
    move = game.process_move(origin, target)
    
    return move