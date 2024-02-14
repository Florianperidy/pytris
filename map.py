import pygame
from data import *

class Map:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.sizeofbox = 50
        self.map = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def display_map(self, window, colors):
        for row in range(self.rows):
            for col in range(self.cols):
                cell_coord = self.map[row][col]
                rect = pygame.Rect(col * self.sizeofbox + 1, row * self.sizeofbox + 1, self.sizeofbox - 1, self.sizeofbox - 1)
                pygame.draw.rect(window, colors[cell_coord], rect)

    def pos_checker(self, row, col):
        if row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            return True
        return False

    def is_occupied(self, row, col):
        if self.map[row][col] == 0:
            return True
        return False

    def clear_row_function(self):
        r = 0
        for i in range(self.rows -1, 0, -1):
            if self.line_checker(i) == True:
                self.line_destroyer(i)
                r += 1
            else:
                if r > 0:
                    self.line_down(i, r)
        return r


    def line_checker(self, row):
        for i in range(self.cols):
            if self.map[row][i] == 0:
                return False
        return True

    def line_destroyer(self, row):
        for i in range(self.cols):
            self.map[row][i] = 0

    def line_down(self, row, nb):
        for i in range(self.cols):
            self.map[row + nb][i] = self.map[row][i]
            self.map[row][i] = 0

    def reset(self):
        for i in range(self.rows):
            for c in range(self.cols):
                self.map[i][c] = 0