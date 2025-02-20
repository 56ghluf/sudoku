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
        self.invalid_board = False
    
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
            if self.apply_constraints(i, self.new_frame) == -1:
                self.invalid_board = True
                return

        while old_frame != self.new_frame:
            old_frame = deepcopy(self.new_frame)

            for i in range(81):
                if self.apply_constraints(i, self.new_frame) == -1:
                    self.invalid_board = True
                    return

    def initialize_parameters(self):
        # Constraint optimisation algorithm
        self.bpos = 0
        self.fpos = 0

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
                else:
                    if self.fpos == 0:
                        self.invalid_board = True
                        return

                    self.frames[self.fpos-1][self.bposes[self.fpos]].remove(self.frames[self.fpos][self.bposes[self.fpos]][0])
                    self.bpos = self.bposes[self.fpos]
                    
                    self.frames.pop()
                    self.bposes.pop()

                    self.fpos -= 1
                break
        else:
            self.frames.append(self.new_frame)
            self.bposes.append(self.bpos)

            self.fpos += 1

            for i in range(81):
                if len(self.frames[self.fpos][i]) != 1:
                    self.bpos = i
                    break
            else:
                self.unsolved = False

class Panel:
    def __init__(self, x, y, w, h, text, screen):
        self.rect = pygame.Rect(x, y, w, h)

        self.screen = screen

        self.font = pygame.font.Font(None, int(w*0.16))

        self.text_surface = self.font.render(text, True, "black")
        self.font_size = self.font.size(text)

        self.colour = (244, 51, 51)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)

        self.screen.blit(self.text_surface,
                         (self.rect.x + self.rect.w/2 - self.font_size[0]/2,
                          self.rect.y + self.rect.h/2 - self.font_size[1]/2.3))

class InputBox:
    def __init__(self, x, y, w, h, screen):
        self.input_rect = pygame.Rect(x, y, w, h)
        self.cover_rect = pygame.Rect(x + 1, y + 1, w - 2, h - 2)

        self.screen = screen

        self.active = False
        self.text = ""

        self.font = pygame.font.Font(None, int(w*1.5))

        self.passive_colour = (240, 240, 240)
        self.active_colour = (255, 255, 255)

    def draw(self):
        current_colour = self.active_colour if self.active else self.passive_colour
        pygame.draw.rect(self.screen, current_colour, self.cover_rect)

        text_surface = self.font.render(self.text, True, "black")
        font_size = self.font.size(self.text)
        self.screen.blit(text_surface,
                         (self.input_rect.x + self.input_rect.w/2 - font_size[0]/2,
                          self.input_rect.y + self.input_rect.h/2 - font_size[1]/2.3))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.unicode == "\r":
                    self.active = False
                # For backspace
                elif event.unicode == "\b":
                    self.text = ""
                else:
                    if event.unicode in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        self.text = event.unicode
                        self.active = False

