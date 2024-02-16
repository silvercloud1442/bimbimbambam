import pygame
import random
from finder import *
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

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 0]]
]
#
# # Initialize pygame
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Tetris")

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
        'x': 0,
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

def check_lines(board):
    score = 0
    lines_to_clear = []
    for i in range(len(board)):
        if all(board[i]):
            lines_to_clear.append(i)
    for line in lines_to_clear:
        del board[line]
        score += 100
        board.insert(0, [0] * GRID_WIDTH)
    return score

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

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
        clock.tick(15)

    pygame.quit()

def get_best_pos(board, piece, n):
    possible_positions = generate_possible_positions(board, piece)
    bz, em_c, brn, hg, ktl, phg = n
    figs = {}
    for position in possible_positions:
        new_pos = return_final_position(deepcopy(board), *position)
        tax =  (
               (bz * below_zeros(new_pos)) +
               (em_c * count_empty_cells(new_pos)) -
               (brn * burn(new_pos)) +
               (hg * calculate_height(new_pos)) +
               (ktl * count_kotls(new_pos)) +
               (phg * place_height(new_pos))
                )
        try:
            figs[tax].append((position))
        except:
            figs[tax] = []
            figs[tax].append((position))
    best_score = sorted(figs.keys())[0]
    pos = figs[best_score][0]
    return pos


def al(n):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    score = 0

    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    piece = new_piece()
    row_num, col_num, rotate_pos = get_best_pos(board, piece['shape'], n)

    clock = pygame.time.Clock()
    game_over = False
    c = 0
    while not game_over:
        if piece['shape'] != rotate_pos:
            rotated_shape = [list(reversed(row)) for row in zip(*piece['shape'])]
            if is_valid_position(board, {'shape': rotated_shape, 'x': piece['x'], 'y': piece['y']}):
                piece['shape'] = rotated_shape
        else:
            if piece['x'] < col_num:
                if is_valid_position(board, piece, adj_x=1):
                    piece['x'] += 1

        if c == 2:
            if is_valid_position(board, piece, adj_y=1):
                piece['y'] += 1
            else:
                merge_piece(board, piece)
                score += check_lines(board)
                piece = new_piece()
                row_num, col_num, rotate_pos = get_best_pos(board, piece['shape'], n)
                if not is_valid_position(board, piece):
                    game_over = True
            c = 0

        screen.fill(BLACK)
        draw_grid(screen)
        draw_piece(screen, piece)
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                if val:
                    draw_block(screen, x, y, COLORS[val - 1])
        pygame.display.update()
        clock.tick(1000)
        c += 1
    pygame.quit()
    return score


def generate_individual(n=[random.uniform(0, 10) for _ in range(5)]):
    # Генерация случайной комбинации входных данных
    return n


def crossover(parent1, parent2):
    # Одноточечное скрещивание
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def mutate(individual, mutation_rate=0.1):
    # Мутация с некоторой вероятностью
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.uniform(0, 10)
    return individual


def _evo_():
    population_size = 10
    num_generations = 100

    # Инициализация начальной популяции
    population = [generate_individual([2.21, 4, 4.7, 9.13, 6.44, 3]) for _ in range(population_size)]

    for generation in range(num_generations):
        # Оценка пригодности популяции
        fitness_scores = [al(individual) for individual in population]

        # Выбор родителей для скрещивания
        parents = random.choices(population, weights=fitness_scores, k=population_size)

        # Создание нового поколения
        next_generation = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(parents, 2)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            next_generation.extend([mutate(child1), mutate(child2)])

        # Замена текущей популяции на новое поколение
        population = next_generation
        print(generation, population[0])

    # Находим лучший индивид в конечной популяции
    best_individual = max(population, key=al)
    best_score = al(best_individual)
    [8.086109650556615, 1.4011185321924224, 8.787523056243622, 1.6451242696550206, 4.961335274398152, 2.5003765546244026]
    print("Best individual:", best_individual)
    print("Best score:", best_score)

if __name__ == '__main__':
    n = [2.21, 4, 4.7, 9.13, 6.44, 3]
    _evo_()