import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        #  Constructor for the cell class
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False
        pass

    def get_value(self):
        return self.value

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_cell_value(self, value):
        #  Setter for this cell's value
        self.value = value
        pass

    def set_sketched_value(self, value):
        #  Setter for this cell's sketched value
        self.sketched_value = value
        pass

    def draw(self):
        # draws this cell, along with the value in it
        # Font
        num_font = pygame.font.Font(None, 50)
        sketched_num_font = pygame.font.Font(None, 35)
        if self.value != 0:
            # Square with number
            num_surf = num_font.render(str(self.value), 0, (0, 0, 0))
            num_rect = num_surf.get_rect(
                center=((self.col * 75 + 75 // 2) + 62, (self.row * 75 + 75 // 2) + 2))
        elif self.sketched_value != 0:
            num_surf = sketched_num_font.render(
                str(self.sketched_value), 0, (192, 192, 192))
            num_rect = num_surf.get_rect(
                center=((self.col * 75 + 75 // 2) + 42, (self.row * 75 + 75 // 2) - 15))
        else:
            # square without number
            num_surf = num_font. render(" ", 0, (0, 0, 0))
            num_rect = num_surf.get_rect(
                center=((self.col * 75 + 75 // 2) + 62, (self.row * 75 + 75 // 2) + 2))
        self.screen.blit(num_surf, num_rect)
