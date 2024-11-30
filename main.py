import pygame
import sys
import os

pygame.init()

WINDOW_SIZE = 640  # Rozmiar okna (400x400 pikseli)
SIZE = 8
CELL_SIZE = WINDOW_SIZE // SIZE  # Rozmiar jednego pola

WHITE = (240, 240, 240)
BLACK = (0, 40, 0)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Szachownica")
folder_path = os.path.join(os.path.dirname(__file__),'pieces')
piece = pygame.image.load(os.path.join(folder_path,'Chess_nlt60.png'))

def draw_chessboard():
    for row in range(SIZE):
        for col in range(SIZE):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_chessboard()
        screen.blit(piece, (90, 90))
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()