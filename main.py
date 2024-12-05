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

def draw_possible_moves(possible_moves):
    for row in range(SIZE):
        for col in range(SIZE):
            if (col, row) in possible_moves:
                pygame.draw.rect(screen, (48,183,44), (row*CELL_SIZE, col*CELL_SIZE, 60, 60), 6)

def initialize_board():
    board = [[None for _ in range(SIZE)] for _ in range(SIZE)]
    main_color = "white"
    secondary_color = "black"
    if BOARD_TYPE != "W":
        main_color = "black"
        secondary_color = "white"
    board[7] = [
        Rook(7, 0, main_color), Knight(7, 1, main_color), Bishop(7, 2, main_color),
        Queen(7, 3, main_color), King(7, 4, main_color), Bishop(7, 5, main_color),
        Knight(7, 6, main_color), Rook(7, 7, main_color)
    ]
    board[6] = [Pawn(6, col, main_color) for col in range(SIZE)]

    board[0] = [
        Rook(0, 0, secondary_color), Knight(0, 1, secondary_color), Bishop(0, 2, secondary_color),
        Queen(0, 3, secondary_color), King(0, 4, secondary_color), Bishop(0, 5, secondary_color),
        Knight(0, 6, secondary_color), Rook(0, 7, secondary_color)
    ]
    board[1] = [Pawn(1, col, secondary_color) for col in range(SIZE)]

    return board

def check_possible_moves(board, piece):
    possible_moves = []
    row, col = piece.row, piece.column
    if piece.sign == "p":
        if (piece.color == "white" and BOARD_TYPE == "W") or (piece.color == "black" and BOARD_TYPE != "W"):
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1
        if 0 <= row + direction < SIZE and board[row + direction][col] is None:
            possible_moves.append((row + direction, col))
        if row == start_row and board[row + direction][col] is None and board[row + 2 * direction][col] is None:
            possible_moves.append((row + 2 * direction, col))
        for dc in [-1, 1]:
            if (
                    0 <= row + direction < SIZE
                    and 0 <= col + dc < SIZE
                    and board[row + direction][col + dc] is not None
                    and board[row + direction][col + dc].color != piece.color
            ):
                possible_moves.append((row + direction, col + dc))


    elif piece.sign == "r":
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for dist in range(1, SIZE):
                nr, nc = row + dr * dist, col + dc * dist
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if board[nr][nc] is None:
                        possible_moves.append((nr, nc))
                    elif board[nr][nc].color != piece.color:
                        possible_moves.append((nr, nc))
                        break
                    else:
                        break
                else:
                    break

    elif piece.sign == "k":
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                if board[nr][nc] is None or board[nr][nc].color != piece.color:
                    possible_moves.append((nr, nc))

    elif piece.sign == "b":
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for dist in range(1, SIZE):
                nr, nc = row + dr * dist, col + dc * dist
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if board[nr][nc] is None:
                        possible_moves.append((nr, nc))
                    elif board[nr][nc].color != piece.color:
                        possible_moves.append((nr, nc))
                        break
                    else:
                        break
                else:
                    break

    elif piece.sign == "q":
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for dist in range(1, SIZE):
                nr, nc = row + dr * dist, col + dc * dist
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if board[nr][nc] is None:
                        possible_moves.append((nr, nc))
                    elif board[nr][nc].color != piece.color:
                        possible_moves.append((nr, nc))
                        break
                    else:
                        break
                else:
                    break

    elif piece.sign == "K":
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in king_moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                if board[nr][nc] is None or board[nr][nc].color != piece.color:
                    possible_moves.append((nr, nc))

    print(f"Possible moves for {piece.sign} at ({row}, {col}): {possible_moves}")
    return possible_moves


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
    possible_moves = []

    while running:
        draw_chessboard()

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
                        possible_moves = check_possible_moves(board, dragging_piece)
                        board[row][col] = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging_piece:
                        row, col = get_square_under_mouse()
                        if 0 <= row < SIZE and 0 <= col < SIZE:
                            if (board[row][col] is None or board[row][col].color != dragging_piece.color) and (row,col) in possible_moves:
                                dragging_piece.row, dragging_piece.column = row, col
                                board[row][col] = dragging_piece
                            else:
                                start_row, start_col = dragging_start_pos
                                board[start_row][start_col] = dragging_piece
                        else:
                            start_row, start_col = dragging_start_pos
                            board[start_row][start_col] = dragging_piece
                        possible_moves = []
                        dragging_piece = None
            elif event.type == pygame.MOUSEMOTION and dragging_piece:
                dragging_piece_pos = pygame.mouse.get_pos()
        draw_pieces(board)
        if dragging_piece:
            mouse_x, mouse_y = dragging_piece_pos
            piece_key = f"{dragging_piece.sign}_{dragging_piece.color[0]}"
            draw_possible_moves(possible_moves)
            screen.blit(pieces_images[piece_key], (mouse_x - CELL_SIZE // 2, mouse_y - CELL_SIZE // 2))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
