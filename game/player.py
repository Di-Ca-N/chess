from dataclasses import dataclass
from datetime import datetime
from game import ChessGame

@dataclass
class Player:
    id: int
    username: str
    rating: int

@dataclass
class AnonymousPlayer(Player):
    id: int = 0
    username: str = ''
    rating: int = 0
    
@dataclass
class MatchManager:
    white_player: Player
    black_player: Player

    board: ChessGame
    game_mode: str
    timestamp: int
    time_control: tuple[int, int]
