import pygame
import cell
import sudoku_generator


class Board:
    # This class represents an entire Sudoku board. A Board object has 81 Cell objects
    def __init__(self, width, height, window, difficulty):
        self.width = width
        self.height = height
        self.window = window
        self.difficulty = difficulty
        self.player_board = []
        self.TwoD_unsolved = []
        self.TwoD_solved = []
        self.current_selected_cell = None
        self.game_state = "start_menu"

    def draw(self):
        # draw an outline of the sudoku grid, with bold lines to delineate the 3x3 boxes.
        # Draws every cell on this board
        rows, cols = 9, 9
        SQUARE_SIZE = 75
        self.window.fill((255, 255, 255))

        # ---BOARD---
        # drawing the initial board
        # draw the rows
        for i in range(0, rows + 1):
            if i % 3 == 0:  # darker lines for 3x3 grid
                pygame.draw.line(
                    self.window,
                    (0, 0, 0),
                    # 62 to center it, +2 to account for the line width so the top line isn't cut off
                    (62, i * SQUARE_SIZE + 2),
                    # 62+675(length of sudoku board) = 77
                    (737, i * SQUARE_SIZE + 2),
                    5,  # line width
                )
            else:
                pygame.draw.line(
                    self.window,
                    (0, 0, 0),
                    (62, i * SQUARE_SIZE + 2),  # 62 to center it
                    # 62+675(length of sudoku board) = 77
                    (737, i * SQUARE_SIZE + 2),
                    2,
                )
        # draw the columns
        for i in range(0, cols + 1):
            if i % 3 == 0:  # darker lines for 3x3 grid
                pygame.draw.line(
                    self.window,
                    (0, 0, 0),
                    ((i * SQUARE_SIZE) + 62, 0),  # 62 to center it
                    # goes to height of board, 9x75=675
                    ((i * SQUARE_SIZE) + 62, 675),
                    5,
                )
            else:
                pygame.draw.line(
                    self.window,
                    (0, 0, 0),
                    ((i * SQUARE_SIZE) + 62, 0),  # 62 to center it
                    # goes to height of board, 9x75=675
                    ((i * SQUARE_SIZE) + 62, 675),
                    2,
                )

        # initialize the boards to get the cells

    def select(self, row, col):
        # toggles off selected cell property off cell
        if self.current_selected_cell != None:
            self.current_selected_cell.selected = False
        # Marks the cell at (row, col) in the board as the current selected cell.
        # Once a cell has been selected, the user can edit its value or sketched value.
        self.current_selected_cell = self.player_board[row][col]
        # toggles on selected cell property
        self.current_selected_cell.selected = True
        # self.current_selected_cell.selected = True
        pass

    def click(self, x, y):
        # If a tuple of (x, y) coordinates is within the displayed board, this function returns a tuple of the (row,
        # col) of the cell which was clicked. Otherwise, this function returns None.
        # given: x,y coords
        row = y // 75
        col = (x - 62) // 75
        if (0 <= row <= 8) and (0 <= col <= 8):
            return (row, col)
        else:
            return None

    def clear(self):
        row = self.current_selected_cell.row
        col = self.current_selected_cell.col
        if self.TwoD_unsolved[row][col] == 0:
            self.sketch(0)
            self.place_number(0)

    def sketch(self, value):
        row = self.current_selected_cell.row
        col = self.current_selected_cell.col
        if self.TwoD_unsolved[row][col] == 0:
            self.current_selected_cell.set_sketched_value(value)
        pass

    def place_number(self, value):
        row = self.current_selected_cell.row
        col = self.current_selected_cell.col
        if self.TwoD_unsolved[row][col] == 0:
            self.current_selected_cell.set_cell_value(value)
        if self.is_full():
            if self.check_board():
                self.game_state = 'win'
                self.game_win_screen()
            else:
                self.game_state = 'loss'
                self.game_lose_screen()

    def reset_to_original(self):
        # Reset all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        for i in range(len(self.player_board)):
            for j in range(len(self.player_board[i])):
                self.player_board[i][j].set_cell_value(self.TwoD_unsolved[i][j])
                self.player_board[i][j].set_sketched_value(0)
        pygame.display.update()

    def is_full(self):
        # Returns a Boolean value indicating whether the board is full or not.
        # Returns False if NOT full, returns True if it IS full
        # determined by if there are any "empty"(denoted by value = 0) cells left in player_board
        for i in range(len(self.player_board)):
            for j in range(len(self.player_board[i])):
                if self.player_board[i][j].get_value() == 0:
                    return False
        return True
        pass

    def update_board(self):
        # Updates the underlying 2D board with the values in all cells
        pass

    def find_empty(self):
        # Finds an empty cell and returns its row and col as a tuple (x, y).
        # Returns (row, col) of the first cell obj with value = 0
        for i in range(len(self.player_board)):
            for j in range(len(self.player_board[i])):
                if self.player_board[i][j].get_value() == 0:
                    return (
                        self.player_board[i][j].get_row(),
                        self.player_board[i][j].get_col(),
                    )
        return None

    def check_board(self):
        # Check whether the Sudoku board is solved correctly.
        # Returns False if solved INCORRECTLY, returns True if solved CORRECTLY
        for i in range(len(self.player_board)):
            for j in range(len(self.player_board[i])):
                if self.player_board[i][j].get_value() != self.TwoD_solved[i][j]:
                    return False
        return True

    def draw_start_menu(self):  # blits welcome text, as well as buttons visually
        # start menu background png
        background = pygame.image.load("pictures/sudoku_background.png")
        title = pygame.image.load("pictures/welcometo.png")
        button_surface = pygame.image.load("pictures/button.png")
        # scales down imported pictures, original size too large
        button_surface = pygame.transform.scale(button_surface, (110, 40))

        self.window.fill((255, 255, 255))  # Clear the screen
        self.window.blit(background, (0, 0))
        self.window.blit(title, (0, 0))

        buttons = {  # dictionary of buttons, with each button's position and text
            "Easy": ((217, 430), "Easy"),
            "Medium": ((400 - button_surface.get_width() / 2, 430), "Medium"),
            "Hard": ((486, 430), "Hard"),
        }
        if self.game_state == "start_menu":
            for button_key, (button_pos, button_label) in buttons.items():
                button_rect = pygame.Rect(button_pos, button_surface.get_size())
                button_text_rendered = self.button_color(
                    button_rect, button_label, *pygame.mouse.get_pos()
                )

                text_x = (
                    button_pos[0]
                    + (button_surface.get_width() - button_text_rendered.get_width())
                    // 2
                )
                text_y = (
                    button_pos[1]
                    + (button_surface.get_height() - button_text_rendered.get_height())
                    // 2
                )

                # displays the button in form (button.png, pos)
                self.window.blit(button_surface, button_pos)
                self.window.blit(button_text_rendered, (text_x, text_y))
        pygame.display.update()

    # functionality of every button in start menu and game... board is created based off user input in start_menu buttons (easy, med, hard)
    def button_pressed(self, mouse_x, mouse_y):
        button_surface = pygame.image.load("pictures/button.png")
        # scales down imported pictures, original size too large
        button_surface = pygame.transform.scale(button_surface, (110, 40))

        if (
            self.game_state == "start_menu"
        ):  # registers button clicks only for start menu
            buttons = {
                "Easy": ((217, 430), "Easy"),
                "Medium": ((400 - button_surface.get_width() // 2, 430), "Medium"),
                "Hard": ((486, 430), "Hard"),
            }
            for button_key, (button_pos, _) in buttons.items():
                button_rect = pygame.Rect(button_pos, button_surface.get_size())
                if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(
                    mouse_x, mouse_y
                ):
                    self.game_state = "play"
                    self.difficulty = button_key
                    self.player_board = []
                    self.create_board(self.difficulty)
                    self.draw_grid()

        if self.game_state == "play":  # functionality of buttons during game
            buttons = {
                # stops the program
                "Exit": ((650, 750), "Exit"),
                # resets the board while maintaining the same difficulty
                "Reset": ((420, 750), "Reset"),
                # restarts the game... sending player back to start_menu prompting for new difficulty selection
                "Restart": ((535, 750), "Restart"),
            }
            for button_key, (button_pos, _) in buttons.items():
                button_rect = pygame.Rect(button_pos, button_surface.get_size())
                # optional visual enhancer.. text color of buttons changes when hovered
                button_text_rendered = self.button_color(
                    button_rect, button_key, *pygame.mouse.get_pos()
                )
                if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(
                    mouse_x, mouse_y
                ):
                    if button_key == "Exit":
                        # refers to game_state on main... pygame.quit() here in case of error
                        self.game_state == "exit"
                        pygame.quit()
                        return
                    if button_key == "Reset":  # FIXME: visuals not updating
                        # places a new sudoku grid
                        self.reset_to_original()
                        # button text position with respect to button picture
                    if button_key == "Restart":
                        self.game_state = "start_menu"  # sends you back to start screen
        if self.game_state == "win" or self.game_state == "loss":
            buttons = {
                "Restart": ((535, 750), "Restart"),
                "Exit": ((650, 750), "Exit"),
            }
            for button_key, (button_pos, _) in buttons.items():
                button_rect = pygame.Rect(button_pos, button_surface.get_size())
                # optional visual enhancer.. text color of buttons changes when hovered
                button_text_rendered = self.button_color(
                    button_rect, button_key, *pygame.mouse.get_pos()
                )
                if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(
                    mouse_x, mouse_y
                ):
                    if button_key == "Exit":
                        # refers to game_state on main... pygame.quit() here in case of error
                        self.game_state == "exit"
                        pygame.quit()
                        return
                    if button_key == "Restart":
                        self.game_state = "start_menu"  # sends you back to start screen
        pygame.display.update()

    # improves readibility by only defining rendering font, button borders and text color once // used in start_menu buttons and game buttons
    def button_color(self, button_rect, button_text, mouse_x, mouse_y):
        font = pygame.font.SysFont("tahoma", 20, True)
        if button_rect.collidepoint(mouse_x, mouse_y):
            button_text_color = "dodgerblue"
        else:
            button_text_color = "white"

        button_text_rendered = font.render(button_text, True, button_text_color)
        return button_text_rendered

    def draw_grid(self):
        # paste background picture
        button_surface = pygame.image.load("pictures/button.png")
        # scales down imported pictures, original size too large
        button_surface = pygame.transform.scale(button_surface, (110, 40))
        self.window.blit(
            pygame.image.load("pictures/gamebackground.png"), (0, 0)
        )  # background image
        # BIG ORANGE BLUE BOX
        light = pygame.Surface((725, 725), pygame.SRCALPHA)
        # semi-transparent box , makes numbers easier to see
        pygame.draw.rect(light, (30, 70, 225, 150), light.get_rect())
        self.window.blit(light, (40, 25))

        for i in range(10):  # Total lines: 0 to 9
            # every third line is orange.. creating an illusion of 9 smaller boxes
            color = "orange" if i % 3 == 0 else "white"
            line_width = 5 if i % 3 == 0 else 2

            # creates horizontal lines of grid
            pygame.draw.line(
                self.window,
                color,
                (45, 25 + i * 80),
                (45 + 715, 25 + i * 80),
                line_width,
            )
            pygame.draw.line(
                self.window,
                color,
                (40 + i * 80, 25),
                (40 + i * 80, 25 + 720),
                line_width,
            )  # creates the vertical lines

        # Creates a box, border of grid
        pygame.draw.rect(self.window, "orange", pygame.Rect(39, 23, 725, 725), 4)
        self.draw_numbers()
        if self.game_state == "play":  # buttons
            buttons = {
                "Exit": ((650, 750), "Exit"),
                "Reset": ((420, 750), "Reset"),
                "Restart": ((535, 750), "Restart"),
            }

            for button_key, (button_pos, _) in buttons.items():
                button_rect = pygame.Rect(button_pos, button_surface.get_size())
                button_text_rendered = self.button_color(
                    button_rect, button_key, *pygame.mouse.get_pos()
                )

                self.window.blit(button_surface, (button_pos[0], button_pos[1]))
                self.window.blit(
                    button_text_rendered, (button_pos[0] + 25, button_pos[1] + 7)
                )
        pygame.display.update()

    def draw_numbers(self):  # you don't have to call, called within draw grid function
        font_size = 35  # Customize the font size
        font = pygame.font.SysFont("tahoma", font_size, True)  # Create a custom font
        sk_font = pygame.font.SysFont("tahoma", 25, True)

        for row in range(len(self.TwoD_unsolved)):
            for col in range(len(self.TwoD_unsolved[row])):
                # Assuming self.TwoD_unsolved contains the numbers
                number = self.player_board[row][col].get_value()
                sketched = self.player_board[row][col].sketched_value
                selected = self.player_board[row][col].selected
                number_text = font.render(
                    str(number), True, "wheat"
                )  # Customize the color
                sketched_text = sk_font.render(
                    str(sketched), True, "red"
                )  # Customize the color
                if selected:
                    text_width, text_height = number_text.get_size()
                    x = (col * 80) + 75 / 2 + 8
                    # # Adjust the y position
                    y = (row * 80) + 28
                    rectangle = pygame.Rect(x, y, 75, 75)
                    pygame.draw.rect(self.window, (255, 0, 128), rectangle, 5)
                    # self.window.blit(font.render('x', True, 'wheat'), (x, y))
                if sketched != 0 and number == 0:
                    text_width, text_height = number_text.get_size()
                    x = (col * 80) + (75 / 2) + 15
                    y = (row * 80) + 28
                    self.window.blit(sketched_text, (x, y))
                if number != 0:
                    text_width, text_height = number_text.get_size()
                    x = (col * 80) + (160 - text_width) // 2
                    # Adjust the y position
                    y = (row * 80) + (130 - text_height) // 2
                    self.window.blit(number_text, (x, y))

    def create_board(self, difficulty):
        # creates the randomized cells
        if difficulty == "Easy":
            self.TwoD_solved, self.TwoD_unsolved = sudoku_generator.generate_sudoku(
                9, 30
            )
        elif difficulty == "Medium":
            self.TwoD_solved, self.TwoD_unsolved = sudoku_generator.generate_sudoku(
                9, 40
            )
        elif difficulty == "Hard":
            self.TwoD_solved, self.TwoD_unsolved = sudoku_generator.generate_sudoku(
                9, 50
            )

        self.TwoD_unsolved = self.TwoD_unsolved[
            :9
        ]  # fixes an error that counts 10 sublists upon generating

        # ---CELLS---
        # initialize the player_board by creating cell objs containing the correct values/col/rows from unsolved_board
        for i in range(len(self.TwoD_unsolved)):
            # player_board is a list of OBJECTS, TwoD_solved and _unsolved are lists of INTEGERS
            self.player_board.append([])
            for j in range(len(self.TwoD_unsolved[i])):
                new_cell = cell.Cell(self.TwoD_unsolved[i][j], i, j, self.window)
                # adds cells to invisible list
                self.player_board[i].append(new_cell)

        pygame.display.update()

    def game_win_screen(self): # empty screen with game win text
        font = pygame.font.SysFont("tahoma", 100, True)
        text = font.render("You Win!", 1, (250, 70, 22))
        self.window.fill((0, 33, 165))  # Fill the screen with black
        self.window.blit(text, (800 // 2 - text.get_width() // 2, 800 // 2 - text.get_height() // 2))

        button_surface = pygame.image.load("pictures/button.png")
        button_surface = pygame.transform.scale(button_surface, (110, 40))

        buttons = {
            "Restart": ((535, 750), "Restart"),
            "Exit": ((650, 750), "Exit"),
        }

        for button_key, (button_pos, _) in buttons.items():
            button_rect = pygame.Rect(button_pos, button_surface.get_size())
            button_text_rendered = self.button_color(
                button_rect, button_key, *pygame.mouse.get_pos()
            )

            self.window.blit(button_surface, (button_pos[0], button_pos[1]))
            self.window.blit(
                button_text_rendered, (button_pos[0] + 25, button_pos[1] + 7)
            )
        pygame.display.update()
    
    def game_lose_screen(self): # empty screen with game lose text
        font = pygame.font.SysFont("tahoma", 100, True)
        text = font.render("Game Over!", 1, (250, 70, 22))
        self.window.fill((0, 33, 165))  # Fill the screen with black
        self.window.blit(text, (800 // 2 - text.get_width() // 2, 800 // 2 - text.get_height() // 2))

        button_surface = pygame.image.load("pictures/button.png")
        button_surface = pygame.transform.scale(button_surface, (110, 40))

        buttons = {
            "Restart": ((535, 750), "Restart"),
            "Exit": ((650, 750), "Exit"),
        }

        for button_key, (button_pos, _) in buttons.items():
            button_rect = pygame.Rect(button_pos, button_surface.get_size())
            button_text_rendered = self.button_color(
                button_rect, button_key, *pygame.mouse.get_pos()
            )

            self.window.blit(button_surface, (button_pos[0], button_pos[1]))
            self.window.blit(
                button_text_rendered, (button_pos[0] + 25, button_pos[1] + 7)
            )
        pygame.display.update()