class Button:
    def __init__(self, x, y, w, h, screen, text, font_size, callback):
        self.clickable_rect = pygame.Rect(x, y, w, h)

        self.clicked_time = 0

        self.text = text

        self.font = pygame.font.Font(None, font_size) 

        self.text_x = self.clickable_rect.x + self.clickable_rect.w/2 - self.font.size(self.text)[0]/2
        self.text_y = self.clickable_rect.y + self.clickable_rect.h/2 - self.font.size(self.text)[1]/2

        self.passive_colour = (50, 160, 210)
        self.active_colour = (60, 190, 255)

        self.screen = screen

        self.callback = callback

    def draw(self):
        current_colour = self.active_colour if pygame.time.get_ticks() - self.clicked_time < 200 else self.passive_colour
        pygame.draw.rect(self.screen, current_colour, self.clickable_rect)

        text_surface = self.font.render(self.text, True, "black") 
        self.screen.blit(text_surface, (self.text_x, self.text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.clickable_rect.collidepoint(event.pos):
                self.clicked_time = pygame.time.get_ticks()
                self.callback()

class Window:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 700

        # Start pygame
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 50)

        # Create the board with all the logic
        self.board = Board()

        self.solve_state = False

        self.first_step_taken = False

        w = self.WIDTH / 9
        self.input_boxes = [InputBox((i - (i//9) * 9)*w, (i//9)*w, w, w, self.screen) for i in range(81)]

        # Seperation between squares
        self.sep_rects = [pygame.Rect(i*3*w + 3*w - 1, 0, 2, 600) for i in range(2)]
        self.sep_rects.extend([pygame.Rect(0, i*3*w + 3*w - 1, 600, 2) for i in range(2)])

        # Solve the current board
        self.solve_button = Button(0, 600, 100, 50, self.screen, "Solve", 50, self.verifiy_solve_state)

        # Cancel solving
        self.cancel_button = Button(100, 600, 125, 50, self.screen, "Cancel", 50, self.cancel_solving)

        # Reset the board
        self.reset_button = Button(225, 600, 100, 50, self.screen, "Reset", 50, self.reset_board)

        # Used for the reset button
        self.invalid_panel = Panel(self.WIDTH / 2 - 250, self.HEIGHT / 2 - 100, 500, 100, "Sudoku is invalid", self.screen)
        self.invalid_button = Button(self.WIDTH / 2 - 50, self.HEIGHT / 2 + 10, 100, 50, self.screen, "Continue", 30, self.verify_validity)

    # Go into solve state
    def verifiy_solve_state(self):
        self.solve_state = True

    # Cancel the solving
    def cancel_solving(self):
        self.solve_state = False

    # Reset all the numbers to nothing
    def reset_board(self):
        for i in range(len(self.input_boxes)):
            self.input_boxes[i].text = ""

    # Reset board to being valid
    def verify_validity(self):
        self.solve_state = False
        self.first_step_taken = False
        self.board.invalid_board = False


    def show(self):
        runing = True
        
        while runing:
            for event in pygame.event.get():
                # Pygame quit
                if event.type == pygame.QUIT:
                    runing = False

                # Stuff that should only happen when not solving
                if not self.solve_state:
                    # Input for input boxes
                    for input_box in self.input_boxes:
                        input_box.handle_event(event)

                    # Solve button
                    self.solve_button.handle_event(event)

                    # Rest board button
                    self.reset_button.handle_event(event)

                else:
                    self.cancel_button.handle_event(event)

                if self.solve_state and self.board.invalid_board:
                    self.invalid_button.handle_event(event)

            # Background colour
            self.screen.fill((200, 200, 200))

            # All the input boxes
            for input_box in self.input_boxes:
                input_box.draw()

            # Seperation between squares
            for sep_rect in self.sep_rects:
                pygame.draw.rect(self.screen, (100, 100, 100), sep_rect)

            # Solve button
            self.solve_button.draw()

            # Cancel solving button
            self.cancel_button.draw()

            # Reset board button
            self.reset_button.draw()

            # Show the error message if the board is invalid
            if self.board.invalid_board:
                self.invalid_panel.draw()
                self.invalid_button.draw()

            # Show the display
            pygame.display.flip()

            # self.clock.tick(1)

            # Do the actual solving here
            if self.solve_state and not self.board.invalid_board:
                self.solve_sudoku()

                if not self.board.unsolved:
                    self.solve_state = False
                    self.first_step_taken = False

    # Function to solve the sudoku
    def solve_sudoku(self):
        if not self.first_step_taken:
            # Create the borad from the input boxes
            for i in range(81):
                if self.input_boxes[i].text == "":
                    self.board.board[i] = 0
                else:
                    self.board.board[i] = int(self.input_boxes[i].text)

            # Solve the initial constraints and intialize parameters
            self.board.solve_initial_constraints()
            self.board.initialize_parameters()
            if self.board.invalid_board:
                return
            
            # Make sure not to take this first step again
            self.first_step_taken = True

        self.board.take_step()

        if self.board.invalid_board:
            return

        # Update all the input boxes
        for i in range(81):
            self.input_boxes[i].text = str(self.board.new_frame[i][0]) if len(self.board.new_frame[i]) == 1 else ""

if __name__ == "__main__":
    window = Window()
    window.show()
