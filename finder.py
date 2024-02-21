from copy import deepcopy
from pprint import pprint


# Function to rotate a Tetris figure clockwise
def rotate_clockwise(figure):
    return [list(row) for row in zip(*figure[::-1])]

# Function to check if a position is valid
def is_valid_position(glass, figure, row, col):
    glass_height = len(glass)
    glass_width = len(glass[0])
    figure_height = len(figure)
    figure_width = len(figure[0])

    # Check if the figure exceeds the bounds of the glass
    if row + figure_height > glass_height or col + figure_width > glass_width:
        return False

    # Check if the figure collides with filled fields in the glass
    for i in range(figure_height):
        for j in range(figure_width):
            if figure[i][j] == 1:
                if row + i >= glass_height or col + j >= glass_width or glass[row + i][col + j] == 1:
                    return False
                # Check if there is any filled field below the figure
                for k in range(row + i, 1, -1):
                    if glass[k][col + j] == 1:
                        return False
    return True

# Function to generate all possible positions for placing a Tetris figure
def generate_possible_positions(glass, figure):
    possible_positions = []
    c = len(glass) - 4
    for idx, row in enumerate(glass):
        if 1 in row:
            c = idx - 4
            break
    c = c if c >= 0 else 0
    for row in range(c, len(glass)):
        for col in range(len(glass[0])):
            for rotation in range(4):
                rotated_figure = figure
                for _ in range(rotation):
                    rotated_figure = rotate_clockwise(rotated_figure)
                if is_valid_position(glass, rotated_figure, row, col):
                    possible_positions.append((row, col, rotated_figure))
    return possible_positions

# Function to display the final position of a Tetris figure in the glass
def return_final_position(glass, row, col, figure):
    for i in range(len(figure)):
        for j in range(len(figure[0])):
            if figure[i][j] == 1:
                glass[row + i][col + j] = 2
    out = []
    for row in glass:
        out.append(row)
    return out

def calculate_height(glass):
    c = 0
    for idx, row in enumerate(glass):
        if 2 in row:
            c = idx
            break
    return len(glass) - c

# Function to count the empty cells from the top to the bottom of a column in the glass
def count_empty_cells(glass):
    empty_count = 0
    count = False
    for row in glass:
        if (1 in row or 2 in row) and not count:
            count = True
            continue
        if count:
            empty_count += row.count(0)
    return empty_count

def count_kotls(glass):
    # kotls = 0
    # l_c = 0
    # m_c = 0
    # r_c = 0
    # for row in glass:
    #     s_row = ''.join(map(str, row))
    #     if s_row[:2] == '01' or s_row[:2] == '02':
    #         l_c += 1
    #         if l_c == 3:
    #             l_c = 0
    #             kotls += 1
    #     else:
    #         l_c = 0
    #     if '101' in s_row or '202' in s_row:
    #         m_c += 1
    #         if m_c == 3:
    #             m_c = 0
    #             kotls += 1
    #     else:
    #         m_c = 0
    #     if s_row[:2] == '10' or s_row[:2] == '20':
    #         r_c += 1
    #         if r_c == 3:
    #             r_c = 0
    #             kotls += 1
    #     else:
    #         r_c = 0
    # return kotls
    count = 0
    for col in range(len(glass[0])):
        for row in range(len(glass) - 3):  # Ensure at least 4 rows left
            if all(glass[row + i][col] == 0 for i in range(4)):
                # Check if the column is surrounded by '1' or the edge
                if (col == 0 or all(glass[row + i][col - 1] == 1 for i in range(4))) and \
                        (col == len(glass[0]) - 1 or all(glass[row + i][col + 1] == 1 for i in range(4))):
                    count += 1
    return count

def below_zeros(glass):
    np_glass = [i for i in list(map(list, zip(*glass))) if 0 in i]
    zeros = 0
    for row in np_glass:
        if 1 in row or 2 in row:
            new_row = map(str, row)
            closed = False
            for i in new_row:
                if i == '1' or i == '2':
                    closed = True
                if closed and i == '0':
                    zeros += 1
    return zeros

def burn(glass):
    c = 0
    for row in glass:
        if 0 not in row:
            c += 1
    return c

def height_dif(glass):
    f = False
    top = 0
    bot = 0
    for idx, row in enumerate(glass):
        if 1 in row:
            top = len(glass) - idx
            break
    for idx, row in enumerate(glass):
        if 0 in row:
            bot = len(glass) - idx
    return top - bot

# Example usage
if __name__ == "__main__":

    glass = [[0] * 10 for _ in range(20)]

    tetris_figures = [[[1],
                      [1],
                      [1],
                      [1]]]
    # Iterate over all Tetris figures
    figs = {}
    for figure in tetris_figures:
        possible_positions = generate_possible_positions(glass, figure)
        print("Possible positions for figure:")
        for position in possible_positions:
            # print(position)
            new_pos = return_final_position(deepcopy(glass), *position)
            # pprint(new_pos)
            tax = calculate_height(new_pos) + count_empty_cells(new_pos)
            pprint(new_pos)
            print(tax)
    #         try:
    #             figs[tax].append((position, new_pos))
    #         except:
    #             figs[tax] = []
    #             figs[tax].append((position, new_pos))
    # best_score = sorted(figs.keys())[0]
    # pos = figs[best_score][0][1]
    # pprint(pos)
    # print(figs[best_score][0][0])