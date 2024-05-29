import pygame

from maze_generator import *
from login_startgame import *

import pickle # save game/load game library

# constant
WIDTH, HEIGHT, FPS = 1300, 750, 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game by Group 2 - 23TNT1")

# save a maze into a file
def saveMaze(maze: Maze, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(maze, f)

# load a maze from a file and return it
def loadMaze(filename: str):
    with open(filename, 'rb') as f:
        maze = pickle.load(f)
    return maze

def getImage(filename: str):
    return pygame.image.load(rf'assets\{filename}').convert_alpha()

# main function
def main():
    clock = pygame.time.Clock()
    run = True

    g = LoginMenu()
    g.start()

if __name__ == '__main__':
    main()