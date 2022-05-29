import pygame
import pieces
from board import Board
from moves import Promotion


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

        self.piece_images = {
            piece.get_image(): pygame.image.load(piece.get_image()) 
            for _, piece in self.board 
            if piece is not None
        }

    def run(self):
        pygame.init()
        pygame.display.set_caption("Chess Game")
        self.screen = pygame.display.set_mode((512, 512))

        try:
            while True:
                self.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    self.handle_event(event)
        except pygame.error as e:
            print(e)

    def update(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        for (y, x), piece in self.board:
            if piece is None:
                continue

            if (x, y) == self.dragging_from:
                continue

            piece_image = self.piece_images[piece.get_image()]
            piece_position = (x * SQUARE_SIZE + PIECE_OFFSET, y * SQUARE_SIZE + PIECE_OFFSET)
            self.screen.blit(piece_image, piece_position)

        if self.dragging:
            x, y = self.dragging_from
            piece = self.board[y, x]
            if piece is not None:
                image = pygame.image.load(piece.get_image())
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
        if not self.dragging:
            return
        self.mouse_position = pygame.mouse.get_pos()

        old_x, old_y = self.dragging_from
        new_x, new_y = self._get_board_position(self.mouse_position)
        move = self.board.process_move((old_y, old_x), (new_y, new_x))

        if isinstance(move, Promotion) and move.is_valid():
            promotes_to = PromotionOverlay(self.screen, move.piece.color, new_x, new_y).get()
            move.promotes_to = promotes_to

        self.board.make_move(move)
        self.dragging = False
        self.dragging_from = (None, None)

    def _get_board_position(self, position):
        return (position[0] // SQUARE_SIZE, position[1] // SQUARE_SIZE)

    def handle_keyboard(self, event):
        if event.key == ord('u'):
            self.board.undo_move()
        elif event.key == ord('n'):
            self.board.new_game()


class PromotionOverlay:
    def __init__(self, screen, piece_color, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.piece_color = piece_color

        if piece_color == pieces.Colors.WHITE:
            self.menu_cooords = (x * SQUARE_SIZE, y * SQUARE_SIZE)
        else:
            self.menu_cooords = (x * SQUARE_SIZE, (y - 3) * SQUARE_SIZE)

        self.overlay = pygame.Surface((512, 512))
        self.overlay.set_alpha(64)
        self.overlay.fill((0, 0, 0))

        self.menu = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE * 4), pygame.SRCALPHA)
        self.menu.fill((200, 200, 200, 255))
        self.menu_items = dict(
            enumerate((
                ('queen', pieces.Queen), 
                ('knight', pieces.Knight),
                ('rook', pieces.Rook),
                ('bishop', pieces.Bishop)
            )
        ))

        for index, (piece_name, _) in self.menu_items.items():
            self.menu.blit(
                pygame.image.load(f"images/{piece_color.name.lower()}/{piece_name}.png"), 
                (PIECE_OFFSET, PIECE_OFFSET + SQUARE_SIZE * index)
            )

    def get(self):
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.menu, self.menu_cooords)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    item_x, item_y = x // SQUARE_SIZE, y // SQUARE_SIZE

                    if item_x == self.x:
                        item_y = item_y if self.piece_color == pieces.Colors.WHITE else (item_y + 4) % 4
                        if item_y < 4:
                            return self.menu_items[item_y][1]
                            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        pass
