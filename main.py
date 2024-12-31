from itertools import product
from copy import deepcopy
import pygame

#board = [
#        6, 0, 0, 1, 0, 0, 0, 0, 2,
#        8, 0, 1, 0, 9, 0, 0, 0, 0,
#        0, 7, 5, 0, 8, 4, 0, 0, 0,
#        4, 3, 0, 0, 2, 0, 5, 6, 1,
#        5, 1, 8, 7, 0, 0, 4, 0, 9,
#        0, 9, 6, 4, 1, 0, 3, 0, 0,
#        0, 0, 0, 0, 7, 0, 0, 0, 0,
#        0, 6, 0, 0, 3, 1, 0, 5, 0,
#        7, 0, 2, 5, 4, 0, 6, 0, 3,
#    ]

board = [0, 3, 0, 2, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 5, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 7, 0, 0, 1, 0, 7, 0, 6, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 3, 0, 9, 0, 0, 0, 0, 0, 0, 7, 6, 0, 0, 4, 6, 0, 0, 5, 0, 2, 0, 0, 0, 1, 0, 0, 0, 8, 4, 0, 0]

def print_board(frame=board):
    for i in range(9):
        for j in range(9):
            print(frame[i*9+j], end=" ")
        print()
    print()

print_board()

def create_frame_from_board():
    frame = [None] * 81

    for i in range(len(frame)):
        if board[i] == 0:
            frame[i] = list(range(1, 10))
        else:
            frame[i] = [board[i]]

    return frame

already_removed_count = 0

def apply_constraints(pos, frame):
    if -1 in [apply_row_constraint(pos, frame), apply_col_constraint(pos, frame), apply_box_constraint(pos, frame)]:
        return -1
    return 0

def apply_row_constraint(pos, frame):
    global already_removed_count
    start_index = (pos // 9) * 9
    end_index = start_index + 9

    for i in range(start_index, end_index):
        if i == pos:
            continue

        if len(frame[i]) == 1:
            try:
                frame[pos].remove(frame[i][0]) 
            except:
                already_removed_count += 1

        if len(frame[i]) == 0:
            return -1

    return 0

def apply_col_constraint(pos, frame):
    global already_removed_count

    start_index = pos % 9

    for i in [start_index + j*9 for j in range(9)]:
        if i == pos:
            continue

        if len(frame[i]) == 1:
            try:
                frame[pos].remove(frame[i][0]) 
            except:
                already_removed_count += 1

        if len(frame[i]) == 0:
            return -1

    return 0

def apply_box_constraint(pos, frame):
    global already_removed_count
    box_start = (pos // 3) * 3 - 9 * ((pos // 9) % 3)

    for i in range(3):
        for j in range(3):
            if box_start + i*9 + j == pos:
                continue

            if len(frame[box_start + i*9 + j]) == 1:
                try:
                    frame[pos].remove(frame[box_start + i*9 + j][0])
                except:
                    already_removed_count += 1

            if len(frame[i]) == 0:
                return -1

    return 0

def get_indicies_row(pos):
    start_index = (pos // 9) * 9
    end_index = start_index + 9
    return [i for i in range(start_index, end_index) if i != pos]

def get_indicies_col(pos):
    start_index = pos % 9
    return [start_index + i*9 for i in range(9) if start_index + i*9 != pos] 

def get_indicies_box(pos):
    box_start = (pos // 3) * 3 - 9 * ((pos // 9) % 3)

    indicies = []

    for i in range(3):
        for j in range(3):
            if box_start + i*9 + j == pos:
                continue
            else:
                indicies.append(box_start + i*9 + j)

    return indicies

def get_indicies(pos):
    return get_indicies_row(pos) + get_indicies_col(pos) + get_indicies_box(pos)

def solve_sudoku():
    # Run through sudoku until all constraints are filled
    new_frame = create_frame_from_board()
    old_frame = deepcopy(new_frame)

    for i in range(81):
        apply_constraints(i, new_frame)

    while old_frame != new_frame:
        old_frame = deepcopy(new_frame)

        for i in range(81):
            apply_constraints(i, new_frame)

    # Constraint optimisation algorithm
    bpos = -1
    fpos = 0
    next_pos = False

    for i in range(81):
        if len(new_frame[i]) != 1:
            bpos = i
            break

    frames = [new_frame]
    bposes = [bpos]

    unsolved = True

    # Pygame setup
    pygame.init()

    WIDTH = 750
    HEIGHT = 750

    l = WIDTH / 9

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    runing = True

    font = pygame.font.SysFont(None, 50)

    while runing:
        # Pygame quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            
        if unsolved:
            new_frame = deepcopy(frames[fpos])
            new_frame[bpos] = new_frame[bpos][:1]
            
            for i in get_indicies(bpos):
                if apply_constraints(i, new_frame) == -1:
                    if len(frames[fpos][bpos]) > 1:
                        frames[fpos][bpos].remove(new_frame[bpos][0])
                        next_pos = False
                    else:
                        frames[fpos-1][bposes[fpos]].remove(frames[fpos][bposes[fpos]][0])
                        bpos = bposes[fpos]
                        
                        next_pos = False

                        frames.pop()
                        bposes.pop()

                        fpos -= 1
                    break
            else:
                frames.append(new_frame)
                bposes.append(bpos)

                fpos += 1
                next_pos = True

            if next_pos:
                for i in range(81):
                    if len(frames[fpos][i]) != 1:
                        bpos = i
                        break
                else:
                    unsolved = False

        # Rendering code
        pygame.display.flip()
        
        screen.fill((255, 255, 255))

        for i in range(9):
            for j in range(9):
                if len(new_frame[i*9+j]) == 1:
                    number = font.render(str(new_frame[i*9+j][0]), 1, (0, 0, 0))
                    screen.blit(number, (l*j, l*i))
        clock.tick(1)

def draw_frame(frame, screen, font):
    pass

if __name__ == "__main__":
    solve_sudoku()
