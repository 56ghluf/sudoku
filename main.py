from itertools import product
from copy import deepcopy

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
    apply_row_constraint(pos, frame)
    apply_col_constraint(pos, frame)
    apply_box_constraint(pos, frame)

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

def get_indicies_row(pos):
    start_index = (pos // 9) * 9
    end_index = start_index + 9
    return [i for i in range(start_indei, end_indei) if i != pos]

def get_indices_col(pos):
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
    pos = -1

    for i in range(81):
        if len(new_frame[i]) != 1:
            pos = i
    else:
        print_board(new_frame)
        return

    current_frame = 0
    frames = [new_frame]

    while True:
        new_frame = deepcopy(new_frame)
        new_frame[pos] = new_frame[pos][:1]
        
        for i in get_indicies:
            apply_constraints(i, new_frame) 

        frames.append(new_frame)
        break
    
    print_board(new_frame)

if __name__ == "__main__":
    solve_sudoku()
