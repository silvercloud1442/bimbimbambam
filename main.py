import pygame
import random
from pprint import pprint

# Constants
WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128), (0, 255, 0), (255, 0, 0), (255, 165, 0)]
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[5, 5, 0],
     [0, 5, 5]],

    [[0, 6, 0, 0],
     [0, 6, 0, 0],
     [0, 6, 0, 0],
     [0, 6, 0, 0]],

    [[7, 0, 0],
     [7, 7, 7]],

    [[7, 7, 7],
     [7, 0, 0]]
]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Functions
def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

def draw_block(surface, x, y, color):
    pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def new_piece():
    shape = random.choice(SHAPES)
    piece = {
        'shape': shape,
        'color': random.choice(COLORS),
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0
    }
    return piece

def draw_piece(surface, piece):
    shape = piece['shape']
    color = piece['color']
    x = piece['x']
    y = piece['y']
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                draw_block(surface, x + j, y + i, color)

def is_valid_position(board, piece, adj_x=0, adj_y=0):
    shape = piece['shape']
    x = piece['x'] + adj_x
    y = piece['y'] + adj_y
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or board[y + i][x + j]:

                    return False

    return True

def merge_piece(board, piece):
    shape = piece['shape']
    x = piece['x']
    y = piece['y']
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                board[y + i][x + j] = 1
    pprint(board)

def check_lines(board):
    lines_to_clear = []
    for i in range(len(board)):
        if all(board[i]):
            lines_to_clear.append(i)
    for line in lines_to_clear:
        del board[line]
        board.insert(0, [0] * GRID_WIDTH)

def main():
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    piece = new_piece()
    clock = pygame.time.Clock()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_position(board, piece, adj_x=-1):
                        piece['x'] -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_position(board, piece, adj_x=1):
                        piece['x'] += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_position(board, piece, adj_y=1):
                        piece['y'] += 1
                elif event.key == pygame.K_UP:
                    # Rotate piece
                    rotated_shape = [list(reversed(row)) for row in zip(*piece['shape'])]
                    if is_valid_position(board, {'shape': rotated_shape, 'x': piece['x'], 'y': piece['y']}):
                        piece['shape'] = rotated_shape

        if is_valid_position(board, piece, adj_y=1):
            piece['y'] += 1
        else:
            merge_piece(board, piece)
            check_lines(board)
            piece = new_piece()
            if not is_valid_position(board, piece):
                game_over = True

        screen.fill(BLACK)
        draw_grid(screen)
        draw_piece(screen, piece)
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                if val:
                    draw_block(screen, x, y, COLORS[val - 1])
        pygame.display.update()
        clock.tick(3)

    pygame.quit()

if __name__ == "__main__":
    main()
