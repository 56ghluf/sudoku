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

class Board:
    def __init__(self):
        self.board = [0, 3, 0, 2, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 5, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 7, 0, 0, 1, 0, 7, 0, 6, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 3, 0, 9, 0, 0, 0, 0, 0, 0, 7, 6, 0, 0, 4, 6, 0, 0, 5, 0, 2, 0, 0, 0, 1, 0, 0, 0, 8, 4, 0, 0]
    
    def set_board(self, board):
        self.board = board
        self.print_board()

    def print_board(self, frame=None):
        frame = frame or self.board
        for i in range(9):
            for j in range(9):
                print(frame[i*9+j], end=" ")
            print()
        print()

    def create_frame_from_board(self):
        frame = [None] * 81

        for i in range(len(frame)):
            if self.board[i] == 0:
                frame[i] = list(range(1, 10))
            else:
                frame[i] = [self.board[i]]

        return frame

    def apply_constraints(self, pos, frame):
        if -1 in [self.apply_row_constraint(pos, frame), self.apply_col_constraint(pos, frame), self.apply_box_constraint(pos, frame)]:
            return -1
        return 0

    def apply_row_constraint(self, pos, frame):
        start_index = (pos // 9) * 9
        end_index = start_index + 9

        for i in range(start_index, end_index):
            if i == pos:
                continue

            if len(frame[i]) == 1:
                try:
                    frame[pos].remove(frame[i][0]) 
                except:
                    pass

            if len(frame[i]) == 0:
                return -1

        return 0

    def apply_col_constraint(self, pos, frame):
        start_index = pos % 9

        for i in [start_index + j*9 for j in range(9)]:
            if i == pos:
                continue

            if len(frame[i]) == 1:
                try:
                    frame[pos].remove(frame[i][0]) 
                except:
                    pass

            if len(frame[i]) == 0:
                return -1

        return 0

    def apply_box_constraint(self, pos, frame):
        box_start = (pos // 3) * 3 - 9 * ((pos // 9) % 3)

        for i in range(3):
            for j in range(3):
                if box_start + i*9 + j == pos:
                    continue

                if len(frame[box_start + i*9 + j]) == 1:
                    try:
                        frame[pos].remove(frame[box_start + i*9 + j][0])
                    except:
                        pass

                if len(frame[i]) == 0:
                    return -1

        return 0

    def get_indicies_row(self, pos):
        start_index = (pos // 9) * 9
        end_index = start_index + 9
        return [i for i in range(start_index, end_index) if i != pos]

    def get_indicies_col(self, pos):
        start_index = pos % 9
        return [start_index + i*9 for i in range(9) if start_index + i*9 != pos] 

    def get_indicies_box(self, pos):
        box_start = (pos // 3) * 3 - 9 * ((pos // 9) % 3)

        indicies = []

        for i in range(3):
            for j in range(3):
                if box_start + i*9 + j == pos:
                    continue
                else:
                    indicies.append(box_start + i*9 + j)

        return indicies

    def get_indicies(self, pos):
        return self.get_indicies_row(pos) + self.get_indicies_col(pos) + self.get_indicies_box(pos)

    def solve_initial_constraints(self):
        # Run through sudoku until all constraints are filled
        self.new_frame = self.create_frame_from_board()
        old_frame = deepcopy(self.new_frame)

        for i in range(81):
            self.apply_constraints(i, self.new_frame)

        while old_frame != self.new_frame:
            old_frame = deepcopy(self.new_frame)

            for i in range(81):
                self.apply_constraints(i, self.new_frame)

    def initialize_parameters(self):
        # Constraint optimisation algorithm
        self.bpos = 0
        self.fpos = 0
        self.next_pos = False

        for i in range(81):
            if len(self.new_frame[i]) != 1:
                self.bpos = i
                break

        self.frames = [self.new_frame]
        self.bposes = [self.bpos]

        self.unsolved = True

    def take_step(self):
        self.new_frame = deepcopy(self.frames[self.fpos])
        self.new_frame[self.bpos] = self.new_frame[self.bpos][:1]
        
        for i in self.get_indicies(self.bpos):
            if self.apply_constraints(i, self.new_frame) == -1:
                if len(self.frames[self.fpos][self.bpos]) > 1:
                    self.frames[self.fpos][self.bpos].remove(self.new_frame[self.bpos][0])
                    self.next_pos = False
                else:
                    self.frames[self.fpos-1][self.bposes[self.fpos]].remove(self.frames[self.fpos][self.bposes[self.fpos]][0])
                    self.bpos = self.bposes[self.fpos]
                    
                    self.next_pos = False

                    self.frames.pop()
                    self.bposes.pop()

                    self.fpos -= 1
                break
        else:
            self.frames.append(self.new_frame)
            self.bposes.append(self.bpos)

            self.fpos += 1
            self.next_pos = True

        if self.next_pos:
            for i in range(81):
                if len(self.frames[self.fpos][i]) != 1:
                    self.bpos = i
                    break
            else:
                self.unsolved = False

"""
    # Pygame setup
    pygame.init()

    WIDTH = 750
    HEIGHT = 750

    l = WIDTH / 9

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    runing = True

    font = pygame.font.SysFont(None, 50)

    # Pygame quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
            
    # Rendering code
    pygame.display.flip()
    
    screen.fill((255, 255, 255))

    for i in range(9):
        for j in range(9):
            if len(new_frame[i*9+j]) == 1:
                number = font.render(str(new_frame[i*9+j][0]), 1, (0, 0, 0))
                screen.blit(number, (l*j + l/2 - 25, l*i + l/2 - 25))
    # clock.tick(1)
"""

def draw_frame(frame, screen, font):
    pass

if __name__ == "__main__":
    board = Board()

    board.print_board()

    board.solve_initial_constraints()
    board.initialize_parameters()

    while board.unsolved:
        board.take_step()

    board.print_board(frame=board.new_frame)
