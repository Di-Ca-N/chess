from screens.main import MainUI
from game import ChessGame


game = ChessGame()
ui = MainUI(game)

ui.run()
