import pygame
from utils import import_folder
from maze_generator import *

class Player():
    def __init__(self, level, maze, tilesize):
        self.maze = maze
        self.level = level
        self.loc = (maze.startX, maze.startY)
        self.tilesize = tilesize

        self.image = pygame.image.load("assets/test/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect(topleft=maze.grid[self.loc[0]][self.loc[1]].get_center())

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.speed = 50

        self.frame_index = 0
        self.animation_speed = 0.2

        self.direction = pygame.math.Vector2(0, 0)
        self.hintPath = []

    def import_player_assets(self):
        character_path = 'assets/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle' : [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
                           'catch' : [], 'catch_idle' : []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path, self.tilesize)

    def input(self):
        if self.status == 'catch':
            self.direction = (0, 0)
            return

        if len(self.hintPath) > 0:
            y, x = self.loc[0], self.loc[1]
            ny, nx = self.hintPath[0]
            del self.hintPath[0]

            dx, dy = nx - x, ny - y
            if dy < 0:
                self.direction = (0, -1)
                self.status = 'up'
            elif dy > 0:
                self.direction = (0, 1)
                self.status = 'down'
            elif dx > 0:
                self.direction = (1, 0)
                self.status = 'right'
            elif dx < 0:
                self.direction = (-1, 0)
                self.status = 'left'
            else:
                self.direction = (0, 0)
        else:
            keys = pygame.key.get_pressed()
            grid = self.maze.grid[self.loc[0]][self.loc[1]]

            if keys[pygame.K_UP] and grid.walls['top'] is False:
                self.direction = (0, -1)
                self.status = 'up'
            elif keys[pygame.K_DOWN] and grid.walls['bottom'] is False:
                self.direction = (0, 1)
                self.status = 'down'
            elif keys[pygame.K_RIGHT] and grid.walls['right'] is False:
                self.direction = (1, 0)
                self.status = 'right'
            elif keys[pygame.K_LEFT] and grid.walls['left'] is False:
                self.direction = (-1, 0)
                self.status = 'left'
            else:
                self.direction = (0, 0)

    def move(self):
        if self.direction != pygame.math.Vector2(0, 0):
            new_loc = (self.loc[0] + self.direction[1], self.loc[1] + self.direction[0])
            pos_loc = self.maze.grid[self.loc[0]][self.loc[1]].get_center()
            pos_new_loc = self.maze.grid[new_loc[0]][new_loc[1]].get_center()

            BASE_DOT = 10
            if self.direction[0] > 0:
                for pos in [tmp / float(BASE_DOT) for tmp in range(pos_loc[0] * BASE_DOT, pos_new_loc[0] * BASE_DOT, self.speed)]:
                    self.level.q.put((pos, pos_loc[1]))
            elif self.direction[0] < 0:
                for pos in [tmp / float(BASE_DOT) for tmp in range(pos_loc[0] * BASE_DOT, pos_new_loc[0] * BASE_DOT, -self.speed)]:
                    self.level.q.put((pos, pos_loc[1]))
            elif self.direction[1] > 0:
                for pos in [tmp / float(BASE_DOT) for tmp in range(pos_loc[1] * BASE_DOT, pos_new_loc[1] * BASE_DOT, self.speed)]:
                    self.level.q.put((pos_loc[0], pos))
            elif self.direction[1] < 0:
                for pos in [tmp / float(BASE_DOT) for tmp in range(pos_loc[1] * BASE_DOT, pos_new_loc[1] * BASE_DOT, -self.speed)]:
                    self.level.q.put((pos_loc[0], pos))
            self.loc = new_loc
        else:
            self.maze.grid[self.loc[0]][self.loc[1]].draw(self.image)

    def getPosition(self):
        return self.maze.grid[self.loc[0]][self.loc[1]].get_center()

    def animate(self, pause):
        # idle status
        if self.direction == (0, 0):
            if 'idle' not in self.status:
                self.status = self.status + '_idle'
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]

    def getHint(self):
        self.hintPath = self.maze.getHint(self.loc[0], self.loc[1])

    def update(self, pause):
        if pause is False:
            self.input()
            self.move()
        self.animate(pause)
        return self.status