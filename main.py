from screens.main import MainUI
from game import ChessGame


game = ChessGame(id=None, player_white=None, player_black=None)
ui = MainUI(game)

ui.run()
