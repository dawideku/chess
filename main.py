import pygame
import sys
import os
from chess_objects import Rook, Knight, Bishop, Queen, King, Pawn

pygame.init()

WINDOW_SIZE = 480  # Rozmiar okna
SIZE = 8
CELL_SIZE = WINDOW_SIZE // SIZE  # Rozmiar jednego pola
BOARD_TYPE = "W"

# Kolory pól szachownicy
WHITE = (240, 240, 240)
BLACK = (0, 40, 0)

# Tworzenie ekranu
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Szachownica")

# Folder z obrazkami figur
folder_path = os.path.join(os.path.dirname(__file__), 'pieces')

# Ładowanie obrazków figur
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


def main():
    board = initialize_board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_chessboard()
        draw_pieces(board)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
