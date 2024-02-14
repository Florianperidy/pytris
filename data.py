import pygame
from map import *
import random

def get_colors():
    black = (0, 0, 0)
    red = (255, 0, 0)
    orange = (255, 128, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    purple = (255, 0, 255)
    grey = (150, 150, 150)
    return [black, red, orange, yellow, green, cyan, blue, purple, grey]

class Data:
    def __init__(self, game):
        self.font = pygame.font.Font(None, 50)
        self.score = self.font.render("Score", True, (255, 255, 255))
        self.next_block = self.font.render("Next block", True, (255, 255, 255))
        self.game_over = self.font.render("GAME OVER", True, (255, 0, 0))
        self.restart = self.font.render("Press any key to restart", True, (255, 255, 255))
        self.score_value = self.font.render(str(game.score_value), True, (255, 255, 255))
        self.score_window = pygame.Rect(665, 100, 170, 60)
        self.next_block_window = pygame.Rect(550, 300, 400, 200)

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Gameloop:
    def __init__(self, grid):
        self.all_blocks = [Block_Z(), Block_L(), Block_O(), Block_S(), Block_I(), Block_J(), Block_T(), Block_U()]
        self.block = self.get_block()
        self.new_block = self.get_block()
        self.grid = grid
        self.endgame = 0
        self.score_value = 0
        self.line_sound = pygame.mixer.Sound("sounds/line_sound.ogg")
        self.block_placed_sound = pygame.mixer.Sound("sounds/block_placed.ogg")
        self.endgame_sound = pygame.mixer.Sound("sounds/endgame_sound.ogg")
        pygame.mixer.music.load("sounds/Theme.ogg")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

    def get_block(self):
        if len(self.all_blocks) == 0:
            self.all_blocks = [Block_Z(), Block_L(), Block_O(), Block_S(), Block_I(), Block_J(), Block_T(), Block_U()]
        block = random.choice(self.all_blocks)
        self.all_blocks.remove(block)
        return block

    def display(self, window, colors):
        self.block.draw_block(window, colors, 1, 1)
        if self.new_block.nb == 3:
            self.new_block.draw_block(window, colors, 500, 345)
            return
        if self.new_block.nb == 5:
            self.new_block.draw_block(window, colors, 500, 375)
            return
        self.new_block.draw_block(window, colors, 525, 345)

    def move_left(self):
        self.block.get_coords(0, -1)
        if self.block_checker() == False or self.collision_checker() == False:
            self.block.get_coords(0, 1)

    def move_right(self):
        self.block.get_coords(0, 1)
        if self.block_checker() == False or self.collision_checker() == False:
            self.block.get_coords(0, -1)

    def move_down(self):
        self.block.get_coords(1, 0)
        if self.block_checker() == False or self.collision_checker() == False:
            self.block.get_coords(- 1, 0)
            self.bottom()

    def score(self, lines, down, placed):
        if lines == 1:
            self.score_value += 100
        if lines == 2:
            self.score_value += 250
        if lines == 3:
            self.score_value += 400
        if lines == 4:
            self.score_value += 750
        self.score_value += down
        self.score_value += placed

    def bottom(self):
        block = self.block.move_block()
        self.block_placed_sound.set_volume(0.15)
        self.block_placed_sound.play()
        for i in block:
            self.grid.map[i.row][i.col] = self.block.nb
        self.block = self.new_block
        self.new_block = self.get_block()
        self.score(0, 0, 25)
        lines = self.grid.clear_row_function()
        if lines > 0:
            self.line_sound.play()
        self.score(lines, 0, 0)
        if self.collision_checker() == False:
            self.endgame = 1
            self.endgame_sound.set_volume(0.15)
            self.endgame_sound.play()

    def block_checker(self):
        block = self.block.move_block()
        for i in block:
            if self.grid.pos_checker(i.row, i.col) == False:
                return False
        return True

    def collision_checker(self):
        block = self.block.move_block()
        for i in block:
            if self.grid.is_occupied(i.row, i.col) == False:
                return False
        return True

    def rotate(self):
        self.block.rotate_block()
        if self.block_checker() == False or self.collision_checker() == False:
            self.block.rotate_back_block()
            return

    def reset(self):
        self.grid.reset()
        self.all_blocks = [Block_Z(), Block_L(), Block_O(), Block_S(), Block_I(), Block_J(), Block_T(), Block_U()]
        self.block = self.get_block()
        self.new_block = self.get_block()
        self.score_value = 0
        pygame.mixer.music.play(-1)


class Block:
    def __init__(self, nb):
        self.nb = nb
        self.sizeofbox = 50
        self.rot = 0
        self.block = {}
        self.coord_X = 0
        self.coord_Y = 0

    def get_coords(self, row, col):
        self.coord_X += row
        self.coord_Y += col

    def move_block(self):
        cur_pos = self.block[self.rot]
        new_pos = []
        for position in cur_pos:
            position = Position(position.row + self.coord_X, position.col + self.coord_Y)
            new_pos.append(position)
        return new_pos

    def draw_block(self, window, colors, x, y):
        block = self.move_block()
        for i in block:
            block_rect = pygame.Rect(x + i.col * self.sizeofbox, y +  i.row * self.sizeofbox, self.sizeofbox - 1, self.sizeofbox - 1)
            pygame.draw.rect(window, colors[self.nb], block_rect)

    def rotate_block(self):
        if self.rot == 3:
            self.rot = 0
            return
        self.rot += 1

    def rotate_back_block(self):
        if self.rot == 0:
            self.rot = 3
            return
        self.rot -= 1

class Block_Z(Block):
    def __init__(self):
        super().__init__(1)
        self.block = {
            0 :[Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1 :[Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2 :[Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3 :[Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.get_coords(0, 3)


class Block_L(Block):
    def __init__(self):
        super().__init__(2)
        self.block = {
            0 :[Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1 :[Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2 :[Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3 :[Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.get_coords(0, 3)

class Block_O(Block):
    def __init__(self):
        super().__init__(3)
        self.block = {
            0 :[Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)],
            1 :[Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)],
            2 :[Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)],
            3 :[Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]
        }
        self.get_coords(0, 4)

class Block_S(Block):
    def __init__(self):
        super().__init__(4)
        self.block = {
            0 :[Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1 :[Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2 :[Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3 :[Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.get_coords(0, 3)

class Block_I(Block):
    def __init__(self):
        super().__init__(5)
        self.block = {
            0 :[Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1 :[Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2 :[Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3 :[Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.get_coords(-1, 3)

class Block_J(Block):
    def __init__(self):
        super().__init__(6)
        self.block = {
            0 :[Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1 :[Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2 :[Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3 :[Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.get_coords(0, 3)

class Block_T(Block):
    def __init__(self):
        super().__init__(7)
        self.block = {
            0 :[Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1 :[Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2 :[Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3 :[Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.get_coords(0, 3)

class Block_U(Block):
    def __init__(self):
        super().__init__(8)
        self.block = {
            0 :[Position(0, 0), Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1 :[Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1), Position(2, 2)],
            2 :[Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 2)],
            3 :[Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.get_coords(0, 3)
