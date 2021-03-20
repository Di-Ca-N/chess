import pygame
from board import Board

PIECE_SPRITE_SIZE = 60
SQUARE_SIZE = 64
PIECE_OFFSET = (SQUARE_SIZE - PIECE_SPRITE_SIZE) // 2

class Game:
    background = pygame.image.load("./images/chessboard.png")

    def __init__(self):
        self.board = Board()

        self.screen = None
        self.dragging = False
        self.dragging_from = (None, None)
        self.mouse_position = (0, 0)

        self.handlers = {
            pygame.MOUSEBUTTONDOWN: self.handle_mouse_down,
            pygame.MOUSEMOTION: self.handle_mouse_move,
            pygame.MOUSEBUTTONUP: self.handle_mouse_up,
            pygame.KEYUP: self.handle_keyboard,
        }

    def run(self):
        pygame.init()
        pygame.display.set_caption("Chess Game")
        self.screen = pygame.display.set_mode((512, 512))

        while True:
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                self.handle_event(event)

    def update(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        for x in range(8):
            for y in range(8):
                piece = self.board[y][x]

                if piece is not None and (x, y) != self.dragging_from:
                    piece_image = piece.get_image()
                    piece_position = (x * SQUARE_SIZE + PIECE_OFFSET, y * SQUARE_SIZE + PIECE_OFFSET)
                    self.screen.blit(piece_image, piece_position)

        if self.dragging:
            x, y = self.dragging_from
            if self.board[y][x] is not None:
                image = self.board[y][x].get_image()
                real_blit_position = (
                    self.mouse_position[0] - PIECE_SPRITE_SIZE // 2,
                    self.mouse_position[1] - PIECE_SPRITE_SIZE // 2
                )
                self.screen.blit(image, real_blit_position)
        pygame.display.update()

    def handle_event(self, event):
        handler = self.handlers.get(event.type)
        if handler is not None:
            handler(event)

    def handle_mouse_down(self, event):
        self.mouse_position = pygame.mouse.get_pos()
        self.dragging = True
        self.dragging_from = self._get_board_position(self.mouse_position)

    def handle_mouse_move(self, event):
        self.mouse_position = pygame.mouse.get_pos()

    def handle_mouse_up(self, event):
        self.mouse_position = pygame.mouse.get_pos()

        old_x, old_y = self.dragging_from
        new_x, new_y = self._get_board_position(self.mouse_position)
        self.board.move_piece((old_y, old_x), (new_y, new_x))

        self.dragging = False
        self.dragging_from = (None, None)

    def _get_board_position(self, position):
        return (position[0] // SQUARE_SIZE, position[1] // SQUARE_SIZE)

    def handle_keyboard(self, event):
        if event.key == ord('u'):
            self.board.undo_move()
        if event.key == ord('n'):
            self.board.new_game()


if __name__ == "__main__":
    game = Game()
    game.run()
