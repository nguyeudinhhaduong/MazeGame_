'''
file này gồm các class:
class Cell: Một ô của mê cung
class Maze: Mê cung
'''
import pygame, random
from queue import Queue

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# tạo class cho một ô
class Cell:
    '''
    các hàm của class:
    def neighbor(self): trả về tọa độ của các ô kể cạnh không bị ngăn cách bởi tường
    def render(self, screen, center_x, center_y): trả về
    '''

    def __init__(self, screen, x, y, pos, width, wall_width, data = None):
        '''
        :param pos: tọa độ topleft của Cell
        :param width: độ rộng của Cell
        :param image_width: kích cỡ của tường
        vis_dir: hướng đi của gợi ý
        walls: các bức tường bao quanh ô
        '''
        self.x, self.y = x, y
        self.screen = screen
        if data is None:
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        else:
            self.walls = data

        self.pos = pos
        self.width = width
        self.wall_width = wall_width

        self.image = pygame.image.load('assets/tile/wall.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (wall_width, wall_width))
        self.image_rect = self.image.get_rect()

    def get_center(self):
        return (self.pos[0] + self.width // 2, self.pos[1] + self.width // 2)

    def draw(self, image):
        rect = image.get_rect(center = self.get_center())
        self.screen.blit(image, rect)

    def render(self):
        for i in range(self.width // self.wall_width):
            if self.walls['top']:
                self.image_rect.topleft = (self.pos[0] + i * self.wall_width, self.pos[1])
                self.screen.blit(self.image, self.image_rect)
            if self.walls['right']:
                self.image_rect.topright = (self.pos[0] + self.width, self.pos[1] + i * self.wall_width)
                self.screen.blit(self.image, self.image_rect)
            if self.walls['bottom']:
                self.image_rect.bottomleft = (self.pos[0] + i * self.wall_width, self.pos[1] + self.width)
                self.screen.blit(self.image, self.image_rect)
            if self.walls['left']:
                self.image_rect.topleft = (self.pos[0], self.pos[1] + i * self.wall_width)
                self.screen.blit(self.image, self.image_rect)

        self.image_rect.topright = (self.pos[0] + self.width, self.pos[1])
        self.screen.blit(self.image, self.image_rect)

        self.image_rect.bottomright = (self.pos[0] + self.width, self.pos[1] + self.width)
        self.screen.blit(self.image, self.image_rect)

        self.image_rect.bottomright = (self.pos[0] + self.width, self.pos[1] + self.width)
        self.screen.blit(self.image, self.image_rect)

        self.image_rect.bottomleft = (self.pos[0], self.pos[1] + self.width)
        self.screen.blit(self.image, self.image_rect)

    # trả về tọa độ của các ô kề cạnh không bị ngăn cách bởi tường
    def neighbor(self):
        neibor = []
        walls = ['top', 'right', 'bottom', 'left']
        dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for wall, (dx, dy) in zip(walls, dir):
            if self.walls[wall] == False:
                neibor.append((self.x + dx, self.y + dy))
        return neibor


# tạo class cho một mê cung
class Maze:
    '''
    class gồm các hàm:
    def breakWall(self, x: int , y: int, dx: int, dy: int): phá tường theo hướng (dx, dy)
    def mazeGenerate(self): Sinh một mê cung
    def makeHint(self): tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def getHint(self, x: int, y: int) -> list[tuple]: trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã ba
    '''

    def __init__(self, screen, size, startX, startY, endX, endY, width, wall_width, data = None):
        '''
        :param size: kích thước của mê cung
        :param startX, startY: tọa độ ô bắt đầu
        :param endX, endY: tọa độ ô kết thúc

        grid: ma trận của mê cung
        hint: gợi ý ô tiếp theo hướng đến điểm kết thúc
        '''
        self.screen = screen
        self.size = size

        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY

        if size == 100:
            self.BASE = 40
        else:
            self.BASE = 0

        self.width = width
        self.wall_width = wall_width

        if data is None:
            self.grid = [[Cell(screen, x, y, (y * (width - wall_width) + self.BASE, x * (width - wall_width) + self.BASE), width, wall_width) for y in range(size)] for x in range(size)]
        else:
            self.grid = [[Cell(screen, x, y,(y * (width - wall_width) + self.BASE, x * (width - wall_width) + self.BASE), width, wall_width, data[x][y]) for y in range(size)] for x in range(size)]

        self.trace = [[(0, 0)] * size for _ in range(size)]
        self.hint = [[(0, 0)] * size for _ in range(size)]
        self.makeHint()

    def pack_data(self):
        data = []
        for x in range(self.size):
            data.append([])
            for y in range(self.size):
                data[-1].append(self.grid[x][y].walls)
        return data

    def reset(self):
        self.grid = [[Cell(self.screen, x, y, (y * (self.width - self.wall_width) + self.BASE, x * (self.width - self.wall_width) + self.BASE), self.width, self.wall_width)
                      for y in range(self.size)] for x in range(self.size)]

        self.trace = [[(0, 0)] * self.size for _ in range(self.size)]
        self.hint = [[(0, 0)] * self.size for _ in range(self.size)]

    # phá tường theo hướng (dx, dy)
    def breakWall(self, x: int, y: int, dx: int, dy: int):
        nx, ny = x + dx, y + dy
        if dx == 1:
            self.grid[x][y].walls['bottom'] = False
            self.grid[nx][ny].walls['top'] = False
        if dx == -1:
            self.grid[x][y].walls['top'] = False
            self.grid[nx][ny].walls['bottom'] = False
        if dy == 1:
            self.grid[x][y].walls['right'] = False
            self.grid[nx][ny].walls['left'] = False
        if dy == -1:
            self.grid[x][y].walls['left'] = False
            self.grid[nx][ny].walls['right'] = False

    # trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã 3
    def getHint(self, x: int, y: int) -> list[tuple]:
        endNode = (self.endX, self.endY)
        hintPath = []

        while True:
            if (x, y) == endNode:
                break
            nx, ny = self.hint[x][y]
            hintPath.append((nx, ny))

            x, y = nx, ny
            if list(self.grid[x][y].walls.values()).count(False) > 2:
                break
        return hintPath

    # tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def makeHint(self):
        # khởi tạo các biến
        visited = [[False] * self.size for _ in range(self.size)]
        q = Queue()

        visited[self.endX][self.endY] = True
        q.put((self.endX, self.endY))

        # BFS
        while q.qsize() > 0:
            x, y = q.get()
            for nx, ny in self.grid[x][y].neighbor():
                if visited[nx][ny] is False:
                    visited[nx][ny] = True
                    self.hint[nx][ny] = (x, y)
                    q.put((nx, ny))

    # Sinh ra một mê cung
    def mazeGenerate(self):
        # randomized DFS generator
        # sử dụng DFS khử đệ quy
        visited = [[False] * self.size for _ in range(self.size)]
        visited[0][0] = True
        stack = [(0, 0)]

        while stack:
            x, y = stack[-1]
            dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(dir)
            deadEnd = 1

            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx and nx < self.size and 0 <= ny and ny < self.size and visited[nx][ny] == False:
                    deadEnd = 0
                    visited[nx][ny] = True
                    self.breakWall(x, y, dx, dy)
                    stack.append((nx, ny))
                    break
            if deadEnd == 1:
                stack.pop()
        # Sau khi sinh xong mê cung thì tạo gợi ý
        self.makeHint()

    def render(self):
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y].render()
