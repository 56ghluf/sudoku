from itertools import product

board = [
        [6, 0, 0, 1, 0, 0, 0, 0, 2],
        [8, 0, 1, 0, 9, 0, 0, 0, 0],
        [0, 7, 5, 0, 8, 4, 0, 0, 0],
        [4, 3, 0, 0, 2, 0, 5, 6, 1],
        [5, 1, 8, 7, 0, 0, 4, 0, 9],
        [0, 9, 6, 4, 1, 0, 3, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [0, 6, 0, 0, 3, 1, 0, 5, 0],
        [7, 0, 2, 5, 4, 0, 6, 0, 3],
        ]

def printb(board):
    for i in board:
        for j in i:
            print(j, end=" ")

        print()

def check_num_in_row(row, num):
    if num < 1 or num > 9:
        raise Exception("Number being checked for in row must be between 1 and 9.")
    if num in board[row]:
        return True
    else:
        return False

def get_col(col):
    return [x[col] for x in board]

def check_num_in_col(col, num):
    if num < 1 or num > 9:
        raise Exception("Number being checked for in column must be between 1 and 9.")

    if num in get_col(col):
        return True
    else:
        return False

def get_square_indicies(square_num):
    square_row = square_num // 3
    square_col = square_num % 3

    row_indicies = [square_row*3 + i for i in range(3)]
    col_indicies = [square_col*3 + i for i in range(3)]

    return product(row_indicies, col_indicies)

def place_all_in_square(square_num):
    print(list(get_square_indicies(square_num)))

if __name__ == "__main__":
    place_all_in_square(3)
