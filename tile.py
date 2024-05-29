import pygame

class Goal():
    def __init__(self, tilesize, grid):
        self.grid = grid
        self.image = pygame.image.load('assets/test/goal.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))

    def render(self):
        self.grid.draw(self.image)

class Hint():
    def __init__(self, dir, tilesize, grid):
        self.dir = dir
        self.grid = grid
        self.image = pygame.image.load(rf'assets/test/hint_{dir}.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize, tilesize))

    def pack_data(self):
        return (self.dir, self.grid.x, self.grid.y)

    def render(self):
        self.grid.draw(self.image)

class Auto():
    def __init__(self, nametile, tilesize, grid):
        self.grid = grid
        self.image = pygame.image.load(rf'assets/test/{nametile}.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (tilesize - 1, tilesize - 1))

    def render(self):
        self.grid.draw(self.image)