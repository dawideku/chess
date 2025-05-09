import pygame
import sys
import os
import chess

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
    'R': pygame.image.load(os.path.join(folder_path, "rook_w.png")),
    'N': pygame.image.load(os.path.join(folder_path, "knight_w.png")),
    'B': pygame.image.load(os.path.join(folder_path, "bishop_w.png")),
    'Q': pygame.image.load(os.path.join(folder_path, "queen_w.png")),
    'K': pygame.image.load(os.path.join(folder_path, "king_w.png")),
    'P': pygame.image.load(os.path.join(folder_path, "pawn_w.png")),
    'r': pygame.image.load(os.path.join(folder_path, "rook_b.png")),
    'n': pygame.image.load(os.path.join(folder_path, "knight_b.png")),
    'b': pygame.image.load(os.path.join(folder_path, "bishop_b.png")),
    'q': pygame.image.load(os.path.join(folder_path, "queen_b.png")),
    'k': pygame.image.load(os.path.join(folder_path, "king_b.png")),
    'p': pygame.image.load(os.path.join(folder_path, "pawn_b.png")),
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
            drawing_square = get_square(row, col)
            if drawing_square in possible_moves:
                pygame.draw.rect(screen, (48,183,44), (col*CELL_SIZE, row*CELL_SIZE, 60, 60), 6)

def get_legal_moves_for_piece(board, square):
    piece = board.piece_at(square)

    if piece is None or piece.color != board.turn:
        return []

    legal_moves = [
        move for move in board.legal_moves
        if move.from_square == square
    ]
    return legal_moves

def get_square(row, col):
    return 56 - (row * 8) + col


def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            square = get_square(row, col)
            piece = board.piece_at(square)
            if piece is not None:
                piece_key = piece.symbol()
                if piece_key in pieces_images:
                    screen.blit(pieces_images[piece_key], (col * CELL_SIZE, row * CELL_SIZE))

def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // CELL_SIZE
    col = mouse_x // CELL_SIZE
    return row, col

def main():
    board = chess.Board()
    running = True
    dragging_piece = None
    dragging_piece_pos = (0, 0)
    dragging_piece_key = None
    dragging_piece_square = None
    possible_moves = []

    while running:
        draw_chessboard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    row, col = get_square_under_mouse()
                    if board.piece_at(get_square(row, col)):
                        dragging_piece = True
                        dragging_piece_pos = pygame.mouse.get_pos()
                        row, col = get_square_under_mouse()
                        piece = board.piece_at(get_square(row, col))
                        dragging_piece_square = get_square(row, col)
                        dragging_piece_key = piece.symbol()
                        moves = get_legal_moves_for_piece(board, get_square(row, col))
                        possible_moves = [move.to_square for move in moves]
                        print(possible_moves)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging_piece:
                        row, col = get_square_under_mouse()
                        new_square = get_square(row, col)
                        if 0 <= row < SIZE and 0 <= col < SIZE:
                            if new_square in possible_moves:
                                piece = chess.Piece.from_symbol(dragging_piece_key)
                                board.set_piece_at(new_square, piece)
                                print(board)
                                board.turn = not board.turn
                            else:
                                piece = chess.Piece.from_symbol(dragging_piece_key)
                                board.set_piece_at(dragging_piece_square, piece)
                        else:
                            piece = chess.Piece.from_symbol(dragging_piece_key)
                            board.set_piece_at(dragging_piece_square, piece)
                        possible_moves = []
                        dragging_piece = None
            elif event.type == pygame.MOUSEMOTION and dragging_piece:
                dragging_piece_pos = pygame.mouse.get_pos()
        draw_pieces(board)
        if dragging_piece:
            draw_possible_moves(possible_moves)
            mouse_x, mouse_y = dragging_piece_pos
            piece_key = dragging_piece_key
            board.remove_piece_at(dragging_piece_square)
            screen.blit(pieces_images[piece_key], (mouse_x - CELL_SIZE // 2, mouse_y - CELL_SIZE // 2))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
