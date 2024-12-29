from itertools import product

board = [
        6, 0, 0, 1, 0, 0, 0, 0, 2,
        8, 0, 1, 0, 9, 0, 0, 0, 0,
        0, 7, 5, 0, 8, 4, 0, 0, 0,
        4, 3, 0, 0, 2, 0, 5, 6, 1,
        5, 1, 8, 7, 0, 0, 4, 0, 9,
        0, 9, 6, 4, 1, 0, 3, 0, 0,
        0, 0, 0, 0, 7, 0, 0, 0, 0,
        0, 6, 0, 0, 3, 1, 0, 5, 0,
        7, 0, 2, 5, 4, 0, 6, 0, 3,
    ]

def print_board(frame=board):
    for i in range(9):
        for j in range(9):
            print(frame[i*9+j], end=" ")
        print()
    print()

def create_frame_from_board():
    frame = [None] * 81

    for i in range(len(frame)):
        if board[i] == 0:
            frame[i] = list(range(1, 10))
        else:
            frame[i] = [board[i]]

    return frame

def apply_constraints(pos, frame):
    apply_row_constraints(pos, frame)
    apply_col_constraints(pos, frame)
    apply_box_constraints(pos, frame)

def apply_row_constraints(pos, frame):
    start_index = pos // 9 * 9
    end_index = start_index + 9

    for i in range(start_index, end_index):
        if len(frame[i]) == 1:
            frame[pos].remove(frame[i][0]) 

def apply_col_constraint(pos, frame):
    for i in [pos + i*9 for i in range(9)]:
        if len(frame[i]) == 1:
            frame[pos].remove(frame[i][0]) 

if __name__ == "__main__":
    start_frame = create_frame_from_board()

    apply_col_constraint(1, start_frame)
    print_board(start_frame)
