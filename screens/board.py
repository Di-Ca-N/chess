import pygame
from game import pieces
from game.moves import Promotion

from .screen_transition import ScreenTransition

PIECE_SPRITE_SIZE = 60
SQUARE_SIZE = 64
PIECE_OFFSET = (SQUARE_SIZE - PIECE_SPRITE_SIZE) // 2


class Board:
    background = pygame.image.load("./assets/images/chessboard.png")

    def __init__(self, game):
        self.board = game

        self.dragging = False
        self.dragging_from = (None, None)

        self.handlers = {
            pygame.MOUSEBUTTONDOWN: self.handle_mouse_down,
            pygame.MOUSEBUTTONUP: self.handle_mouse_up,
            pygame.KEYUP: self.handle_keyboard,
        }

        self.piece_images = {
            piece.get_image_path(): pygame.image.load(piece.get_image_path())
            for _, piece in self.board
            if piece is not None
        }

    def update(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background, (0, 0))

        for (y, x), piece in self.board:
            if piece is None:
                continue

            if (y, x) == self.dragging_from:
                continue

            piece_image = self.piece_images[piece.get_image_path()]
            piece_position = (
                x * SQUARE_SIZE + PIECE_OFFSET,
                y * SQUARE_SIZE + PIECE_OFFSET,
            )
            surface.blit(piece_image, piece_position)

        if self.dragging:
            piece = self.board[self.dragging_from]
            if piece is not None:
                image = self.piece_images[piece.get_image_path()]
                mouse_position = pygame.mouse.get_pos()
                real_blit_position = (
                    mouse_position[0] - PIECE_SPRITE_SIZE // 2,
                    mouse_position[1] - PIECE_SPRITE_SIZE // 2,
                )
                surface.blit(image, real_blit_position)

    def handle_event(self, event) -> ScreenTransition | None:
        handler = self.handlers.get(event.type)
        if handler is not None:
            return handler(event)

    def handle_mouse_down(self, event) -> None:
        self.dragging = True
        self.dragging_from = self.get_hovered_square()

    def handle_mouse_up(self, event) -> None:
        if not self.dragging:
            return

        target_position = self.get_hovered_square()
        move = self.board.process_move(self.dragging_from, target_position)

        if isinstance(move, Promotion) and move.is_valid():
            promotes_to = PromotionOverlay(move.piece.color, *target_position).get()
            move.promotes_to = promotes_to

        self.board.make_move(move)
        self.dragging = False
        self.dragging_from = (None, None)

    def get_hovered_square(self):
        position = pygame.mouse.get_pos()
        return (position[1] // SQUARE_SIZE, position[0] // SQUARE_SIZE)

    def handle_keyboard(self, event):
        if event.key == ord("u"):
            self.board.undo_move()
        elif event.key == ord("n"):
            self.board.new_game()
        elif pygame.K_ESCAPE:
            return ScreenTransition("game", "menu")


class PromotionOverlay:
    def __init__(self, piece_color, position):
        y, x = position
        self.x = x
        self.y = y
        self.piece_color = piece_color

        if piece_color == pieces.Color.WHITE:
            self.menu_cooords = (x * SQUARE_SIZE, y * SQUARE_SIZE)
        else:
            self.menu_cooords = (x * SQUARE_SIZE, (y - 3) * SQUARE_SIZE)

        self.overlay = pygame.Surface((512, 512))
        self.overlay.set_alpha(64)
        self.overlay.fill((0, 0, 0))

        self.menu = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE * 4), pygame.SRCALPHA)
        self.menu.fill((200, 200, 200, 255))
        self.menu_items = dict(
            enumerate(
                (
                    ("queen", pieces.Queen),
                    ("knight", pieces.Knight),
                    ("rook", pieces.Rook),
                    ("bishop", pieces.Bishop),
                )
            )
        )

        for index, (piece_name, _) in self.menu_items.items():
            self.menu.blit(
                pygame.image.load(
                    f"assets/images/{piece_color.name.lower()}/{piece_name}.png"
                ),
                (PIECE_OFFSET, PIECE_OFFSET + SQUARE_SIZE * index),
            )

    def get(self):
        screen = pygame.display.get_surface()
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.menu, self.menu_cooords)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    item_x, item_y = x // SQUARE_SIZE, y // SQUARE_SIZE

                    if item_x == self.x:
                        item_y = (
                            item_y
                            if self.piece_color == pieces.Color.WHITE
                            else (item_y + 4) % 4
                        )
                        if item_y < 4:
                            return self.menu_items[item_y][1]

            pygame.display.update()
