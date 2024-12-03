import pygame
import sys
import os
from chess_objects import Rook, Knight, Bishop, Queen, King, Pawn

pygame.init()

WINDOW_SIZE = 480
SIZE = 8
CELL_SIZE = WINDOW_SIZE // SIZE
BOARD_TYPE = "W"

WHITE = (240, 240, 240)
BLACK = (0, 40, 0)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Szachownica")

folder_path = os.path.join(os.path.dirname(__file__), 'pieces')

pieces_images = {
    "r_w": pygame.image.load(os.path.join(folder_path, "rook_w.png")),
    "k_w": pygame.image.load(os.path.join(folder_path, "knight_w.png")),
    "b_w": pygame.image.load(os.path.join(folder_path, "bishop_w.png")),
    "q_w": pygame.image.load(os.path.join(folder_path, "queen_w.png")),
    "K_w": pygame.image.load(os.path.join(folder_path, "king_w.png")),
    "p_w": pygame.image.load(os.path.join(folder_path, "pawn_w.png")),
    "r_b": pygame.image.load(os.path.join(folder_path, "rook_b.png")),
    "k_b": pygame.image.load(os.path.join(folder_path, "knight_b.png")),
    "b_b": pygame.image.load(os.path.join(folder_path, "bishop_b.png")),
    "q_b": pygame.image.load(os.path.join(folder_path, "queen_b.png")),
    "K_b": pygame.image.load(os.path.join(folder_path, "king_b.png")),
    "p_b": pygame.image.load(os.path.join(folder_path, "pawn_b.png")),
}


def draw_chessboard():
    for row in range(SIZE):
        for col in range(SIZE):
            if BOARD_TYPE == "W":
                color = WHITE if (row + col) % 2 == 0 else BLACK
            else:
                color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def initialize_board():
    board = [[None for _ in range(SIZE)] for _ in range(SIZE)]
    main_color = "white"
    secondary_color = "black"
    if BOARD_TYPE != "W":
        main_color = "black"
        secondary_color = "white"
    board[7] = [
        Rook(0, 0, main_color), Knight(0, 1, main_color), Bishop(0, 2, main_color),
        Queen(0, 3, main_color), King(0, 4, main_color), Bishop(0, 5, main_color),
        Knight(0, 6, main_color), Rook(0, 7, main_color)
    ]
    board[6] = [Pawn(1, col, main_color) for col in range(SIZE)]

    board[0] = [
        Rook(7, 0, secondary_color), Knight(7, 1, secondary_color), Bishop(7, 2, secondary_color),
        Queen(7, 3, secondary_color), King(7, 4, secondary_color), Bishop(7, 5, secondary_color),
        Knight(7, 6, secondary_color), Rook(7, 7, secondary_color)
    ]
    board[1] = [Pawn(6, col, secondary_color) for col in range(SIZE)]

    return board

def draw_pieces(board):
    for row in range(SIZE):
        for col in range(SIZE):
            piece = board[row][col]
            if piece:
                piece_key = f"{piece.sign}_{piece.color[0]}"
                if piece_key in pieces_images:
                    screen.blit(pieces_images[piece_key], (col * CELL_SIZE, row * CELL_SIZE))

def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // CELL_SIZE
    col = mouse_x // CELL_SIZE
    return row, col


def main():
    board = initialize_board()
    running = True
    dragging_piece = None
    dragging_piece_pos = (0, 0)

    while running:
        draw_chessboard()
        draw_pieces(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    row, col = get_square_under_mouse()
                    if board[row][col]:
                        dragging_piece = board[row][col]
                        dragging_start_pos = (row, col)
                        dragging_piece_pos = pygame.mouse.get_pos()
                        board[row][col] = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging_piece:
                        row, col = get_square_under_mouse()
                        dragging_piece.row, dragging_piece.column = row, col
                        board[row][col] = dragging_piece
                        dragging_piece = None
            elif event.type == pygame.MOUSEMOTION and dragging_piece:
                dragging_piece_pos = pygame.mouse.get_pos()

        if dragging_piece:
            mouse_x, mouse_y = dragging_piece_pos
            piece_key = f"{dragging_piece.sign}_{dragging_piece.color[0]}"
            screen.blit(pieces_images[piece_key], (mouse_x - CELL_SIZE // 2, mouse_y - CELL_SIZE // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
