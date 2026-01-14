import random
import typing as tp
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for y in range(self.cell_height):
                for x in range(self.cell_width):
                    grid[y][x] = random.randint(0, 1)
        return grid

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        alive = pygame.Color("green")
        dead = pygame.Color("white")
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                color = alive if self.grid[y][x] == 1 else dead
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        neighbours: Cells = []
        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_y == 0 and offset_x == 0:
                    continue
                new_y = y + offset_y
                new_x = x + offset_x
                if 0 <= new_y < self.cell_height and 0 <= new_x < self.cell_width:
                    neighbours.append(self.grid[new_y][new_x])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid: Grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                neighbours = self.get_neighbours((y, x))
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if sum(neighbours) in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if sum(neighbours) == 3 else 0
        return new_grid

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_ca_
