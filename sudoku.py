import pygame
from board import Board


def main():
    pygame.init()
    global mouse_x, mouse_y, window, width

    width = 800
    window = pygame.display.set_mode((width, width))

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Captures coordinates of mouse

    board = Board(width, width, window, "difficulty")

    running = True
    SQUARE_SIZE = 80
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # KEYDOWN EVENTS
            if event.type == pygame.KEYDOWN and board.current_selected_cell is not None:
                key_pressed = pygame.key.name(event.key)
                key_pressed = key_pressed.replace("[", "")  # Strip brackets from key_pressed to support num pad
                key_pressed = key_pressed.replace("]", "")
                print(f"The following key was pressed: {key_pressed}")

                if key_pressed in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    new_value = int(key_pressed)
                    board.sketch(new_value)
                    board.place_number(0)
                # when user presses enter it sets the sketch value to be the cell value.
                if (
                        (key_pressed == "return" or key_pressed == "enter")
                        and board.current_selected_cell.sketched_value != 0
                ):
                    board.place_number(board.current_selected_cell.sketched_value)
                    print(
                        f"Guess was submitted! The selected cell has set its sketched value to its value {board.current_selected_cell.value}"
                    )
                if key_pressed == "backspace":
                    board.clear()
                if key_pressed in ["left", "right", "up", "down"]:
                    prev = board.current_selected_cell
                    row = prev.row
                    col = prev.col
                    if key_pressed == "left":
                        col = col - 1
                    if key_pressed == "right":
                        col = col + 1
                    if key_pressed == "up":
                        row = row - 1
                    if key_pressed == "down":
                        row = row + 1
                    try:
                        board.current_selected_cell = board.player_board[row][col]
                        board.current_selected_cell.selected = True
                        prev.selected = False
                    except:
                        print("could not update")
                        pass
                if key_pressed == "right":
                    pass
                if key_pressed == "up":
                    pass
                if key_pressed == "down":
                    pass
            # CLICKING EVENTS
            if event.type == pygame.MOUSEBUTTONDOWN:  # New event for mouse button down
                x, y = event.pos
                x = x - 37
                y = y - 37
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                print(f"Clicked on row: {row}, clicked on col: {col}")
                # Selecting cell and updating cell values.

                # left click, selects cell for value input
                if event.button == 1 and board.game_state == "play":
                    # updates the selected cell
                    try:
                        board.select(row, col)
                        print(
                            f"The cell located at row {row}, {col}. With a current value of {board.current_selected_cell.value} and SKETCH value of {board.current_selected_cell.sketched_value}"
                        )
                    except:
                        pass

                if event.button == 3 and board.game_state == "play":
                    board.select(row, col)
                    board.clear()
                if event.button == 1:  # If left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Grabs position of mouse
                    print(f"x :{mouse_x}, y:{mouse_y}")
                    # Inserts in function to see if click is within any buttons
                    board.button_pressed(mouse_x, mouse_y)
        if board.game_state == "start_menu":
            board.draw_start_menu()
        if board.game_state == "play":
            board.draw_grid()
        if board.game_state == "exit":
            pygame.quit()
    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
